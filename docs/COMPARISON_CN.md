# 设计背景与对比

[English](COMPARISON.md) · [简体中文](COMPARISON_CN.md)

本模板把科研 Agent 的实践思路组织为可移植的项目契约：研究问题、证据、实验、结果和稿件能够逐项对应。区别体现在实际结构和执行要求中。

| 设计选择 | 具体落实 |
|---|---|
| 科学判断有负责人 | 00记录范围与权限；A–F结论写入对应阶段记录 |
| 先恢复科学问题，再构建方法 | 01–05记录数据、问题候选、可行性、比较对象与证伪条件 |
| 结果保留完整来源链 | 不可变运行身份、配置哈希、原始状态和统一台账 |
| 结果表按预先约定的集合生成 | 表构建器核验运行覆盖、终态、指标及数值来源 |
| 稿件围绕证据组织 | 09追踪论断/图表/章节，10–11核验图表和稿件 |
| 变化只使相关检查失效 | A–F有明确依赖路由，保留未受影响的判断 |
| 助手可以替换 | 通用文件契约、规范技能目录、Claude副本与显式读取入口 |
| 上下文按需展开 | 00当前状态、阶段文档和能力profile分层读取 |

## 设计借鉴与本模板的实现

本模板的设计借鉴包括下列项目。借鉴主要体现为科研推进、文献处理、技能组织、图文协同与审阅修复的工作方法；下表把来源与本模板中可检查的实现方式对应起来。公开包保留其18项核心和项目记录，不要求运行所有上游项目。

| 设计借鉴来源 | 借鉴的侧重 | 在本模板中的组织方式与区别 |
|---|---|---|
| [AI Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) | 自主研究与实验迭代 | 把探索推进落实为有预算、停止条件与产物核验的阶段流程 |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 文献—实验—报告的角色协作 | 交接携带问题、论断和运行 ID，主控核验后整合 |
| [AI-Researcher](https://github.com/HKUDS/AI-Researcher) | 连接选题、研究执行与论文的端到端流程 | 用项目内记录接续全流程，保留工具替换和研究者决定 |
| [AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 可复用科研技能与研究构思视角 | 围绕 Stage 0–6、Gate A–F 组织18项核心；问题质量参考保留来源 |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 系统文献流程、引文核验与科学可视化 | 文献服务于可检验论断，图表关联真实运行和数据；不要求装完整技能库 |
| [Nature Skills](https://github.com/Yuan1z0825/nature-skills) | 结构化文献处理、学术表达与科研绘图流程 | 把文献、论断、图表和稿件接入统一阶段记录与核验规则 |
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) | 研究—写作—审阅—修订的闭环 | 审阅结论绑定稿件版本，修复后重验受影响的 Gate |
| [PaperOrchestra](https://github.com/Ar9av/PaperOrchestra) | 技能驱动的论文流水线与质量评估 | 按具体风险选择审阅视角，以实际证据和修订闭环验收 |
| [Research Literature Review](https://github.com/huangwb8/ChineseResearchLaTeX/tree/main/skills/research-literature-review) | 全流程文献综合与相关工作组织 | 文献综合进入问题和证据图，保持引用核验与正文论断一致 |
| [AIPOCH Systematic Review](https://github.com/aipoch/medical-research-skills) | 检索、筛选与证据质量评价的规范化 | 按研究类型明确纳入规则与证据强度；通用流程不等同医学系统综述认证 |
| [Medical Imaging Review](https://github.com/luwill/research-skills/tree/main/medical-imaging-review) | 面向具体领域的问题、方法与文献组织 | 以数据审计和领域评价协议承接专项知识，保护比较公平性 |
| [Research Superpower](https://github.com/kthorn/research-superpower) | 文献发现、筛选、引文追踪与综合 | 检索服务于研究缺口与论断判断；原文支持和来源标识进入记录 |

### 一个具体例子

采用文献流程的检索、筛选和综合经验后，相关工作不止成为一份读书报告：它进入 `03_idea_report.md` 的问题与证据图，支持 `05_experiment_plan.md` 的比较和检验，再关联 `08_analysis.md` 的论断处置、`09_paper_plan.md` 的叙事位置及 `11_pre_submission_audit.md` 的引文核验。文献技能、实验助手和写作助手由这条共同记录链接续。

Nature Skills 的文献流水线、K-Dense 的文献综述工具和本模板可承担不同层次的工作。设计借鉴不表示本模板自动拥有它们的定时推送、所有数据库、专项医学流程或完整工具集合。

## 来源与收录范围

设计借鉴依据维护者的开发说明；上游功能依据链接中的项目文档，本模板的实现依据当前文件和工具。逐项代码或文字改编的声明仍须对应具体材料与许可，见 [NOTICE](../NOTICE.md)；实际随包范围见[来源与收录范围](ECOSYSTEM_CN.md)。

Medical Imaging Review 在多个仓库中存在同名技能，表中链接明确指定本次对比对象；PaperOrchestra 与 Orchestra Research 是不同项目。比较说明设计侧重，不代表其他项目缺少某种能力，也不宣称论文质量、录用率、成本或速度优势。一手项目页面核验日期：2026-10-06。
