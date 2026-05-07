# 深度学习研究项目

## 服务器配置

```yaml
ssh_host: your-server.example.com
ssh_port: 22
ssh_user: root
python: /opt/conda/bin/python
venue: ELSEVIER_DC   # ELSEVIER_DC | ELSEVIER_SC | IEEE_JOURNAL | IEEE_CONF | ICLR | NeurIPS | ICML
target_journals:     # 列出 2-3 个候选期刊
  - primary:   填写首选期刊名
  - backup1:   填写备选期刊名
  - backup2:   填写备选期刊名
```

SSH：`ssh -o StrictHostKeyChecking=no -p PORT root@your-server.example.com`  
screen 内用显式路径，不用 `conda activate`。

> 服务器在检查点①通过后才开，Stage 0–1 全程本地。

---

> 文档清单（含字段说明）· Context 管理见 SETUP.md。  
> **26 个核心 Skills 已在本文件完整定义。**

---

## 核心 Skills（26）+ MCP

| 分组 | Skills |
|------|--------|
| 常驻审稿 | `academic-paper-reviewer` · `research-review` |
| 脚手架 | `pl-ml-project-template` |
| Idea 链 | `idea-discovery` · `research-lit` · `idea-creator` · `novelty-check` · `research-refine` |
| 实验 | `experiment-plan` · `ablation-planner` · `experiment-bridge` · `run-experiment` · `pytorch-lightning` · `result-to-claim` |
| 监控 | `auto-monitor` |
| 结果审查 | `auto-review-loop` · `analyze-results` |
| 图表 | `paper-figure` · `scientific-visualization` · `scientific-figure-making` · `paper-illustration` |
| 写作 | `paper-plan` · `paper-write` · `paper-compile` · `humanizer` · `paper-audit` |

**MCP**：`arxiv` · `semanticscholar` · `openalex`  
**全局 MCP 可用**：`deepseek`（offload 简单任务）· `tavily`（补充搜索）· `mcp-server-chart`（快速出图）

---

## 模型分配策略（节省 token）

| 层级 | 模型 | 论文场景 |
|---|---|---|
| **Opus 4.7** | 最强 | Idea 新颖性判断、贡献定义、审稿人角色、paper-audit 批判 |
| **Sonnet 4.6 ≈ DeepSeek-v4-pro** | 中等 | 大多数写作、代码实现、文献整理、experiment-bridge、paper-write |
| **DeepSeek-v4-pro（thinking=max）** | 推理 | 公式推导（formula-derivation）、消融分析、统计检验解释 |
| **Haiku 4.5 ≈ DeepSeek-v4-flash** | 最廉价 | citation 格式、期刊缩写查询、翻译初稿、日志解析、模板填充 |

**DeepSeek offload 示例**（主线程调用 deepseek MCP）：
```
# Stage 1B：文献摘要批量生成（flash + thinking关闭，最省钱）
deepseek.chat_completion(model="deepseek-v4-flash", thinking={"type":"disabled"}, prompt="总结以下论文的方法和贡献：...")

# Stage 2B：实验日志解析（flash + thinking关闭）
deepseek.chat_completion(model="deepseek-v4-flash", thinking={"type":"disabled"}, prompt="从日志中提取最终 val_loss 和 epoch：...")

# Stage 4：citation 格式标准化（flash + thinking关闭）
deepseek.chat_completion(model="deepseek-v4-flash", thinking={"type":"disabled"}, prompt="将以下引用格式化为 IEEE 格式：...")

# 数学推导验证（pro + thinking max）
deepseek.chat_completion(model="deepseek-v4-pro", reasoning_effort="max", prompt="验证以下梯度推导是否正确：...")

# 写作润色/分析（pro，关 thinking 省 token）
deepseek.chat_completion(model="deepseek-v4-pro", thinking={"type":"disabled"}, prompt="改进以下段落的学术表达：...")
```
注：两个模型 thinking 均默认开启，缓存命中后价格降至原价 1/10。

## 实验监控

**禁止在主线程轮询监控**（上下文污染 + token 浪费）。

**首选方案：`auto-monitor`**

```
run-experiment 启动训练后 → /auto-monitor
  → 生成原生 bash 监控脚本（含 sleep 循环 + 关键词检测）
  → Bash(run_in_background=True) 启动为 OS 进程
  → 自适应轮询：0 → 5 → 15 → 30 → 60 min
  → 完成/出错/停滞时自动通知主线程
  → 主线程上下文零增长
```

