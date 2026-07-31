<!--
generated_by_skill: documentation-quality-evaluator
skill_version: 0.2.0
source_commit: n/a (evaluation run; target is an external eoopt artifact staged under tests/)
source_documents:
  - tests/最终目标设计与开发路线图.md (target under review)
  - evals/skills/harness/hard-fail.md (HF-1..HF-12)
  - evals/skills/harness/rubric.md (8-dim soft rubric + reader protocol)
  - evals/skills/harness/checkers/run_checks.py (deterministic checkers)
status: DECIDED (verdict FAIL — HF-9 blocker)
last_verified: 2026-07-30
-->

# Quality Report — `tests/最终目标设计与开发路线图.md`

**VERDICT = FAIL**  ·  total = n/a（在硬门失败处停止评分）  ·  blockers = **[HF-9]**

> 单一硬门失败（缺可追溯 front-matter）即钉死为 FAIL；其余硬门全部通过，文档实质质量高（见 §4 指示性评分与 §6 读者测试）。**修一处即可复评**。评分是**相对比较、非绝对保证**。

---

## 0. 评估范围与关键限制（务必先读）

被评文档是 **eoopt 项目**的目标设计+路线图，被搬进**本 skills 工作区**（`research-code-dev`）的 `tests/` 下作为评估夹具。因此：

- **代码态无法在本工作区核实（影响 HF-1）**：本仓库**没有** `src/eoopt/`、`docs/adr/`、`docs/design/`、`references/lit-review-*` 或 `references/algorithm/`。文档声称的"59/69 测试全绿""`PhysicsBackend` 已实现""`keep_in_box` 分支分离"等**代码态断言，从本工作区无法打开对应文件验证**。本报告据此**只判文档内部证据纪律**（每条断言是否指向某个可核证据句柄），并明确标注"外部可解析性未核"。
- **链接检查器的 "broken link" 基本是搬运产物**：36 条断链几乎都因目标在 eoopt 仓、不在此处；且文档混用**仓根相对**（`src/...`）与**文档相对**（`adr/...`、`design/...`、`../references/...`）两套约定 —— 详见 §7 的 NIT。
- **HF-9 与内容级发现不受搬运影响**：缺 front-matter、59/69 自相矛盾、术语未定义等，都是**原文档自身**的问题，判定成立。
- SKILL.md 引用的模板 `references/templates/quality-report.template.md` **在 skill 目录中缺失**（该目录仅有 SKILL.md）；本报告按 SKILL 工作流规格手工组织（§7 FYI）。

---

## 1. 工件分类（复合型）

| 维度 | 判定 |
|---|---|
| 主类型 | **roadmap（开发路线图，§三 9 个阶段）** |
| 内嵌 | **state report**（§Context + 阶段 1/2 完成态）· **evidence matrix**（§二 对齐表）· **ADR 计划 / algorithm-spec**（§四 + §1.5/阶段3 四族优化器） |
| 适用硬门并集 | roadmap(HF-6,7,9,12) ∪ state-report(HF-1,8,9,12) ∪ evidence-matrix(HF-2,9,10,12) ∪ algorithm-spec(HF-9,10,12) = **HF-1,2,6,7,8,9,10,12** |

---

## 2. 确定性检查器结果（`run_checks.py --json`，已运行未凭眼看）

```json
{
  "files_checked": 1,
  "hard_fail": true,
  "hard": {
    "frontmatter":  { "pass": false, "problems": ["no front-matter block found (need YAML '---' header or leading HTML comment)"] },
    "status_vocab": { "pass": true }
  },
  "advisory": {
    "markdown_links": { "pass": false, "problems": "36 broken links (见 §0：≈全部为搬运产物 + 混用链接约定)" },
    "placeholders":   { "pass": true }
  }
}
```

