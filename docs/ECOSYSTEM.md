# Design sources and distribution scope

[English](ECOSYSTEM.md) | [简体中文](ECOSYSTEM_CN.md)

[Home](../README.md) · [Design comparison](COMPARISON.md) · [Attribution](../NOTICE.md)

This distribution is a focused workflow, not a mirror of every research-skill library. Its value is the contract connecting questions, protocols, runs, evidence, figures and manuscripts. Skills can extend that contract when a study needs them.

## Material-level references, adaptations and licenses

The public core retains explicitly documented references to [Orchestra Research / AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) in its question-quality lenses, and adapted prose heuristics from [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone). Their notices are included in `licenses/` and exported to new projects. Academic sources remain identified in the relevant reference files. See [NOTICE](../NOTICE.md).

## Design influences and bundled scope

The maintainer identifies these projects as design influences. The table separately describes the public distribution boundary; influence does not imply copying a complete toolkit. See the [design comparison](COMPARISON.md) for the mapping. Ranking labels can be ambiguous; the linked repository identifies each reference.

| Repository / skill | Useful when | Distribution status |
|---|---|---|
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Broader scientific tooling; systematic literature review and scientific visualization | Design influence. The personal AgentHub skill catalog includes K-Dense-derived `literature-review` and `scientific-visualization`; neither ships in this repository or is an installable public profile of `project.py`. |
| [Nature Skills](https://github.com/Yuan1z0825/nature-skills), including `nature-literature-pipeline` | Literature processing, manuscript and figure workflows | Design influence; the complete upstream toolkit is not bundled. The name does not imply Nature journal endorsement. |
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) | Academic research and manuscript workflows | Design influence; the complete upstream toolkit is not bundled. |
| [ChineseResearchLaTeX / research-literature-review](https://github.com/huangwb8/ChineseResearchLaTeX/tree/main/skills/research-literature-review) | Research literature synthesis in a LaTeX-oriented toolkit | Design influence; not the same as the K-Dense `literature-review` skill. |
| [AIPOCH medical-research-skills](https://github.com/aipoch/medical-research-skills) | Medical systematic-review and screening tasks | Design influence; the complete upstream toolkit is not bundled. |
| [luwill / medical-imaging-review](https://github.com/luwill/research-skills/tree/main/medical-imaging-review) | Medical-imaging literature reviews | Design influence; similarly named skills also exist elsewhere, so check the source. |
| [PaperOrchestra / literature-review-agent](https://github.com/Ar9av/PaperOrchestra/tree/main/skills/literature-review-agent) | Agent-based related-work and literature workflows | Design influence; distinct from Orchestra Research above. |
| [Research Superpower](https://github.com/kthorn/research-superpower) | Literature search, screening, citation traversal and synthesis | Design influence; the complete upstream toolkit is not bundled. |

The K-Dense text provenance is supported by the historical [literature-review file](https://github.com/K-Dense-AI/scientific-agent-skills/blob/0936740e52033a6256085be5fc81e5e56d606110/skills/literature-review/SKILL.md) and [scientific-visualization file](https://github.com/K-Dense-AI/scientific-agent-skills/blob/878519452f5adacbe6ec89964dd8288c968dbb7f/skills/scientific-visualization/SKILL.md). The personal catalog is not an additional downloadable bundle or installation service provided by this repository; design influence and invocation in an individual task are separate questions. The bundled `scientific-figure-making` is a different skill from optional `scientific-visualization`.

## Extend a project deliberately

1. Identify the missing capability in the current stage. Read the upstream skill and inspect its scripts, dependencies and license.
2. Select only the relevant skill, record its source and version, and use the host's documented project-local import mechanism. This repository's `project.py add` handles bundled skills only; it does not download these repositories.
3. Preserve upstream notices and avoid overwriting existing skill identities or project records. Check actual discovery and tools in the selected agent.
4. Store outputs under the existing question/claim/experiment IDs. A literature skill still needs source verification; a figure skill still needs real data and visual checks.

Repository identities checked on 2026-10-06. Optional capabilities must be verified against the upstream version chosen for the study.