**备选方案**（auto-monitor 不适用时）：

| 方案 | 场景 |
|------|------|
| `monitor-experiment` | 手动单次查看实验快照 |
| `/schedule` | 需要跨会话持续监控（cron agent） |

主线程恢复锚点：`docs/06_experiment_tracker.md` 当前状态。

---

## 审稿人（全程常驻）

`academic-paper-reviewer`：5 角色（EIC + 3 审稿人 + Devil's Advocate）  
`research-review`：Opus critic

**4 个强制检查点：**

| # | 时机 | 检查内容 | 不通过 |
|---|------|---------|--------|
| ① | Stage 2A 末 | Idea 新颖性 + 实验计划完整性 + 消融设计 → **人工确认通过才开服务器** | 回 Stage 1 |
| ② | Stage 3 末 | 结果质量 + 声明支撑强度 → **通过才写论文** | 回 Stage 2 补实验 |
| ③ | Stage 4A 末 | 大纲结构 / 贡献 / 逻辑 → **人工确认才写 LaTeX** | 修改大纲 |
| ④ | Stage 4D 首 | 草稿整体质量（paper-audit 首轮） | 修 Major 后再迭代 |

---

## 工作流

### Stage 0｜初始化

**0A 目标期刊确认**

```
与 AI 对话 → 讨论 2-3 个候选期刊
  → 查阅各期刊：研究范围 / 页数限制 / 图表要求 / 投稿格式 / 接受率
  → 填写 CLAUDE.md 的 target_journals 字段
  → 生成 docs/00_venue_requirements.md（期刊要求速查表）
```

**0B 脚手架**

```
pl-ml-project-template → 生成项目脚手架（classification / regression / timeseries）
```

---

### Stage 1｜数据解析 · 文献调研 · Idea · 实验规划

**1A 数据解析**（与 AI 对话，理解数据集）→ `docs/01_data_analysis.md`

**1B 文献调研 + Idea 发现（一体化）**

```
research-lit  ← 告知保存到 docs/02_literature_research.md
  → docs/02_literature_research.md（文献综述，为 idea-discovery 提供基础）

idea-discovery（以 02 为上下文）
  ├─ research-lit          → 深度文献扫描
  ├─ idea-creator          → 生成 8-12 个 idea，Pilot 实验筛选
  ├─ novelty-check         → 查新
  ├─ research-review       → 批判审查
  └─ research-refine + experiment-plan
       → research-refine   → docs/04_final_proposal.md（精炼方法方案）
       → experiment-plan   → docs/05_experiment_plan.md（声明→实验映射）
                           → docs/06_experiment_tracker.md（逐条运行追踪表）
→ docs/03_idea_report.md（Idea 排名 + Pilot 结果 + 推荐）

ablation-planner
  → idea 确认后立即设计消融方案
  → experiment-bridge 阶段 5.6 将消融实验追加到 docs/05 和 docs/06
```

---

### Stage 2｜实验执行 · 结果门控

**2A 准备（检查点 ①）**

```
与 AI 对话 → 对照 docs/05_experiment_plan.md 创建 docs/07_result_record.md（逐条空白结果表）
academic-paper-reviewer + research-review
  → 审 idea 新颖性 + 实验计划完整性 + 消融设计合理性
  → 通过后：提示用户开启服务器，等待端口号
```

**→ 用户提供端口号 → 继续 2B**

**2B 实验执行（需 GPU）**

```
experiment-bridge
  → 读 docs/05_experiment_plan.md + docs/04_final_proposal.md
  → 实现代码 → 上传服务器 → 完成后告知用户可启动
run-experiment → screen 内逐批启动训练
auto-monitor   → 后台监控实验进度（可选）
```

实验完成后，手动将结果数值逐条填入 `docs/07_result_record.md`（手动维护文档）。

**2C 结果门控**

```
result-to-claim → docs/08_findings.md + docs/09_claims.md（结构化声明）
  supported     → Stage 3
  partial       → 按消融计划补实验 → 回 2B
  not supported → 分析原因 → 审稿人批准改进方向 → 回 Stage 1 或 2A
```

---

### Stage 3｜结果整理 · 质量审查（检查点 ②）

> 本阶段专注整理结果与研究质量审查，**不画图**。  
> 图表在 4B（大纲确认后）才决定画什么、怎么画。

