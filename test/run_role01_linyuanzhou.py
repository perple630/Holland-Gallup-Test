"""
角色一：林远舟 · 工程结构师
假设验证性研究 — 代入角色完成 Holland + Gallup 测评，写入数据库并导出报告。

角色画像要点：
- 结构工程师，高度分析型，C 极高，E 极低，社会称许性极低
- 预期 Holland：R/I/C 主导（RIC 或 IRC）
- 预期 Gallup：执行力 + 战略思维（分析、审慎、专注、纪律、责任、排难）
"""
from __future__ import annotations

import json
import os
import random
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

import requests

BASE = os.environ.get("ASSESSMENT_API_BASE", "http://127.0.0.1:8000")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "roles", "01_林远舟")

ROLE = {
    "username": "role01_linyuanzhou",
    "password": "role123456",
    "display_name": "林远舟",
    "label": "角色一 · 工程结构师",
}

# Holland 兴趣倾向（1-5）：结构工程 + 分析 + 规范，低社交/低艺术/低企业
HOLLAND_BIAS = {
    "R": 4.3,  # 动手、结构、工具
    "I": 4.4,  # 分析、数理、研究
    "C": 4.2,  # 精确、流程、安全
    "S": 2.0,  # 人际沟通弱
    "E": 1.8,  # 低外倾、不热衷领导推销
    "A": 1.6,  # 不认同「创新艺术」式自我描述
}

# Gallup 主题（中文，与题库 theme_tags 一致）
GALLUP_FAVORED = {
    "分析", "审慎", "专注", "纪律", "责任", "排难", "公平", "学习", "战略", "思维",
}
GALLUP_DISFAVORED = {
    "取悦", "沟通", "和谐", "积极", "适应", "行动", "统率", "竞争", "追求", "自信",
    "伯乐", "体谅", "交往", "包容", "个别", "关联", "理念", "前瞻",
}

# 社会称许性极低：高分上限 4，Gallup 极端值少用 ±2
STRICT_SCORING = True
RANDOM_SEED = 20260323


