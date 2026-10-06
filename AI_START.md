# Start a research project / 开始科研项目

Read `AGENTS.md`, `docs/00_start.md` and the document index before acting. Follow the current user's project decisions and the host's higher-priority instructions. Load only the current stage and relevant skill; do not run the entire workflow just because this template is present.

先读 `AGENTS.md`、`docs/00_start.md` 和文档索引。当前用户决定与宿主的上位规则优先。只读取当前阶段及相关技能，不因模板存在而自动启动完整科研流程。

Skills have one canonical copy under `.agents/skills/<name>/SKILL.md`. If native skill discovery is unavailable, explicitly read the selected `SKILL.md` and its required references. Use `python tools/project.py list` to inspect the bundled profiles.

技能事实源是 `.agents/skills/<name>/SKILL.md`。原生发现不可用时显式读取选中的技能及必需参考；用 `python tools/project.py list` 查看随仓库提供的分组。

Verify available tools, project environment, data permissions and budget before execution. Missing tools stay explicit. An assistant or model change does not authorize new uploads, installations or compute spending. Keep claims tied to actual evidence and completed work.

执行前核验工具、项目环境、数据权限和预算。缺少工具时记录具体缺口；切换模型或助手不扩大上传、安装及算力授权。论断对应真实证据和实际完成的工作。

English overview: [Workflow](docs/WORKFLOW_EN.md) · [Records](docs/README_EN.md)

中文完整规则：[工作流](docs/WORKFLOW.md) · [记录索引](docs/README.md)
