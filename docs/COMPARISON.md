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

## Related projects

- [The AI Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) describes autonomous hypothesis generation, experiments and manuscripts with progressive agentic tree search. This repository supplies a researcher-owned project workspace and gate protocol for an existing assistant rather than the same exploration engine.
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) describes specialized agents covering literature review, experimentation and report writing, with varying human involvement. This template focuses on persistent claim/evidence/run contracts and the review decision tied to an artifact version.
- [AI-Researcher](https://github.com/HKUDS/AI-Researcher) describes an integrated autonomous scientific pipeline. This project's distribution emphasizes replaceable tools, project-local files, selected capability profiles and explicit research-owner decisions.
- [AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) provides broad domain skills and an autoresearch orchestration layer. This template packages a focused core around its numbered records and gates; the original sources and notices remain acknowledged.

These comparisons describe intended designs, not measured superiority, absence of
features in another project, or endorsement. No common benchmark has been run here
to rank novelty, manuscript quality, acceptance rate, cost or speed. Source READMEs
were checked on 2026-10-06; the projects may evolve independently.

## Attribution

Directly documented adapted reference material is identified in [NOTICE.md](../NOTICE.md).
Other related projects are comparison/design references, not automatically copied
dependencies. The template brings together iterative experimentation, artifact-based
state, progressive loading and evidence-aware review without claiming to incorporate
every capability or codebase from the research-agent ecosystem.
