# TAG 标注系统规范 / TAG Annotation System Specification

> **版本 / Version**: 1.0  
> **用途 / Purpose**: 对 Holland 职业集群进行多维度标注，使其能够同时承载 RIASEC 兴趣类型、能力要求、工作情境、价值取向、发展路径、CliftonStrengths 优势亲和与潜在张力，从而桥接 Gallup CliftonStrengths 与 Holland RIASEC 两类测评结果。

---

## 1. 设计原则 / Design Principles

### 1.1 多维性（Multidimensionality）
每个职业集群同时标注多个维度，避免单一 RIASEC 代码的信息损失。

### 1.2 层级性（Hierarchy）
TAG 支持从“大类标签”到“具体标签”的多级表达，便于聚合与细化。

### 1.3 兼容性（Compatibility）
- 与 Holland RIASEC 六类型兼容；
- 与 CliftonStrengths 34 主题兼容；
- 保留与未来 O*NET、SOC、ISCO 等职业分类系统对接的扩展空间。

### 1.4 非决定性（Non-Determinism）
TAG 仅描述“关联性”或“亲和性”，不对个体下“适合/不适合”的绝对结论。

### 1.5 可验证性（Verifiability）
每个 TAG 标注应尽可能基于职业描述、O*NET 数据或文献资料，并在条目中注明证据来源或备注。

---

## 2. TAG 维度与编码前缀 / TAG Dimensions and Prefixes

| 维度 / Dimension | 前缀 / Prefix | 说明 / Description | 必填 / Required |
|-----------------|--------------|-------------------|----------------|
| RIASEC 主类型 | `RIASEC-` | 主要 Holland 类型与三码 | 是 |
| 能力倾向 | `ABIL-` | 该集群通常需要的能力倾向 | 是 |
| 工作活动 | `ACT-` | 典型工作任务或活动类型 | 否 |
| 工作情境 | `CTX-` | 工作环境、节奏、组织形态 | 是 |
| 社会互动 | `SOC-` | 人际互动频率与深度 | 否 |
| 价值取向 | `VAL-` | 该集群可能满足的核心价值 | 是 |
| 发展路径 | `PATH-` | 典型职业发展轨迹 | 否 |
| 教育准备 | `EDU-` | 典型教育程度与专业背景 | 否 |
| 优势亲和 | `STR-` | 与 CliftonStrengths 主题的可能亲和 | 是 |
| 潜在张力 | `TENS-` | 该集群可能与其他类型/优势产生冲突的情境 | 是 |

---

## 3. 受控词表 / Controlled Vocabularies

### 3.1 RIASEC- / RIASEC Type

**值格式**：`RIASEC-<primary>-<secondary>-<tertiary>` 或 `RIASEC-<primary>`

| 代码 | 英文 | 中文 |
|-----|------|------|
| R | Realistic | 现实型 |
| I | Investigative | 研究型 |
| A | Artistic | 艺术型 |
| S | Social | 社会型 |
| E | Enterprising | 企业型 |
| C | Conventional | 常规型 |

**示例**：
- `RIASEC-I-R-C`：研究型-现实型-常规型
- `RIASEC-S-A-E`：社会型-艺术型-企业型
- `RIASEC-I`：单一主类型强调

**混合类型标注**：对于新兴职业或边界模糊职业，可使用多个主类型：
- `RIASEC-I+A+E`：研究、艺术、企业三种类型高度混合

### 3.2 ABIL- / Ability Tendency

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| analytical | Analytical thinking | 分析思维 |
| creative | Creative thinking | 创造性思维 |
| social | Social communication | 社交沟通 |
| mechanical | Mechanical reasoning | 机械推理 |
| numerical | Numerical reasoning | 数理推理 |
| verbal | Verbal reasoning | 言语推理 |
| spatial | Spatial reasoning | 空间推理 |
| leadership | Leadership | 领导力 |
| detail | Attention to detail | 细节关注 |
| manual-dexterity | Manual dexterity | 手部灵巧性 |
| empathy | Empathy | 共情能力 |
| persuasion | Persuasion | 说服能力 |
| systems | Systems thinking | 系统思维 |

**示例**：
- `ABIL-analytical`
- `ABIL-creative+social`

### 3.3 ACT- / Work Activity

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| research | Research and analysis | 研究与分析 |
| design | Design and creation | 设计与创造 |
| build | Building and repair | 建造与维修 |
| teach | Teaching and training | 教学与培训 |
| counsel | Counseling and guidance | 咨询与辅导 |
| sell | Selling and persuading | 销售与说服 |
| organize | Organizing and planning | 组织与规划 |
| operate | Operating equipment | 操作设备 |
| communicate | Communicating information | 信息沟通 |
| manage | Managing people/projects | 管理人际/项目 |
| inspect | Inspecting and monitoring | 检查与监控 |
| experiment | Experimenting | 实验 |

