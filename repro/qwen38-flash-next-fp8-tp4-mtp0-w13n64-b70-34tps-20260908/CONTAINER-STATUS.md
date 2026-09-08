# Container route status

**Not provided** as of 2026-09-08. This line's delivery is `native` only.

No Dockerfile is published here, and that is deliberate rather than an omission
being tracked. The MTP1 sibling guide
(`repro/qwen38-flash-next-fp8-tp4-mtp1-qsafused-b70-38tps-20260907/`) does carry a
container recipe, and its own status file records that the build stops on purpose
at the runtime check: the base image `vllm/vllm-openai-xpu` ships `torch 2.13.0+xpu`
while this family's records run on `torch 2.11.0+xpu`, and the kernel stage's native
modules are built against that ABI. That blocker applies unchanged to this line,
which shares the stage, the oneCCL build and the torch pin.

Publishing a copy of a recipe that is known not to build past its runtime check
would add a file without adding a route. When a base image (or an in-image
environment build from an installable lock) pins `torch 2.11.0+xpu` and
`triton 3.7.0`, the container route can be built once and inherited by both lines,
and this file gains the image id, the registry digest, the replay attempt and its
result hashes.
