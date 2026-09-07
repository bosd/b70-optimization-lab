# Reproduce Qwen3.5 9B FP8-dynamic with its own MTP head on one B70

> **Certification: `candidate-portable-repro`, not a starter guide.** The
> model revision, container image, launch chain and validation identities are
> pinned and were verified on the lab host on 2026-09-07. The remaining gates
> are a tested Intel driver/Docker installation path, beginner recovery
> guidance, and an independent clean-host replay. See the
> [guide catalog](../guide-catalog.json) and
> [certification standard](../../docs/reproduction-guide-certification.md).

RedHatAI's FP8-dynamic quantization of Alibaba's Qwen3.5-9B (compressed-tensors
per-channel FP8 weights, dynamic activations), served as published by vLLM XPU
on one Intel Arc Pro B70 32 GiB card through the lab's R276 image, with the
publisher's MTP head as a lossless speculative draft (`qwen3_5_mtp`) and full
decode-only XPU graph capture. The stack is the Qwen3.8 INT4 lane's image and
the Qwen3.8 FP8 recipe's strict launchers; nothing here is model-specific
beyond the model manifest and the launcher defaults.

## Headline (campaign c2, 2026-09-07, one B70)

- **MTP depth 3 with the draft-only INT4 lm_head: `98.251 / 98.027 tok/s`**
  class-balanced median decode over tokens 1-100 after TTFT on the strict
  12-prompt six-class suite over the completions API, 512-token completion
  cap, cache zero (two fresh servers, empty compile cache each). Median TTFT
  `74 ms`.
- **No speculation: `50.165 / 50.173 tok/s`** on the same suite (`50.183 /
  50.150` in c1).
- **Lossless:** the two MTP0 servers matched 12/12 complete token arrays (G1);
  the two depth-3 servers matched 12/12 against each other (G2) and 12/12
  against the MTP0 oracle (G3); the canary set passed on every server.
- The draft-only INT4 lm_head (`DRAFT_HEAD_INT4=1`, the launcher default)
  quantizes a draft-pass copy of the 248,320-row output head to INT4; the FP8
  target verifier is unchanged, so outputs are identical, and the draft step
  gets 27.6% cheaper: `76.917 / 76.879 tok/s` with the FP8 draft head (c1).
- Evidence: `experiments/qwen35-9b-b70/data/2026-09-07-qwen35-9b-fp8-matrix-result.json`
  (entries `c1_…`, `c2_…`, `c3_…`), attestation
  `experiments/qwen35-9b-b70/data/qwen35-9b-fp8-tp1-mtp3-graph1-dhint4-20260907-c2-strict-result.json`.
- ML Bottleneck's tuned-run target for `qwen3.5_9b`, FP8, vLLM on one B70 is
  `56.56 tok/s` (physical ceiling `80.31`); the headline is 1.74x the target.

### Matrix (one B70, strict completions suite, two fresh servers per row)

| depth | draft head | XPU graph | tok/s (a / b) | G1 | G2 | G3 vs MTP0 | run |
| ---: | --- | --- | ---: | --- | --- | --- | --- |
| 0 | - | on | 50.183 / 50.150 | 12/12 | - | - | c1 |
| 3 | FP8 | on | 76.917 / 76.879 | - | 12/12 | 12/12, 12/12 | c1 |
| 3 | INT4 draft copy | on | **98.251 / 98.027** | - | 12/12 | 12/12, 12/12 | c2 |
| 4 | INT4 draft copy | on | 98.418 / 98.550 | - | 12/12 | **8/12, 8/12** (withheld) | c3 |
| 3 | INT4 draft copy | off | 96.779 / 96.748 | - | 12/12 | 12/12, 12/12 | c4 |
| 0 | - | off | 49.477 / 49.454 | 12/12 | - | - | c4 |

Depth 4 is repeat-exact but not lossless: four prompts (`benchmark-analysis`
at token 342, `bug-report-synthesis` at 48, `decision-memo` at 75,
`risk-register` at 403) take a different valid branch from the oracle when the
verify batch grows to five rows, and it is no faster on this workload. XPU graph capture is worth about 1.5% on one card (c4). Rows for two cards
and the 2K-32K context ladder are appended as their campaigns complete.