### 3.4 CTX- / Work Context

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| office | Office environment | 办公环境 |
| lab | Laboratory | 实验室 |
| field | Field / outdoor | 外勤/户外 |
| remote | Remote work | 远程工作 |
| hybrid | Hybrid work | 混合工作 |
| client-site | Client site | 客户现场 |
| hospital | Hospital / clinic | 医院/诊所 |
| school | School / university | 学校/大学 |
| studio | Studio / workshop | 工作室/车间 |
| startup | Startup / small team | 初创/小团队 |
| corporate | Corporate / large org | 大型企业 |
| public | Public sector | 公共部门 |
| nonprofit | Nonprofit | 非营利组织 |
| freelance | Freelance / self-employed | 自由职业 |
| high-pace | Fast-paced | 快节奏 |
| structured | Highly structured | 高度结构化 |
| flexible | Flexible schedule | 弹性安排 |

### 3.5 SOC- / Social Interaction

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| high | High interaction | 高频互动 |
| moderate | Moderate interaction | 中度互动 |
| low | Low interaction | 低频互动 |
| one-on-one | One-on-one focus | 一对一为主 |
| team | Team-based | 团队为主 |
| public-facing | Public-facing | 面向公众 |
| written | Primarily written communication | 以书面沟通为主 |

### 3.6 VAL- / Value Orientation

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| service | Service to others | 服务他人 |
| achievement | Achievement and recognition | 成就与认可 |
| creativity | Creativity and expression | 创造与表达 |
| autonomy | Autonomy and independence | 自主与独立 |
| security | Security and stability | 安全与稳定 |
| influence | Influence and leadership | 影响与领导 |
| knowledge | Knowledge and learning | 知识与学习 |
| justice | Justice and social impact | 公正与社会影响 |
| precision | Precision and accuracy | 精确与准确 |
| variety | Variety and novelty | 多样与新奇 |

### 3.7 PATH- / Development Path

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| specialist | Specialist / technical expert | 专家路径 |
| managerial | Managerial / administrative | 管理路径 |
| entrepreneurial | Entrepreneurial | 创业路径 |
| academic | Academic / research | 学术路径 |
| freelance | Freelance / portfolio | 自由职业/组合路径 |
| consultant | Consultant / advisor | 咨询顾问路径 |

### 3.8 EDU- / Education Preparation

| 值 / Value | 英文 | 中文 |
|-----------|------|------|
| high-school | High school diploma | 高中毕业 |
| associate | Associate degree / vocational | 大专/职业培训 |
| bachelor | Bachelor's degree | 本科学位 |
| master | Master's degree | 硕士学位 |
| doctoral | Doctoral / professional degree | 博士/专业学位 |
| certification | Professional certification | 专业认证 |
| self-taught | Self-taught / portfolio-based | 自学/作品导向 |

### 3.9 STR- / CliftonStrengths Affinity

**值格式**：`STR-<theme-name>`

直接引用 34 个主题名称。可多个组合，表示不同优势主题与该集群的亲和。

| 主题示例 | 与 RIASEC / 职业集群的亲和说明 |
|---------|-------------------------------|
| `STR-achiever` | 高目标导向、执行型集群（C/E/R） |
| `STR-relator` | 一对一深度关系型集群（S/counseling） |
| `STR-woo` | 社交启动、外向型集群（E/sales） |
| `STR-analytical` | 数据分析、研究型集群（I） |
| `STR-ideation` | 创意、概念设计型集群（A） |
| `STR-strategic` | 战略规划、咨询型集群（I/E） |
| `STR-deliberative` | 风险管理、合规型集群（C） |
| `STR-developer` | 教育、辅导、人才培养型集群（S） |
| `STR-command` | 领导、危机管理型集群（E/managerial） |
| `STR-individualization` | 个性化服务、人才发展型集群（S/HR） |

**完整 34 主题清单**：
Achiever, Activator, Adaptability, Analytical, Arranger, Belief, Command, Communication, Competition, Connectedness, Consistency, Context, Deliberative, Developer, Discipline, Empathy, Focus, Futuristic, Harmony, Ideation, Includer, Individualization, Input, Intellection, Learner, Maximizer, Positivity, Relator, Responsibility, Restorative, Self-Assurance, Significance, Strategic, Woo.

### 3.10 TENS- / Potential Tension

**值格式**：`TENS-<description>`

用于描述该职业集群内部或与其他类型/优势主题之间可能存在的张力。建议使用简短描述，如：

- `TENS-high-structure-vs-creativity`：高度结构化要求与创造性需求之间的张力
- `TENS-social-demand-vs-autonomy`：高社会互动需求与个体自主需求之间的张力
- `TENS-detail-vs-big-picture`：细节处理与全局视野之间的张力
- `TENS-stability-vs-change`：稳定性偏好与快速变化环境之间的张力

---

## 4. 标注格式 / Annotation Format

### 4.1 Markdown 条目格式

