# Figure Type Selection (论文类型 → 图结构选型)

> Step 1 front-end for this skill: **classify the paper type first, then pick the diagram
> structure** — instead of defaulting to a generic "input→model→output" flow.
> Visual style (colors / arrows / fonts / CVPR-NeurIPS rules) lives in `SKILL.md`; this file
> only covers *which structure to draw* and *which prompt failure modes to avoid*.

---

## Section 1 · Paper Type × Diagram Structure (master table)

| Paper Type | Typical signals | Primary diagram | Secondary options | Visual focus |
|-----------|----------------|-----------------|-------------------|-------------|
| **A · Method** | New model / framework / loss / training strategy | Method Overview / Model Architecture | Layered pipeline, Contrastive method | Core module hierarchy + info flow |
| **B · Mechanism** | Ablation, probing, attention, module analysis | Mechanism Zoom-in / Contrastive | Multi-panel, Ablation matrix | Innovation mechanism + before/after |
| **C · Benchmark** | New dataset / eval suite / leaderboard | Evaluation Pipeline / Data Construction | Multi-panel, Taxonomy tree | Task construction + metric aggregation |
| **D · Scaling Law** | Compute curves, perf trend, law fitting | Trend Panel / Experimental Matrix | Variable-relationship diagram | Variable relations + design implications |
| **E · Robot / Embodied** | Perception-action loop, manipulation, navigation | **Closed-Loop Feedback** | System framework, State diagram | Full sense→plan→act→feedback cycle |
| **F · AI for X** | Medical AI, AI4Science, smart mfg, cybersecurity | Cross-domain Application Framework | System arch w/ domain labels | Domain data + AI model + task + validation |
| **G · Survey** | Literature taxonomy, roadmap, comparison | Taxonomy Tree / Timeline / Comparison Matrix | Multi-panel historical overview | Coverage breadth + classification logic |

> ⚠️ This skill (`paper-illustration`) is for **schematic / conceptual** figures. For
> **data plots** (line/bar/scatter/box/heatmap) use `scientific-figure-making` instead — types
> D and the quantitative panels of B/C often belong there, not here.

---

## Section 2 · 11 Diagram Structures — when + how

Each entry feeds the **Step 1 prompt template** in `SKILL.md` (component list, layout, connections).

1. **Method Overview (方法总览)** — full input→output pipeline. Multi-stage horizontal/vertical flow; core module = accent color + larger, support modules = neutral gray. *e.g. Transformer/diffusion method papers.*
2. **System Framework (系统框架)** — end-to-end system, multiple subsystems. Layered blocks grouped by function (subtle background zones); interfaces = dashed connectors; storage = cylinder/card stack. *e.g. RAG, multi-agent, prod ML.*
3. **Model Architecture (模型架构)** — NN internal structure matters. Layer-by-layer blocks; skip/residual = bypass arrows; dim labels encouraged for transformers. *e.g. ViT/U-Net/LLM arch.*
4. **Mechanism Diagram (机制示意)** — one sub-mechanism (attention/routing/gating) is the contribution. Zoom-in on a single module; magnifying-glass metaphor; ops (softmax, cross-attn) shown symbolically, **not as formulas**. *e.g. sparse attention, MoE routing.*
5. **Closed-Loop Feedback (闭环反馈)** — robots, embodied AI, RLHF, active learning. Circular flow Perceive→Understand→Plan→Act→Observe→repeat; **the loop arrow MUST visually close**; environment = external zone, agent = central entity, each phase color-coded. *e.g. RT-2, EmbodiedGPT, RLHF.*
6. **Multi-Panel Composite (多面板)** — multiple contributions/modalities/settings. 2×2 / 3×1 / asymmetric grid; per-panel (a)(b)(c) labels; shared palette + font; one panel dominant if there is a primary result.
7. **Experimental Trend Summary (实验规律)** — scaling laws, empirical/sensitivity analysis. Trend panels / annotated curves; axes labeled w/ units; inflection points in callout boxes; multi-curve uses distinct **line style AND color**; bottom summary banner. *(borderline data-plot — consider `scientific-figure-making`.)*
8. **Evaluation Pipeline (评测流程)** — benchmark / eval-framework / metric-design papers. Sequential: data→preprocess→task construction→model I/O→metric→aggregation; inline sample cards; formulas symbolic. *e.g. MMLU, HumanEval.*
9. **Contrastive Method (对比式方法)** — proposed vs prior/baseline. Left(prior) vs Right(proposed) or Top/Bottom; **consistent module notation both sides**; prior issues = warning/crossed-out, improvements = green check/accent; don't make prior look "wrong". *Any "unlike prior work…" intro.*
10. **Data Construction Pipeline (数据构建)** — dataset / data-centric / synthetic-data papers. Source→Collect→Filter→Annotate→QC→Final; volume numbers per stage; filter = diamond decision node; annotation = person icon; final stats as badge/mini-table. *e.g. LAION, DataComp.*
11. **Cross-Disciplinary Application (跨学科应用)** — medical/climate/bio/chem/materials + AI. Domain-data zone + AI-model zone + task zone + validation/impact zone; domain symbols must reflect the field (MRI, molecular graphs, sensor traces); validation uses domain metrics (not just acc/F1). *e.g. AlphaFold, medical seg, climate downscaling.*

---

## Section 3 · Five prompt failure modes (self-check before generating)

1. **Abstract-only input** — abstract = results, not structure → random boxes + arrows. **Fix:** require the method section / key-module descriptions / bullet contributions. If user pastes only an abstract, ask before proceeding.
2. **Vague style keywords** — "high-end / sci-fi / technology aesthetic" push the model to 3D, glow, cyberpunk. **Fix:** replace with venue/format anchors: ✅ "IEEE TPAMI-style mechanism diagram: flat vector, white background, clean lines" / "NeurIPS method overview: 2D, functional color only, no decoration".
3. **Paper type not declared** — without a type the model defaults to generic left→center→right, wrong for most types. **Fix:** declare the type (A–G), pick the matching structure from Section 1 *before* assembling the prompt.
4. **Information overload** — more elements ≠ higher quality; 15+ modules / 30+ arrows / paragraph labels get rejected. **Fix:** "what is the ONE thing this figure must communicate?" — build around that thread, demote/grey support modules, push extras to caption. Capacity:

   | Figure size | Max primary modules | Max arrows |
   |------------|--------------------|-----------|
   | Single column | 5–7 | 6–10 |
   | Full-page | 8–12 | 12–18 |

5. **Decoration overload** — quality comes from order/restraint, not gradients/shadows/glow/texture. **Fix:** enforce flat-vector spec; if the model decorates, add the negative constraint:
   ```
   Prohibited: 3D perspective, drop shadows, glow effects, gradient backgrounds,
   neon colors, texture fills, commercial poster visual elements.
   禁止：3D透视、阴影、发光、渐变背景、霓虹色、纹理填充、商业海报风格元素。
   ```
   (This complements the "What to AVOID" list already in `SKILL.md`.)

---

## Section 4 · Quick diagnosis flow

```
paper content
  └─ only an abstract? ── YES → request method/modules first
        │ NO
  classify paper type (A–G, Section 1)
        │
  select structure (Section 2)
        │
  schematic or data plot?
     data plot → hand off to scientific-figure-making
     schematic ▼
  assemble Step-1 prompt (SKILL.md) + run 5-failure self-check (Section 3)
        │
  generate → STRICT review (SKILL.md Step 5) → pass? deliver : refine
```
