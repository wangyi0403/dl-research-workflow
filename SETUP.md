# Portable setup

[English](SETUP.md) | [简体中文](SETUP_CN.md)

[Home](README.md) · [Copy the startup prompt](README.md#start-here)

## Prerequisites

Use Python 3.10+ and an assistant able to read project files. Setup uses only the standard library. Scientific execution needs the packages and tools required by the chosen study; these are not installed automatically.

## Interface details

| Interface | Setup option | Entry / discovery |
|---|---|---|
| Codex | `--agent codex` | `AGENTS.md`; canonical `.agents/skills/` |
| Claude Code | `--agent claude` | `CLAUDE.md`; additional `.claude/skills/` copies |
| DeepSeek Harness | `--agent dsh` | Shared file contract; explicitly provide `AI_START.md` and skill files |
| ZCode | `--agent zcode` | Workspace `AGENTS.md`; explicit skill reading or project-scoped UI import |
| Other file-capable agents | `--agent generic` | Explicitly read `AI_START.md`, `AGENTS.md` and selected skill files |

This table describes bundled file adapters, not a certification of every assistant, tool, operating system or model. Generic mode requires a capable file-reading assistant; native integrations for unspecified agents are not claimed.

DSH/ZCode modes retain the canonical project skill directory; they do not install a vendor plugin or modify global configuration. See [compatibility notes and official sources](docs/AGENT_COMPATIBILITY.md).

## Initialize a separate study

Run from the distribution checkout:

```bash
python tools/project.py init ../my-study --agent generic --profile research --dry-run
python tools/project.py init ../my-study --agent generic --profile research
python tools/project.py check ../my-study
```

Use a separate directory outside the distribution checkout. Initialization checks all planned files for conflicts before writing and refuses to replace different content. New projects retain the local setup/check utility, so future checks can run from their own directory.

## Select profiles

| Profile | Scope |
|---|---|
| `full` | All 18 core skills |
| `research` | Questions, data, methods, experiments, claims and gates |
| `writing` | Planning, drafting, language, citations, numerics and manuscript review |
| `figures` | Data visualization, illustrations and evidence checks |
| `release` | Local submission/release preparation |

```bash
python tools/project.py init ../my-study --agent claude --profile research
python tools/project.py add ../my-study --profile writing figures
python tools/project.py list
```

`--skill <name> ...` selects individual bundled skills. When adding skills, omit `--agent` to preserve the existing adapter. `add` supplements an existing project without rewriting its research records. Use the distribution checkout as the source for adding profiles; a partial study does not contain the omitted skills.

The public distribution includes only the 18-core catalog. Additional domain skills can be separately selected from a reviewed source under the project owner's authorization; the full local skill marketplace is not bundled.

## Dependencies and state

`paper-audit` uses ten project-local support scripts in `.agenthub/runtime/latex-paper-en/scripts/`. They are installed when the selected profile needs them and are not a nineteenth skill. Optional plotting packages are listed in `.agents/skills/scientific-figure-making/requirements.txt`.

`docs/00_start.md` is the scientific project state entry. `.agenthub/project.json` only records installed skills and the file adapter; it contains no credentials or absolute source path and is ignored by Git.

Fill the question, data boundaries, evidence targets, budget, permissions and next gate in `00_start.md`. Then ask the assistant to follow the appropriate workflow stage. Initialization does not launch experiments or schedule monitoring.

## Check the package

```bash
python tools/project.py check .
python -B -m unittest discover -s tools/tests -p "test_*.py"
python -B -m unittest discover -s experiments/tests -p "test_*.py"
```

These verify setup, protected writes and experiment-table contracts. Scientific conclusions, source support, research ethics, figures and manuscript compilation need their own applicable checks.
