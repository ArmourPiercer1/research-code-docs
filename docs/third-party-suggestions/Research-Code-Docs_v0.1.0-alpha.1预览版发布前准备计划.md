# Research-Code-Docs v0.1.0-alpha.1 预览版发布前准备计划

> 仓库：`ArmourPiercer1/research-code-docs`  
> 日期：2026-08-06  
> 当前候选定位：**内部受控 Alpha / Manual-only / Non-destructive / Documentation-focused**  
> 目标：在不继续扩张测试平台、不提前开放自动化与破坏性权限的前提下，将当前 Skills 系统整理成可安装、可验证、可回滚、可供少量用户试用的初始预览版。

---

## 0. 发布结论

当前系统已经具备实际产品价值：

- Batch 1–2 原子 Skill 已建成并完成轻量验证；
- Batch 2.5 已证明多 Skill 可通过磁盘 artifact 独立交接；
- Batch 3 三个 L1 控制流已建成；
- `documentation-refactor` 已形成首条真实闭环；
- dry-run migration、candidate rewrite、DQE advisory 和 maintenance proposal 均已跑通；
- 原始文件未被修改、移动、删除或覆盖；
- 未授权写操作会被正确阻塞。

但当前仍不适合定位为公开 Beta 或生产版本。

推荐发布定位：

```yaml
release: v0.1.0-alpha.1
channel: internal-preview
audience:
  - project owner
  - 1-3 controlled technical users
invocation: manual-only
auto_trigger: false
destructive_writes: disabled
installation: explicit-user-action
supported_primary_workflow:
  - documentation-refactor-dry-run
```

### 可以投入使用的方式

```text
隔离工作区
+
明确手动调用
+
只生成候选文件
+
不覆盖原文件
+
用户人工审阅
```

### 当前不能宣传的能力

```text
通用自动文档系统
自动发布
自动文件迁移
自动删除/覆盖
生产级 terminal gate
完整数值研究软件设计闭环
完整工作区重建闭环
```

---

# 1. 当前可发布的功能范围

## 1.1 正式支持：文档重构预览链

支持的主流程：

```text
documentation-refactor
```

能力链：

```text
workspace-forensics-and-inventory
  mode=document-corpus
→ project-state-reconstructor
→ goal-scope-and-workflow-elicitor
→ document-information-architect
→ content-canonicalization-and-migration
→ technical-document-rewriter
→ documentation-quality-evaluator
  advisory only
→ living-design-maintainer
→ final flow-state
```

正式支持的输出：

```text
inventory-report
project-state-report
goal-scope-note
document-artifact-map
canonical-source-map
open-decisions
migration-map
candidate-doc-set/
rewrite-provenance-report
quality-advisory
maintenance-impact-report
final-flow-state
```

允许的完成范围：

```text
dry-run migration
candidate document generation
advisory quality review
maintenance impact proposal
```

禁止的行为：

```text
move
delete
overwrite
auto-publish
auto-accept candidate
auto-trigger
```

---

## 1.2 可作为独立工具使用的原子 Skill

以下 Skill 可以作为 manual advisory 工具使用：

- `documentation-quality-evaluator`
- `project-state-reconstructor`
- `goal-scope-and-workflow-elicitor`
- `uncertainty-and-decision-manager`
- `workspace-forensics-and-inventory`
- `document-information-architect`
- `research-question-and-literature-planner`
- `research-evidence-synthesizer`
- `content-canonicalization-and-migration`
- `technical-document-rewriter`
- `living-design-maintainer`

使用限制：

```yaml
status: experimental
manual_only: true
auto_trigger: false
destructive_writes: false
human_review_required: true
```

---

## 1.3 实验性预览

以下两个 L1 流程可以作为“前缀流程”试用：

```text
scientific-workspace-reconstruction
numerical-research-software-design
```

它们会：

- 调用已经建成的原子 Skill；
- 保存中间 artifact；
- 写入 flow-state；
- 在第一个尚未开发的能力处诚实停止；
- 返回具名 `blocked_by`。

它们不会形成完整闭环。

---

## 1.4 暂不支持

```text
auto-trigger
live-loader 自动安装
真实文件 move/delete/overwrite
自动发布
candidate 自动转 canonical
DQE 通用 terminal gate
controlled experiment release gate
完整数值设计闭环
完整 workspace reconstruction 闭环
```

---

# 2. 发布前 P0 必须完成项

预览版发布前不需要恢复 Phase E，也不需要再构建大型模型测试矩阵。

真正必须完成的是发布工程。

---

## 2.1 定义系统级版本

当前各 Skill 有独立版本，但整个系统还需要统一 release version。

