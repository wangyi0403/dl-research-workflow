---
name: "research-ideation"
description: "Develop literature-grounded research questions and testable candidates. Use for novelty checks, topic selection, or Stage 1C; search absence does not prove novelty."
---

# Research Ideation

Turn an initial topic into a small set of research directions whose problem, evidence gap, feasibility, and failure conditions can be inspected. This is a decision process with the user, not an automatic idea generator.

## Principles

- Define what counts as a good research question before asking AI to propose one: object, observable outcome, constraints, practical or scientific importance, support criteria, and falsification conditions.
- Treat papers, datasets, code, experiments, and expert judgment according to their source role. Discovery records and summaries can suggest a direction but cannot establish novelty or support a technical claim.
- Generate genuinely different candidates only when alternatives would improve the decision. Do not satisfy fixed idea, paper, score, or pilot quotas.
- Prefer the smallest test that distinguishes the central hypothesis from a plausible competing explanation.
- The user decides whether to pursue, revise, hold, or reject a direction.

## Workflow

### 1. Freeze the problem contract

Complete the research-question card in `docs/03_idea_report.md`:

- question and question type;
- object, observable variables, operating conditions, and excluded scope;
- why the problem matters and why existing practice is insufficient;
- expected mechanism or design hypothesis;
- current evidence, missing evidence, support criterion, and falsification criterion;
- data, compute, time, expertise, and authorization constraints.

For engineering research, distinguish the field problem, the reusable measurement/physical/inference question, and the proposed method used to test it.

### 2. Establish evidence readiness

Use the available scholarly-search route for discovery and authoritative records or original sources for verification. Start with a bounded, auditable batch, then expand only when nearest work, contradictory evidence, or coverage gaps remain material.

For each consequential source, record:

- stable identity and version;
- source role and verification status;
- exact section, table, figure, page, dataset record, or experiment artifact that supports or challenges the idea;
- local artifact or hash when one exists;
- limitations and unresolved conflicts.

Stop when the nearest-work boundary and important disagreements are clear enough to make the next decision, or explicitly record why coverage remains insufficient. Do not substitute citation counts, venue labels, recency scores, or an arbitrary paper count for evidence quality.

### 3. Generate candidate directions

Generate a small set of meaningfully different directions. The 5D lenses in `references/5d-framework.md` may help when the search space is narrow, but they are prompts rather than required quotas.

Each candidate must state:

- problem and proposed knowledge increment;
- closest prior work and the precise difference;
- linchpin assumption and competing explanation;
- required data, compute, skills, and permissions;
- decisive evidence and failure route.

### 4. Run collision and feasibility checks

Search for the closest prior art using terminology variants and adjacent fields. Record both confirming and conflicting work. “No hit found” means unresolved coverage, not proven novelty.

Reject, revise, or hold a candidate when required variables are unavailable, the comparison would be invalid, the cost exceeds the recorded budget, or existing evidence already defeats its central mechanism. Do not use a fixed novelty score or generic month estimate as a gate.

### 5. Design a discriminating pilot

When a safe local or already-authorized test can reduce uncertainty, define the smallest test that probes the linchpin assumption. Its code size, runtime, hardware, and number of candidates depend on the actual mechanism and Stage 0 budget; CPU, a fixed line count, a two-hour limit, and three parallel pilots are not universal requirements.

Record protocol, inputs, expected outcomes, stopping rule, result artifact, and how each possible outcome changes the candidate's status. Do not launch remote, paid, or externally mutating work without the required approval.

### 6. Gate the decision

Use `research-quality-gate` Gate A for consequential choices. Reviewers receive the question card, evidence bundle, and rubric without being told the desired conclusion. Preserve evidence-backed dissent; the final decision is based on blockers and evidence, not vote count.

## Output

Update `docs/03_idea_report.md` with:

1. research-question card;
2. evidence boundary and source registry;
3. closest-work and collision analysis;
4. candidate directions and rejection reasons;
5. pilot evidence when available;
6. selected direction, fallback, unresolved risks, and author decision;
7. Gate A record.

The stage is ready to advance when the selected direction has a meaningful and testable question, a credible evidence gap, a feasible data/compute path, explicit failure conditions, and a smallest useful next step. Evidence gaps may remain, but they must be visible and must constrain the permitted claim.

## References

| File | Open when |
|---|---|
| `references/5d-framework.md` | Additional lenses are needed to diversify candidate directions. |
| `references/lifecycle-assessment.md` | Project-specific feasibility and scheduling need deeper analysis. Treat example timelines as prompts, not gates. |
| `references/RESEARCH_BRIEF_TEMPLATE.md` | A standalone research brief is requested. |
| `references/pre-registration-template.md` | A confirmatory experiment needs hypotheses and falsification criteria frozen before execution. |
| `references/legal-fulltext-access.md` | Full text must be acquired through an open, user-provided, or user-authorized route. |