- **HARD `frontmatter` = FAIL → HF-9 命中（BLOCKER，见 §3）。** roadmap 类型不豁免 HF-9。
- HARD `status_vocab` = PASS（无非法/空状态词；"提议中/已建/已完成/待补充调研/OPEN" 用词自洽）。
- ADVISORY `markdown_links` = FAIL，但按 §0 判定为**搬运产物为主 + 链接约定混用**（NIT），非硬门。
- ADVISORY `placeholders` = PASS（目标无占位符标记；文中大量"算例届时定"是**显式设计性延迟**，非未填坑）。

---

## 3. 硬门逐条（HF-1 … HF-12）

| HF | 适用 | 判定 | 依据（引用具体行/节） |
|---|---|---|---|
| HF-1 代码态臆造 | ✔ | **无法在本区核实 / 无臆造迹象** | 断言具体且可证伪（命名 `tests/test_adr0009.py`、`test_s6.py`；`Bifurcation→3/Fold→2` 等，[行133/144]）。但见 **M1（59/69 自相矛盾）**。eoopt 代码不在本区 → 外部核实不在范围。 |
| HF-2 文献臆造 | ✔ | **无臆造迹象 / 可解析性未核** | 引用键与 arXiv ID 具体且跨 §二/§三/§附 一致（[absil2012]、[he2020]、[neustock2019]、arXiv:2006.07746 等）。本区无参考库，逐条解析未做。 |
| HF-6 路线阶段缺验收 | ✔ | **边界性软失败（局限于阶段9）** | 阶段1–2 有硬指标；阶段3–8 为方向性 + "算例届时定"（[行184/201/209/227]，属 [行11] 显式延迟）；**阶段9（[行237–249]）完全无"验证"行** → HF-6 就该阶段字面命中。计为 **MAJOR M3**，不升为第二 BLOCKER。 |
| HF-7 静默丢弃 OPEN | ✔ | **PASS** | §六（[行284–289]）保留 6 个开放问题 + §附研究/代码台账；GA 蓝本、地基小实验、连通性路线、AD 框架均前向携带。无外部决策册可 diff。 |
| HF-8 需未述**对话**上下文 | ✔ | **PASS** | 读者仅凭本文即答出目标/现状/下一步/开放问题（§6 Pass A Q1–4）。justification 层依赖的是**可引用的持久工件**（ADR/transfer/review.md），非聊天记录。术语未定义（§7 M2/m3）是读者契合度问题，非 HF-8 对话依赖。 |
| **HF-9 缺可追溯 front-matter** | ✔ | **FAIL — BLOCKER** | 检查器确认：无 YAML `---` 头、无起始 HTML 注释块，缺 skill/version/commit/time/status。**原文档自身缺陷，与搬运无关。** |
| HF-10 把 ≤E2 证据当 E3+ | ✔ | **PASS** | 外部成果标 "外部成果/就绪度 ◐新建/后期"（§二表），[neustock2019]/[amstutz2017] 明标"先例/同域佐证"；仅**本项目自有测试**（59/69）被当已验证——合法。四族选型标"设计完成待实现/押注"，未冒充实测。 |
| HF-12 承重断言→证据 | ✔ | **PASS（纪律很强）** | 抽样见 §5 claim→evidence 表：几乎每条承重断言都带句柄（引用键/测试文件/ADR/review.md 行号）或显式标 assumption/OPEN。未见"裸述为事实且无句柄且未标不确定"的承重断言。59/69 属**一致性缺陷**（M1），非 HF-12 无证据。 |

**结论：唯一硬 BLOCKER = HF-9。** 依工作流"任一硬门失败 → verdict=FAIL、停止评分"，§4 只给**指示性**观察，不计总分。

---

## 4. 软规则（指示性，未计入判定 —— 判定已由 HF-9 钉死）

> 下列为定性观察，用于修好 HF-9 后预估复评走向，**不构成本轮的评分总额**。

