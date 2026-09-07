#!/usr/bin/env bash
# Verify the Triton-HC overlay series: the bundle must carry tag
# q38-hctriton-mtp1-62219122 whose commit is 62219122 (one patch over the placement MTP1 head 005dc578),
# With --apply the single patch is
# applied onto 005dc578 in a throwaway worktree and must produce the same tree.
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
tree="${REPRO_VLLM_TREE:?set REPRO_VLLM_TREE to a vllm clone that contains 005dc578 (restore it from the placement bundle first)}"
base=005dc57895896f770157ea94f68e473e7447139e
head=622191221475b53cc6f7f4d847860939f4c300ab
expected_tree=e79ab58bb96b807d4bebad5644bafa5e0d4327aa
bundle="$script_dir/vllm-q38-hctriton-mtp1-62219122-20260907.bundle"
(cd "$script_dir" && sha256sum --quiet -c series.sha256)
git -C "$tree" cat-file -e "$base^{commit}" || { echo "base $base is not in $tree" >&2; exit 2; }
git -C "$tree" bundle verify "$bundle" >/dev/null
git -C "$tree" fetch --quiet "$bundle" "refs/tags/q38-hctriton-mtp1-62219122:refs/tags/q38-hctriton-mtp1-62219122" 2>/dev/null || git -C "$tree" fetch --quiet "$bundle" "+refs/tags/q38-hctriton-mtp1-62219122:refs/tags/q38-hctriton-mtp1-62219122"
[[ "$(git -C "$tree" rev-parse refs/tags/q38-hctriton-mtp1-62219122^{commit})" == "$head" ]] || { echo "tag does not resolve to $head" >&2; exit 2; }
[[ "$(git -C "$tree" rev-parse "$head^{tree}")" == "$expected_tree" ]] || { echo "tree mismatch" >&2; exit 2; }
[[ "$(git -C "$tree" rev-list --count "$base..$head")" == 1 ]] || { echo "series length changed (expected 1)" >&2; exit 2; }
git -C "$tree" merge-base --is-ancestor "$base" "$head"
if [[ "${1:-}" == "--apply" ]]; then
  wt="$(mktemp -d)"
  git -C "$tree" worktree add --quiet --detach "$wt" "$base"
  git -C "$wt" am --quiet "$script_dir"/00*.patch
  applied="$(git -C "$wt" rev-parse HEAD^{tree})"
  git -C "$tree" worktree remove --force "$wt"
  [[ "$applied" == "$expected_tree" ]] || { echo "applied series tree $applied != $expected_tree" >&2; exit 2; }
  echo "series applies onto $base and reproduces tree $expected_tree"
fi
echo "overlay series verified: $head (tree $expected_tree) over the placement MTP1 head $base"
