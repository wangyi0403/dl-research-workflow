# Author Voice Matching Guide

Match the manuscript's voice to the author's prior published work or the target venue's register.

## When Voice Matching Matters

- The author has prior accepted papers → match their established voice
- The paper is going to a specific venue → match that venue's register
- Multiple co-authors → blend voices consistently

## How to Extract Voice

Read 1-2 prior accepted papers from the same author. Note these features:

### Sentence Rhythm
- Average sentence length (words): short (15-20) vs. medium (20-30) vs. long (30+)
- Variation: monotonous (all similar length) vs. varied (mix of short and long)
- Opening style: subject-first ("We propose...") vs. clause-first ("To address X, we propose...")

### Connective Habits
- Heavy connector use: "Furthermore", "Moreover", "In addition", "Consequently"
- Light connector use: mostly "and", "but", "however"
- Transition style: explicit signposting ("In Section 3, we...") vs. implicit flow

### Hedging Level
- Heavy hedging: "may", "suggest", "potentially", "appears to", "might"
- Moderate hedging: occasional "suggest" and "may" when evidence is partial
- Light hedging: claims only when evidence is strong; "may" used sparingly

### Section Opener Patterns
- "We begin by..." / "This section describes..."
- Direct: "The model consists of three components."
- Context-first: "Accurate detection requires both spatial and temporal information. Our model..."

### Notation Conventions
- Scalar: italic `x` vs. non-italic
- Vector: bold `\mathbf{x}` vs. arrow `\vec{x}`
- Matrix: bold uppercase `\mathbf{X}` vs. `X`
- Sets: calligraphic `\mathcal{X}` vs. blackboard bold `\mathbb{X}`

### Recurring Phrasings
- "In contrast to..." vs. "Unlike..." vs. "Compared with..."
- "We observe that..." vs. "The results show..." vs. "As shown in Table 1..."
- "It is important to note..." — if the author NEVER uses this, don't introduce it

## Venue Register Matching

### ICLR / NeurIPS / ICML (ML conferences)
- **Terse, direct, results-forward**
- Short paragraphs (3-5 sentences)
- Minimal "roadmap" text ("The rest of this paper is organized as follows...")
- Method equations are central; text supports them
- "We" is standard and frequent

### Nature / Science / PNAS
- **Expository, broader significance**
- First paragraph must be accessible to non-specialists
- Methods often in supplementary (Nature) or condensed
- "Here we show..." pattern common in opening
- Citations as superscript numbers, not author-year

### Elsevier Journals (engineering/applied science)
- **Neutral, methodical, comprehensive**
- Longer introduction (2-3 pages) with thorough literature review
- Detailed method section — reproducibility is expected
- "This paper"/"This study" more common than "We"
- section-based structure with numbered subsections

### IEEE Transactions
- **Technical, precise, self-contained**
- Abstract with specific numbers
- Heavy use of "we" acceptable
- Extensive mathematical notation
- Figures and tables must be understandable in grayscale

## Practical Process

1. **Read 1-2 prior accepted papers** from the author. Note the 6 dimensions above.
2. **Compare with the current draft**. Where does the voice diverge?
3. **Adjust**: sentence rhythm first (biggest impact), then connectors, then hedging.
4. **Don't over-fit**: match the author's best paper, not their quirkiest one.
5. **When in doubt, default to venue register**: a paper that sounds like it belongs in the journal is better than one that sounds like the author's idiosyncratic voice.

## Red Flags (Voice Inconsistency)

- Author's prior papers use "we" sparingly → new draft uses "we" in every paragraph
- Author's prior papers have 25-word average sentences → new draft alternates 10-word and 50-word
- Author's prior papers never use "Moreover" → new draft has three "Moreover"s in the introduction
- Author's prior papers use `\mathbf{x}` for vectors → new draft uses `\vec{x}`
