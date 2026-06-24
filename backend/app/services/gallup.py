from typing import Dict, List
from collections import defaultdict

THEME_DOMAINS = {
    "成就": "Executing", "统筹": "Executing", "信仰": "Executing", "公平": "Executing",
    "审慎": "Executing", "纪律": "Executing", "专注": "Executing", "责任": "Executing", "排难": "Executing",
    "行动": "Influencing", "统率": "Influencing", "沟通": "Influencing", "竞争": "Influencing",
    "完美": "Influencing", "自信": "Influencing", "追求": "Influencing", "取悦": "Influencing",
    "适应": "Relationship Building", "关联": "Relationship Building", "伯乐": "Relationship Building",
    "体谅": "Relationship Building", "和谐": "Relationship Building", "包容": "Relationship Building",
    "个别": "Relationship Building", "积极": "Relationship Building", "交往": "Relationship Building",
    "分析": "Strategic Thinking", "回顾": "Strategic Thinking", "前瞻": "Strategic Thinking",
    "理念": "Strategic Thinking", "搜集": "Strategic Thinking", "思维": "Strategic Thinking",
    "学习": "Strategic Thinking", "战略": "Strategic Thinking",
}

THEME_EN = {
    "成就": "Achiever", "统筹": "Arranger", "信仰": "Belief", "公平": "Consistency",
    "审慎": "Deliberative", "纪律": "Discipline", "专注": "Focus", "责任": "Responsibility", "排难": "Restorative",
    "行动": "Activator", "统率": "Command", "沟通": "Communication", "竞争": "Competition",
    "完美": "Maximizer", "自信": "Self-Assurance", "追求": "Significance", "取悦": "Woo",
    "适应": "Adaptability", "关联": "Connectedness", "伯乐": "Developer",
    "体谅": "Empathy", "和谐": "Harmony", "包容": "Includer",
    "个别": "Individualization", "积极": "Positivity", "交往": "Relator",
    "分析": "Analytical", "回顾": "Context", "前瞻": "Futuristic",
    "理念": "Ideation", "搜集": "Input", "思维": "Intellection",
    "学习": "Learner", "战略": "Strategic",
}

DOMAIN_ZH = {
    "Executing": "执行力",
    "Influencing": "影响力",
    "Relationship Building": "关系建立",
    "Strategic Thinking": "战略思维",
}

def calculate_gallup(
    answers: List[Dict[str, int]],
    a_side_map: Dict[int, List[str]],
    b_side_map: Dict[int, List[str]]
) -> Dict:
    """
    answers: list of {question_num: int, choice: int -2..2}
    choice: -2=very B, -1=somewhat B, 0=neutral, 1=somewhat A, 2=very A
    a_side_map: question_num -> A-side themes (choice added)
    b_side_map: question_num -> B-side themes (choice subtracted)

    计分说明：
    - 原始分 raw_scores：A 侧主题 += choice，B 侧主题 -= choice
    - 归一化分 normalized_scores：按各主题在题目中的出现次数取均值，减少「题量多的主题」偏差
    - Top 5/10 与领域判定基于归一化分
    """
    raw_scores = {theme: 0.0 for theme in THEME_DOMAINS.keys()}
    theme_exposure = {theme: 0 for theme in THEME_DOMAINS.keys()}

    total_questions = len(answers)
    covered_b = 0
    covered_a = 0
    dual_covered = 0

    for ans in answers:
        qn = ans["question_num"]
        choice = ans["choice"]
        a_themes = a_side_map.get(qn) or []
        b_themes = b_side_map.get(qn) or []
        if a_themes:
            covered_a += 1
        if b_themes:
            covered_b += 1
        if a_themes and b_themes:
            dual_covered += 1

        for theme in a_themes:
            raw_scores[theme] += choice
            theme_exposure[theme] += 1
        for theme in b_themes:
            raw_scores[theme] -= choice
            theme_exposure[theme] += 1

    normalized_scores = {}
    for theme, raw in raw_scores.items():
        exp = theme_exposure[theme]
        normalized_scores[theme] = round(raw / exp, 4) if exp > 0 else 0.0

    sorted_themes = sorted(normalized_scores.items(), key=lambda x: -x[1])
    top5 = [t for t, _ in sorted_themes[:5]]
    top10 = [t for t, _ in sorted_themes[:10]]

    domain_count = defaultdict(float)
    for idx, t in enumerate(top10):
        weight = 1.0 / (idx + 1)
        domain_count[THEME_DOMAINS[t]] += weight

    ranked_domains = sorted(
        domain_count.items(),
        key=lambda x: (-x[1], -_domain_raw_score(x[0], normalized_scores)),
    )
    dominant_domain = ranked_domains[0][0]
    secondary_domain = ranked_domains[1][0] if len(ranked_domains) > 1 else None

    # 领域归属置信度：第一名与第二名加权差距
    domain_margin = 0.0
    if len(ranked_domains) >= 2:
        domain_margin = round(ranked_domains[0][1] - ranked_domains[1][1], 3)

    return {
        "scores": raw_scores,
        "normalized_scores": normalized_scores,
        "top5": top5,
        "top10": top10,
        "domain": DOMAIN_ZH[dominant_domain],
        "domain_en": dominant_domain,
        "secondary_domain": DOMAIN_ZH[secondary_domain] if secondary_domain else None,
        "secondary_domain_en": secondary_domain,
        "domain_distribution": {DOMAIN_ZH[k]: round(v, 2) for k, v in domain_count.items()},
        "domain_margin": domain_margin,
        "coverage": {
            "total_questions": total_questions,
            "a_side_covered": covered_a,
            "b_side_covered": covered_b,
            "dual_side_covered": dual_covered,
            "a_side_ratio": round(covered_a / total_questions, 3) if total_questions else 0,
            "b_side_ratio": round(covered_b / total_questions, 3) if total_questions else 0,
            "dual_side_ratio": round(dual_covered / total_questions, 3) if total_questions else 0,
            "themes_scored": sum(1 for e in theme_exposure.values() if e > 0),
        },
    }


def _domain_raw_score(domain_en: str, scores: Dict[str, float]) -> float:
    return sum(score for theme, score in scores.items() if THEME_DOMAINS.get(theme) == domain_en)
