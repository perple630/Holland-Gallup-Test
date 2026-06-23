# 引用格式规范 / Citation Style Guide

## 1. 基本原则 / Basic Principles

- **中文文献**：采用 GB/T 7714-2015 格式。
- **英文文献**：采用 APA 7th edition 格式。
- 优先引用原始研究、同行评审期刊论文与官方技术手册。
- 所有引用须可在 `references/references.bib` 或 `references/notes/` 中追溯。

## 2. 正文引用格式 / In-Text Citation

### 直接引用 / Direct Quote

> “直接引用的原文内容”（Author, Year, p. xx）

### 转述 / Paraphrase

转述内容（Author, Year）。

### 中文文献示例

张三和李四（2020）指出……

### 英文文献示例

Holland (1997) proposed that…
Some studies found moderate test-retest reliability (Asplund et al., 2007; Lopez et al., 2010).

## 3. 参考文献格式 / Reference Format

### 期刊论文（英文）

Author, A. A., & Author, B. B. (Year). Title of article. *Title of Periodical, volume*(issue), page-page. https://doi.org/xx.xxx/yyyy

### 期刊论文（中文）

作者. (年份). 文章标题. *期刊名称*, 卷(期), 页码.

### 技术手册 / Technical Manual

Publisher. (Year). *Title of manual* (Version). Publisher Name.

### 网页 / Webpage

Author or Organization. (Year, Month Day). *Title of page*. Site Name. URL

## 4. 引用管理 / Reference Management

- `references/references.bib` 为 BibTeX 格式主库；
- `references/notes/` 存放每篇文献的阅读笔记；
- 笔记文件名建议：`Author-Year-ShortTitle.md`。

## 5. 证据等级标注 / Evidence Level Tagging

在引用后建议附加证据等级标签，如：

- `[A]`：多项大样本独立研究，方法严谨；
- `[B]`：中等样本研究，方法可接受；
- `[C]`：小样本或方法学薄弱研究；
- `[D]`：专家意见、宣传材料或未经验证案例。

示例：
> CliftonStrengths 的内部一致性在不同研究中较为稳定（Asplund et al., 2007）\[B]。
