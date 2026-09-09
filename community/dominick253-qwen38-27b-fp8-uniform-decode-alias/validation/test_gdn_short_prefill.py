#!/usr/bin/env python3
"""CPU test of the actual installed GDN builder call and actual split helper.

This does not import GPU runner/model code or validate GPU kernel numerics.
--apply-candidate changes only the in-memory parsed call for red/green testing.
"""
import argparse
import ast
from pathlib import Path
from types import SimpleNamespace

import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path,
                        default=Path("/opt/venv/lib/python3.12/site-packages/vllm"))
    parser.add_argument("--apply-candidate", action="store_true")
    expected = parser.add_mutually_exclusive_group()
    expected.add_argument("--expect-fixed", action="store_true")
    expected.add_argument("--expect-stock", action="store_true")
    args = parser.parse_args()
    backend = args.source_root / "v1/attention/backends"
    helper_tree = ast.parse((backend / "utils.py").read_text())
    helper = next(n for n in helper_tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "split_decodes_and_prefills")
    ns = {"torch": torch, "CommonAttentionMetadata": object}
    exec(compile(ast.Module(body=[helper], type_ignores=[]), "actual-split-helper", "exec"), ns)
    builder = ast.parse((backend / "gdn_attn.py").read_text())
    calls = [n for n in ast.walk(builder) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "split_decodes_and_prefills"]
    assert len(calls) == 1, "expected one GDN non-spec split call"
    call = calls[0]
    if args.apply_candidate:
        assert not any(k.arg == "treat_short_extends_as_decodes" for k in call.keywords)
        call.keywords.append(ast.keyword(
            arg="treat_short_extends_as_decodes",
            value=ast.parse("m.is_prefilling is None", mode="eval").body))
    fixed = any(k.arg == "treat_short_extends_as_decodes" for k in call.keywords)
    if args.expect_fixed:
        assert fixed, "expected the installed GDN short-prefill correction"
    if args.expect_stock:
        assert not fixed, "expected the stock GDN split call"
    code = compile(ast.fix_missing_locations(ast.Expression(call)), "actual-builder-call", "eval")
    cases = [
        ("fresh-one", [1], [True], (0, 1, 0, 1), (1, 0, 1, 0)),
        ("fresh-two", [2], [True], (0, 1, 0, 2), (0, 1, 0, 2)),
        ("decode", [1], [False], (1, 0, 1, 0), (1, 0, 1, 0)),
        ("short-extend", [1], [True], (0, 1, 0, 1), (1, 0, 1, 0)),
        ("decode-and-fresh", [1, 1], [False, True], (1, 1, 1, 1), (2, 0, 2, 0)),
        ("decode-and-extends", [1, 1, 3], [False, True, True], (1, 2, 1, 4), (2, 1, 2, 3)),
        ("capture-padding", [1, 0], [False, False], (2, 0, 1, 0), (2, 0, 1, 0)),
        ("metadata-less-draft", [1], None, (1, 0, 1, 0), (1, 0, 1, 0)),
    ]
    for label, lengths, phases, expected_fixed, expected_stock in cases:
        m = SimpleNamespace(max_query_len=max(lengths), num_reqs=len(lengths),
                            num_actual_tokens=sum(lengths),
                            query_start_loc_cpu=torch.tensor([0] + lengths).cumsum(0),
                            is_prefilling=None if phases is None else torch.tensor(phases))
        observed = eval(code, dict(ns, m=m))
        expected = expected_fixed if fixed else expected_stock
        assert observed == expected, (label, observed, expected)
    print(f"PASS: {len(cases)} actual-source GDN split cases; fixed={fixed}")


if __name__ == "__main__":
    main()