```markdown
### 职业集群：[中文名] / [English Name]
- **RIASEC**: <code>
- **ABIL-**: <value1>, <value2>, ...
- **ACT-**: <value1>, <value2>, ...
- **CTX-**: <value1>, <value2>, ...
- **SOC-**: <value>
- **VAL-**: <value1>, <value2>, ...
- **PATH-**: <value1>, <value2>, ...
- **EDU-**: <value>
- **STR-**: <theme1>, <theme2>, ...
- **TENS-**: <description>
- **来源 / Sources**: <O*NET code or literature>
- **证据备注 / Evidence Note**: <level + note>
```

### 4.2 CSV 表格格式

| cluster_name_en | cluster_name_cn | riasec | abil | act | ctx | soc | val | path | edu | str | tens | sources | evidence_note |
|----------------|----------------|--------|------|-----|-----|-----|-----|------|-----|-----|------|---------|---------------|

### 4.3 JSON 格式

```json
{
  "cluster_name": {
    "en": "Clinical Psychologist",
    "cn": "临床心理学家"
  },
  "riasec": "I-S-A",
  "abil": ["analytical", "empathy", "verbal"],
  "act": ["research", "counsel", "communicate"],
  "ctx": ["office", "hospital", "one-on-one"],
  "soc": "one-on-one",
  "val": ["service", "knowledge", "autonomy"],
  "path": ["specialist", "academic", "consultant"],
  "edu": "doctoral",
  "str": ["relator", "developer", "intellection", "empathy", "learner"],
  "tens": ["high-emotional-demand + need-boundaries", "research-rigor vs clinical-flexibility"],
  "sources": ["O*NET-SOC 19-3033.00"],
  "evidence_note": "基于职业描述与理论映射；未经实证验证 [C]"
}
```

---

## 5. 标注规则 / Annotation Rules

### 5.1 多标签原则
- 一个集群可拥有多个 `ABIL-`、`ACT-`、`CTX-`、`VAL-`、`PATH-`、`STR-` 标签。
- `RIASEC-` 通常以三码形式呈现；若职业边界模糊，可用 `+` 连接多个主类型。

### 5.2 证据等级标注
每个条目末尾须添加 `Evidence Note`，标注证据等级：
- `[A]`：基于 O*NET 数据、官方手册或多项独立研究；
- `[B]`：基于职业描述分析或单一独立研究；
- `[C]`：基于理论映射或专家判断；
- `[D]`：基于推测或常见叙述。

### 5.3 避免绝对化
- 使用“可能亲和”“常需要”“倾向于”等措辞，避免“必须”“只适合”等绝对化表达。
- `STR-` 标签表示该优势主题与该职业集群存在理论亲和，不表示只有具备该主题者才能胜任。

### 5.4 动态更新
- 新兴职业或快速变化的职业应定期复核 TAG 标注。
- 对存在争议或证据不足的标注，使用 `TENS-` 或 `Evidence Note` 说明。

---

## 6. 与 CliftonStrengths 的桥接逻辑 / Bridging Logic with CliftonStrengths

### 6.1 桥接层级
TAG 系统通过以下层级将 CliftonStrengths 与 RIASEC 关联：

```
CliftonStrengths 主题
    ↓ 映射到
职业集群的 STR- 标签
    ↓ 共享
同一职业集群的 RIASEC-、ABIL-、CTX-、VAL- 等标签
    ↓ 形成
兴趣-优势整合描述
```

### 6.2 桥接示例

**示例 1：数据分析师（Data Analyst）**
- `RIASEC-I-C-R`
- `ABIL-analytical, numerical, systems`
- `STR-analytical, learner, input, focus`
- `TENS-detail-vs-big-picture`

**一个学生如果**：
- Holland：I 高、C 高
- CliftonStrengths：Analytical、Learner、Input 靠前
→ 该组合在“数据分析师”集群上呈现较强的亲和性，但需关注其是否能处理细节与全局视野之间的张力。

**示例 2：人力资源发展专员（HR Development Specialist）**
- `RIASEC-S-E-A`
- `ABIL-social, empathy, leadership`
- `STR-developer, relator, individualization, empathy`
- `TENS-social-demand-vs-autonomy`

**一个学生如果**：
- Holland：S 高、E 中高
- CliftonStrengths：Developer、Relator、Empathy 靠前
→ 该组合在人际发展与培训类集群上呈现亲和，但需评估其是否愿意承受高社会互动需求。

---

## 7. 质量控制 / Quality Control

### 7.1 标注者自检清单
1. 是否每个必填维度都已标注？
2. `RIASEC-` 是否与 O*NET 或主流职业描述一致？
3. `STR-` 标注是否基于主题的行为定义，而非主观联想？
4. 是否标注了证据等级？
5. 是否识别了至少一个潜在张力？

### 7.2 复核流程
- 第一轮：由标注者完成初稿；
- 第二轮：由第二人依据受控词表与职业描述进行复核；
- 第三轮：依据整合设计思路进行一致性检查。

---

## 8. 版本记录 / Version History

| 版本 | 日期 | 变更说明 |
|-----|------|---------|
| 1.0 | 2026-06-17 | 初始版本，定义 10 个 TAG 维度与受控词表 |

---

*文件位置 / File Location*: `03-tag-system/tag-schema.md`  
*创建日期 / Created*: 2026-06-17