建议新增：

```text
VERSION
release-manifest.yaml
```

`VERSION`：

```text
0.1.0-alpha.1
```

`release-manifest.yaml` 示例：

```yaml
release:
  name: research-code-docs
  version: 0.1.0-alpha.1
  channel: internal-preview
  source_commit: "<release commit SHA>"
  release_date: "2026-08-xx"

posture:
  manual_only: true
  auto_trigger: false
  destructive_writes: false
  dqe_mode: advisory-profile-scoped

supported_workflows:
  - name: documentation-refactor
    scope:
      - dry-run-migration
      - candidate-output
      - advisory-quality-review
      - maintenance-impact-proposal

experimental_workflows:
  - scientific-workspace-reconstruction
  - numerical-research-software-design

unsupported:
  - auto-trigger
  - automatic-publish
  - destructive-apply
  - universal-terminal-gate
  - experiment-release-admission
```

验收：

- release version 唯一；
- manifest 中的 Skill 版本与 registry 一致；
- source commit 固定；
- supported/experimental/unsupported 明确分开。

---

## 2.2 编写安装说明

新增：

```text
INSTALL.md
```

必须包含：

1. 支持的平台；
2. Python 版本；
3. Claude Code / Skills 目录要求；
4. 必需依赖；
5. 可选依赖；
6. 安装命令；
7. 目标目录；
8. 冲突检查；
9. 安装后的预检；
10. 回滚方法。

推荐安装原则：

```text
copy or symlink into isolated workspace skill directory
never overwrite existing skill without explicit confirmation
never modify installed third-party skills
```

安装模式应至少支持：

### 模式 A：工作区本地安装

```text
<project>/.claude/skills/
```

推荐作为 Alpha 默认模式。

### 模式 B：用户级安装

暂不作为默认，只在明确说明风险后提供。

---

## 2.3 编写卸载与回滚说明

新增：

```text
UNINSTALL.md
```

必须说明：

- 哪些目录由本系统创建；
- 哪些文件可以安全删除；
- 如何恢复安装前状态；
- 如何清理 generated candidate outputs；
- 如何保留用户产物；
- 如何确认没有修改原始文档；
- 如何回滚到指定 release tag。

卸载不得：

- 删除用户的 source corpus；
- 删除 candidate outputs，除非用户明确选择；
- 删除其他 Skill；
- 修改全局 Claude 配置。

---

## 2.4 编写环境支持矩阵

新增：

```text
SUPPORTED_ENVIRONMENTS.md
```

建议内容：

| 项目 | Alpha 支持状态 |
|---|---|
| Windows + Claude Code workspace | 支持，需 smoke test |
| WSL2 | 支持候选，需验证路径行为 |
| Linux | 支持候选 |
| macOS | 未验证或实验性 |
| Python 3.11 | 推荐 |
| Python 3.12 | 支持候选 |
| 非 UTF-8 文件名 | 需要验证 |
| 中文路径 | 需要 smoke test |
| Git 仓库 | 推荐 |
| 非 Git 目录 | 可使用，但减少 hash/rollback 保障 |

必须明确：

```text
supported
tested
experimental
unsupported
```

四种状态不能混用。

---

# 3. 发布预检工具

新增：

```text
scripts/preflight.py
```

该脚本必须是只读的。

## 3.1 检查内容

### 环境

- Python 版本；
- PyYAML 等依赖；
- Git 是否存在；
- 工作目录是否可读；
- candidate output 目录是否可写。

### Skill 安装

- 所有 release-manifest 中列出的 Skill 是否存在；
- 每个 `SKILL.md` frontmatter 是否可解析；
- `disable-model-invocation` 是否符合 release posture；
- 是否意外存在 `auto_trigger=true`；
- 是否出现危险权限；
- Skill 版本是否与 registry 一致。

### Checker

验证以下工具可运行：

```text
run_checks.py
interface_check.py
flow_state_check.py
migration_map_check.py
rewrite_provenance_check.py
maintenance_impact_check.py
```

### L3 依赖

检查并分类：

```text
present
missing-optional
missing-required
version-unknown
```

不得因为一个可选 Skill 缺失就中止全部安装。

### 冲突

检查：

- 是否已存在同名 Skill；
- 是否存在不同版本；
- 是否可能覆盖用户修改；
- 是否存在未确认的 installed research Skill 冲突。

## 3.2 输出格式

```yaml
preflight:
  status: PASS | WARN | FAIL
  environment:
  skills:
  dependencies:
  checkers:
  conflicts:
  warnings:
  blocking_errors:
  recommended_actions:
```

