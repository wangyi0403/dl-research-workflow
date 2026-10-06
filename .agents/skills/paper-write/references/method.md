# Method Writing Guide

Describe the method as actually implemented, with enough information to understand and reproduce the scientifically important operations. Use the problem formulation, assumptions and notation in the approved methodology record.

## Establish the object

Define inputs, outputs, available information, assumptions, objective and any new construct. Keep notation and names stable, and distinguish training, calibration, inference and evaluation. State when ground truth, future information or a privileged resource is unavailable at deployment.

## Explain the design

Order the account by mathematical or operational dependencies. Explain why a consequential design choice is needed, what it does, and what evidence or formal argument supports the proposed effect. A component motivation is not itself a result; an empirical gain is not proof of a physical mechanism.

Use equations for precise relations, an algorithm when state/order/branching would otherwise remain ambiguous, or an overview figure when connections are difficult to follow. Choose the representation by its explanatory role. A clear simple method need not contain a diagram or pseudocode.

For a pipeline, show how information passes between components and define intermediate objects before their use. For a theoretical result, state assumptions and the exact conclusion, explain where assumptions enter, and link to the complete proof. Do not present an empirical regularity as a theorem.

## Connect to execution

Identify implementation parameters and choices that affect the result: transforms, losses, stopping rules, tolerances, sampling, precision and selection criteria as applicable. Put essential interpretation details in the main text; place exhaustive settings in the supplement or linked reproducibility material. Check the prose, equations, algorithm and executed code path against the same version.

For a numerical or physical model, define units and boundary/initial conditions and refer to the project's validation contract. Solver residuals, conservation and convergence establish different properties from agreement with observations; report only checks actually performed.

## Verify

Can a reader trace each scientifically important input to the output, see the actual insight and locate the conditions for a claim? Recover the argument from the section without assuming the overview picture fills a missing definition. Keep genuine inherited design choices and limits visible. Do not add a per-component novelty claim or force every paragraph to explain its own purpose.

Optional pipeline patterns are indexed in [method-examples.md](examples/method-examples.md). They are examples, not a universal module template.
