"""
从 gallup_180_questions_list.md + gallup_questions_students_association.md
生成完整的 A/B 双侧主题映射 gallup_theme_mapping.json。

策略：
1. 解析 association 中每个主题的题目列表
2. 用主题关键词 + 示例题干，判断主题归属 A 侧或 B 侧
3. 对仍未覆盖的题目，对 A/B 陈述分别做关键词推断
4. 若仅一侧有主题，尝试为对侧推断「配对主题」
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Set, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "research", "测评研究", "data", "processed")

ALL_THEMES = [
    "成就", "统筹", "信仰", "公平", "审慎", "纪律", "专注", "责任", "排难",
    "行动", "统率", "沟通", "竞争", "完美", "自信", "追求", "取悦",
    "适应", "关联", "伯乐", "体谅", "和谐", "包容", "个别", "积极", "交往",
    "分析", "回顾", "前瞻", "理念", "搜集", "思维", "学习", "战略",
]

# 各主题中文关键词（用于陈述文本匹配）
THEME_KEYWORDS: Dict[str, List[str]] = {
    "成就": ["努力工作", "一贯努力", "干劲", "成就", "精力充沛", "持久", "完成任务", "不懈"],
    "统筹": ["同时照顾", "纷繁复杂", "几件事", "协调", "安排"],
    "信仰": ["价值观", "理想", "正直", "哲学", "稳定", "信条"],
    "公平": ["平等对待", "规则", "一视同仁", "公平", "一致"],
    "审慎": ["谨慎", "专家", "正确答案", "风险", "稳妥"],
    "纪律": ["整洁", "计划", "按部就班", "井井有条", "规章制度", "条理"],
    "专注": ["专心", "专注", "目标", "重要的事", "聚焦", "完成的事"],
    "责任": ["责任感", "说到做到", "言而有信", "期限", "负责"],
    "排难": ["解决问题", "故障", "难题", "修复", "排除", "建设性"],
    "行动": ["付诸行动", "作出决定", "立刻", "马上", "先干"],
    "统率": ["领导", "规矩", "控制", "威逼", "指挥"],
    "沟通": ["交谈", "讲话", "倾听", "解释", "表达", "沟通"],
    "竞争": ["第一", "竞赛", "竞争", "力争", "前茅", "赢", "重在参与"],
    "完美": ["完美", "改进", "尽善尽美", "出色", "同行", "有待改进"],
    "自信": ["自信", "实事求是", "可信", "专业化", "不在乎别人", "能干", "不在乎"],
    "追求": ["成就非凡", "很有成就", "重要", "显著", "影响力", "崇拜"],
    "取悦": ["陌生人", "攀谈", "招待", "讨人喜欢", "喜欢我和", "每个人喜欢", "喜欢我"],
    "适应": ["顺其自然", "走一步", "灵活", "随机应变", "当下", "看一步", "统观全局"],
    "关联": ["相连", "巧合", "事出有因", "宏观", "超越自我", "全人类"],
    "伯乐": ["成就感", "发展", "推动", "成功", "认识其价值", "培养", "助人", "帮助", "乐于助人"],
    "体谅": ["设身处地", "感受", "体会", "同情", "理解"],
    "和谐": ["平静", "和谐", "平息", "避免冲突", "融洽"],
    "包容": ["不排斥", "张罗", "一起做事", "接纳", "包括", "与人合作", "合作"],
    "个别": ["个性", "区别", "特点", "个别", "每个人不同"],
    "积极": ["欢乐", "喜悦", "活力", "乐观", "积极", "极好", "感觉极好"],
    "交往": ["知己", "深交", "亲密", "朋友", "Relator", "与人合作"],
    "分析": ["分析", "研究", "调查", "数据", "逻辑", "拆解", "拆开", "原理", "奥妙"],
    "回顾": ["历史", "过去", "起因", "传统", "回顾"],
    "前瞻": ["未来", "前景", "预测", "规划", "远景"],
    "理念": ["创意", "点子", "新想法", "创新", "构思"],
    "搜集": ["收藏", "收集", "信息", "输入", "积累"],
    "思维": ["思考", "哲理", "反思", "智力", "深入想", "个人奋斗", "独立"],
    "学习": ["学习", "求知欲", "成长", "学", "知识"],
    "战略": ["战略", "竞争优势", "规律", "一目了然", "全局"],
}

# 从 association 示例题干人工校验的「主题→题号→侧」硬编码（高置信）
MANUAL_SIDE: Dict[Tuple[str, int], str] = {
    ("专注", 21): "b", ("适应", 21): "a",
    ("前瞻", 2): "a", ("回顾", 2): "b",
    ("取悦", 9): "b", ("沟通", 23): "b", ("体谅", 23): "a",
    ("竞争", 4): "b", ("成就", 5): "b",
    ("完美", 6): "b", ("思维", 6): "a",
    ("个别", 8): "b", ("交往", 14): "a", ("统率", 14): "b",
    ("和谐", 19): "b", ("行动", 20): "b",
    ("关联", 22): "b", ("理念", 163): "b",
    ("学习", 49): "b", ("行动", 50): "a", ("适应", 50): "b",
    ("纪律", 57): "b", ("适应", 57): "a",
    ("公平", 63): "a", ("个别", 63): "b",
    ("分析", 38): "b", ("排难", 136): "b",
    ("完美", 84): "b", ("战略", 85): "a", ("分析", 85): "b",
}


def parse_questions(md_path: str) -> Dict[int, dict]:
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = re.compile(
        r"###\s*第\s*(\d+)\s*题\s*\n+"
        r"\*\*A:\*\*\s*(.+?)\s*\n+"
        r"\*\*B:\*\*\s*(.+?)\s*\n+"
        r"💡\s*\*\*场景提示\*\*：\s*(.+?)"
        r"(?=\n\s*非常认同A|\n+---|\n+###|$)",
        re.DOTALL,
    )
    out = {}
    for num_str, a, b, scenario in pattern.findall(content):
        n = int(num_str.strip())
        out[n] = {"statement_a": a.strip(), "statement_b": b.strip(), "scenario_hint": scenario.strip()}
    return out


def parse_theme_questions(assoc_path: str) -> Dict[str, List[int]]:
    with open(assoc_path, "r", encoding="utf-8") as f:
        content = f.read()
    mapping: Dict[str, List[int]] = {}
    sections = re.split(r"###\s+(.+?)\s*\n", content)
    current_theme = None
    for i, section in enumerate(sections):
        if i == 0:
            continue
        if i % 2 == 1:
            name = section.strip().split()[0]
            if name in ALL_THEMES:
                current_theme = name
        elif current_theme:
            m = re.search(r"题目编号：\s*([\d,\s]+?)(?=\n\s*\n|\*\*示例|\###|$)", section, re.DOTALL)
            if m:
                nums = [int(x.strip()) for x in m.group(1).replace("\n", " ").split(",") if x.strip().isdigit()]
                mapping[current_theme] = nums
    if "适应" not in mapping:
        mapping["适应"] = [21, 50, 57, 74, 79, 91]
    return mapping


def score_text(text: str, theme: str) -> float:
    text = text.replace(" ", "")
    score = 0.0
    for kw in THEME_KEYWORDS.get(theme, []):
        if kw in text:
            score += 1.0 + len(kw) * 0.01
    if theme in text:
        score += 2.0
    return score


def best_themes(text: str, exclude: Set[str], n: int = 2) -> List[str]:
    """返回与文本最相关的 n 个主题；保证至少返回 1 个（即使弱匹配）。"""
    scored = []
    for theme in ALL_THEMES:
        if theme in exclude:
            continue
        s = score_text(text, theme)
        scored.append((s, theme))
    scored.sort(reverse=True)
    if not scored:
        return ["思维"][:n]
    # 若最高分仍为 0，仍取前 n 个（后续由 force_fill 兜底）
    return [t for s, t in scored[:n] if s > 0] or [scored[0][1]]


def assign_theme_to_side(theme: str, qnum: int, q: dict) -> str:
    key = (theme, qnum)
    if key in MANUAL_SIDE:
        return MANUAL_SIDE[key]
    a, b = q["statement_a"], q["statement_b"]
    sa, sb = score_text(a, theme), score_text(b, theme)
    if sa > sb + 0.3:
        return "a"
    if sb > sa + 0.3:
        return "b"
    # 平局：主题名出现在哪侧
    if theme in a and theme not in b:
        return "a"
    if theme in b and theme not in a:
        return "b"
    return "a" if sa >= sb else "b"


def force_fill_side(text: str, other_side_themes: List[str]) -> List[str]:
    """保证每侧至少有一个主题；优先与对侧不同。"""
    exclude = set(other_side_themes)
    picks = best_themes(text, exclude, n=2)
    if picks:
        return picks[:1]
    # 最终兜底：34 主题中择与对侧不同的第一个
    for t in ALL_THEMES:
        if t not in exclude:
            return [t]
    return ["思维"]


def build_mapping() -> Dict[str, dict]:
    md_path = os.path.join(DATA_DIR, "gallup_180_questions_list.md")
    assoc_path = os.path.join(DATA_DIR, "gallup_questions_students_association.md")
    questions = parse_questions(md_path)
    theme_questions = parse_theme_questions(assoc_path)

    q_to_a: Dict[int, List[str]] = defaultdict(list)
    q_to_b: Dict[int, List[str]] = defaultdict(list)

    # Pass 1: association 主题分配
    for theme, nums in theme_questions.items():
        for n in nums:
            if n not in questions:
                continue
            side = assign_theme_to_side(theme, n, questions[n])
            target = q_to_a if side == "a" else q_to_b
            if theme not in target[n]:
                target[n].append(theme)

    # Pass 2: 用陈述 + 场景推断缺失侧
    for n, q in questions.items():
        combined_a = q["statement_a"] + q.get("scenario_hint", "")
        combined_b = q["statement_b"] + q.get("scenario_hint", "")
        if not q_to_a[n]:
            q_to_a[n].extend(best_themes(combined_a, set(q_to_b[n]), n=1))
        if not q_to_b[n]:
            q_to_b[n].extend(best_themes(combined_b, set(q_to_a[n]), n=1))

    # Pass 3: 强制 100% 覆盖 — 每题 A/B 各至少 1 主题
    for n, q in questions.items():
        combined_a = q["statement_a"] + q.get("scenario_hint", "")
        combined_b = q["statement_b"] + q.get("scenario_hint", "")
        if not q_to_a[n]:
            q_to_a[n].extend(force_fill_side(combined_a, q_to_b[n]))
        if not q_to_b[n]:
            q_to_b[n].extend(force_fill_side(combined_b, q_to_a[n]))

    # 去重并输出
    result = {}
    for n in sorted(questions.keys()):
        result[str(n)] = {
            "a": list(dict.fromkeys(q_to_a[n])),
            "b": list(dict.fromkeys(q_to_b[n])),
        }
    return result


def print_stats(mapping: Dict[str, dict], total: int = 180):
    has_a = sum(1 for v in mapping.values() if v.get("a"))
    has_b = sum(1 for v in mapping.values() if v.get("b"))
    both = sum(1 for v in mapping.values() if v.get("a") and v.get("b"))
    print(f"题目总数: {total}")
    print(f"A 侧有映射: {has_a}/{total} ({has_a/total*100:.1f}%)")
    print(f"B 侧有映射: {has_b}/{total} ({has_b/total*100:.1f}%)")
    print(f"A+B 双侧: {both}/{total} ({both/total*100:.1f}%)")
    theme_counts = defaultdict(int)
    for v in mapping.values():
        for t in v.get("a", []):
            theme_counts[t] += 1
    print(f"主题覆盖: {len(theme_counts)}/34")


def main():
    mapping = build_mapping()
    out_path = os.path.join(DATA_DIR, "gallup_theme_mapping.json")
    payload = {
        "_meta": {
            "version": "1.0",
            "description": "Gallup 180 题 A/B 侧 CliftonStrengths 主题映射（启发式 + association 校验）",
            "generator": "backend/scripts/build_gallup_mapping.py",
        },
        "questions": mapping,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"Written: {out_path}")
    print_stats(mapping)
    return 0


if __name__ == "__main__":
    sys.exit(main())
