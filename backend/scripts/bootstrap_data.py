"""从 research 目录下的 Markdown 生成 import_data 所需的 JSON 文件（若缺失）。"""
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "research", "测评研究", "data", "processed")

DOMAIN_MAP = {
    "Executing 执行力": "Executing",
    "Influencing 影响力": "Influencing",
    "Relationship Building 关系建立": "Relationship Building",
    "Strategic Thinking 战略思维": "Strategic Thinking",
}

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


def ensure_holland_scenarios():
    path = os.path.join(DATA_DIR, "holland_scenarios.json")
    if os.path.exists(path):
        return
    scenarios = [
        f"请结合你的学习与生活经历，想象第 {i} 题描述的活动情境，选择最符合你真实偏好的程度。"
        for i in range(1, 61)
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)
    print(f"Created {path}")


def ensure_gallup_missing_mapping():
    path = os.path.join(DATA_DIR, "gallup_missing_mapping.json")
    if os.path.exists(path):
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump({}, f)
    print(f"Created empty {path}")


def ensure_career_mapping():
    path = os.path.join(DATA_DIR, "career_major_mapping.json")
    if os.path.exists(path):
        return
    md_path = os.path.join(DATA_DIR, "career_major_mapping.md")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    items = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or line.startswith("| 职业名称") or line.startswith("|---"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 6:
            continue
        name, riasec_raw, domain_raw, majors_raw, evidence, desc = cols[:6]
        riasec_match = re.match(r"([RIASEC])", riasec_raw)
        if not riasec_match:
            continue
        domain_en = DOMAIN_MAP.get(domain_raw.strip())
        if not domain_en:
            for key, val in DOMAIN_MAP.items():
                if key.split()[0] in domain_raw or val in domain_raw:
                    domain_en = val
                    break
        if not domain_en:
            continue
        majors = [m.strip() for m in re.split(r"[、,，]", majors_raw) if m.strip()]
        items.append({
            "career_name": name,
            "riasec_primary": riasec_match.group(1),
            "cs_domain": domain_en,
            "related_majors": majors,
            "evidence_level": evidence,
            "description": desc,
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    print(f"Created {path} ({len(items)} careers)")


def ensure_theme_materials():
    path = os.path.join(DATA_DIR, "cliftonstrengths_report_materials.json")
    if os.path.exists(path):
        return
    desc_path = os.path.join(DATA_DIR, "cliftonstrengths_theme_descriptions.md")
    descriptions = {}
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            content = f.read()
        for m in re.finditer(r"##\s+(\S+)\s*\n+\*\*标准定义\*\*[：:]\s*(.+?)(?=\n\n|\n##|\Z)", content, re.DOTALL):
            descriptions[m.group(1).strip()] = m.group(2).strip()

    data = {}
    for theme, domain in THEME_DOMAINS.items():
        data[theme] = {
            "domain": domain,
            "standard_definition": descriptions.get(theme, f"{theme} 主题的标准定义待补充。"),
            "feature": "",
            "description": "",
            "application": "",
            "blind_spots": "",
        }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Created {path} ({len(data)} themes)")


def main():
    if not os.path.isdir(DATA_DIR):
        raise SystemExit(f"Data directory not found: {DATA_DIR}")
    ensure_holland_scenarios()
    ensure_gallup_missing_mapping()
    ensure_career_mapping()
    ensure_theme_materials()
    print("Bootstrap data files ready.")


if __name__ == "__main__":
    main()
