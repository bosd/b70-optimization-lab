#!/usr/bin/env bash
# Queued behind the Gemma target download: fetch RedHatAI/Qwen3.5-9B-FP8-dynamic at revision 790f0576d2d77dd5322aa0603a470bd9e3a3d1f6
# (12 files, 14.0 GB incl. the 0.49 GB MTP head) into /home/steve/llm-models/qwen35-9b-fp8-dynamic for the "quick fun" 9B lane.
set -u
until grep -q ALL-DONE /home/steve/llm-models/gemma4-aria2-download.log 2>/dev/null; do sleep 300; done
R=RedHatAI/Qwen3.5-9B-FP8-dynamic; REV=790f0576d2d77dd5322aa0603a470bd9e3a3d1f6; D=/home/steve/llm-models/qwen35-9b-fp8-dynamic; mkdir -p "$D"; cd "$D"
files=$(curl -s --max-time 60 "https://huggingface.co/api/models/$R/tree/$REV" | python3 -c "import json,sys; [print(x['path']) for x in json.load(sys.stdin) if x['type']=='file']")
echo "$(date +%T) files: $files" | tr '\n' ' '; echo
for f in $files; do
  [ -f "$D/$f" ] && continue
  case $f in *.safetensors) aria2c -c -x 16 -s 16 -k 16M --file-allocation=none --max-tries=0 --retry-wait=10 --summary-interval=300 --console-log-level=warn -d "$D" -o "$f" "https://huggingface.co/$R/resolve/$REV/$f" ;;
     *) curl -4 -sS -L --fail --retry 20 --retry-all-errors --retry-delay 5 -o "$D/$f" "https://huggingface.co/$R/resolve/$REV/$f" ;; esac
  echo "$(date +%T) got $f rc=$?"
done
echo "$REV" > "$D/REVISION"; echo QWEN35-DONE
