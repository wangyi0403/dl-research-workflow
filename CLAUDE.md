# Research project entry point

Read `AGENTS.md`, `AI_START.md` and `docs/00_start.md` before project work.
The same scientific contracts and authorization boundaries apply across assistants.

Canonical skills are in `.agents/skills/`. Projects initialized with `--agent claude`
also contain `.claude/skills/` copies for native discovery. These copies must match
their canonical counterparts; do not edit both independently.

If a skill is unavailable to native discovery, read its canonical `SKILL.md`
explicitly. Tool integrations and scheduling must be verified in the current host.
Do not install global packages or modify account/configuration settings on startup.
