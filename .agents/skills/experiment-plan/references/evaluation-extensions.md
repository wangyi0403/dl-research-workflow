# Conditional Evaluation Extensions

Use only the section that matches the experiment. These checks supplement the claim-driven plan; they do not create a new mandatory workflow.

## Generative or agent outputs

Before defining a hallucination, correctness, or task-success metric, state:

- **Reference world or source of truth:** the document, database, simulator state, environment, rubric, or human record against which observable claims are judged.
- **Observability:** what the model can and cannot see at the decision point.
- **Conflict policy:** which source wins when instructions, retrieved context, world knowledge, tools, or later state disagree.
- **Unknown and abstention policy:** when the model may or must defer, refer, or return unknown.
- **Error taxonomy:** separate reference-world mismatch from perception, planning, reward, schema, tool, or execution errors.

The evaluator and model must not silently use different reference worlds. Record adjudication rules and inter-rater disagreement when human judgment supplies the truth source.

Primary source: [A Unified Definition of Hallucination](https://arxiv.org/abs/2512.21577).

## Physics-informed or numerical models

Do not evaluate a physics-informed model only by training loss or residual. When applicable, specify:

- governing equations, units, boundary/initial conditions, and enforcement method;
- analytical, manufactured-solution, FEM, FDM, or validated-solver reference;
- discretization or resolution study and error norm;
- collocation/sampling sensitivity and optimization stability;
- accuracy, convergence failures, runtime, memory, and setup cost under comparable conditions;
- forward, inverse, interpolation, extrapolation, and parameter-identification claims separately.

Do not call the learned method a replacement for a numerical solver unless the declared benchmarks support that statement across the intended operating regime.

Primary sources: [original PINN framework](https://doi.org/10.1016/j.jcp.2018.10.045) and [PINN training-pathology analysis](https://doi.org/10.1016/j.jcp.2021.110768).

## Engineering surrogate models and uncertainty

For safety- or decision-relevant surrogates, report more than average predictive accuracy:

- intended decision and cost of an overconfident error;
- aleatoric and epistemic sources when the distinction is meaningful;
- calibration, interval/coverage performance, and subgroup or operating-regime behavior;
- out-of-distribution or extrapolation checks;
- sensitivity to training design and high-fidelity reference error;
- how uncertainty changes acceptance, referral, safety factor, inspection, or design decisions.

Treat interpretability and uncertainty as claim-specific evaluation dimensions, not decorative plots. If uncertainty is not validated, limit the claim to point prediction under the tested conditions.
