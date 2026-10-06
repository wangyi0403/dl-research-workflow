# AI Writing Tell Catalog

Use this catalog as a diagnostic inventory, not a blacklist. A phrase, punctuation mark, or structure is not evidence of AI authorship by itself. Mark each candidate as **keep**, **revise**, **remove**, or **author decision** before editing.

## Triage rule

For every candidate, ask:

1. Is the pattern actually present, or is the judgment based only on a vague impression?
2. Does it create repetition, inflated emphasis, weak reader reference, unnecessary explanation, or a mismatch with the author's/venue's voice?
3. Does the proposed edit preserve the claim, evidence, scope, uncertainty, structure, and information density?

If the answer to any question is unclear, keep the original or flag it for the author. Never optimize for an AI detector score.

## Layer 1: General AI-tell candidates

These are context-sensitive signals. Replace them only when they add no precise meaning or create a demonstrable problem.

### Inflated significance

Candidates include "marking a pivotal moment", "groundbreaking", "revolutionary", "transformative", "a testament to", and claims that an ordinary result represents a broad historical shift. Replace with the observed result or mechanism. Keep the wording when the manuscript supplies evidence for the broader significance.

### Superficial participial tails

Examples include ", highlighting the importance of...", ", demonstrating the effectiveness of...", ", reflecting...", and ", contributing to..." when the tail merely restates the sentence. Keep a participial clause when it expresses a distinct, supported relationship.

### Promotional or figurative filler

Words such as "rich", "vibrant", "robust", "seamless", and "powerful" are candidates only when they are promotional filler. Preserve technical meanings such as a robust estimator, a robust controller, or a rich feature representation.

### Vague attribution

Flag "experts argue", "observers note", "many studies show", or "the industry believes" when no identifiable source or evidence follows. Do not invent a source. Either add an author-supplied citation, narrow the claim, or flag it.

### Stock vocabulary

Words such as *delve*, *underscore*, *intricate*, *tapestry*, *testament*, *landscape*, *pivotal*, *showcase*, *foster*, *leverage*, *crucial*, *notably*, and *moreover* are not banned. Change them only when they are repetitive, vague, promotional, or replace a simpler precise verb.

### Copula avoidance

Review filler constructions such as "serves as", "functions as", "stands as", "boasts", and "features" when a direct "is", "has", or action verb is clearer. Preserve the construction when it carries a real functional distinction.

### Negative parallelism and forced triads

"Not just X, but Y" and three-part lists are candidates when they manufacture contrast or completeness without adding information. Preserve a genuine contrast, a complete taxonomy, a controlled experiment with three conditions, or a deliberate rhetorical structure.

### Elegant variation

When several synonyms refer to one object, choose the stable technical term. Do not cycle through "system", "framework", "architecture", and "platform" merely to avoid repetition. Preserve distinct terms when they denote distinct objects.

### Clause stacking and filler

Review sentences with stacked clauses, "it is worth noting that", "in order to", and "it should be emphasized that" when logical relations or referents become hard to follow. Do not split by a fixed clause count; do not remove a connective that carries a real relation.

### Em-dash use

Do not remove em dashes globally. Review them when they repeatedly create a reveal, insert ordinary parenthetical material, or replace a clearer sentence boundary. Prefer a direct sentence, comma, or other punctuation only when it preserves the relation and matches the author's/venue's style. Preserve mathematical notation, ranges, established terminology, deliberate author voice, and a single well-motivated dash.

## Layer 1A: Chinese structural and discourse signals

Apply this section only to Chinese prose. It is the main integration of the conservative rules from `lieflat-less-ai-tone`.

**Source note:** The structural heuristics were adapted from [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone), reviewed at commit `27d2923` on 2026-08-26. That MIT-licensed project reports an unpublished corpus study; this skill adopts its conservative rule ideas and negative findings, not its unverifiable frequency claims or corpus.

### 翻案腔

