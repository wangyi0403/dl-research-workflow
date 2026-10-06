# Design context and comparison

[English](COMPARISON.md) · [简体中文](COMPARISON_CN.md)

DL Research Workflow distills practical research-agent patterns into a portable
project contract: research question → evidence → experiment → result → manuscript.
Its key choices are inspectable in the actual files below.

| Design choice | Concrete implementation |
|---|---|
| Scientific judgment has an owner | Scope and authority in `00_start.md`; A–F decisions in their owning records |
| Questions precede model construction | Data audit, question candidates, feasibility, comparison and falsification in 01–05 |
| Results carry their lineage | Immutable experiment IDs, configuration hashes, source states and registry |
| Tables follow a declared run set | Result builder checks coverage, terminal states and metric provenance |
| Manuscripts follow the evidence | Claim/figure/section map in 09; figure and manuscript checks in 10–11 |
| Changes invalidate affected checks | Explicit A–F dependency routing, without restarting all unrelated work |
| Agents are replaceable | Shared file contracts, canonical skills, native Claude copies and generic explicit reading |
| Context is progressive | Current-stage entry in 00; relevant numbered records and selected profiles |

## Design influences and implementation

The projects below informed this template's design. The influences concern research progression, literature handling, skill organization, figure/manuscript alignment and review/repair. The table maps those ideas to inspectable implementation choices. The distribution keeps its focused 18-skill core and project records; running every upstream project is not required.

| Design influence | Pattern considered | How this template organizes it |
|---|---|---|
| [AI Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | Autonomous research and experimental iteration | Stage-based progress with budgets, stop rules and checked artifacts |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | Literature–experiment–report role collaboration | Handoffs carry question, claim and run IDs; the lead agent verifies integration |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | Connecting ideas, research execution and manuscripts | Persistent project records across stages, with replaceable tools and researcher decisions |
| [AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Reusable research skills and ideation lenses | 18 focused skills organized around Stage 0–6 and Gate A–F; question-quality references retain attribution |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Systematic literature workflows, citation checks and scientific visualization | Literature supports testable claims; figures trace to recorded runs and data without requiring the whole library |
| [Nature Skills](https://github.com/Yuan1z0825/nature-skills) | Structured literature processing, academic expression and figure workflows | Literature, claims, figures and manuscripts connect through shared stage records and checks |
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) | Research–writing–review–revision loops | Review findings bind to manuscript versions; repairs recheck affected gates |
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra) | Skill-based paper pipelines and quality assessment | Review perspectives follow the actual risk, with evidence and completed repairs as acceptance criteria |
| [Research Literature Review](https://github.com/huangwb8/ChineseResearchLaTeX/tree/main/skills/research-literature-review) | End-to-end literature synthesis and related-work organization | Synthesis feeds the question/evidence map and checked manuscript claims |
| [AIPOCH Systematic Review](https://github.com/aipoch/medical-research-skills) | Structured search, screening and evidence appraisal | Study-specific inclusion rules and evidence strength; a generic workflow is not a certified medical review |
| [Medical Imaging Review](https://github.com/luwill/research-skills/tree/main/medical-imaging-review) | Domain-specific questions, methods and literature organization | Data audit and domain-specific evaluation protocols keep comparisons meaningful |
| [Research Superpower](https://github.com/kthorn/research-superpower) | Literature discovery, screening, citation tracing and synthesis | Search serves research gaps and claim decisions; original-source support enters the records |

### A concrete example

Literature discovery, screening and synthesis feed the question/evidence map in `03_idea_report.md`, comparisons and tests in `05_experiment_plan.md`, claim decisions in `08_analysis.md`, narrative locations in `09_paper_plan.md`, and citation checks in `11_pre_submission_audit.md`. Literature tools, experiment assistants and writing assistants share that persistent record chain.

Nature Skills' literature pipeline, K-Dense's review tools and this template can serve different layers of the work. Design influence does not automatically supply their scheduled delivery, every database, specialized medical procedures or complete tool collections.

## Sources and distribution scope

Design influence follows the maintainer's development account; upstream capabilities are grounded in the linked project documentation, and implementation descriptions in this repository's current files and tools. Claims of specific code/text adaptation still require material-level attribution and licenses: see [NOTICE](../NOTICE.md). See [sources and distribution scope](ECOSYSTEM.md) for the actual bundled boundary.

Several repositories contain a skill named Medical Imaging Review; the table identifies the reference used here. PaperOrchestra and Orchestra Research are different projects. These are design comparisons, not claims that other projects lack a capability or measured rankings of paper quality, acceptance rate, cost or speed. Primary project pages checked on 2026-10-06.
