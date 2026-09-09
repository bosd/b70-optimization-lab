"""Test the classifier extracted from a real runner file, without loading GPUs.

Run with --expect-stock before applying the reported patch, then without it.
Unlike the contributor's illustrative test, failures return a nonzero status.
"""
import argparse
import ast
from pathlib import Path
from types import SimpleNamespace

import numpy as np


def check(source, expect_stock=False):
    tree = ast.parse(source.read_text())
    runner = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                  and n.name == "GPUModelRunner")
    method = next(n for n in runner.body if isinstance(n, ast.FunctionDef)
                  and n.name == "_is_uniform_decode")
    method.decorator_list = []
    namespace = {}
    exec(compile(ast.Module(body=[method], type_ignores=[]), str(source), "exec"), namespace)
    fn = namespace[method.name]
    bound = method.args.args[0].arg == "self"
    cases = [
        # label, computed, prompt, max scheduled, query length, total, requests, force, expected
        ("mtp1 tiny prefill", [0], [2], 2, 2, 2, 1, None, False),
        ("mtp2 tiny prefill", [0], [3], 3, 3, 3, 1, None, False),
        ("chunk tail", [5], [8], 3, 3, 3, 1, None, False),
        ("prefix cache tail", [127], [128], 1, 1, 1, 1, None, False),
        ("mixed batch", [5, 0], [3, 3], 3, 3, 6, 2, None, False),
        ("one token prefill", [0], [1], 1, 1, 1, 1, None, False),
        ("prompt boundary", [3], [3], 3, 3, 3, 1, None, True),
        ("ordinary decode", [10] * 16, [8] * 16, 1, 1, 16, 16, None, True),
        ("spec decode", [10] * 6, [8] * 6, 5, 5, 30, 6, None, True),
        ("inactive padded rows", [10, 0], [8, 100], 2, 2, 2, 1, None, True),
        ("query mismatch", [10], [8], 2, 1, 2, 1, None, False),
        ("total mismatch", [10, 10], [8, 8], 2, 2, 3, 2, None, False),
        ("capture override", [], [], 2, 2, 2, 1, True, True),
        ("capture shape override", [], [], 2, 1, 7, 1, True, True),
        ("forced mixed", [], [], 1, 1, 1, 1, False, False),
    ]
    failures = []
    for index, (label, computed, prompt, maximum, query, total, count, force, expected) in enumerate(cases):
        # The first six cases reproduce the shape-only false positives.
        if expect_stock and index < 6:
            expected = True
        batch = SimpleNamespace(num_computed_tokens_cpu=np.array(computed),
                                num_prompt_tokens=np.array(prompt))
        # Capture overrides must work before input_batch is initialized.
        owner = SimpleNamespace() if force is not None else SimpleNamespace(input_batch=batch)
        args = (maximum, query, total, count, force)
        actual = fn(owner, *args) if bound else fn(*args)
        if bool(actual) != expected:
            failures.append(f"{label}: got {actual}, expected {expected}")
    if failures:
        raise AssertionError("; ".join(failures))
    print(f"PASS: {len(cases)} actual-source cases ({'stock defect reproduced' if expect_stock else 'fixed'}): {source}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--expect-stock", action="store_true")
    args = parser.parse_args()
    check(args.source, args.expect_stock)
