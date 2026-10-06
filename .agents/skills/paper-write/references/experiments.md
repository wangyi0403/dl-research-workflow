# Experiments and Results Writing Guide

Present the evidence that answers the declared scientific questions. Use the approved protocol and current Claim/Evidence/Experiment records. The article type determines whether comparisons, interventions, proofs, cases or transfer tests are needed.

## Organize by claim

For each central empirical claim, identify the relevant result, comparison class, protocol, readout and interpretation. Report the minimal decisive evidence first; organize sections by questions rather than dataset names or run chronology when that improves understanding.

Use an ablation only when it tests a design or mechanism claim. A deletion that changes parameter count, optimization or available information may have several explanations. A matched replacement, controlled intervention or alternative prediction may discriminate better. A component-dependent gain does not alone identify why it occurs.

Transfer and robustness claims require independently justified settings. Do not choose only favorable datasets after inspecting results. Separate confirmatory analysis from exploratory or post hoc findings, and preserve protocol deviations and the predeclared run coverage.

## Establish comparison fairness

Name the baseline and version, data/split access, preprocessing, external training data, tools or privileged labels, tuning and model selection, inference budget and relevant hardware/software conditions. For agents include retries, samples, context and tool budget; for systems state batch, precision, workload and quality target.

Separate copied literature values or resource-unmatched comparisons from controlled rankings. A non-SOTA contribution may concern cost, calibration, data requirements, assumptions, reliability or a new measurement. State that axis directly without reinterpreting a post hoc selected regime as independently validated.

## Report uncertainty precisely

Specify the experimental or sampling unit, independent sample count, repeated measurements, seeds and aggregation. Repeated frames, time points or measurements from one subject/site/event do not automatically supply independent observations. Paired or clustered designs require an analysis that respects those dependencies.

Define each interval or error bar: SD, SE, confidence, credible or prediction interval are different quantities. State the variation captured, computation method and applicable assumptions. Report a meaningful effect estimate and uncertainty where the design supports them; do not manufacture an interval from a single result.

Statistical significance is not effect size or practical importance. A large p-value does not establish equivalence or absence of effect; overlapping intervals do not establish equality. An equivalence or noninferiority claim requires the corresponding design, margin and analysis. Explain multiplicity, missing/excluded results and analysis-set differences when relevant.

## Write from exact artifacts

Refer to a particular cell, curve region, operating point, case or formal condition and explain what it supports. A selected case illustrates behavior; broad frequency or superiority claims need an appropriate aggregate analysis. State case selection and denominator when they matter.

Preserve material negative, null and contrary results. A claim-changing result changes the claim or requires further evidence; a real trade-off belongs in the scoped conclusion. Secondary diagnostics may move to the supplement while preserving access and selection logic. Internal debugging records stay outside the manuscript unless they affect scientific interpretation or reproduction.

## Figure and table conventions

Use a table for exact lookup, a plot for a trend/distribution/trade-off, and prose for a simple fact. Avoid duplicate main-text displays without distinct roles. Provide metric direction, units, analysis unit, uncertainty definition and source. Keep precision consistent with measurement accuracy.

Follow the verified venue for caption position and formatting. Booktabs, decimal alignment and restrained emphasis are useful where permitted, not universal requirements. Never use a color or bold best value to imply a fair rank among unmatched methods; use non-color cues and inspect the rendered final size.

## Finish check

Reconcile methods as performed, registered/planned comparisons, actual coverage, values and conclusions. Complete scientific and visual checks appropriate to the claim; a successfully generated table is not a statistical analysis. Reuse unchanged verified records and report material unresolved items separately from manuscript prose.