Workload note: through the chat API this model first streams a long
"Thinking Process" preamble that the MTP head predicts unusually well; the
same depth-3 configuration measures `131.5 tok/s` on those prompts (`105.7`
with the FP8 draft head), and depth 4 `148.0`
(`experiments/qwen35-9b-b70/notes/2026-09-07-qwen35-9b-fp8-one-card-quick-lane.md`).
The headline above is the lab's standard completions-suite convention.

## Model

Pinned in `manifests/model-direct-redhatai-qwen35-9b-fp8-dynamic-790f0576.json`:
`RedHatAI/Qwen3.5-9B-FP8-dynamic` at revision
`790f0576d2d77dd5322aa0603a470bd9e3a3d1f6`, three LFS files
(`model.safetensors` 13,520,203,008 B, `model_mtp.safetensors`
486,582,848 B, `tokenizer.json` 19,989,343 B) plus nine small files. Download
with a resumable, multi-connection tool and keep the filenames:

```bash
REV=790f0576d2d77dd5322aa0603a470bd9e3a3d1f6; R=RedHatAI/Qwen3.5-9B-FP8-dynamic; D=/models/Qwen3.5-9B-FP8-dynamic; mkdir -p "$D"
for f in $(curl -s "https://huggingface.co/api/models/$R/tree/$REV" | python3 -c 'import json,sys;[print(x["path"]) for x in json.load(sys.stdin) if x["type"]=="file"]'); do
  case $f in *.safetensors) aria2c -c -x 8 -s 8 -d "$D" -o "$f" "https://huggingface.co/$R/resolve/$REV/$f" ;;
     *) curl -sSL -o "$D/$f" "https://huggingface.co/$R/resolve/$REV/$f" ;; esac
done
```

The launcher verifies every LFS file's size and SHA-256 against the manifest
before the container starts (`repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/verify-model-direct.sh`).

## Image

The lab's published R276 image, identical to the Qwen3.8 INT4 recipe's:

```bash
docker pull ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad
docker tag ghcr.io/steveseguin/vllm-openai-xpu-qwen38-int4@sha256:521eb277c0733f8c2ce47aea1bb98ed576c6f1ad63bf5baf22d38fc07abf54ad \
  neural-download/vllm-openai-xpu:qwen38-int4-gdn-spec-group-sync-free-r276
```

vLLM 0.27.2rc1.dev77+gac7509e2b (XPU) with the lab kernel library
(vllm-xpu-kernels `1e90ffa6` + patches, oneDNN `0e2a5bfe` + patches; the
clean-clone rebuild is documented in the
[INT4 recipe](../qwen38-27b-autoround-int4-b70/README.md)) and the R213b,
R224, R228, R256 and R276 overlays. The launcher verifies the image id and the
kernel-library, ops-file and layer-norm digests before serving. vLLM resolves
`Qwen3_5ForConditionalGeneration` and offers the `qwen3_5_mtp` speculative
method; the FP8 weights go through vLLM's compressed-tensors path (no lab
W8A16 kernel involved: `VLLM_XPU_FP8_BLOCK_W8A16=0`).

## Launch

```bash
cd /path/to/b70-optimization-lab
MODEL_DIR=/models/Qwen3.5-9B-FP8-dynamic VLLM_CACHE_DIR=/tmp/qwen35-cache \
  repro/qwen35-9b-fp8-b70/scripts/run-qwen35-9b-fp8-server.sh
```

