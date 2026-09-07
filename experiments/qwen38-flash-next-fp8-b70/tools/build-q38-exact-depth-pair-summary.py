#!/usr/bin/env python3
"""Build an exact-depth pair summary across servers (the attestation builder's --pair-summary input):
every listed run's output_token_ids_sha256 is compared with the reference run's; rows carry the rate.

  build-q38-exact-depth-pair-summary.py --reference "<label>" --reference-json <run.json> \
      --server A266="<head and identity>" [--server …] --row A266:a266-exact-depth-2k-r1=<json> [--row …] --out <json>
"""
import argparse, json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reference', required=True); ap.add_argument('--reference-json', required=True, type=Path)
    ap.add_argument('--server', action='append', default=[], help='ATTEMPT=description')
    ap.add_argument('--row', action='append', default=[], help='ATTEMPT:run-name=path/to/exact-depth.json')
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    ref = json.loads(a.reference_json.read_text())['response']['output_token_ids_sha256']
    servers = dict(s.split('=', 1) for s in a.server)
    rows = []
    for r in a.row:
        key, path = r.split('=', 1); attempt, run = key.split(':', 1)
        d = json.loads(Path(path).read_text())
        sha = d['response']['output_token_ids_sha256']
        rows.append({'run': run, 'overlay_head': servers[attempt].split(' ')[0], 'output_sha12': sha[:12],
                     'ids_equal_to_reference': sha == ref, 'tok_s': round(d['metric_window']['conventional_99_interval_tok_s'], 3)})
    out = {'reference': a.reference, 'reference_sha256': ref, 'servers': servers, 'rows': rows, 'all_identical': all(r['ids_equal_to_reference'] for r in rows)}
    a.out.write_text(json.dumps(out, indent=2) + '\n'); print(json.dumps({'rows': len(rows), 'all_identical': out['all_identical']}))

if __name__ == '__main__':
    main()
