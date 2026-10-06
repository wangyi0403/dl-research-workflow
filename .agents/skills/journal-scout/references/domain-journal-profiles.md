# Domain Journal Profiles: Civil/Transport Engineering + AI

General observations from publishing in AI × civil infrastructure journals. Principles, not specific papers.

## Journal Archetypes

### Type A: Domain-Application Journals
Focus on how AI solves a real infrastructure problem. The domain problem drives the narrative; the method serves it.

**Common expectations**:
- Clear description of the physical/engineering problem BEFORE introducing the method
- Real-world data (not synthetic) with domain-appropriate evaluation
- Practical significance demonstrated — what can engineers DO differently with your method?
- Comparison against current engineering practice, not just other ML methods

**Typical review culture**: Reviewers are domain experts first, ML experts second. Technical novelty may be less important than demonstrated usefulness. Expect questions about data representativeness, deployment feasibility, and failure modes.

### Type B: AI-Application Journals
Bridge between method novelty and engineering impact. Both the AI contribution and the application must be solid — neither can be weak.

**Common expectations**:
- Method novelty clearly distinguished from prior AI work
- Engineering problem described with enough depth that a non-domain ML reviewer understands the constraints
- Ablations that prove each component matters, not just "we added X and it helped"
- Comparison against both classic ML baselines AND recent domain-specific methods

**Typical review culture**: Mixed panel — some reviewers focus on method, some on application. The paper must satisfy both. Weak method → "just applying X to Y." Weak application → "toy problem."

### Type C: Method-Specialist Journals
Method novelty is the primary criterion. The application domain is a case study.

**Common expectations**:
- Formal problem statement, theoretical analysis preferred
- Strong ablation design with statistical rigor
- Multiple benchmark comparisons, ideally across domains
- The method pattern must be transferable — reviewer will ask "would this work on [different domain]?"

**Typical review culture**: Reviewers are method experts. Expect deep technical questions. "It works on our dataset" is not sufficient — you must explain WHY it works.

## Domain-Specific Scope Notes

### Infrastructure Inspection & Monitoring
Journals in this space value papers that move beyond "we detect defects" to "we enable better maintenance decisions." The key transition: detection → diagnosis → prediction → decision support. Each step upward increases novelty and impact.

### Structural Health Monitoring
Papers that use domain physics (even as loose constraints or interpretability anchors) are preferred over pure data-driven approaches. If your method exploits any physical knowledge of the system (material properties, load paths, failure modes), make it explicit and center the contribution around it.

### Railway/Transit Engineering
These journals expect familiarity with relevant industry standards and maintenance specifications. A method that ignores the standard defect taxonomy or the operational constraints of inspection vehicles will face skepticism. Cite the relevant codes/standards in your domain context.

## Common Rejection Patterns

1. **"Just applying [standard method] to [domain]"** — The method has no novelty; the domain contribution is not articulated as transferable knowledge.
2. **"Toy dataset"** — Data is too small, too clean, or too synthetic to convince domain reviewers.
3. **"No comparison with engineering practice"** — Only compared against other ML methods, not against what engineers currently do.
4. **"Over-claimed significance"** — Claims "real-time" but inference time is >100ms; claims "robust" but tested on only one weather condition.
5. **"Scope mismatch"** — Paper written as a method contribution but submitted to a domain-application journal (or vice versa). The contribution framing doesn't match the journal's expectations.
