#!/usr/bin/env python3
"""Append a ladder campaign entry (ladder + ladder-mtp0 rungs, per-request first-divergence positions vs the sequential
oracle) to a result JSON, in the shape used by the R281/R282 entries.
usage: append-ladder-result-entry.py <campaign-root> <result-json> <key> --date D --boot B --image I --config C --verdict V"""
import argparse, json, os, sys
ap = argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('result'); ap.add_argument('key')
for k in ('date', 'boot', 'image', 'config', 'verdict'): ap.add_argument('--' + k, default='')
a = ap.parse_args()
def stage(name):
    p = os.path.join(a.root, name, 'ladder.json')
    if not os.path.exists(p): return None, None
    d = json.load(open(p)); orc = {r['prompt_id']: r['token_ids'] for r in d['oracle']['rows']}
    rungs, div = [], {}
    for b in d['batches']:
        rungs.append({'concurrency': b['concurrency'], 'repeat': b['repeat'], 'exact': f"{b['oracle_exact_count']}/{b['oracle_exact_total']}",
                      'aggregate_tok_s_wall': round(b['aggregate_tok_s_wall'], 1), 'ttft_s_max': round(max(r['ttft_s'] for r in b['rows']), 2)})
        bad = []
        for r in b['rows']:
            o = orc.get(r['prompt_id']); t = r['token_ids']
            if o is not None and t != o:
                bad.append([r['prompt_id'], next((i for i, (x, y) in enumerate(zip(t, o)) if x != y), min(len(t), len(o)))])
        if bad: div[f"c{b['concurrency']}_r{b['repeat']}"] = sorted(bad, key=lambda x: x[1])
    return rungs, div
res = json.load(open(a.result))
entry = {'date': a.date, 'boot': a.boot, 'image': a.image, 'config': a.config}
for name, key in (('ladder', 'ladder'), ('ladder-mtp0', 'ladder-mtp0')):
    rungs, div = stage(name)
    if rungs is not None:
        entry[key] = rungs; entry[key + '_first_divergence_vs_oracle'] = div
entry['verdict'] = a.verdict
res[a.key] = entry
json.dump(res, open(a.result, 'w'), indent=1, ensure_ascii=False); open(a.result, 'a').write('\n')
print(json.dumps({k: v for k, v in entry.items() if 'divergence' not in k}, indent=1)[:1500])
