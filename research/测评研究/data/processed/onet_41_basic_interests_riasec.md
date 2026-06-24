# O*NET 41 个基本兴趣领域（Specific Interest Areas）与 RIASEC 对照表

> **版本 / Version**：1.0  
> **数据来源 / Source**：O*NET 30.3，`Specific Interest Areas to Career Interest Types`（源自 CABIN 量表，Su et al., 2019）  
> **原始文件**：`../raw/onet_specific_interest_areas_to_riasec.txt`  
> **方法说明**：National Center for O*NET Development, *Updating Vocational Interests Information for the O*NET Content Model* (2023)  
> **覆盖范围**：41 个基本兴趣领域；约 **891** 个 O*NET 数据级职业可与之关联（O*NET 30.3 发布说明）

---

## 使用说明

### 与 Holland 三码的关系（重要）

　　**41 个基本兴趣领域并不直接对应某个固定的 Holland 三码**（如 `ESR`、`RIC`）。三码是个体测评后得到的**三个 RIASEC 字母排序**；基本兴趣领域则是 O*NET 在六型之下划分的**更细兴趣维度**。

　　对应逻辑如下：

1. **每个基本兴趣领域** → 映射到 **1 个或 2 个** RIASEC 一般兴趣类型（R/I/A/S/E/C）。
2. **个体的 Holland 三码**（如 `ESR`）→ 表示第一、第二、第三兴趣类型分别为 E、S、R。
3. **筛选与该个体相关的基本兴趣**：取出所有「关联 RIASEC 类型 ∈ {E, S, R}」的领域（共通常 **15–25 个**，视三码组合而定）。
4. **双关联领域（12 个）**：若某领域同时关联三码中的**两个**字母（如 Athletics 关联 R+E，而三码为 `REA`），可视为**尤其契合**的交叉兴趣面。

　　示例（三码 `ESR`）：

| 字母 | 可纳入的基本兴趣领域（节选） |
|------|------------------------------|
| **E**（第一） | Sales、Management/Administration、Business Initiatives、Public Speaking、Law… |
| **S**（第二） | Teaching/Education、Social Service、Personal Service、Human Resources… |
| **R**（第三） | Engineering、Athletics、Mechanics/Electronics、Agriculture… |
| **E+S 双关联** | Professional Advising、Religious Activities |
| **R+E 双关联** | **Athletics**（运动员、教练、裁判等） |
| **R+S 双关联** | Animal Service |

### 命名变更（O*NET 30.3）

　　O*NET 30.3 起，原称 **Basic Interests** 在数据字典中更名为 **Specific Interest Areas**；与 RIASEC 的映射文件同步更名为 `Specific Interest Areas to Career Interest Types`，内容结构与 30.2 的 `Basic Interests to RIASEC` 一致（**53 行** = 41 领域 + 12 条双关联重复行）。

---

## 完整对照表（41 项）

