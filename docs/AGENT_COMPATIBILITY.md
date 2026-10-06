# Agent compatibility / Agent兼容

The scientific workflow is a file contract, not a vendor API or autonomous
runtime. The initializer deploys a project; the chosen agent supplies actual tools.
Project instructions and available tools must be checked in that host.

科研流程是一套项目文件契约，不绑定厂商API或独立运行时。初始化器部署项目，实际工具由所选助手提供；在具体宿主核验规则读取和工具能力。

| Agent / 助手 | Included entry / 已提供入口 | Scope / 边界 |
|---|---|---|
| Codex | `--agent codex`, `AGENTS.md`, `.agents/skills/` | Project-local canonical skills / 项目内技能 |
| Claude Code | `--agent claude`, `CLAUDE.md`, `.claude/skills/` copies | Copies match canonical files / 副本与事实源一致 |
| DeepSeek Harness (`dsh`) | `--agent dsh`, explicit `AI_START.md` and selected skills | File-contract mode; no native plugin bundled / 文件读取方式，不包含原生插件 |
| ZCode | `--agent zcode`, workspace `AGENTS.md` | Explicit reading or user-selected project import / 显式读取或自行选择项目级导入 |
| Other file-capable assistants | `--agent generic` | Explicit startup and relevant `SKILL.md` / 显式启动与技能读取 |

## Official references / 官方依据

[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) identifies `dsh`
as DeepSeek's plugin-based agent harness and currently labels it a developer
preview. This distribution does not assert a stable DSH native plugin interface;
pass the startup files to the selected agent and verify its file-reading/tool use.

DeepSeek官方仓库说明DSH是插件式Agent Harness，当前处于开发者预览。本仓库提供通用文件方式，不宣称DSH原生插件接口稳定或已完成实测。

[ZCode instructions](https://zcode.z.ai/en/docs/agents) document reading the current
workspace's `AGENTS.md`. Keep these rules at the opened workspace root rather than
rely on ancestor merging or `CLAUDE.md` runtime loading.

ZCode官方说明读取当前工作区根目录的 `AGENTS.md`；不要依赖父目录合并或运行时持续读取 `CLAUDE.md`。

[ZCode skills](https://zcode.z.ai/en/docs/skill) document importing external-agent
skills with either global or current-project scope. If using its importer, choose
the current project and verify discovered skill names and descriptions. The setup
utility never performs this UI action or changes a global skill directory.

ZCode支持在界面导入其他Agent的技能，并选择全局或当前项目。使用时选择当前项目并核验发现结果；本初始化器不自动操作导入界面或改写全局技能目录。

Documentation checked on 2026-10-06. Filesystem/adaptor tests do not prove live
native invocation, scheduling, network access or scientific validity.

官方文档核验日期2026-10-06。文件和适配测试不等于原生技能调用、调度、联网及科学有效性实测。