```
analyze-results ← 读 docs/07_result_record.md
  → docs/10_result_summary.md
    （关键结果汇总：统计检验 / 消融对比 / baseline 对比 / 主要发现）
    [07 是原始数值记录；10 是事后分析合成，用于写作]

auto-review-loop ≤ 4 轮（以 docs/09_claims.md 为输入，由 Stage 2C result-to-claim 生成）
  → 更新 docs/09_claims.md（迭代精炼声明）
  → docs/12_auto_review.md（审稿记录）
  → score < 6：补实验 → 回 Stage 2
  → score ≥ 6：进入检查点 ②

academic-paper-reviewer + research-review（检查点 ②）
  → 审结果质量 + 声明支撑强度 → 通过才进 Stage 4
```

---

### Stage 4｜写论文

**4A 大纲（检查点 ③，人工确认后才写 LaTeX）**

```
与 AI 对话 → 用户提供研究思路 / 章节方向 / 重点贡献
paper-plan  → 基于对话 + docs/09_claims.md + docs/12_auto_review.md
           → 完善大纲 → docs/13_paper_plan.md（含图表计划）
academic-paper-reviewer + research-review → 审大纲
→ 人工确认后进 4B
```

**4B 图表生成（主线程之外可并行）**

```
paper-figure
  ← 读 docs/13_paper_plan.md 图表计划
  → 生成每张数据图的 Python 脚本（figures/gen_fig*.py）
  → 脚本注释清晰：用哪些数据、怎么画、输出哪个文件

scientific-visualization（Nature/Science/Cell 等生物医学期刊特殊规范图）
  ← ML 会议标准图用 paper-figure；高规格期刊多面板图用此 skill

paper-illustration（架构图 / 流程图，替代手绘）
  ← 传入图描述 prompt（从 docs/13_paper_plan.md 手绘图计划提取）

→ docs/11_figure_report.md（逐图制作指南，见 SETUP.md 格式说明）
  · 数据图：脚本路径 + 数据来源 + 运行命令
  · AI 生成图：paper-illustration prompt
  · 手绘图：draw.io/TikZ 绘制说明

用户可在主线程之外并行完成图表制作
```

**4C LaTeX 草稿**

```
paper-write → paper/main.tex + sections/*.tex + references.bib
citation-verification（按需）→ 验证引用准确性（与 paper-write Step 4 互补）
人工替换 preamble（保留 \input{sections/...}，换 \documentclass / \usepackage）
有现成 .bib → 告知 paper-write 跳过引用生成
paper-compile → 编译 PDF，自动修复 LaTeX 错误
```

**4D 审查 + 迭代（检查点 ④，全自动）**

```
paper-audit      → 深度审查草稿（结构 / 声明 / 证据），输出 Major / Minor
[修复 Major 问题]
humanizer        → 去 AI 味（仅作用于正文段落文本，跳过 LaTeX 命令和 \section 标题）
adversarial-qa（按需）→ 精细 QA（5 层 critic-fixer 循环，paper-audit 后补充使用）
auto-review-loop → 迭代至 score ≥ 6（≤ 4 轮）
paper-audit      → 最终质量确认
```

---

### Stage 5｜投稿准备

**5A 投稿辅助材料（按 venue 类型选择）**

```
所有 venue：
  → Keywords（5-8 个，从 docs/13_paper_plan.md 提取，paper-write 已插入 \keywords{}）
  → Cover Letter（读 docs/04_final_proposal.md + docs/00_venue_requirements.md 生成）
  → paper-compile → 最终编译 PDF

Elsevier（DC/SC）额外：
  → Highlights（3-5 条，每条≤85 字符，从 docs/09_claims.md 提取）
  → Graphical Abstract（paper-illustration 生成摘要图）

NeurIPS / ICLR / ICML 额外：
  → Reproducibility Checklist（venue-templates 模板，按需加载）
  → Supplementary PDF（附录独立编译）
  → Ethics Statement（ICML）
```

**5B 最终检查**

```
人工审核：
  → paper-audit 最终报告
  → 图表分辨率 ≥ 300 DPI、字号 ≥ 8pt
  → 参考文献格式与目标期刊一致
  → 页数符合限制（见 docs/00_venue_requirements.md）
  → 确认无误后投稿
```

**投稿后（按需加载 rebuttal skill）**
