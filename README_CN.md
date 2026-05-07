# DL Research Workflow

[English](README.md) | [中文](README_CN.md)

> 面向 Claude Code 的半自动化深度学习科研工作流——从文献调研到论文投稿，每个关键决策节点都有人工专家把关。

![工作流总览](diagram/fig01.png)

## 为什么做这个项目？

全自动 AI 科研工具承诺端到端论文生成，但在需要领域专家判断的场景中频繁失败。本工作流采用不同思路：**在每个决策点设置人工检查点**，AI 负责中间的重复性工作。

### 与现有方案对比

![对比图](diagram/fig03.png)

| 特性         | 全自动方案（AI Scientist 等） | 本工作流                                    |
| ------------ | ----------------------------- | ------------------------------------------- |
| 人工监督     | 极少——AI 全权决策           | **4 个强制检查点**，专家审查          |
| 领域准确性   | 通用——容易幻觉              | 领域定制 prompt + 对抗式审稿                |
| 工具需求     | 多个 API、平台、账号          | **单一工具**（Claude Code、Codex 等） |
| 可定制性     | 固定流水线                    | 26 个模块化 skill——可替换、扩展、移除     |
| 实验监控     | 外部工具（W&B、MLflow）       | 内置后台监控——主线程零上下文增长          |
| 论文质量门控 | 无或简单阈值                  | 5 角色评审团 + 批判审查                     |

### 两大核心优势

**1. 人工纠正检查点**

不同于全自动流水线的无人值守，本工作流强制设置 4 个门控，由领域专家审查并纠正 AI 决策：

| 检查点 | 时机        | 审查内容                     |
| ------ | ----------- | ---------------------------- |
| Gate 1 | 开服务器前  | Idea 新颖性 + 实验计划完整性 |
| Gate 2 | 写论文前    | 结果质量 + 声明-证据对齐     |
| Gate 3 | 写 LaTeX 前 | 大纲结构 + 贡献清晰度        |
| Gate 4 | 投稿前      | 草稿整体质量审计             |

每个门控阻止低质量工作向下游传播。不通过则回退到对应阶段修正——不浪费算力和写作时间。

**2. 单一工具执行**

无需管理 API key。无需创建平台账号。无需配置外部服务。

整个流程在单个 AI 编程助手内完成。文献检索通过 MCP 服务器（arXiv、Semantic Scholar、OpenAlex）——一次配置，跨项目可用。

---

## 工作流总览

```
Stage 0: 初始化          → 项目脚手架 + 期刊选择
Stage 1: 调研 + 构思     → 文献 → Ideas → 查新 → 实验规划
         ──── Gate 1 ────
Stage 2: 实验执行         → 代码实现 → 训练 → 结果分析
         ──── Gate 2 ────
Stage 3: 质量审查         → 统计分析 → 声明验证 → 评分 ≥ 6
         ──── Gate 3 ────
Stage 4: 论文写作         → 大纲 → 图表 → LaTeX → 审计迭代
         ──── Gate 4 ────
Stage 5: 投稿准备         → Cover Letter → Highlights → 最终检查
```

## 文档数据流

![文档数据流](diagram/fig02.png)

工作流生成 14 个结构化文档（`docs/00` 至 `docs/13`），完整追踪从期刊选择到最终投稿的研究脉络。

## 26 个核心 Skill

| 分组     | Skills                                                                                                                      | 用途                                             |
| -------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 常驻审稿 | `academic-paper-reviewer` `research-review`                                                                             | 5 角色评审团 + 批判审查                          |
| 脚手架   | `pl-ml-project-template`                                                                                                  | PyTorch Lightning 项目生成器                     |
| Idea 链  | `idea-discovery` `research-lit` `idea-creator` `novelty-check` `research-refine`                                  | 文献 → 头脑风暴 → 验证 → 精炼                 |
| 实验     | `experiment-plan` `ablation-planner` `experiment-bridge` `run-experiment` `pytorch-lightning` `result-to-claim` | 规划 → 实现 → 运行 → 评估                     |
| 监控     | `auto-monitor`                                                                                                            | 后台实验监控                                     |
| 结果审查 | `auto-review-loop` `analyze-results`                                                                                    | 迭代评分 + 统计分析                              |
| 图表     | `paper-figure` `scientific-visualization` `scientific-figure-making` `paper-illustration`                           | 数据图 + 出版级图表 + matplotlib 模式库 + 架构图 |
| 写作     | `paper-plan` `paper-write` `paper-compile` `humanizer` `paper-audit`                                              | 大纲 → 草稿 → 编译 → 去 AI 味 → 审计         |