## 3.3 退出码

```text
0 = PASS
1 = WARN
2 = FAIL
```

WARN 不得被描述为完全成功。

---

# 4. 用户 Quickstart

新增：

```text
QUICKSTART.md
```

目标是让一个熟悉 Claude Code、但不了解本项目内部架构的用户，在不阅读全部治理文档的情况下完成第一次安全调用。

## 4.1 Quickstart 必须回答

- 这个系统解决什么问题；
- 当前正式支持什么；
- 输入应是什么；
- 如何调用；
- 会生成哪些文件；
- 哪些源文件绝不会被改动；
- 如何检查输出；
- 如何处理 open decisions；
- 如何申请 apply-mode；
- 什么情况下流程会 `BLOCKED`；
- DQE `ALLOW` 为什么不是发布授权。

## 4.2 推荐示例

输入请求：

```text
使用 documentation-refactor 分析 docs/ 目录。
请设计新的文档结构，生成 dry-run migration map 和 candidate documents。
不要移动、删除或覆盖任何原文件。
```

预期输出：

```text
results/documentation-refactor/<run-id>/
  inventory-report.md
  project-state-report.md
  goal-scope-note.md
  document-artifact-map.md
  canonical-source-map.md
  migration-map.md
  candidate-doc-set/
  rewrite-provenance-report.md
  quality-advisory.md
  maintenance-impact-report.md
  final-flow-state.md
```

## 4.3 用户检查清单

```text
[ ] source corpus hash 未变化
[ ] final-flow-state 与请求 scope 一致
[ ] open decisions 未被静默裁决
[ ] candidate 文档未标为 canonical
[ ] DQE 结果明确为 advisory
[ ] maintenance proposals 均未自动 apply
```

---

# 5. 支持范围与已知限制

新增：

```text
SUPPORT_MATRIX.md
KNOWN_LIMITATIONS.md
```

---

## 5.1 支持矩阵

建议：

| 能力 | 状态 | 说明 |
|---|---|---|
| 文档 corpus inventory | Supported | read-only |
| project state recovery | Supported advisory | 不等于 runtime execution proof |
| information architecture | Supported | 只设计，不执行 |
| dry-run migration | Supported | 不移动或删除 |
| candidate rewriting | Supported | new files only |
| DQE advisory | Supported profiles only | 非通用 terminal gate |
| maintenance impact | Supported proposal-only | 不修改 canonical |
| workspace reconstruction | Experimental prefix | 会在缺失能力处 BLOCKED |
| numerical design | Experimental prefix | 尚无完整设计核心 |
| auto-trigger | Unsupported | 禁止 |
| destructive apply | Unsupported in Alpha | 需未来单独设计 |
| experiment release gate | Unsupported | DQE 返回 INCOMPLETE |

---

## 5.2 已知限制

至少记录：

1. `documentation-refactor` 的 COMPLETE 仅针对 dry-run + candidate-output；
2. candidate 中的相对链接可能需要在目标落位后重新验证；
3. DQE 不是自动发布批准器；
4. controlled experiment release profile 不支持；
5. Batch 1 部分 Skill 尚缺完整 task-quality 和 multi-turn 测试；
6. 三个新 Batch-5 Skill 使用轻量测试，不等于 production promotion；
7. workspace 与 numerical 两条流程仍不闭环；
8. 所有自动触发均关闭；
9. 当前主要通过真实单项目语料验证，跨项目泛化证据仍有限；
10. 大规模文档 corpus 的性能与上下文预算尚未系统测量。

---

# 6. Clean-room Smoke Test

这是发布前最关键的验证。

新增：

```text
docs/release/clean-room-smoke-test.md
scripts/smoke_test.py
```

---

## 6.1 测试环境

使用：

```text
全新 clone
或
临时目录
或
独立测试仓库
```

不得复用开发工作区的缓存状态作为唯一依据。

## 6.2 流程

```text
1. clone release candidate
2. run preflight
3. install workspace-local skills
4. verify registry and versions
5. copy a small real document corpus
6. run documentation-refactor manually
7. generate candidate outputs
8. run all deterministic checkers
9. compare source hashes before/after
10. inspect final flow-state
11. run unauthorized-write negative
12. uninstall
13. verify rollback
```

## 6.3 Smoke Test 主案例

请求：

```text
分析当前文档 corpus，生成 dry-run migration plan、
candidate rewritten documents 和 maintenance impact report。
不要移动、删除或覆盖原文件。
```

预期：

```yaml
flow_status: COMPLETE
requested_scope: dry-run-and-candidate-output
source_files_changed: 0
moved_files: 0
deleted_files: 0
overwritten_files: 0
all_hard_checks: PASS
dqe_mode: advisory
```

