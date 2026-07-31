
你现在位于一个用于开发研究软件文档 Skills 系统的工作区。

skills 开发工作模式：

- 工作区与实际 claude code skills 加载之间通过 github 隔离，方便版本维护。
- 你应当仅在该工作区中编写 skills 文档与代码，并启动 sub-agent 通过直接注入提示词的方法进行测试；
- **禁止**在不通知我的情况下直接推送到 github、或者直接执行 claude code 中的安装、删除、改动。

你的目标不是立即创建全部 Skills，也不是直接改写任何项目文档。你需要先建立一套可复用、可评测、可版本化的 Skills 架构，用于：

1. 数值计算、优化和科学计算软件的研究型设计文档；
2. 开发—测试—实验复合工作区的梳理、重构与维护文档；
3. 已有混乱文档集合的审计、讨论和重构。

具体的设计请参照 `docs\研究软件文档Skills系统_设计与创建指南.md`。

现有环境中包含 Matt Pocock 的大量软件开发 Skills，以及若干上游文档和科研写作 Skills。你必须区分：

- 可继续使用的实现类 Skills；
- 需要缩窄触发范围的 Skills；
- 需要拆分的 Skills；
- 将被新总控流程替代的 Skills；
- 只可作为参考、不得自动激活的 Skills。

第一阶段只完成以下工作：

A. 审计现有 Skills

1. 列出当前已安装和参考目录中的所有 Skills。
2. 为每个 Skill 记录：用途、触发条件、输入、输出、写入范围、依赖、冲突、是否自动触发、许可证和上游 commit。
3. 按以下类别分类：
   - KEEP
   - KEEP_WITH_LIMITS
   - SPLIT
   - REPLACE
   - REFERENCE_ONLY
   - REMOVE
4. 重点检查与以下新流程的冲突：
   - numerical-research-software-design
   - scientific-workspace-reconstruction
   - documentation-refactor

B. 设计系统架构

用作设计参考的 `docs\研究软件文档Skills系统_设计与创建指南.md` 是由第三方评估给出的，不一定适配本机实际环境。请你再第一阶段审计的基础上，**微调设计使其适配当前状态**。

建立：

- 总控 Skill 与原子 Skill 的职责边界；
- 调用链；
- 触发优先级；
- 冲突矩阵；
- 规范来源；
- 写入权限；
- 状态和证据等级；
- 上下文预算；
- Skill 注册表 schema；
- 版本和废弃策略。

C. 建立评测基础

仅在当前工作区中创建，但不要推送到 github：

1. documentation-quality-evaluator
2. project-state-reconstructor
3. goal-scope-and-workflow-elicitor
4. uncertainty-and-decision-manager

其中 documentation-quality-evaluator 必须最先创建，用于评测后续 Skills。

为每个 Skill 建立：

- 10 个 should-trigger；
- 10 个 should-not-trigger；
- 5 个冲突案例；
- 3 个多轮案例；
- 至少 2 个真实历史项目任务；
- 硬性失败条件；
- 软评分量表。

D. 创建过程约束

1. 不允许简单拼接上游 SKILL.md。
2. 每条采用的规则必须记录来源和适用边界。
3. 任何尚未通过评测的新 Skill 均不得自动触发。
4. 审计类 Skill 默认只读。
5. 重写类 Skill 不得覆盖原文件。
6. 迁移类 Skill 必须先生成 dry-run 映射。
7. 不得将项目专用算法、测试数量或当前状态写入通用 Skill。
8. 不得把论文中的间接证据写成项目已验证事实。
9. 能用脚本检查的内容必须创建确定性检查器。
10. 所有输出必须记录 Skill 版本、来源 commit 和生成时间。

E. 第一轮交付物

生成：

- docs/skill-development/system-architecture.md
- docs/skill-development/current-skills-audit.md
- docs/skill-development/conflict-matrix.md
- docs/skill-development/creation-roadmap.md
- docs/skill-development/quality-control-plan.md
- docs/skill-development/skills-registry.yaml
- references/documentation-methodology/upstream-method-matrix.md
- evals/skills/ 的初始结构

然后创建第一批四个 Skill 的草案，但设置为 experimental 和 manual-only。

完成后运行触发评测、冲突评测和一个端到端真实案例。只有 documentation-quality-evaluator 通过基础评测后，才能继续创建第二批 Skills。


---
