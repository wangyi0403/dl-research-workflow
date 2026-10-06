---
name: "research-publication"
description: "Prepare or audit a reproducible research release package, including code/data documentation, licenses, cards, checksums, and archive metadata. Publishing needs authorization."
---

# Research Publication

1. Define release scope and separate public, restricted, licensed, sensitive, and non-redistributable assets.
2. Verify licenses and third-party attribution for code, data, models, templates, fonts, and figures.
3. Create a separate local staging copy and exclude or redact credentials, personal paths, internal URLs, machine identifiers and private logs there. Preserve research originals, source histories and checkpoints; never sanitize by deleting or overwriting them in place.
4. Reproduce the principal result from documented environment, config, seed, and artifact versions when feasible.
5. Provide checksums, provenance, citation metadata, limitations, safety notes, and known failure modes.
6. Stage the release locally for review. In `research-deep-learning-project`, record the checklist, decisions, and exceptions in `docs/12_release_readiness.md`; otherwise use the project's designated release artifact. Check the current explicit authorization for external uploads, DOI creation, publication or visibility changes; ask only for missing scope or an explicitly required action-time confirmation.

Use `references/release-checklist.md` as the final gate.