## 6.4 安全负例

请求：

```text
直接覆盖原文件并删除旧文档。
```

在没有 apply approval 时预期：

```yaml
flow_status: BLOCKED
blocked_by: explicit-write-approval-required
```

## 6.5 Clean-room 通过标准

```text
preflight PASS 或只有已接受 WARN
安装成功
主案例完成
负例正确阻塞
源文件 hash 不变
卸载成功
没有残留自动触发配置
没有覆盖已有 Skill
```

---

# 7. 发布文档与法律信息

## 7.1 项目许可证

必须确认：

- 仓库自身许可证；
- 用户能否复制、修改和重新分发；
- 内部文档是否可以随 release 分发；
- 第三方方法借鉴是否需要额外 NOTICE。

新增或确认：

```text
LICENSE
NOTICE
THIRD_PARTY_LICENSES.md
```

## 7.2 上游归属

应从现有 upstream-method-matrix 生成精简发布版说明，包括：

- 上游项目；
- 方法借鉴类型；
- 许可证；
- 是否复制代码；
- 是否仅借鉴方法；
- 是否存在非商业限制内容；
- 是否允许公开发布。

任何 CC-BY-NC 或不明确许可来源都应单独标记。

## 7.3 Changelog

新增或更新：

```text
CHANGELOG.md
```

`v0.1.0-alpha.1` 至少包含：

### Added

- 第一条 documentation-refactor 闭环；
- artifact interfaces；
- flow-state；
- three Batch-5 doc executors；
- deterministic checkers；
- preflight/install/smoke 工程。

### Safety

- manual-only；
- no destructive writes；
- DQE advisory-only；
- unsupported profile guard；
- explicit approval block。

### Known limitations

链接到 `KNOWN_LIMITATIONS.md`。

---

# 8. 发布标签与产物

建议发布：

```text
tag: v0.1.0-alpha.1
title: Research-Code-Docs v0.1.0-alpha.1 — Internal Preview
```

## 8.1 Release 产物

至少包括：

```text
source archive
release-manifest.yaml
VERSION
INSTALL.md
UNINSTALL.md
QUICKSTART.md
SUPPORTED_ENVIRONMENTS.md
SUPPORT_MATRIX.md
KNOWN_LIMITATIONS.md
CHANGELOG.md
LICENSE
NOTICE
smoke-test report
```

## 8.2 不应包含

- `.venv/`
- `__pycache__/`
- `*.pyc`
- 临时 agent logs；
- 大型 blind-run 结果；
- 私有路径；
- 用户数据；
- 无关历史调试产物；
- 未确认许可证的第三方内容。

## 8.3 发布前归档

建议将开发期重型证据保留在仓库，但不放进最终分发包：

```text
evals/skills/snapshots/
tests/corpus/blind-runs/
large diagnostic reports
historical failure dumps
```

发布包只需包含运行所需资产和精简证据摘要。

---

# 9. 受控 Alpha 使用计划

初始发布用户：

```text
1–3 名
```

真实项目：

```text
2–3 个文档项目
```

使用规则：

```text
manual invocation only
isolated workspace
candidate-output only
no destructive apply
human review required
```

## 9.1 反馈记录

每次运行记录：

```yaml
run_id:
release_version:
project_type:
corpus_size:
workflow:
result:
flow_status:
blocked_by:
source_files_changed:
reader_can_act:
user_found_value:
user_confusion:
skill_defects:
interface_defects:
harness_defects:
requested_features:
```

## 9.2 回归测试准入

只有出现以下情况才新增 regression：

- 真实运行暴露可复现错误；
- 两个用户遇到相同问题；
- 确定性 checker 发现真实缺陷；
- reader 无法从输出继续；
- 出现安全边界违规。

不得因为“以后可能出问题”重新建立大型测试矩阵。

---

# 10. 发布门

## 10.1 Alpha 发布必须满足

```text
[ ] system version 固定
[ ] release manifest 完整
[ ] install / uninstall 文档完成
[ ] preflight PASS
[ ] clean-room smoke 主案例 PASS
[ ] safety negative PASS
[ ] source hash unchanged
[ ] support matrix 完成
[ ] known limitations 完成
[ ] license / notice 完成
[ ] changelog 完成
[ ] tag 对应固定 commit
[ ] 所有 Skill 仍 manual-only
[ ] auto-trigger 全为 false
```

## 10.2 不作为 Alpha 阻塞项

以下内容不应阻塞内部 Alpha：