Flag a canned reversal that invents a reader misconception and immediately overturns it, such as `不是……而是……`, `并非……而是……`, `不在于……而在于……`, or `表面……实际……`. State the supported judgment directly when the contrast is ornamental. Preserve a genuine correction of a claim already stated in the manuscript, a real hypothesis contrast, or an argument whose evidence actually moves from an initial interpretation to a revised one.

### 顿号并列过密

Two or more `、` marks within one clause joining three or more same-level items are only a **candidate**. Revise only when the items form a compressed inventory, flatten a meaningful hierarchy, or create clear reading friction. A natural three-item list by itself is not an AI tell, and this rule is not a ban on three-part rhetoric.

Prefer changing the syntax, grouping items by a real stage or function, or making one item the main clause while retaining the others. Do not delete statutory terms, variables, taxonomy members, complete materials, or required configuration items. Markdown lists and table cells are not this pattern.

### 破折号的揭晓式或插入式滥用

Flag repeated `——` used to create a dramatic reveal or to append an ordinary explanation that could be a normal sentence. Preserve a dash when it expresses a genuine interruption, contrast, range, technical notation, or the author's established style.

### 理想化职业拟人喻体

Flag a tool, model, or process described as `一位智慧的导师`, `永不疲倦的助手`, `数字秘书`, or another idealized occupational persona when the comparison only adds praise and repeats an already stated mechanism. Replace it with the actual operation only when that operation is already present in the manuscript. Preserve a metaphor that supplies real understanding, a concrete human comparison, or a deliberate literary/teaching device.

### 空转冒号和提示语冒号

Flag a lead-in such as `核心是：`, `原因如下：`, `一句话总结：`, or a sentence that only announces a following list. If the lead-in carries no information, delete or rewrite it so the sentence states a real judgment. Preserve:

- total-to-part relations where the colon encodes hierarchy;
- dialogue, quotations, citations, labels, URLs, code, and machine fields;
- headings and complete technical or legal lists.

### 相邻句同骨架

Flag adjacent prose sentences that repeat the same subject–verb–object order, comma positions, length band, and closing form, making the paragraph read like a filled template. Change only one sentence or merge/split where needed. Do not disturb procedures, parallel requirements, tables, deliberate rhetoric, quotations, or literary style.

### 序数词标题模板

Flag—but do not automatically edit—three or more consecutive headings beginning with `一、二、三` or `第一、第二、第三` when the numbers add no navigation value. Preserve numbering that is a legal/technical reference, a genuine procedure, a cross-reference target, or a Markdown ordered list. Section-title changes require author/venue approval.

### 段首无回指评论

In a non-first paragraph, flag a comment opener such as `听起来`, `值得注意的是`, `更重要的是`, `关键在于`, or `问题在于` when the sentence contains no `这/那/其/该/上文`-type referent and the reader must search backward for the object. Add the smallest available referent only if the original paragraph clearly supplies it. Do not invent an object or alter the paragraph order.

### 概括语盖住已有材料

When a paragraph already contains a number, date, time, named object, or concrete result, flag a nearby abstraction such as `显著提升`, `大幅改善`, `大量`, or `完成了优化` that hides the available material. Bring the existing detail into the sentence or restore a direct verb. Never add a number or example that is absent from the manuscript.

### 口号式起手

Review `说白了`, `说穿了`, `先说结论`, and similar openers when deleting them leaves the judgment unchanged. Preserve them in dialogue, quoted speech, or an author voice that deliberately uses the phrase.

## Layer 2: Academic-specific signals

### Template openers and vague gaps

Flag openers such as `In recent years, ... has attracted increasing attention` and gaps such as `existing methods still face crucial challenges` when they do not identify the actual problem, evidence, or scope. Replace with the supported problem and its boundary. Preserve a concise context sentence when it is necessary for the argument.

### Over-summarized closers

Flag `In summary, this paper has demonstrated...` when it repeats the abstract or claims more than the results establish. Close with the specific supported finding, or omit the sentence if the result is already clear.

### Hollow future work

Flag `Future work will explore...` when it names only "more advanced models", "larger datasets", or "real-world deployment". Keep a concrete extension tied to a stated limitation; do not invent a future experiment.

### Defensive report voice