| 序号 | Element ID | 英文名称 | 中文名称 | 关联 RIASEC | RIASEC 中文 | 双关联 |
|------|------------|----------|----------|-------------|-------------|--------|
| 1 | 1.B.3.a | Mechanics/Electronics | 机械/电子 | R | 现实型 | |
| 2 | 1.B.3.b | Construction/Woodwork | 建筑/木工 | R | 现实型 | |
| 3 | 1.B.3.c | Transportation/Machine Operation | 运输/机械操作 | R | 现实型 | |
| 4 | 1.B.3.d | Physical/Manual Labor | 体力劳动 | R | 现实型 | |
| 5 | 1.B.3.e | Protective Service | 安保/执法 | R | 现实型 | |
| 6 | 1.B.3.f | Agriculture | 农业 | R | 现实型 | |
| 7 | 1.B.3.g | Nature/Outdoors | 自然/户外 | R | 现实型 | |
| 8 | 1.B.3.h | Animal Service | 动物服务 | R, S | 现实型、社会型 | ★ |
| 9 | 1.B.3.i | Athletics | 体育运动 | R, E | 现实型、企业型 | ★ |
| 10 | 1.B.3.j | Engineering | 工程 | R | 现实型 | |
| 11 | 1.B.3.k | Physical Science | 物理科学 | I | 研究型 | |
| 12 | 1.B.3.l | Life Science | 生命科学 | I | 研究型 | |
| 13 | 1.B.3.m | Medical Science | 医学科学 | I | 研究型 | |
| 14 | 1.B.3.n | Social Science | 社会科学 | I, S | 研究型、社会型 | ★ |
| 15 | 1.B.3.o | Humanities | 人文学科 | I, A | 研究型、艺术型 | ★ |
| 16 | 1.B.3.p | Mathematics/Statistics | 数学/统计 | I, C | 研究型、常规型 | ★ |
| 17 | 1.B.3.q | Information Technology | 信息技术 | C | 常规型 | |
| 18 | 1.B.3.r | Visual Arts | 视觉艺术 | A | 艺术型 | |
| 19 | 1.B.3.s | Applied Arts and Design | 应用艺术与设计 | A | 艺术型 | |
| 20 | 1.B.3.t | Performing Arts | 表演艺术 | A | 艺术型 | |
| 21 | 1.B.3.u | Music | 音乐 | A | 艺术型 | |
| 22 | 1.B.3.v | Creative Writing | 创意写作 | A | 艺术型 | |
| 23 | 1.B.3.w | Media | 媒体 | A | 艺术型 | |
| 24 | 1.B.3.x | Culinary Art | 烹饪艺术 | A, S | 艺术型、社会型 | ★ |
| 25 | 1.B.3.y | Teaching/Education | 教学/教育 | S | 社会型 | |
| 26 | 1.B.3.z | Social Service | 社会服务 | S | 社会型 | |
| 27 | 1.B.3.aa | Health Care Service | 医疗保健服务 | I, S | 研究型、社会型 | ★ |
| 28 | 1.B.3.ab | Religious Activities | 宗教活动 | E, S | 企业型、社会型 | ★ |
| 29 | 1.B.3.ac | Personal Service | 个人服务 | S | 社会型 | |
| 30 | 1.B.3.ad | Professional Advising | 专业咨询/指导 | E, S | 企业型、社会型 | ★ |
| 31 | 1.B.3.ae | Business Initiatives | 商业拓展 | E | 企业型 | |
| 32 | 1.B.3.af | Sales | 销售 | E | 企业型 | |
| 33 | 1.B.3.ag | Marketing/Advertising | 营销/广告 | E, A | 企业型、艺术型 | ★ |
| 34 | 1.B.3.ah | Finance | 金融 | E, C | 企业型、常规型 | ★ |
| 35 | 1.B.3.ai | Accounting | 会计 | C | 常规型 | |
| 36 | 1.B.3.aj | Human Resources | 人力资源 | S, C | 社会型、常规型 | ★ |
| 37 | 1.B.3.ak | Office Work | 办公室事务 | C | 常规型 | |
| 38 | 1.B.3.al | Management/Administration | 管理/行政 | E | 企业型 | |
| 39 | 1.B.3.am | Public Speaking | 公开演讲 | E | 企业型 | |
| 40 | 1.B.3.an | Politics | 政治 | E | 企业型 | |
| 41 | 1.B.3.ao | Law | 法律 | E | 企业型 | |

★ = 该领域在 O*NET 映射中关联 **2 个** RIASEC 类型（共 12 项，见下节）。

---

## 按 RIASEC 类型索引

　　下列为「该 RIASEC 类型下可探索的基本兴趣领域」清单。双关联领域在多个字母下重复出现。

### R 现实型（10 项）

Mechanics/Electronics · Construction/Woodwork · Transportation/Machine Operation · Physical/Manual Labor · Protective Service · Agriculture · Nature/Outdoors · Animal Service ★ · Athletics ★ · Engineering

### I 研究型（8 项）

Physical Science · Life Science · Medical Science · Social Science ★ · Humanities ★ · Mathematics/Statistics ★ · Health Care Service ★

### A 艺术型（9 项）

Humanities ★ · Visual Arts · Applied Arts and Design · Performing Arts · Music · Creative Writing · Media · Culinary Art ★ · Marketing/Advertising ★

### S 社会型（12 项）

Animal Service ★ · Social Science ★ · Culinary Art ★ · Teaching/Education · Social Service · Health Care Service ★ · Religious Activities ★ · Personal Service · Professional Advising ★ · Human Resources ★

### E 企业型（14 项）

Athletics ★ · Religious Activities ★ · Professional Advising ★ · Business Initiatives · Sales · Marketing/Advertising ★ · Finance ★ · Management/Administration · Public Speaking · Politics · Law

### C 常规型（7 项）

Mathematics/Statistics ★ · Information Technology · Finance ★ · Accounting · Human Resources ★ · Office Work

---

## 12 个双关联领域明细

　　依据 Su et al. (2019) CABIN 量表的 CFA/ESEM 结果；O*NET 对交叉负荷 >.30 的领域赋予双 RIASEC 关联（少数为概念相关性补充）。