### Skill 来源说明

大部分 skill 基于社区开源项目改编，适配本工作流的文档交接协议。两个 skill 为本项目原创。

| 来源               | Skills                                              | 备注                                                                               |
| ------------------ | --------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **原创**     | `auto-monitor` `pl-ml-project-template`         | 本项目从零构建                                                                     |
| **社区改编** | 其余 24 个 skill（含 `scientific-figure-making`） | 来自多个 Claude Code skill 社区仓库。全部经修改以适配 skill 间文档交接和流水线集成 |

---

## 快速开始

### 前置条件

- [Claude Code](https://claude.ai/code)（或兼容的 AI 编程助手）
- [uv](https://docs.astral.sh/uv/)（Python 包管理器，arxiv 和 semanticscholar MCP 需要）
- [Node.js](https://nodejs.org/)（openalex MCP 需要）
- SSH 可达的 GPU 服务器（训练用）

### 安装

1. 克隆本仓库：

```bash
git clone https://github.com/wangyi0403/dl-research-workflow.git
```

2. 安装文献检索 MCP 服务器：

```bash
# arXiv — 搜索和下载论文（无需 API key）
uv tool install arxiv-mcp-server

# Semantic Scholar — 已发表论文检索（API key 可选但推荐）
uv tool install semantic-scholar-mcp
# 可选：在 https://www.semanticscholar.org/product/api 获取 API key

# OpenAlex — 开放学术数据（无需 API key）
npm install -g openalex-mcp
```

3. 将配置文件和 skills 复制到你的研究项目（项目级，无需全局安装）：

```bash
# Linux / macOS
cd your-project
cp /path/to/dl-research-workflow/CLAUDE.md .
cp /path/to/dl-research-workflow/SETUP.md .
cp /path/to/dl-research-workflow/.mcp.json .
mkdir -p .claude/skills
cp -r /path/to/dl-research-workflow/skills/* .claude/skills/

# Windows (PowerShell)
Set-Location your-project
Copy-Item \path\to\dl-research-workflow\CLAUDE.md .
Copy-Item \path\to\dl-research-workflow\SETUP.md .
Copy-Item \path\to\dl-research-workflow\.mcp.json .
New-Item -ItemType Directory -Path ".claude\skills" -Force
Copy-Item -Path "\path\to\dl-research-workflow\skills\*" -Destination ".claude\skills\" -Recurse
```

全部 26 个 skill 存放于项目的 `.claude/skills/` 下——无需全局安装，每个研究项目完全自包含。

4. 编辑 `CLAUDE.md`——填写服务器配置（SSH 地址、端口、目标期刊）。
5. （可选）设置环境变量提高 API 速率限制：

```bash
# Semantic Scholar（更高速率限制）
export SEMANTIC_SCHOLAR_API_KEY="your-key"
# OpenAlex（100 req/s 而非 10）
export OPENALEX_DEFAULT_EMAIL="your@email.com"
```

6. 在 Claude Code 中打开项目，输入：

```
新建项目 timeseries
```

脚手架 skill 会生成项目结构。按 `SETUP.md` 加载全部 skill。

### 模型路由（成本优化）

| 层级 | 模型   | 场景                                               |
| ---- | ------ | -------------------------------------------------- |
| 最强 | Opus   | Idea 新颖性判断、贡献定义、审稿人角色、paper-audit |
| 标准 | Sonnet | 大部分写作、代码实现、experiment-bridge            |
| 最省 | Haiku  | 引用格式化、日志解析、模板填充                     |

## 期刊/会议支持

| 类型              | 支持特性                                     |
| ----------------- | -------------------------------------------- |
| Elsevier（DC/SC） | Highlights、Graphical Abstract、Cover Letter |
| IEEE（期刊/会议） | IEEEtran 格式                                |
| NeurIPS / ICLR    | Reproducibility Checklist、Supplementary PDF |
| ICML              | Ethics Statement、Reproducibility Statement  |

## 文件结构

```
.
├── CLAUDE.md          # 项目级 AI 指令（复制到你的项目）
├── SETUP.md           # 安装指南 + 文档规范（复制到你的项目）
├── .mcp.json          # 项目级 MCP 配置：arxiv + semanticscholar + openalex
├── skills/            # 26 个核心 skill
│   ├── academic-paper-reviewer/
│   ├── auto-monitor/
│   ├── idea-discovery/
│   ├── paper-audit/
│   ├── ...
│   └── run-experiment/
├── diagram/           # 架构图和流程图
└── README.md
```

---

## License

MIT License — 见 [LICENSE](LICENSE)。