Flag stacked caveats and self-protective markers such as `it is important to note`, `strictly speaking`, `it should be emphasized`, `it is worth mentioning`, `需要指出的是`, `严格来说`, `值得强调的是`, and `必须说明的是` when they surround an ordinary claim without changing its scope or interpretation.

Keep the smallest caveat that matters, but delete only semantically redundant markers. A real limitation should retain the observed constraint and any effect or validation that the manuscript actually states; if a piece is missing, flag it rather than generating it. Do not remove legitimate uncertainty, but do not use several layers of hedging to avoid making a supported statement.

### Unprompted question-and-answer

Flag invented reader dialogue such as:

- `What does this mean? The answer is...`
- `You may ask why...`
- `很多人会问：...答案是...`
- `这意味着什么？答案是...`

when the delivery request, genre, and intended reader do not require a question-and-answer structure. State the supported claim directly. Preserve a real research question, a pedagogical explanation required by the audience, or a question that advances the argument rather than merely creating a hook.

### Redundant self-explanation

Review `this means`, `this shows`, `in other words`, `这意味着`, `这表明`, `换句话说`, and similar markers when the next sentence only paraphrases the previous one. Keep them when they introduce a nontrivial inference, limitation, or change of scope.

### Empty process narration

Review `the following section will discuss...`, `本文将...`, `下面将详细介绍...`, and similar announcements. Keep a short roadmap when the venue or a long document needs navigation. Remove or compress it when it only restates visible headings or promises a discussion without delivering content.

## Layer 2A: Narrow translationese screen for Chinese prose

Treat "translationese" as a narrow structural screen, not permission to rewrite formal Chinese. Only review these five forms when their context supports the diagnosis:

1. overlong pre-nominal modifiers, including stacked `的` constructions;
2. a fronted `当……时` time clause when removing the shell preserves the time relation;
3. fronted topic shells such as `对于……来说`, `对……而言`, and `在……方面` when the object can occupy the subject/topic position;
4. sentence-initial signposts such as `然而`, `因此`, `此外`, and `与此同时` when moving or simplifying them improves flow without losing the logical relation;
5. `这意味着/这表明/这说明` restatement when it repeats the previous sentence.

Do not use passive voice, nominalization, long sentences, `被认为/被视为`, or ordinary formal vocabulary as translationese evidence by themselves.

## Layer 3: Do not touch by default

- Field-specific terminology, established translations, legal/procedural wording, and venue-required phrasing
- Mathematical notation, equations, variables, LaTeX commands/environments, citation markers, figure/table references, code, URLs, and machine fields
- Numbers, dates, units, results, named entities, quotations, sources, links, causal relations, and scope conditions
- Legitimate hedging such as `may`, `might`, `suggest`, `potentially`, `appears to`, `可能`, `通常`, and `在……条件下`
- Questions that carry research content, dialogue, FAQ/teaching structure, or a genuine rhetorical function
- Complete lists, statutory/technical taxonomies, Markdown lists, tables, and required numbered procedures
- Em dashes, Chinese enumeration, and colons when they encode a real relation or match the established author/venue style
- Sentence length, paragraph length, passive voice, pronoun use, sentence-internal parallelism, and metaphor in the abstract

## Final audit questions

Before delivery, confirm:

- Every edit maps to a named pattern and a local textual reason.
- Every candidate that was kept has a reason: evidence, function, style, genre, or venue.
- No facts, numbers, citations, limitations, hedges, or concrete details were added, removed, or strengthened.
- The manuscript's headings, paragraph order, list/table/code structure, and citation coverage are preserved. If sentence edits require moving a citation marker, verify that it still supports exactly the same claim.
- Dense enumeration was not confused with a necessary list or a natural rhetorical triad.
- Em dashes, colons, questions, and numbered headings were not removed by blacklist.
- A real limitation was not deleted merely because it sounded defensive.
- No invented reader question or self-answer remains unless the genre requires it.
- No explanation was added merely because the assistant guessed that a reader might ask.
- The final prose matches the author's sample or venue register rather than a generic "human" persona.