| 维度 | 指示带 | 要点 |
|---|---|---|
| Factual accuracy | 中高，被 M1 拉低 | 引用纪律强；但 59/69 现态自相矛盾是"活文档漂移"已实际发生（[行5/131/269] vs [行144]）。 |
| Information architecture | **强** | 论点在 [行9] blockquote **明述未埋没**；§一→§附 无孤儿节；§三↔§四 ADR 映射自洽（[行225/257/261]）。见下"反向大纲"。 |
| Actionability | 中 | 有阶段+ADR计划+§五验证策略；但未来阶段验收方向性/延迟，**阶段9无验收**（M3）。 |
| Evidence traceability | 中高 | 句柄密度高；但**未采用 harness 的 E0–E5 等级词**，用 ◐/★ 就绪度 + 内联替代。 |
| Uncertainty expression | **强** | "⚠蓝本待补充调研""提议中""押注""算例届时定"、§六 OPEN、31:1 标"d=3 旧实测·高维未测"。 |
| Reader fit | 中 | 对**内行目标读者**好（读者答出 Q1–4）；对一般读者被"工作流A–D/eoopt/tier-3/缩略语"未定义拉低（M2/m3）。 |
| Maintainability | 中 | 单源引用纪律好（引兄弟文档不复制）；但漂移已实际发生（M1/m1/m2）→ 维护风险已兑现。 |
| Concision | 中高 | 密而有的；个别超长句（[行144/328]）信息过载。 |

**反向大纲一致性检查（喂 IA）= PASS**：论点（[行9]）清晰未埋；§一(架构)/§二(文献对齐)/§三(路线)/§四(ADR)/§五(验证)/§六(开放)/§附(核实) 每节均可映射到"双表述匹配流形平台"目标，**无孤儿节**。唯一皱褶：§Context+[行7] 以"前瞻规划"口吻写，正文实为"进度报告到阶段3"——**框架/内容漂移**（m2），未达孤儿节封顶级。

**ADR/algorithm-spec 理由锚（喂相关维度）**：
- §四 ADR 计划是**索引**（why/备选/后果在被链的 `adr/00xx` 文件里，本区不可见）→ 索引本身不适用理由锚。
- **algorithm-spec 内容（§1.5 + 阶段3）强满足锚**：记录了 **why**（可移植性门/几何由确定性侧算）、**≥1 被拒备选带理由**（闭式 geodesic [colutto2010]、Laplace–Beltrami 特征对 [jaquier2021]、齐性空间运动律 [dreisigmeyer2017]、GaBO 明确排除，[行76/153/169/177]）、**后果**（四族排序 DFO→ES→GA→BO 的依据，[行180]）。这是全文最扎实的一块。

---

## 5. Claim → Evidence 表（state-report / evidence-matrix / algorithm-spec 内容抽样）

| 承重断言 | 证据句柄 | 状态 |
|---|---|---|
| 内核零改动、两级 seam 两阶段兑现 | 59/69 测试、ADR-0001（[行5/144]） | supported（自有测试）·**但 59/69 不一致→M1** |
| 阶段1 完成，含 10 项 ADR-0009 测试 | `tests/test_adr0009.py`（[行133]） | supported（句柄在，外部未核） |
| 阶段2 `keep_in_box` 实现分支干净分离 | ADR-0011 §0.1 + 内联 `Bifurcation→3/Fold→2/…`（[行144]） | supported（自有实验） |
| `project` 是合法 retraction（可移植性门理论桥） | [absil2012]（[行153]） | supported（外部理论） |
| whiten 后 κ≈20（约束雅可比条件数） | ADR-0004（[行76/154]） | supported |
| 31:1 各向异性（目标景观） | "d=3 旧实测·高维未测"（[行166/179]） | **assumption（已显式限定，高维未测）** |
| manifold-sampling 处理目标非光滑性流形≠匹配流形 | review.md:81 / matrix.md:60 / ADR-0010（[行77]） | supported（外部+澄清） |
| 家族③ 经典 GA 流形蓝本缺失 | [he2020] 归 PSO/ES/DE；[fong2019] umbrella（[行171/333]） | **OPEN（正确标记待补研）** |
| AcceleratorBackend 全可微/复步Jacobian/与EO对称 | 已实现([行133]) + 验证项"三供给一致性"([行131]) | supported-with-pointer（外部未核） |

