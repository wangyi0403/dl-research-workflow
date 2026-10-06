# Before/After Examples: AI → Humanized Academic Writing

Concrete examples of common AI writing patterns and their humanized alternatives.
See SKILL.md §Layer 1 and §Layer 2 for the full tell catalog.

## General AI Tells → Fixed

### Inflated Significance
❌ "This groundbreaking work marks a pivotal moment in the field of railway inspection."
✅ "This work addresses railway inspection."

### Superficial -ing Tails
❌ "Our method outperforms all baselines, demonstrating the effectiveness of the proposed approach."
✅ "Our method outperforms all baselines."
If the manuscript reports a metric or statistical test, it may be used here; do not invent one during humanization.

### AI Vocabulary
❌ "We leverage a novel framework to delve into the intricate tapestry of multimodal sensor fusion."
✅ "We use a framework for multimodal sensor fusion."

### Copula Avoidance
❌ "The attention module serves as a mechanism for feature selection."
✅ "The attention module selects features." (or "acts as a feature selector" if an analogy is needed)

### Filler Phrases
❌ "It is worth noting that in order to achieve real-time performance, we employ a lightweight backbone."
✅ "To achieve real-time performance, we use a lightweight backbone."

### Clause-Stacked Sentences
❌ "We propose a novel framework, which consists of three modules, where Module A extracts spatial features using a ResNet-50 backbone pretrained on ImageNet, while Module B captures temporal dependencies through a bidirectional GRU with 256 hidden units, and Module C fuses the outputs through a cross-attention mechanism that learns to weight spatial and temporal features adaptively."
✅ "We propose a three-module framework. Module A extracts spatial features using a ResNet-50 backbone. Module B captures temporal dependencies through a bidirectional GRU with 256 hidden units. Module C fuses these outputs via cross-attention, adaptively weighting spatial and temporal features."

### Negative Parallelisms
❌ "This is not just a faster detector, but a fundamentally new approach to anomaly detection."
✅ "The detector is faster and adopts a fundamentally new approach to anomaly detection."

### Elegant Variation
❌ "...the railway inspection system... this monitoring framework... our surveillance architecture..."
✅ "...the inspection system... the system... our system..." (pick one term)

## Academic-Specific Tells → Fixed

### Template Openers
❌ "In recent years, deep learning has attracted increasing attention in railway engineering."
✅ "Deep learning has attracted attention in railway engineering."

### Vague Gap Statements
❌ "However, existing methods still face crucial challenges in real-world deployment."
✅ "Either name the deployment constraint already supported by the manuscript, or flag/remove the vague gap statement; do not invent a latency, citation, or operating condition."

### Over-Summarizing Section Closers
❌ "In summary, this paper has demonstrated that our proposed method achieves superior performance across multiple benchmarks."
✅ "Use the specific result already reported in the Results section, or omit the sentence if the result is already clear. Do not add a number or benchmark here."

### Hollow Forward-Looking
❌ "Future work will explore more advanced architectures and additional datasets."
✅ "Name only a future extension tied to a limitation already stated in the manuscript; otherwise flag or remove this sentence."

## Claim-Evidence Mismatches → Fixed

### Verb Too Strong
❌ "We demonstrate that multi-scale features improve detection accuracy." (Only one dataset, small n)
✅ "On the evaluated dataset, the results suggest that multi-scale features may improve detection accuracy." (Keep the claim limited to the reported evidence.)

### Claim Without Evidence
❌ "Our method is robust to sensor noise." (No noise experiment)
✅ Remove the claim or flag the missing noise experiment; do not invent a perturbation, result, or statistical test.

### Abstract Over-Promise
❌ Abstract claims "state-of-the-art performance" but Results show method is second-best on one of three datasets.
✅ Revise the abstract to match the benchmark-specific ranking already reported in Results; do not add an unreported margin or benchmark claim.

## Before/After: Full Paragraph

### Before (Heavy AI)
> In recent years, the rapid development of deep learning techniques has revolutionized the field of railway infrastructure monitoring. However, existing deep learning-based approaches still face significant challenges in handling the complex and dynamic nature of railway environments. In this paper, we propose a novel framework that leverages advanced attention mechanisms to address these crucial challenges. Our comprehensive experiments on multiple benchmark datasets demonstrate the effectiveness and robustness of the proposed method, highlighting its potential for real-world deployment.

