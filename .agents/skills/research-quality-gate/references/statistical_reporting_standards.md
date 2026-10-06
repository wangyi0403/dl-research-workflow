# Statistical Reporting: Design-Conditional Review Reference

Use at Gates B-C when statistical inference matters, or when reviewing the statistical part of a manuscript. This is a decision aid, not a verified journal policy, a universal APA checklist or a numerical acceptance rubric. Select checks from the estimand, study design, analysis unit and actual claim. Mark non-applicable checks explicitly and verify any claimed external reporting requirement against its current primary source.

## 1. Establish the Analysis Contract

Before selecting a test or judging reporting, identify:

- The question, target population or evaluation scope, estimand and outcome units.
- The sampling or assignment process, independent units and dependence structure: repeated measures, matched samples, sites, subjects, sequences, datasets or training seeds.
- The planned comparisons, uncertainty target, decision criteria, stopping rule and distinction between confirmatory and exploratory analyses.
- Missingness, exclusions, failures, data splits and any changes after results were observed.
- Which numbers are estimates, descriptive summaries or deterministic outputs, and where their inputs and aggregation commands are recorded.

Choose descriptive summaries that express the relevant distribution and question; mean/SD, median/IQR, proportions and counts have different roles. Do not require every summary for every variable.

For a substantive comparison, report the effect or difference in interpretable units and its uncertainty when material to the claim. A standardized effect size is useful only when it supports interpretation or comparison; generic small/medium/large cutoffs do not replace domain meaning. State the uncertainty definition and coverage level rather than assuming every interval is a 95% confidence interval.

Justify sample size or computational replication in relation to the inference: prospective power, precision, sensitivity, a fixed available population, established benchmark scope or resource constraints may be relevant. Record the resulting limits. Do not request observed post-hoc power by default or treat a non-significant result as proof of equivalence; inspect the estimated effect, uncertainty and any specified equivalence margin.

## 2. Method-Specific Questions

These prompts apply only when the corresponding method or claim is used. They are not automatic test-selection rules.

| Analysis | Questions that change validity or interpretation |
|---|---|
| Two-group or paired comparisons | Does the test respect pairing and the independent unit? What difference is estimated? Are variance and distribution assumptions relevant to this estimator and sample structure, and how are they assessed? |
| Multi-group or factorial analysis | Are factors, interactions and planned contrasts tied to the question? Which comparison family is being interpreted, and what multiplicity strategy or limitation applies? |
| Regression or prediction | Is the purpose estimation, prediction or causal inference? Are specification, dependence, missingness and influential observations addressed? For prediction, are training, tuning and evaluation separated? |
| Binary outcomes | Are outcome counts, separation or sparsity, calibration and uncertainty addressed where relevant? Is an odds ratio distinguished from a risk or probability difference? |
| Clustered, repeated or longitudinal data | Is dependence represented in the model or uncertainty calculation? Are cluster counts, pairing, time structure and resampling units documented? |
| Latent-variable or structural equation models | Are identification, measurement, estimator assumptions and the claimed interpretation justified? Report relevant diagnostics; do not turn generic sample-size or fit-index cutoffs into automatic pass/fail rules. |
| Categorical counts | Does the analysis match independence, pairing and sparse counts? Select exact, asymptotic or model-based inference with an applicable rationale rather than a universal cell-count threshold. |
| Rank, permutation or bootstrap methods | What hypothesis or estimand is addressed? Are exchangeability, dependence and resampling units appropriate? Do not assume these methods remove all assumptions. |
| Deep-learning comparisons | Which variation is represented: seeds, examples, splits, sites or datasets? Are shared test examples paired appropriately? Are selection, tuning budgets, failed runs and the aggregation over seeds traceable? |
| Causal claims | What identification assumptions and design support the interpretation? A predictive improvement, correlation or significance result alone does not establish a mechanism. |

Assess assumptions using the research design, relevant diagnostics and sensitivity analysis. Formal assumption tests are not mandatory for every model, and a threshold crossing alone does not determine whether an analysis answers its question.

## 3. Reporting and Venue Style

Preserve the statistic, units, denominator, independent sample size, comparison direction and uncertainty definition needed to interpret a result. Report the method and software/version or reproducible code when they affect reproducibility. Use enough numerical precision to preserve meaning without implying unsupported accuracy.

When hypothesis tests are used, state the relevant hypothesis, test, decision threshold, one/two-sided choice when material, and handling of the interpreted comparison family. Report non-significant as well as significant planned results. Distinguish exact, rounded and bounded p-values; do not write a rounded zero as an exact probability.

APA notation, italicization, leading-zero rules, caption position and table style apply only when the confirmed venue requires them. Consult that source for formatting; do not label a scientific result wrong solely because it uses another accepted presentation style. Do not infer a statistic's mathematical range from typography conventions.

## 4. Evidence-Based Review Signals

Investigate the following when the source records support the concern. They are prompts to check context, not proof of misconduct or a preset severity score.

| Signal | Evidence to inspect |
|---|---|
| Selective reporting | Planned outcomes/comparisons versus reported results, including failures and null results |
| Unclear analysis changes | Dated plans, protocol deviations, exploratory labels and their effect on interpretation |
| Multiple comparisons or repeated looks | The actual family of claims, selection/stopping process and control or qualification of error |
| Unexplained exclusions or missingness | Counts, reasons, timing, handling assumptions and material sensitivity |
| Uncertain precision | The interval or other uncertainty measure and whether it permits the stated conclusion |
| Inconsistent numbers | Structured outputs, denominators, degrees of freedom, units and aggregation commands |
| Dependence ignored | Sampling, pairing, clustering and the unit treated as independent |
| Overstated conclusions | Whether superiority, equivalence, mechanism or transfer claims exceed the design and evidence |

A p-value near a threshold, all hypotheses being supported, absence of preregistration or a small sample does not itself establish a defect. State the unresolved consequence after inspecting the relevant evidence. Where an analysis is exploratory, report that status rather than inventing a retrospective confirmatory plan.

## 5. Domain Adaptation

Apply domain-specific checks only to the study actually being reviewed. For example, surveys may require attention to sampling weights and clustering; multi-site experiments to site effects; sensor sequences to temporal dependence; benchmarks to dataset contamination and repeated use of test sets. Do not import a higher-education, clinical or social-science checklist solely because the study is quantitative.

Verify a named reporting guideline when it is genuinely applicable. Record which version and parts apply; this reference does not claim compliance with an unverified standard.

## 6. Review Outcome

Report applicable checks, evidence inspected, material issues, non-applicable items and unresolved information. Assign issue severity by its consequence for the actual claim. Provide the smallest repair, or the narrower wording warranted by current evidence.

Do not compute a weighted completeness or acceptance score from missing checklist items. A fixed formatting preference cannot offset a validity blocker, and missing source evidence cannot be converted into a pass.

## 7. Suggested Review Sequence

Establish the analysis contract, select relevant method questions, compare reported numbers with their sources, inspect material review signals, and then verify applicable venue formatting. Write the decision and evidence links into the designated Gate B/C or manuscript audit record without creating a parallel status ledger.