def _api(method: str, path: str, token: Optional[str] = None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"{BASE}{path}"
    return requests.request(method, url, headers=headers, timeout=60, **kwargs)


def ensure_user() -> dict:
    payload = {"username": ROLE["username"], "password": ROLE["password"], "role": "student"}
    r = _api("POST", "/api/auth/login", json=payload)
    if r.status_code == 200:
        return r.json()
    r = _api(
        "POST",
        "/api/auth/register",
        json={**payload, "display_name": ROLE["display_name"]},
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"注册失败: {r.status_code} {r.text}")
    r = _api("POST", "/api/auth/login", json=payload)
    r.raise_for_status()
    return r.json()


def get_questions(token: str, assessment_type: str) -> List[dict]:
    r = _api("GET", "/api/assessments/questions", token, params={"assessment_type": assessment_type})
    r.raise_for_status()
    return r.json()


def make_holland_answers(questions: List[dict]) -> List[dict]:
    answers = []
    for q in questions:
        themes = [t.upper() for t in (q.get("theme_tags") or [])]
        target = 3.0
        for t, score in HOLLAND_BIAS.items():
            if t in themes:
                target = score
                break
        noise = random.gauss(0, 0.35)
        val = round(target + noise)
        if STRICT_SCORING:
            val = min(val, 4)  # 绝不轻易给满分
        val = max(1, min(5, val))
        answers.append({"question_num": q["question_num"], "score": val})
    return answers


def _theme_weight(themes: Set[str], favored: Set[str], disfavored: Set[str]) -> float:
    w = 0.0
    for t in themes:
        if t in favored:
            w += 1.0
        if t in disfavored:
            w -= 1.0
    return w


def make_gallup_answers(questions: List[dict]) -> List[dict]:
    answers = []
    for q in questions:
        a_themes = set(q.get("theme_tags") or [])
        b_themes = set(q.get("b_side_themes") or [])

        a_w = _theme_weight(a_themes, GALLUP_FAVORED, GALLUP_DISFAVORED)
        b_w = _theme_weight(b_themes, GALLUP_FAVORED, GALLUP_DISFAVORED)

        stmt_a = (q.get("statement_a") or "").lower()
        stmt_b = (q.get("statement_b") or "").lower()

        # 语句级启发：林远舟对社交/称许/模糊创新陈述倾向否定 A
        social_a = any(k in stmt_a for k in ("喜欢", "乐于", "想要每个人", "交友", "聚会", "受欢迎"))
        analytic_b = any(k in stmt_b for k in ("拆开", "原理", "分析", "研究", "精确", "第一"))
        if social_a and analytic_b:
            a_w -= 0.8
            b_w += 0.5
        if "创新" in stmt_a and "第一" not in stmt_a:
            a_w -= 0.4  # 「优化节点不算创新」

        diff = a_w - b_w + random.gauss(0, 0.25)
        if diff > 0.6:
            base = 2 if not STRICT_SCORING else 1
        elif diff > 0.15:
            base = 1
        elif diff < -0.6:
            base = -2 if not STRICT_SCORING else -1
        elif diff < -0.15:
            base = -1
        else:
            base = 0

        choice = max(-2, min(2, base))
        answers.append({"question_num": q["question_num"], "choice": choice})
    return answers


def submit_holland(token: str, answers: List[dict]) -> dict:
    r = _api("POST", "/api/assessments/holland", token, json={"answers": answers})
    if r.status_code != 200:
        raise RuntimeError(f"Holland 提交失败: {r.status_code} {r.text}")
    return r.json()


def submit_gallup(token: str, answers: List[dict]) -> dict:
    r = _api("POST", "/api/assessments/gallup", token, json={"answers": answers})
    if r.status_code != 200:
        raise RuntimeError(f"Gallup 提交失败: {r.status_code} {r.text}")
    return r.json()


def get_student_report(token: str) -> dict:
    r = _api("GET", "/api/reports/student", token)
    r.raise_for_status()
    return r.json()


def get_professional_report(teacher_token: str, student_id: str) -> dict:
    r = _api("GET", f"/api/reports/professional/{student_id}", teacher_token)
    r.raise_for_status()
    return r.json()


def teacher_login() -> dict:
    r = _api(
        "POST",
        "/api/auth/login",
        json={"username": "teacher", "password": "teacher123", "role": "teacher"},
    )
    r.raise_for_status()
    return r.json()


def save_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(path: str, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def write_rationale(progress: dict, student_report: dict) -> str:
    holland_code = progress.get("holland_code", "")
    gallup_domain = progress.get("gallup_domain", "")
    top5 = progress.get("gallup_top5") or []
    return f"""# 角色一 · 林远舟 — 作答映射说明

> 生成时间：{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

## 角色摘要

- 42 岁男，注册结构工程师；高度分析型，C 极高 (95)，E 极低 (25)，社会称许性极低
- 作答风格：严格、不迎合，能力/兴趣题不轻易给极端高分

## Holland 映射策略

| 类型 | 目标倾向 | 依据 |
|------|---------|------|
| R | 高 (≈4) | 结构工程、动手、工具与实物 |
| I | 高 (≈4) | 空间数理推理、分析验证 |
| C | 高 (≈4) | 规范、精确、安全边际 |
| S/E/A | 低 (≈1.6–2) | 人际与语言弱，不认同艺术/推销型自我描述 |

**实测三码**：`{holland_code}`

## Gallup 映射策略

- ** favored 主题**：分析、审慎、专注、纪律、责任、排难、公平、学习、战略、思维
- ** disfavored 主题**：取悦、沟通、和谐、积极、适应、行动、统率、竞争等社交/冲动类

**实测主导领域**：{gallup_domain}
**实测 Top 5**：{", ".join(top5) if top5 else "（无）"}

## 报告摘要

- 推荐职业数（学生版）：{len(student_report.get("careers") or [])}
- 数据质量提示：见 `student_report.json` → `data_quality_notes`

## 账号信息

- 用户名：`{ROLE["username"]}`
- 密码：`{ROLE["password"]}`
- 显示名：{ROLE["display_name"]}
"""


def main():
    random.seed(RANDOM_SEED)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"=== {ROLE['label']} ({ROLE['display_name']}) ===")
    user = ensure_user()
    token = user["access_token"]
    user_id = user["user_id"]
    print(f"用户 ID: {user_id}")

    holland_qs = get_questions(token, "holland")
    gallup_qs = get_questions(token, "gallup")
    print(f"题目加载：Holland {len(holland_qs)}，Gallup {len(gallup_qs)}")

    hol_answers = make_holland_answers(holland_qs)
    gal_answers = make_gallup_answers(gallup_qs)

    hol_result = submit_holland(token, hol_answers)
    gal_result = submit_gallup(token, gal_answers)
    print(f"Holland 三码: {hol_result.get('holland_code')}")
    print(f"Gallup 领域: {gal_result.get('gallup_domain')}, Top5: {gal_result.get('gallup_top5')}")

    student_report = get_student_report(token)
    teacher = teacher_login()
    professional_report = get_professional_report(teacher["access_token"], user_id)

    save_json(os.path.join(OUTPUT_DIR, "answers_holland.json"), {"answers": hol_answers})
    save_json(os.path.join(OUTPUT_DIR, "answers_gallup.json"), {"answers": gal_answers})
    save_json(os.path.join(OUTPUT_DIR, "assessment_result.json"), {
        "user_id": user_id,
        "username": ROLE["username"],
        "display_name": ROLE["display_name"],
        "holland_result": hol_result,
        "gallup_result": gal_result,
    })
    save_json(os.path.join(OUTPUT_DIR, "student_report.json"), student_report)
    save_json(os.path.join(OUTPUT_DIR, "professional_report.json"), professional_report)

    if student_report.get("report_html"):
        save_text(os.path.join(OUTPUT_DIR, "student_report.html"), student_report["report_html"])
    if professional_report.get("report_html"):
        save_text(os.path.join(OUTPUT_DIR, "professional_report.html"), professional_report["report_html"])

    rationale = write_rationale(gal_result, student_report)
    save_text(os.path.join(OUTPUT_DIR, "role_rationale.md"), rationale)

    summary = {
        "role": ROLE["label"],
        "display_name": ROLE["display_name"],
        "user_id": user_id,
        "username": ROLE["username"],
        "holland_code": hol_result.get("holland_code"),
        "holland_scores": hol_result.get("holland_scores"),
        "gallup_domain": gal_result.get("gallup_domain"),
        "gallup_top5": gal_result.get("gallup_top5"),
        "gallup_secondary_domain": gal_result.get("gallup_secondary_domain"),
        "careers": [c.get("career_name") for c in (student_report.get("careers") or [])],
        "tension": professional_report.get("tension"),
        "output_dir": OUTPUT_DIR,
    }
    save_json(os.path.join(OUTPUT_DIR, "summary.json"), summary)

    print("\n=== 完成 ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n输出目录: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except requests.RequestException as e:
        print(f"API 请求失败（请确认后端已启动 http://127.0.0.1:8000）: {e}", file=sys.stderr)
        sys.exit(1)