### After (Humanized)
> This study examines deep learning for railway infrastructure monitoring. Existing approaches face challenges in complex and dynamic railway environments. We propose a framework that uses attention mechanisms to address these challenges. Experiments on multiple benchmark datasets assess its effectiveness and robustness; the manuscript considers its potential for real-world deployment.

## Chinese Structural and Discourse Patterns

These examples are conservative. They show when to change a pattern and when to preserve it; they are not a universal blacklist.

### Dense Chinese Enumeration

❌ "该系统负责数据采集、清洗、标注、训练、验证、部署。"

✅ "该系统负责数据采集、清洗和标注，并负责训练、验证和部署。"

The rewrite changes the syntax while retaining every item. Do not shorten a complete legal, technical, or taxonomic list merely to avoid `、`.

### Reveal-Style Em Dash

❌ "误差的主要来源不是模型容量——而是训练数据的分布偏移。"

✅ "误差主要来自训练数据的分布偏移。模型容量并非主要因素。"

Preserve an em dash when it expresses a real interruption, range, technical notation, or established author style. The problem is repeated dramatic punctuation, not the character itself.

### Empty Lead-In and Meaningful Colon

❌ "本节有三个重点："

✅ "本节讨论三个重点。"

If a list must follow, a meaningful lead-in is also acceptable: "本节比较三个阶段的计算开销：" The lead-in should contribute information rather than merely announce that a list exists.

### Over-Defensive Report Voice

❌ "需要指出的是，严格来说，在一定程度上可以认为，该方法可能有助于改善检测结果。"

✅ "该方法可能有助于改善检测结果。"
If an independent-dataset limitation is stated elsewhere in the manuscript, preserve it there; do not add the limitation merely to make the sentence sound cautious.

Keep the limitation when it changes the claim's scope. Remove stacked self-protective markers that do not add a separate condition.

### Unprompted Question-and-Answer

❌ "这意味着什么？答案是，该模块改变了特征融合方式。"

✅ "该模块改变了特征融合方式。"

Keep the question when it is a real research question, a dialogue, an FAQ, or a teaching explanation needed by the intended audience.

### Redundant Self-Explanation

❌ "模型在验证集上的误差下降。这意味着模型在验证集上的误差下降。"

✅ "模型在验证集上的误差下降。"

Do not remove `这意味着` or `这表明` when the following clause adds a genuine inference, scope condition, or limitation rather than repeating the previous sentence.

### Empty Process Narration

❌ "下面将对实验结果进行详细分析。实验结果表明，模型在低照度条件下的召回率下降。"

✅ "实验结果表明，模型在低照度条件下的召回率下降。"

Keep a concise roadmap when a long paper or venue requires navigation; remove it when the next sentence already begins the promised analysis.

### Legitimate Patterns to Preserve

✅ "该流程包括采集、清洗和标注三个步骤。" — keep when the list is complete and useful; do not rewrite it only because it contains three items.

✅ "模型在低照度下的性能——尤其是召回率——仍需评估。" — keep a single purposeful parenthetical dash when it matches the author's or venue's style.

✅ "本节比较三个阶段的计算开销：数据准备、训练和部署。" — keep a colon when the lead-in states a real total-to-part relation.

✅ "为什么模型在低照度下失效？这是本文的研究问题。" — keep a genuine research question; the issue is invented reader dialogue, not questions themselves.

### Canned Reversal

❌ "这个问题不是模型容量不足，而是数据分布偏移。"

✅ "这个问题来自数据分布偏移。模型容量不足不是主要原因。"

Preserve the reversal when the manuscript has actually stated the initial hypothesis or when the contrast is necessary to the argument.

### Idealized Occupational Metaphor

❌ "该工具像一位永不疲倦的助手，负责检查格式。"

✅ "该工具负责检查格式。"

Do not replace a metaphor with an invented mechanism. If the metaphor supplies real understanding or matches an established literary/teaching voice, keep it.

### Slogan-Like Opener

❌ "说白了，这个方法没有解决数据偏移问题。"

✅ "这个方法没有解决数据偏移问题。"

Keep the opener in dialogue, quoted speech, or a deliberately conversational author voice.
