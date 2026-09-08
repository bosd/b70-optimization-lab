"""RED/GREEN test for the _is_uniform_decode shape-alias fix (vllm PR #53059).

Self-contained: both classifier bodies are extracted verbatim from the R50
image's vllm/v1/worker/gpu_model_runner.py (stock, sha256 4e0e1aee778bb1f6...)
and the patched file (sha256 921f0a6fd3403119...). The aliased-prefill cases
MUST fail on stock (bug present) and pass on patched (fix works).

Run: python3 test_is_uniform_decode_red_green.py   (stdlib + numpy)
"""
import textwrap
import types

import numpy as np

STOCK = r"""
    def _is_uniform_decode(
        max_num_scheduled_tokens: int,
        uniform_decode_query_len: int,
        num_tokens: int,
        num_reqs: int,
        force_uniform_decode: bool | None = None,
    ) -> bool:
        '''
        Checks if it's a decode batch with same amount scheduled tokens
        across all requests.
        '''
        return (
            (
                (max_num_scheduled_tokens == uniform_decode_query_len)
                and (num_tokens == max_num_scheduled_tokens * num_reqs)
            )
            if force_uniform_decode is None
            else force_uniform_decode
        )
"""

PATCHED = r"""
    def _is_uniform_decode(
        self,
        max_num_scheduled_tokens: int,
        uniform_decode_query_len: int,
        num_tokens: int,
        num_reqs: int,
        force_uniform_decode: bool | None = None,
    ) -> bool:
        '''
        Checks if it's a decode batch with same amount scheduled tokens
        across all requests.
        '''
        if force_uniform_decode is not None:
            return force_uniform_decode
        if not (
            max_num_scheduled_tokens == uniform_decode_query_len
            and num_tokens == max_num_scheduled_tokens * num_reqs
        ):
            return False
        # The shape check alone can misclassify prefills: with spec decode
        # (uniform_decode_query_len = 1 + num_spec_tokens), any batch of
        # prompts scheduled with exactly uniform_decode_query_len tokens per
        # request aliases the uniform-decode shape. Dispatching such a
        # prefill into a cudagraph captured for uniform decode replays stale
        # capture-time metadata for backends with persistent buffers (e.g.
        # GDN), silently skipping prefill state writes and corrupting output
        # (https://github.com/vllm-project/vllm/issues/53051). A batch is
        # only uniform decode if every request is already past its prompt.
        input_batch = self.input_batch
        return bool(
            (
                input_batch.num_computed_tokens_cpu[:num_reqs]
                >= input_batch.num_prompt_tokens[:num_reqs]
            ).all()
        )
"""


def make_self(computed, prompt):
    """Minimal stand-in for `self` with the input_batch arrays."""
    return types.SimpleNamespace(input_batch=types.SimpleNamespace(
        num_computed_tokens_cpu=np.array(computed),
        num_prompt_tokens=np.array(prompt),
    ))


def run(fn_src, self_obj, **kw):
    ns = {}
    exec("import numpy\n" + textwrap.dedent(fn_src), ns)
    fn = ns["_is_uniform_decode"]
    if "self" in fn.__code__.co_varnames:
        return fn(self_obj, **kw)
    return fn(**kw)


CASES = [
    # (name, computed, prompt, kwargs, stock_expected, patched_expected)
    ("genuine decode 16x1", [10] * 16, [8] * 16,
     dict(max_num_scheduled_tokens=1, uniform_decode_query_len=1, num_tokens=16, num_reqs=16),
     True, True),
    ("shape mismatch 2x1", [10] * 16, [8] * 16,
     dict(max_num_scheduled_tokens=2, uniform_decode_query_len=1, num_tokens=16, num_reqs=16),
     False, False),
    ("total mismatch", [10] * 16, [8] * 16,
     dict(max_num_scheduled_tokens=1, uniform_decode_query_len=1, num_tokens=8, num_reqs=16),
     False, False),
    ("genuine spec decode 5-q", [10] * 7, [8] * 7,
     dict(max_num_scheduled_tokens=5, uniform_decode_query_len=5, num_tokens=30, num_reqs=6),
     True, True),
    ("spec shape mismatch", [10] * 7, [8] * 7,
     dict(max_num_scheduled_tokens=5, uniform_decode_query_len=4, num_tokens=30, num_reqs=6),
     False, False),
    ("spec total mismatch", [10] * 7, [8] * 7,
     dict(max_num_scheduled_tokens=5, uniform_decode_query_len=5, num_tokens=36, num_reqs=6),
     False, False),
    # --- THE BUG CASES: aliased prefill shapes ---
    ("ALIASED 3-token prefill (k=2)", [0], [3],
     dict(max_num_scheduled_tokens=3, uniform_decode_query_len=3, num_tokens=3, num_reqs=1),
     True, False),
    ("ALIASED 2-token prefill (k=1)", [0], [2],
     dict(max_num_scheduled_tokens=2, uniform_decode_query_len=2, num_tokens=2, num_reqs=1),
     True, False),
    ("ALIASED chunked-prefill last chunk", [5], [8],
     dict(max_num_scheduled_tokens=3, uniform_decode_query_len=3, num_tokens=3, num_reqs=1),
     True, False),
    ("ALIASED mixed decode+prefill", [5, 0], [3, 3],
     dict(max_num_scheduled_tokens=3, uniform_decode_query_len=3, num_tokens=6, num_reqs=2),
     True, False),
    ("ALIASED 1-token prompt no-spec", [0], [1],
     dict(max_num_scheduled_tokens=1, uniform_decode_query_len=1, num_tokens=1, num_reqs=1),
     True, False),
    ("same shape, past prompt (decode)", [5], [3],
     dict(max_num_scheduled_tokens=3, uniform_decode_query_len=3, num_tokens=3, num_reqs=1),
     True, True),
    ("force=True (capture path)", [0], [3],
     dict(max_num_scheduled_tokens=3, uniform_decode_query_len=3, num_tokens=3, num_reqs=1,
          force_uniform_decode=True),
     True, True),
    ("force=False", [10] * 4, [8] * 4,
     dict(max_num_scheduled_tokens=1, uniform_decode_query_len=1, num_tokens=4, num_reqs=4,
          force_uniform_decode=False),
     False, False),
]

red_fails, green_fails = [], []
for name, comp, prom, kw, stock_exp, patched_exp in CASES:
    s = run(STOCK, make_self(comp, prom), **kw)
    p = run(PATCHED, make_self(comp, prom), **kw)
    ok_s = (s == stock_exp)
    ok_p = (p == patched_exp)
    tag = ""
    if not ok_s:
        red_fails.append(name); tag += " <<RED-FAIL(stock wrong)"
    if not ok_p:
        green_fails.append(name); tag += " <<GREEN-FAIL(patch wrong)"
    print(f"{name:38} stock={s!r:5}(want {stock_exp!r:5}) patched={p!r:5}(want {patched_exp!r:5}){tag}")

print()
print(f"RED  (stock must get bug cases WRONG): {'PASS' if not red_fails else 'FAIL ' + str(red_fails)}")
print(f"GREEN (patched must get all right):    {'PASS' if not green_fails else 'FAIL ' + str(green_fails)}")
