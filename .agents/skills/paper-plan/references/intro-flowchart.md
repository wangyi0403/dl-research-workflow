# Optional Introduction Pattern for Engineering Method Papers

Use this pattern when a concrete operating problem and a proposed method form the paper's argument. It is an example, not a universal introduction structure. The approved paper type, evidence and venue determine which elements belong, their order and their length. Benchmark, evaluation, theoretical and new-setting papers may need different structures.

## Candidate Argument Moves

| Move | Reader question | Evidence to use |
|---|---|---|
| Scene and concrete example | What problem matters in practice? | A documented case or representative example; no invented scale or measurements |
| Existing approaches and limitations | What remains unresolved? | Fair comparisons with verified closest work |
| Problem and constraints | What exactly is being studied? | Task definition, assumptions and actual operating constraints |
| Technical difficulty | Why is the problem not resolved by an obvious alternative? | Evidence about the relevant alternatives and failure conditions |
| Method overview | What design addresses the problem? | The approved methodology and its supported rationale |
| Contribution and evidence | What has the study established? | Verified claims, decisive results and their scope |

Combine or omit moves that do not serve the paper. A running example helps when it makes the task concrete, but need not appear in every paper or section. Do not invent numbers to make it vivid.

## Mapping Challenges, Designs and Claims

Trace a claimed design benefit to the problem it addresses and the experiment that tests it. The mapping can be one-to-many or many-to-one: a shared component may address several constraints, and several components may jointly address one challenge. A component is not automatically a separate contribution, and a contribution can be a finding, dataset or evaluation resource rather than a module.

Use as many contribution statements as the verified contribution set needs. Do not require a fixed number of limitations, challenges, bullets or paragraphs. Preserve benchmark or evaluation contributions when they are supported and central to the selected paper type.

## Review Questions

- Can the reader identify the question and why it matters from supported context?
- Are prior approaches represented fairly, including alternatives that weaken the proposed novelty story?
- Are the task, assumptions and constraints clear enough to understand the scope?
- Does the method overview explain the relevant design idea without replacing the evidence?
- Does each contribution state something the paper actually establishes, with a known evidence location?
- Would another structure better serve the selected paper type or the target venue?

Record the chosen structure in `docs/09_paper_plan.md`; do not create a competing narrative plan in this reference file.
