#!/usr/bin/env bash
# Verify the fused-QSA overlay series: the bundle must carry tag
# q38-qsafused-mtp1-6d872457 whose commit is 6d872457 (two patches over the Triton-HC MTP1 head 62219122),
# With --apply the two patches are
# applied onto 62219122 in a throwaway worktree and must produce the same tree.
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
tree="${REPRO_VLLM_TREE:?set REPRO_VLLM_TREE to a vllm clone that contains 62219122 (restore it from the Triton-HC bundle first)}"
base=622191221475b53cc6f7f4d847860939f4c300ab
head=6d8724577dabbee5fa0bbc70c4d927c6174c8d8a
expected_tree=3e8dfc5937087d186cd4a99a6bf15213be732462
bundle="$script_dir/vllm-q38-qsafused-mtp1-6d872457-20260907.bundle"
(cd "$script_dir" && sha256sum --quiet -c series.sha256)
git -C "$tree" cat-file -e "$base^{commit}" || { echo "base $base is not in $tree" >&2; exit 2; }
git -C "$tree" bundle verify "$bundle" >/dev/null
git -C "$tree" fetch --quiet "$bundle" "refs/tags/q38-qsafused-mtp1-6d872457:refs/tags/q38-qsafused-mtp1-6d872457" 2>/dev/null || git -C "$tree" fetch --quiet "$bundle" "+refs/tags/q38-qsafused-mtp1-6d872457:refs/tags/q38-qsafused-mtp1-6d872457"
[[ "$(git -C "$tree" rev-parse refs/tags/q38-qsafused-mtp1-6d872457^{commit})" == "$head" ]] || { echo "tag does not resolve to $head" >&2; exit 2; }
[[ "$(git -C "$tree" rev-parse "$head^{tree}")" == "$expected_tree" ]] || { echo "tree mismatch" >&2; exit 2; }
[[ "$(git -C "$tree" rev-list --count "$base..$head")" == 2 ]] || { echo "series length changed (expected 2)" >&2; exit 2; }
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
echo "overlay series verified: $head (tree $expected_tree) over the Triton-HC MTP1 head $base"