→ **HF-12 通过**：无裸断言；唯一瑕疵是 M1 的**一致性**（非无证据）。

---

## 6. 两遍无上下文读者测试（新起子代理，仅给本文；已 RECONCILE，未橡皮图章）

**Pass A 理解**：读者仅凭本文**答出** Q1 目标（[行9]）、Q2 现状 FACT/UNKNOWN（阶段1/2 已完成 vs 阶段3 设计未实现 vs §六 未知）、Q3 下一步（[行182] 首轮4方法，验收方向性）、Q4 开放问题（§六 6 条）、Q5 证据来源（句柄密集但均指向本文之外）。→ **Q1–4 可答 → HF-8 不失败。**

**Pass B 对抗 + RECONCILE**：

| 读者发现 | 归类 | 处置 |
|---|---|---|
| 测试数 59（[行5/131/269]）vs 69（[行144]）自相矛盾 | **actionable** | → **M1（本轮最高杠杆）** |
| α 扫小实验：§五#10（[行278]）当作"阶段2前置"，但阶段2 已完成且该实验被"另起一期"延迟（[行144]） | **actionable** | → **m1** |
| §Context 只报阶段1完成、口吻前瞻，正文已到阶段3 | **contract-misread** | → **m2** |
| "不是实现计划"（[行11]）vs 阶段3 已点名 4 个具体类（[行182]） | **valid trade-off**（细节已下沉设计doc） | → FYI f3 |
| "整合用户三条设想"（[行7]）未就地枚举；想法②是书目澄清非"设想" | **actionable** | → **m6** |
| "工作流 A/B/C/D" 贯穿每阶段却从未定义 | **actionable** | → **M2** |
| eoopt/seam/原方案tier-3/大量缩略语未在首次出现处定义 | **actionable** | → **m3** |
| 依赖箭头"→"（[行30]）字面像"内核依赖物理层"，与"内核领域无关"冲突，仅 §附[行307] 化解 | **contract-misread** | → **m4** |
| κ≈20 与 31:1 两个各向异性量首次出现处未清晰区分 | **actionable** | → **m5** |
| 阶段9 无验收、阶段3/5/6/7/8 验收方向性 | **actionable**（阶段9）/ 部分设计性延迟 | → **M3** / m7 |
| "所有引用都指向本文之外，无法在此核实" | **valid trade-off**（语料型文档应引兄弟、非内联） | 不罚（HF-8 PASS） |
| "31:1 连句柄都没有" | **noise**（[行179] 已给来源） | 驳回，仅保留 m5 |

---

## 7. 按严重度排序的修复清单（一处结构问题先于任何 nit）

### BLOCKER（判定为 FAIL 的硬门）
- **[BLOCKER · HF-9] 补齐可追溯 front-matter。** 在文首加 YAML `---` 块或 HTML 注释块，含 `generated_by_skill / skill_version / source_commit / source_documents / status / last_verified` 六键。这是唯一钉死 FAIL 的门，修好即可复评。

### MAJOR（维度薄弱 / 读者关键项失败）
- **[MAJOR · M1] 测试数 59↔69 自相矛盾（Factual/Maintainability）。** 阶段2 已交付 **69**（[行144]，2026-07-29），但 [行5]"当前 59"、[行131]"现有 59"、[行269]"现有 59"仍为旧值。统一为当前真值（并考虑用"截至 <日期>=N"而非无日期"当前/现有"，杜绝再漂移）。
- **[MAJOR · M2] "工作流 A/B/C/D" 承重标签全篇未定义（Reader fit）。** 9 个阶段标题各挂一个工作流字母（[行124/135/148/187/195/204/212/230]），但 A→主线/物理、B→优化器、C→多分支、D→多目标 的映射从未给出。加一张 4 行对照表即可。
- **[MAJOR · M3] 阶段9 无任何验收行（Actionability / HF-6 局部命中）。** [行237–249] 无"验证："。至少补一句方向性验收（如"在合成数据流形上 `SampleLearnedConstraint` 复现已知隐式约束"），与阶段1–8 齐平。

