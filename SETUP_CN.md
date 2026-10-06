# 可移植安装说明

[English](SETUP.md) | [简体中文](SETUP_CN.md)

[返回首页](README_CN.md) · [复制启动提示词](README_CN.md#快速开始)

## 前置条件

使用 Python 3.10+ 和能读取项目文件的助手。初始化仅依赖标准库；研究执行所需的软件、模型与数据依赖按具体项目选择，不自动安装。

## 助手入口细节

| 助手 | 参数 | 入口 / 技能目录 |
|---|---|---|
| Codex | `--agent codex` | `AGENTS.md`、通用 `.agents/skills/` |
| Claude Code | `--agent claude` | `CLAUDE.md`、额外 `.claude/skills/` 副本 |
| DeepSeek Harness | `--agent dsh` | 通用文件契约，显式提供 `AI_START.md` 与技能文件 |
| ZCode | `--agent zcode` | 工作区 `AGENTS.md`，显式读取技能或在界面选择项目级导入 |
| 其他可读取项目文件的助手 | `--agent generic` | 显式读取 `AI_START.md`、`AGENTS.md` 与选定技能 |

这是随仓库提供的文件适配方式，不代表所有助手、工具、系统与模型的实际行为都已认证。通用方式仍要求助手能够读文件；未明确的助手不宣称具备原生集成。

DSH/ZCode方式保留通用项目技能目录，不安装厂商插件或修改全局配置。详见 [兼容说明与官方来源](docs/AGENT_COMPATIBILITY.md)。

## 初始化独立项目

从发布仓库目录运行：

```bash
python tools/project.py init ../my-study --agent generic --profile research --dry-run
python tools/project.py init ../my-study --agent generic --profile research
python tools/project.py check ../my-study
```

目标应为发布仓库之外的独立目录。初始化器先核对全部目标，遇到不同内容就停止，不覆盖现有研究文件。新项目保留本地检查工具，可从新项目目录自行检查。

## 按阶段选择

| profile | 范围 |
|---|---|
| `full` | 全部18个核心技能 |
| `research` | 问题、数据、方法、实验、论断与 Gate |
| `writing` | 规划、写作、语言、引文、数值和稿件审阅 |
| `figures` | 数据图、概念图和证据核验 |
| `release` | 本地投稿与发布准备 |

```bash
python tools/project.py init ../my-study --agent claude --profile research
python tools/project.py add ../my-study --profile writing figures
python tools/project.py list
```

可用 `--skill <name> ...` 选择具体技能。补装时省略 `--agent` 会沿用现有适配器。`add` 补充项目能力，不重写研究记录。补装时从发布仓库执行；只装部分 profile 的研究项目本身没有未选择技能的源文件。

公开版只包含18项核心目录。学科技能按需从经过核验的来源选择，并满足项目授权；完整个人技能市场不随仓库上传。

## 依赖与状态

选择需要 `paper-audit` 的 profile 时，会放入 `.agenthub/runtime/latex-paper-en/scripts/` 中的10个支持脚本，不计为第19个技能。可选绘图库依赖见 `.agents/skills/scientific-figure-making/requirements.txt`。

科研状态唯一入口为 `docs/00_start.md`。`.agenthub/project.json` 只记录已装技能和适配方式，不包含凭据或绝对来源路径，Git 默认忽略它。

填写00中的问题、数据、证据目标、预算、权限和下一 Gate，再让助手按相应阶段推进。初始化不会启动实验、监控或付费计算。

## 验证

```bash
python tools/project.py check .
python -B -m unittest discover -s tools/tests -p "test_*.py"
python -B -m unittest discover -s experiments/tests -p "test_*.py"
```

上述检查覆盖初始化保护与结果表契约。科学结论、原文支持、伦理、图表和稿件编译按当前研究另行核验。