| 基本兴趣领域 | 关联 RIASEC | 典型职业举例（O*NET） |
|-------------|-------------|----------------------|
| Animal Service | R + S | 动物饲养员、动物训练师、兽医 |
| **Athletics** | **R + E** | **职业运动员、教练、裁判、运动训练师** |
| Social Science | I + S | 社会学家、心理咨询师、经济学家 |
| Humanities | I + A | 历史学家、人类学家、文学教师 |
| Mathematics/Statistics | I + C | 数学家、统计学家、数据科学家 |
| Health Care Service | I + S | 护士、医生、牙医、护理助理 |
| Culinary Art | A + S | 厨师、烘焙师、私厨 |
| Religious Activities | E + S | 神职人员、宗教教育负责人 |
| Professional Advising | E + S | 升学/职业咨询师、培训师、艺人经纪 |
| Marketing/Advertising | E + A | 营销经理、公关、广告经理 |
| Finance | E + C | 金融分析师、财务经理、理财顾问 |
| Human Resources | S + C | HR 专员、HR 经理、薪酬分析师 |

---

## Holland 三码 → 基本兴趣领域：查阅方法

　　给定个体 Holland 三码 `L₁L₂L₃`（如 `ESR`），建议按以下优先级阅读基本兴趣领域：

| 优先级 | 规则 | 示例（`ESR`） |
|--------|------|---------------|
| **P1 主导交叉** | 仅关联 `L₁` 的领域 | E：Sales、Management、Law… |
| **P2 次要交叉** | 关联 `L₂` 的领域，或双关联含 `L₁`+`L₂` | S：Teaching、Social Service…；E+S：Professional Advising |
| **P3 第三码** | 关联 `L₃` 的领域，或双关联含 `L₁`+`L₃` | R：Engineering、Agriculture…；R+E：**Athletics** |
| **P4 双关联加分** | 同时命中三码中任意两个字母 | Athletics（R+E）、Animal Service（R+S）|

　　**注意**：上表为**探索性索引**，不是排除法——未列出的领域仍可能通过具体职业路径与个体契合；基本兴趣领域亦不能替代正式测评与真实体验验证。

### 三码字母组合 → 双关联领域速查

| 若三码包含… | 尤其值得关注的双关联领域 |
|------------|-------------------------|
| R + S | Animal Service |
| R + E | **Athletics** |
| I + S | Social Science、Health Care Service |
| I + A | Humanities |
| I + C | Mathematics/Statistics |
| A + S | Culinary Art |
| E + S | Religious Activities、Professional Advising |
| E + A | Marketing/Advertising |
| E + C | Finance |
| S + C | Human Resources |

---

## 各 RIASEC 类型下单关联领域数量

| RIASEC | 仅单关联 | 参与双关联 | 合计可探索项（含双关联重复计数） |
|--------|---------|-----------|--------------------------------|
| R | 8 | 2 | 10 |
| I | 3 | 5 | 8 |
| A | 6 | 3 | 9 |
| S | 4 | 8 | 12 |
| E | 7 | 7 | 14 |
| C | 3 | 4 | 7 |

---

## 与本项目的关系

| 本项目组件 | 与 41 基本兴趣领域的关系 |
|-----------|-------------------------|
| Holland 60 题测评 | 产出六型得分与三码；**未**直接测量 41 领域 |
| 报告交叉矩阵（6×4） | 当前用 78 条具体职业填充；**尚未**接入 41 领域 |
| `career_major_mapping`（78 条） | 可逐步为每条职业标注对应的 Basic Interest ID |
| TAG 试点集群（20 个） | 粒度介于 6 型与 41 领域之间，可建立映射表 |

　　若将报告矩阵改为「集群/方向」呈现，**41 个基本兴趣领域**是 O*NET 公开资料中最可直接引用的中层参照系。

---

## 参考文献与链接

- O*NET Resource Center. (2026). *Specific Interest Areas to Career Interest Types* (O*NET 30.3). https://www.onetcenter.org/dictionary/30.3/text/specific_interest_areas_to_career_interest_types.html
- Putka, D. J., Lewis, P., & Rounds, J. (2023). *Updating Vocational Interests Information for the O*NET Content Model*. https://www.onetcenter.org/reports/Voc_Interests.html
- Su, R., Rounds, J., & Armstrong, P. I. (2019). Development and validation of the Comprehensive Assessment of Basic Interests (CABIN). *Journal of Counseling Psychology*, *66*(5), 698–713.

---

*文件位置*：`research/测评研究/data/processed/onet_41_basic_interests_riasec.md`  
*创建日期*：2026-06-23