### MINOR
- **[MINOR · m1]** §五#10 α 扫（[行278]）与阶段2"另起一期"记录（[行144]）矛盾——改为"（阶段2 已将此延迟至后续期）"。
- **[MINOR · m2]** §Context（[行5]）补记阶段2/3 进展并把[行7]前瞻口吻改为"进度快照+前瞻"，消除框架/内容漂移。
- **[MINOR · m3]** 首次出现处一句话定义 `eoopt`、`seam`（可仍指 ADR-0001）、`原方案 tier-3`（要么给 tier-1/2 图景、要么去掉"tier-3"标签），并对论点句里的 DFO/ES/GA/BO/CI-NEB/CVaR 各加一词注。
- **[MINOR · m4]** [行30] 说明"→"表**组合/数据流经接口**、非 import 依赖（与"内核领域无关"、§附[行307] 呼应），避免读者误读。
- **[MINOR · m5]** 在 κ≈20（约束雅可比条件数）与 31:1（目标景观各向异性）首次出现处点明二者是不同量。
- **[MINOR · m6]** 在[行7]就地枚举三条用户想法（现散落在 §六[行293–295]），并说明想法②实为书目澄清。
- **[MINOR · m7]** 为阶段3–8 各补一句**可证伪的方向性验收**（如"评价数-精度较 PatternSearch 降 X% / 不劣于"），把"算例届时定"从"无阈值"升为"阈值待定但判据明确"。

### NIT
- **[NIT · n1]** 统一链接约定：`src/...` 是仓根相对而 `adr/`/`design/`/`../references/` 是文档相对，二者无法从同一目录同时解析；宜全部改为相对文档自身位置（或全仓根相对）。
- **[NIT · n2]** ADR 编号与阶段序非单调（ADR-0010→阶段3、ADR-0011→阶段2）；加一句"ADR 按创建序编号、非执行序"即免读者困惑。

### FYI（无需动作）
- **[FYI · f1]** 本报告在 skills 工作区评估，eoopt 代码/ADR/参考不在此处 → HF-1 代码态与 HF-2/HF-10 引用可解析性**未逐条外部核实**，仅判内部证据纪律；链接检查器告警≈全为搬运产物。到 eoopt 仓内复评可补此三项。
- **[FYI · f2]** SKILL.md 引用的 `references/templates/quality-report.template.md` 在 skill 目录缺失（仅有 SKILL.md）；本报告按工作流规格手工组织。建议补建模板或修正 SKILL 引用。
- **[FYI · f3]** "不是实现计划"vs 阶段3 已点名类：判为**合理取舍**（细节已下沉 `design/tangent-optimizers-phase3.md`），非缺陷；可在[行11]补一句"阶段3 设计已先行"以消歧。

---

## 8. 交回调用方

```
VERDICT=FAIL total=n/a(stopped-at-hard-gate) blockers=[HF-9]
```

- **FAIL** → 把本严重度清单交回发起流程或 `technical-document-rewriter`；本 skill 不代改目标。
- **复评触发**：补 HF-9 front-matter 后即可 re-run；届时 M1/M2/M3 建议一并处理（成本低、显著抬升 Factual/Reader-fit/Actionability），复评走向大概率 PASS（其余 7 条硬门本轮已过、内容质量高）。
- 本报告对目标文档**只读未改**，自身携可追溯 front-matter（通过其自身 HF-9）。
