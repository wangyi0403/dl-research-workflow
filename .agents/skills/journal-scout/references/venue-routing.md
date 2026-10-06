# Venue Routing: Matching Manuscript to Journal

> How to decide which journal fits your manuscript type, contribution shape, and evidence strength.
> Use BEFORE the 4-phase scout process to narrow the search space.

## Step 1: Classify Your Manuscript

Before searching for journals, classify what kind of paper you have:

| Dimension | Options | Why It Matters |
|-----------|---------|---------------|
| **Contribution type** | Method · Application · Benchmark · Theory · Survey | Different journals prefer different types |
| **Evidence scale** | 2-3 datasets · 5+ datasets · Real deployment · Simulation only | Journals have implicit evidence expectations |
| **Novelty level** | Incremental improvement · New combination · New problem formulation · Paradigm shift | Dictates venue tier |
| **Domain specificity** | Domain-specific tool · Domain-informed method · Domain-agnostic method · Cross-domain validation | Determines breadth of suitable journals |

## Step 2: Journal Types

### Type A: Domain-Specialist Journals
- **Examples**: Automation in Construction, IEEE Trans. Transportation Electrification, Railway Engineering
- **What they want**: Domain problem clearly stated, method validated on domain data, practical impact demonstrated
- **Contribution expectation**: The domain problem is the story; the method serves it
- **Risk**: If your method is generic but domain story is thin → "just applying [X] to [Y]"

### Type B: Method-Specialist Journals
- **Examples**: Pattern Recognition, Neural Networks, IEEE Trans. Pattern Analysis and Machine Intelligence
- **What they want**: Method novelty clearly articulated, strong ablations, multiple benchmark comparisons
- **Contribution expectation**: The method is the story; the domain is a case study
- **Risk**: If domain is railway but method is standard → "insufficient novelty"

### Type C: AI-Application Journals
- **Examples**: Engineering Applications of AI (EAAI), Expert Systems with Applications (ESWA), Advanced Engineering Informatics (AEI)
- **What they want**: AI method + real engineering problem + demonstrated value
- **Contribution expectation**: Both method AND application matter; neither can be weak
- **Risk**: "Good AI, trivial application" or "Good application, trivial AI"

### Type D: General Science / High-Impact
- **Examples**: Nature, Science, PNAS, Nature Communications
- **What they want**: Broad significance, paradigm-shifting finding, accessible to non-specialists
- **Contribution expectation**: ONE big finding that matters beyond your field
- **Risk**: Very high desk-reject rate; only suitable if the finding is genuinely broad

## Step 3: Evidence-to-Venue Match

| Your Evidence Profile | Suitable Venue Type |
|----------------------|-------------------|
| 2-3 datasets + strong ablations | Domain-specialist or AI-application |
| 5+ datasets + cross-domain validation | AI-application or Method-specialist |
| Real deployment + user study | Domain-specialist (strong fit) |
| New problem + proof-of-concept | AI-application (novelty from problem, not method) |
| Theoretical guarantees + empirical validation | Method-specialist |
| Broad, paradigm-shifting finding | General science (rare) |

## Step 4: Quick Elimination

Eliminate journals that:
- Haven't published your method type in the last 2 years
- Have an average review cycle > your time budget
- Require page charges you can't afford
- Are known to desk-reject without external review for papers like yours

## Routing Heuristics

```
IF contribution = method-first AND novelty = high
   → Method-specialist (PAMI, Pattern Recognition, Neural Networks)

IF contribution = problem-first AND domain = strong
   → Domain-specialist (AIC, IEEE T-TE, CACAIE)

IF contribution = hybrid AND both method AND application are solid
   → AI-application (EAAI, ESWA, AEI)

IF finding = paradigm-shifting AND audience = broad
   → General science (Nature, Science — with extreme caution)
```
