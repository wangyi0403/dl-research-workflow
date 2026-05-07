---
name: research-review
description: Get a deep critical review of research via Agent self-review (Opus critic role). Use when user says "review my research", "help me review", "get external review", or wants critical feedback on research ideas, papers, or experimental results.
argument-hint: [topic-or-scope]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent
---

# Research Review via Agent Self-Review (Opus Critic Role)

Get a multi-round critical review of research work using a Claude Opus Agent sub-agent as an adversarial critic.

## Constants

- REVIEWER_MODEL = `claude-sonnet-4-6` — Self-review via Agent sub-agent (critic role)

## Context: $ARGUMENTS

## Prerequisites

No external MCP required. Reviews use the Agent tool to spawn a sub-agent acting as an adversarial ML reviewer.

## Workflow

### Step 1: Gather Research Context
Before calling the reviewer, compile a comprehensive briefing:
1. Read project narrative documents (e.g., STORY.md, README.md, paper drafts)
2. Read any memory/notes files for key findings and experiment history
3. Identify: core claims, methodology, key results, known weaknesses

### Step 2: Initial Review (Round 1)
Use the **Agent tool** with a critic role prompt:

```
Agent prompt:
  You are playing the role of a rigorous external ML reviewer (NeurIPS/ICML level).
  Your job is to find weaknesses, not to be supportive. Be adversarial and honest.

  Research context:
  [Full research context + specific questions]

  Please identify:
  1. Logical gaps or unjustified claims
  2. Missing experiments that would strengthen the story
  3. Narrative weaknesses
  4. Whether the contribution is sufficient for a top venue

  Be brutally honest. Save your review to RESEARCH_REVIEW.md.
```

Save the Agent's response verbatim to `RESEARCH_REVIEW.md`.

### Step 3: Iterative Dialogue (Rounds 2-N)
Each round is a new Agent call. Include the previous review as context in the prompt:

```
Agent prompt:
  You are continuing a multi-round review. Your previous assessment was:
  ---
  [Paste previous review from RESEARCH_REVIEW.md]
  ---

  The researcher has responded:
  [Your response to criticisms / new evidence / counterarguments]

  Follow-up questions:
  [Targeted follow-ups on actionable points]

  Please update your assessment and respond to the above.
```

Key follow-up patterns:
- "If we reframe X as Y, does that change your assessment?"
- "What's the minimum experiment to satisfy concern Z?"
- "Please design the minimal additional experiment package (highest acceptance lift per GPU week)"
- "Please write a mock NeurIPS/ICML review with scores"
- "Give me a results-to-claims matrix for possible experimental outcomes"

### Step 4: Convergence
Stop iterating when:
- Both sides agree on the core claims and their evidence requirements
- A concrete experiment plan is established
- The narrative structure is settled

### Step 5: Document Everything
Save conclusions to `RESEARCH_REVIEW.md`:
- Round-by-round summary of criticisms and responses
- Final consensus on claims, narrative, and experiments
- Claims matrix (what claims are allowed under each possible outcome)
- Prioritized TODO list with estimated compute costs
- Paper outline if discussed

Update project memory/notes with key review conclusions.

## Key Rules

- Send comprehensive context in Round 1 — the sub-agent cannot read your files automatically
- Be honest about weaknesses — hiding them leads to worse feedback
- Push back on criticisms you disagree with, but accept valid ones
- Focus on ACTIONABLE feedback — "what experiment would fix this?"
- The review document should be self-contained (readable without the conversation)
- Include previous review text in each subsequent round's Agent prompt for consistency

## Prompt Templates

### For initial review:
"You are playing a senior ML reviewer (NeurIPS/ICML level). I'm going to present a complete ML research project for your critical review..."

### For experiment design:
"Please design the minimal additional experiment package that gives the highest acceptance lift per GPU week. Our compute: [describe]. Be very specific about configurations."

### For paper structure:
"Please turn this into a concrete paper outline with section-by-section claims and figure plan."

### For claims matrix:
"Please give me a results-to-claims matrix: what claim is allowed under each possible outcome of experiments X and Y?"

### For mock review:
"Please write a mock NeurIPS review with: Summary, Strengths, Weaknesses, Questions for Authors, Score, Confidence, and What Would Move Toward Accept."
