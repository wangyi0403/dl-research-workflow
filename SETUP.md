# 项目初始化手册

> 操作步骤参考，新项目第一次用时执行。日常规则见 `CLAUDE.md`。

---

## 一、安装与初始化

### 1. 克隆本仓库

```bash
git clone https://github.com/wangyi0403/dl-research-workflow.git
```

### 2. 创建新研究项目并复制所有文件

将配置文件和 skills 复制到项目目录（项目级，无需全局安装）：

```bash
# Linux / macOS
mkdir my-research-project && cd my-research-project
cp /path/to/dl-research-workflow/CLAUDE.md .
cp /path/to/dl-research-workflow/SETUP.md .
cp /path/to/dl-research-workflow/.mcp.json .
mkdir -p .claude/skills
cp -r /path/to/dl-research-workflow/skills/* .claude/skills/

# Windows (PowerShell)
mkdir my-research-project; Set-Location my-research-project
Copy-Item \path\to\dl-research-workflow\CLAUDE.md .
Copy-Item \path\to\dl-research-workflow\SETUP.md .
Copy-Item \path\to\dl-research-workflow\.mcp.json .
New-Item -ItemType Directory -Path ".claude\skills" -Force
Copy-Item -Path "\path\to\dl-research-workflow\skills\*" -Destination ".claude\skills\" -Recurse
```

在 Claude Code 中打开项目，运行 `/skills` 确认 26 个 skill 已加载。

### 3. 配置 CLAUDE.md

编辑 `CLAUDE.md` 顶部的服务器配置：

```yaml
ssh_host: your-server.example.com   # ← 改为你的服务器地址
ssh_port: 22                        # ← 改为你的端口
venue: ELSEVIER_DC                  # ← 改为你的目标期刊类型
target_journals:
  - primary: 填写首选期刊名
```

### 4. MCP 配置（文献检索）

本工作流依赖以下 MCP 服务器进行文献检索（Stage 1 起必须）：