| variable | default | meaning |
| --- | --- | --- |
| `MTP_DEPTH` | `3` | speculative tokens per step; `0` serves without speculation |
| `TENSOR_PARALLEL_SIZE` | `1` | `2` splits across both cards (`XPU_DEVICE_MASK=0,1`) |
| `XPU_GRAPH` | `1` | full decode-only XPU graph capture, sizes 1-64; `0` = piecewise compile, graph off |
| `PORT` | `18131` | OpenAI-compatible endpoint (`/v1/completions`, `/v1/chat/completions`, `/health`) |
| `MAX_MODEL_LEN` / `MAX_NUM_SEQS` / `MAX_NUM_BATCHED_TOKENS` | `8192` / `16` / `1024` | server shape; the strict measurements used `1024 / 1 / 1024`, the ladders `256 / 64 / 512` |

The launcher runs the FP8 recipe's strict chain
(`run-w8a16-mtp1-strict-server.sh`, or `run-w8a16-mtp0-strict-server.sh` at
depth 0): `TORCHINDUCTOR_DETERMINISTIC=1`, Inductor autotune off,
`PYTHONHASHSEED=0`, `VLLM_BATCH_INVARIANT=0` (vLLM refuses the GDN backend
otherwise), split-mixed GDN, GDN speculative group 16, packed-serial RMSNorm,
persistent GDN scratch. None of these costs throughput on this model (bisect
in the lane note).

## Validate

Strict suite and canaries (what the headline was measured with):

```bash
OUT_DIR=/tmp/qwen35-strict-a BASE_URL=http://127.0.0.1:18131 MODEL_NAME=qwen35-9b-fp8-mtp3 \
  repro/qwen38-27b-fp8-vllm-tp2-asrock-b70/bench-w8a16-mtp1-strict.sh
```

It refuses to run unless `OUT_DIR` is new, passes the canary set first, sends
the 12 prompts over the completions API with `temperature 0, top_p 1,
seed 42, max_tokens 512`, and writes `performance.json` with the
class-balanced median. Run it against a depth-0 server as well and compare
complete token arrays:

```bash
python3 scripts/compare-strict-attempt-outputs.py /tmp/qwen35-strict-a /tmp/qwen35-strict-mtp0 --output /tmp/compare.json
```

`12/12` exact prompts is the lossless gate. Concurrency ladder (many users):

```bash
python3 scripts/bench-openai-concurrency-oracle.py --base-url http://127.0.0.1:18131 --model qwen35-9b-fp8-mtp3 \
  --api-mode completions --suite experiments/qwen38-27b-b70/data/2026-08-25-qwen38-q4km-tp2-http-smallctx-suite.json \
  --concurrency 1,2,4,8,16,32,64 --repeats 2 --max-tokens 128 --seed 42 --timeout 900 \
  --request-extra-json '{"ignore_eos":true,"temperature":0}' --return-token-ids --require-output-identity --out /tmp/ladder.json
```

## Many users (campaign c2, one B70, warm pass of two)

| users | depth 3 + INT4 draft head tok/s (exact) | no speculation tok/s (exact) |
| ---: | ---: | ---: |
| 1 | 113.0 (1/1) | 50.1 (1/1) |
| 2 | 211.1 (2/2) | 97.2 (2/2) |
| 4 | 310.7 (4/4) | 187.5 (4/4) |
| 8 | 564.7 (8/8) | 355.0 (8/8) |
| 16 | 738.4 (15/16) | 634.7 (15/16) |
| 32 | 883.6 (30/32) | 1055.2 (31/32) |
| 64 | 831.2 (57/64) | 1253.8 (59/64) |

128-token completions on the small-context suite, `max-model-len 256`,
`max-num-seqs 64`, two passes on one server (warm pass shown; the first pass
of a fresh server carries a one-time recompile at two users). Depth 3 is exact
through 8 users and fastest through 16; from 32 users no speculation is
faster (1254 tok/s at 64). The non-identical answers above are near-tie
prompts diverging at one token under the wider batch tiers, valid answers that
the identity gate refuses; the same mechanism as on the Qwen3.8 lanes.

## Known limits

- Through the chat API the model emits its reasoning inline ("Thinking
  Process: ..."); the headline is measured over the completions API.
- Not yet clean-host tested; the INT4 recipe's driver and Docker notes apply.
- One pass per ladder point; strict pairs are two fresh servers each.
