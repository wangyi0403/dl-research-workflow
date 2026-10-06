# 来源与可选科研技能

[English](ECOSYSTEM.md) | [简体中文](ECOSYSTEM_CN.md)

[返回首页](../README_CN.md) · [设计对比](COMPARISON_CN.md) · [来源与许可](../NOTICE.md)

这套模板围绕科研流程组织能力，重点是把问题、协议、运行、证据、图表和稿件连接起来。不同学科可按实际缺口选择扩展技能。

## 有依据的来源

公开核心的问题质量指导明确参考了 [Orchestra Research / AI Research Skills](https://github.com/Orchestra-Research/AI-Research-SKILLs) 的构思视角，学术表达指导改编了 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) 的部分保守结构规则。两份许可保存在 `licenses/`，并随新项目导出；学术参考保留在相关技能文件中。详见 [NOTICE](../NOTICE.md)。

## 可选生态

下表提供外部工具入口；列出链接不表示其代码已随包提供、开发时全部使用过或得到作者背书。第三方排行的展示名称可能有歧义，以表中具体仓库为准，不沿用截图的 Star 排名。

| 仓库 / 技能 | 适合的需求 | 当前关系 |
|---|---|---|
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 广泛科学工具、系统文献综述、科学可视化 | 独立维护的扩展目录中已收录其来源的 `literature-review`、`scientific-visualization`；这两项不在本仓库18项核心内。 |
| [Nature Skills](https://github.com/Yuan1z0825/nature-skills)，含 `nature-literature-pipeline` | 文献处理、稿件和绘图流程 | 外部候选，尚无证据证明已纳入当前核心；项目名称不代表 Nature 期刊背书。 |
| [Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) | 学术研究与稿件流程 | 外部候选，未捆绑。 |
| [ChineseResearchLaTeX / research-literature-review](https://github.com/huangwb8/ChineseResearchLaTeX/tree/main/skills/research-literature-review) | 面向 LaTeX 工具体系的文献综合 | 外部候选，与 K-Dense 的 `literature-review` 不是同一技能。 |
| [AIPOCH medical-research-skills](https://github.com/aipoch/medical-research-skills) | 医学系统综述和文献筛选 | 外部候选，未捆绑。 |
| [luwill / medical-imaging-review](https://github.com/luwill/research-skills/tree/main/medical-imaging-review) | 医学影像文献综述 | 外部候选；其他仓库也有同名技能，使用前核对具体来源。 |
| [PaperOrchestra / literature-review-agent](https://github.com/Ar9av/PaperOrchestra/tree/main/skills/literature-review-agent) | Agent 相关工作与文献流程 | 外部候选，与上方 Orchestra Research 是不同项目。 |
| [Research Superpower](https://github.com/kthorn/research-superpower) | 文献检索、筛选、引文遍历与综合 | 外部候选，未捆绑。 |

K-Dense 来源可对照其历史 [literature-review 文件](https://github.com/K-Dense-AI/scientific-agent-skills/blob/0936740e52033a6256085be5fc81e5e56d606110/skills/literature-review/SKILL.md) 和 [scientific-visualization 文件](https://github.com/K-Dense-AI/scientific-agent-skills/blob/878519452f5adacbe6ec89964dd8288c968dbb7f/skills/scientific-visualization/SKILL.md)。目录里存在不证明过去某次任务实际调用过。核心 `scientific-figure-making` 与选配 `scientific-visualization` 也是不同技能，不能混称。

## 如何扩展

1. 先确认当前阶段缺什么能力，阅读上游技能、脚本、依赖与许可。
2. 只选需要的技能，记录来源和版本，按宿主官方方式导入当前项目。本仓库的 `project.py add` 只处理随包技能，不下载这些外部仓库。
3. 保留许可，保护已有技能身份和科研记录，并在所用 Agent 中核验实际发现与工具调用。
4. 输出继续关联已有问题、论断和实验 ID。文献技能仍需原文核验，绘图技能仍需真实数据与视觉检查。

仓库标识核验日期：2026-10-06。选配能力按项目所选上游版本另行核验。