| MCP | 安装 | API Key |
|-----|------|---------|
| `arxiv` | `uv tool install arxiv-mcp-server` | 不需要 |
| `semanticscholar` | `uv tool install semantic-scholar-mcp` | 可选（[获取](https://www.semanticscholar.org/product/api)） |
| `openalex` | `npm install -g openalex-mcp` | 不需要（设 email 提高速率） |

项目根目录已包含 `.mcp.json`（Step 2 已复制），Claude Code 打开项目时自动加载。如需设置环境变量：

```bash
export SEMANTIC_SCHOLAR_API_KEY="your-key"     # 可选
export OPENALEX_DEFAULT_EMAIL="your@email.com" # 可选
```

### 5. 生成项目脚手架

在 Claude Code 对话中说：

```
新建项目 timeseries
```

（或 `classification` / `regression`）

---

## 二、Context 管理（对话切换时机）

**每个 Stage 建议独立对话**，避免单次 context 溢出。

| 切换时机 | 恢复锚点（新对话开头告知 Claude）|
|---------|-------------------------------|
| Stage 1 结束 | `docs/03_idea_report.md` + `docs/04_final_proposal.md` |
| Stage 2 结束 | `docs/08_findings.md` + `docs/07_result_record.md` |
| Stage 3 结束 | `docs/12_auto_review.md` + `docs/09_claims.md` |
| Stage 4 结束 | `paper/main.tex` + `docs/13_paper_plan.md` |

**Stage 内 context 快满时**（`/compact` 或手动新对话）：
- Stage 2B 实验执行：以 `docs/06_experiment_tracker.md` 当前状态恢复
- Stage 4D 迭代：以 `docs/12_auto_review.md` 最新轮次 + `paper/` 当前状态恢复

新对话开头模板：
```
当前项目：/path/to/project（Stage X，刚完成 Y）
上次进度：[粘贴关键文档最后几行 或 说明状态]
继续：[下一步任务]
```

---

## 三、docs/ 文档清单

| # | 文件 | 生成时机 | 内容说明 |
|---|------|---------|---------|
| 00 | `00_venue_requirements.md` | Stage 0A，AI对话 | 候选期刊列表 / 各期刊范围 + 页数 + 格式 + 图表要求 + 接受率 / 最终选定期刊 |
| 01 | `01_data_analysis.md` | Stage 1A，AI对话 | 数据集特征/分布/规模/缺失值/研究问题定义/评估指标选择 |
| 02 | `02_literature_research.md` | Stage 1B，research-lit | 研究现状综述/竞争方法/开放问题/Gap 分析 |
| 03 | `03_idea_report.md` | Stage 1B，idea-discovery | 候选 Idea 列表/Pilot 实验结果/查新结论/最终推荐排序 |
| 04 | `04_final_proposal.md` | Stage 1B，research-refine | 精炼后的方法方案/核心主张/创新点定义/Problem Anchor |
| 05 | `05_experiment_plan.md` | Stage 1B，experiment-plan | 声明→实验映射/实验块设计/Baseline/成功标准/运行顺序/**消融计划** |
| 06 | `06_experiment_tracker.md` | Stage 1B，experiment-plan | 逐条运行追踪表（RunID / 里程碑 / 方法变体 / 指标 / 优先级 / **状态** / 备注） |
| 07 | `07_result_record.md` | Stage 2A 建表，2B 手动填值 | **原始结果记录**（手动维护）：对照 05 每条实验逐行填入实际数值，无分析 |
| 08 | `08_findings.md` | Stage 2C，result-to-claim | 结论判定（supported / partial / not supported）+ 证据摘要 + 下一步路由建议 |
| 09 | `09_claims.md` | Stage 2C，result-to-claim | 结构化声明表（Claim ID / Statement / Evidence / Confidence），auto-review-loop 迭代精炼 |
| 10 | `10_result_summary.md` | Stage 3，analyze-results | **分析合成**：主要发现 / 统计检验 / 消融对比 / baseline 对比 |
| 11 | `11_figure_report.md` | Stage 4B，AI对话 | **逐图制作指南**（见下方格式说明）|
| 12 | `12_auto_review.md` | Stage 3+4D，auto-review-loop | 每轮审稿得分/批评/修改记录/最终评级 |
| 13 | `13_paper_plan.md` | Stage 4A，paper-plan | 论文大纲/章节计划/声明-证据矩阵/图表计划/引用脚手架 |

**按需生成（无序号）：**

| 文件 | 触发条件 |
|------|---------|
| `idea_candidates.md` | idea-discovery compact 模式（短 context 下替代 03）|
| `ref_paper_summary.md` | idea-discovery 指定参考论文时 |
| `review_state.json` | auto-review-loop 断点恢复，非研究文档 |

---

### 11_figure_report.md 格式规范

每张图独立一节，格式如下：

```markdown
## Fig 1: [图名] — [类型: Python数据图 / 手绘 / AI生成]

<!-- Python 数据图 -->
- **脚本**：`figures/gen_fig1_comparison.py`（paper-figure 已生成）
- **数据**：`results/ablation.json`，字段：method_name, accuracy, std
- **图类型**：分组柱状图，x=方法名，y=accuracy，误差棒=std
- **运行**：`python figures/gen_fig1_comparison.py` → 输出 `figures/fig1_comparison.pdf`

<!-- 手绘图 -->
- **工具**：draw.io
- **内容**：[模块结构、数据流方向、标注说明]
- **输出**：`figures/fig2_architecture.pdf`

<!-- AI 生成图 -->
- **Skill**：paper-illustration
- **Prompt**：[图内容、风格、颜色、标注]
- **输出**：`figures/fig3_diagram.pdf`
```

---

## 四、写作素材对照表

| 文档 | 论文写作用途 |
|------|------------|
| `docs/01_data_analysis.md` | Introduction：问题背景 / 数据规模 / 评估设置 |
| `docs/02_literature_research.md` | Related Work：全部引用来源 / 方法对比 |
| `docs/03_idea_report.md` | Introduction：贡献点列表 / 动机 |
| `docs/04_final_proposal.md` | Method：方法设计依据 / 创新点描述 |
| `docs/05_experiment_plan.md` | Experiments：实验设计说明 / baseline 选择依据 |
| `docs/07_result_record.md` | Experiments：原始数值来源 |
| `docs/09_claims.md` | paper-plan 必需输入：声明→证据矩阵 |
| `docs/10_result_summary.md` | Experiments：结果表 / 消融分析 / 统计显著性 |
| `docs/11_figure_report.md` | Figures：手绘架构图 / 流程图制作参考 |
| `docs/12_auto_review.md` | 修改回应 / Limitations 写作参考 |
| `docs/13_paper_plan.md` | paper-write 必需输入：章节结构 / 图表计划 |

---

## 五、服务器连接（Stage 2B 起）

```bash
PORT=xxxxx

# 验证连接
ssh -o StrictHostKeyChecking=no -p $PORT root@your-server.example.com \
  "echo OK && nvidia-smi --query-gpu=name,memory.total --format=csv"

# 建目录
ssh -o StrictHostKeyChecking=no -p $PORT root@your-server.example.com \
  "mkdir -p /root/projects/${PROJECT_NAME}/{data,outputs,checkpoints,logs}"

# 同步代码
rsync -avz --exclude '.git' --exclude '__pycache__' \
  -e "ssh -o StrictHostKeyChecking=no -p $PORT" \
  ./ root@your-server.example.com:/root/projects/${PROJECT_NAME}/
```

---

## 六、项目文件结构

```
./
├── CLAUDE.md                        # 项目规则（对话自动读入）
├── SETUP.md                         # 本文件
├── main.py                          # 入口：argparse + Trainer
├── utils.py                         # 工具函数
├── Makefile
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── configs/
│   └── default.yaml
├── data/
│   ├── __init__.py
│   ├── data_interface.py            # LightningDataModule（勿改接口名）
│   └── standard_dataset.py
├── model/
│   ├── __init__.py
│   ├── model_interface.py           # LightningModule（勿改接口名）
│   └── standard_model.py
├── scripts/
│   ├── train.sh · test.sh · run_all.sh · ablation.sh
│   ├── visualize.py                 # 训练曲线 → figures/
│   └── export_results.py            # results JSON → LaTeX 表格
│
├── docs/                            # 00–13 研究文档（见三节清单）
│   ├── 00_venue_requirements.md
│   └── doc/                         # 论文素材（YYYY-MM-DD_描述_vN.ext）
├── paper/
│   ├── main.tex
│   ├── sections/
│   └── references.bib
├── figures/                         # 数据图（paper-figure 生成）
├── results/                         # 实验输出 JSON
├── refine-logs/                     # research-refine 内部状态（自动生成，勿删）
├── train_log/
└── test_log/
```

---

## 七、异常处理

| 现象 | 处理 |
|------|------|
| SSH 连接失败 | 确认端口号，检查服务器是否开启 |
| screen session DEAD | `tail -100 logs/train.log` 查原因 → 修 → 重跑 |
| NaN loss | 检查 lr / gradient clipping / 数据归一化 |
| 显存不足 | 减 batch_size → gradient checkpointing → 换小模型 |
| Context 满 | 见二节 Context 管理，用锚点恢复 |
| idea-discovery 子技能报错 | 确认已安装：research-lit · idea-creator · novelty-check · research-refine |
| experiment-bridge 找不到文件 | 确认 docs/05_experiment_plan.md 和 docs/04_final_proposal.md 已生成 |