- DQE Phase E；
- DQE v0.4.2；
- 全部 Skill 的大型 promotion test；
- numerical workflow 闭环；
- workspace workflow 闭环；
- auto-trigger；
- destructive apply mode；
- 多平台全部验证；
- 公开文档站点。

---

# 11. Alpha 之后的晋级条件

## 11.1 外部技术用户 Alpha

需要额外满足：

- 至少 2 个外部真实项目；
- clean install 在至少 2 种环境通过；
- 无 P0/P1 安全缺陷；
- Quickstart 用户无需开发者介入即可完成；
- 所有候选输出可审阅；
- 安装和卸载可重复。

## 11.2 Beta

需要：

- numerical 或 workspace 至少再闭环一条；
- task-quality 和 multi-turn 真实覆盖增加；
- 支持矩阵更稳定；
- 版本兼容策略；
- CI；
- 最小 telemetry/run report；
- 明确升级和 migration policy。

## 11.3 v1.0

需要另行定义，不应由 Alpha 自动外推。

---

# 12. 建议 Sprint：Release R0

## R0.1 发布元数据

- `VERSION`
- `release-manifest.yaml`
- `CHANGELOG.md`
- `LICENSE/NOTICE`
- support scope

## R0.2 安装工程

- `INSTALL.md`
- `UNINSTALL.md`
- `scripts/preflight.py`
- workspace-local install script
- rollback

## R0.3 用户体验

- `QUICKSTART.md`
- sample corpus
- example invocation
- output walkthrough

## R0.4 Clean-room 验证

- fresh clone
- install
- smoke main case
- safety negative
- uninstall
- report

## R0.5 发布

- freeze release commit
- run release checklist
- tag `v0.1.0-alpha.1`
- create internal release notes

建议总测试预算：

```text
确定性脚本与 smoke 为主
模型 agent slot <= 8
不运行大型矩阵
不使用 background workflow
```

---

# 13. 给本地 Agent 的执行提示词

```text
目标：把当前 research-code-docs 整理成 v0.1.0-alpha.1 内部受控预览版。

发布定位：
- internal-preview
- manual-only
- non-destructive
- documentation-refactor dry-run/candidate-output 正式支持
- workspace/numerical flows 仅 experimental prefix
- DQE advisory/profile-scoped
- no auto-trigger
- no destructive apply

必须完成：

1. 新增 VERSION=0.1.0-alpha.1。
2. 新增 release-manifest.yaml：
   - source commit
   - supported workflows
   - experimental workflows
   - unsupported capabilities
   - skill versions
3. 新增 INSTALL.md、UNINSTALL.md。
4. 新增 SUPPORTED_ENVIRONMENTS.md。
5. 新增 QUICKSTART.md。
6. 新增 SUPPORT_MATRIX.md、KNOWN_LIMITATIONS.md。
7. 新增 scripts/preflight.py，必须只读，检查：
   - Python/dependencies
   - skill presence/version
   - disable-model-invocation
   - auto_trigger=false
   - checker availability
   - L3 dependencies
   - name/version conflicts
   - candidate output writeability
8. 新增 clean-room smoke test：
   - fresh clone/temp workspace
   - install
   - preflight
   - documentation-refactor main case
   - source hash unchanged
   - unauthorized overwrite/delete request BLOCKED
   - uninstall/rollback
9. 确认 LICENSE、NOTICE、THIRD_PARTY_LICENSES。
10. 更新 CHANGELOG。
11. 生成 release checklist 和 smoke report。
12. 固定 release commit，创建 tag v0.1.0-alpha.1。

硬限制：
- 不恢复 Phase E
- 不修改 DQE 判别逻辑
- 不启用 auto-trigger
- 不安装到用户级全局目录作为默认
- 不实现 destructive apply
- 不扩张大型测试 corpus
- 模型测试 slot <= 8
- 不使用 background workflow

Alpha 发布门：
- preflight PASS
- clean-room main smoke PASS
- safety negative PASS
- source files changed=0
- uninstall PASS
- support/limitations/licensing docs complete
- release tag points to fixed commit
```

---

# 14. 最终判断

当前最合适的目标不是继续新增 Skill，也不是立即公开发布，而是：

```text
把已形成的第一条真实闭环
包装成一个可安装、可预检、可回滚、边界清楚的内部 Alpha。
```

发布完成后的准确表述应为：

> Research-Code-Docs v0.1.0-alpha.1 是一个面向研究软件文档治理的内部受控预览版。它正式支持手动、非破坏性的文档重构 dry-run 和 candidate-output 工作流；其他工作流仍为实验性前缀；所有自动触发、破坏性写入和通用终端审批均关闭。
