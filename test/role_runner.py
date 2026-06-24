"""假设验证研究 — 角色测评通用运行器（仅专业版报告）。"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Tuple

import requests

BASE = os.environ.get("ASSESSMENT_API_BASE", "http://127.0.0.1:8000")

AnswerHollandFn = Callable[[dict], Tuple[int, str]]
AnswerGallupFn = Callable[[dict], Tuple[int, str]]


def _api(method: str, path: str, token: Optional[str] = None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return requests.request(method, f"{BASE}{path}", headers=headers, timeout=120, **kwargs)


def ensure_user(username: str, password: str, display_name: str) -> dict:
    payload = {"username": username, "password": password}
    r = _api("POST", "/api/auth/login", json=payload)
    if r.status_code == 200:
        return r.json()
    reg = {
        "username": username,
        "password": password,
        "display_name": display_name,
        "school": "角色测试",
        "grade": "测试",
    }
    r = _api("POST", "/api/auth/register", json=reg)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"注册失败: {r.status_code} {r.text}")
    r = _api("POST", "/api/auth/login", json=payload)
    r.raise_for_status()
    return r.json()


def get_questions(token: str, assessment_type: str) -> List[dict]:
    r = _api("GET", "/api/assessments/questions", token, params={"assessment_type": assessment_type})
    r.raise_for_status()
    return r.json()


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


def get_professional_report(student_id: str) -> dict:
    r = _api(
        "POST",
        "/api/auth/login",
        json={"username": "teacher", "password": "Hg@Teacher2026!mP4"},
    )
    r.raise_for_status()
    token = r.json()["access_token"]
    r = _api("GET", f"/api/reports/professional/{student_id}", token)
    r.raise_for_status()
    return r.json()


def build_answers(
    holland_questions: List[dict],
    gallup_questions: List[dict],
    holland_fn: AnswerHollandFn,
    gallup_fn: AnswerGallupFn,
) -> Tuple[List[dict], List[dict], List[dict], List[dict]]:
    hol_answers, hol_log = [], []
    gal_answers, gal_log = [], []

    for q in sorted(holland_questions, key=lambda x: x["question_num"]):
        score, mono = holland_fn(q)
        score = max(1, min(5, int(score)))
        hol_answers.append({"question_num": q["question_num"], "score": score})
        hol_log.append({
            "question_num": q["question_num"],
            "statement": q.get("statement_a"),
            "scenario_hint": q.get("scenario_hint"),
            "theme_tags": q.get("theme_tags"),
            "score": score,
            "monologue": mono,
        })

    for q in sorted(gallup_questions, key=lambda x: x["question_num"]):
        choice, mono = gallup_fn(q)
        choice = max(-2, min(2, int(choice)))
        gal_answers.append({"question_num": q["question_num"], "choice": choice})
        gal_log.append({
            "question_num": q["question_num"],
            "statement_a": q.get("statement_a"),
            "statement_b": q.get("statement_b"),
            "scenario_hint": q.get("scenario_hint"),
            "theme_tags": q.get("theme_tags"),
            "b_side_themes": q.get("b_side_themes"),
            "choice": choice,
            "choice_label": _choice_label(choice),
            "monologue": mono,
        })

    return hol_answers, gal_answers, hol_log, gal_log


def _choice_label(choice: int) -> str:
    return {
        2: "非常认同A",
        1: "比较认同A",
        0: "两者居中",
        -1: "比较认同B",
        -2: "非常认同B",
    }.get(choice, "未知")


def run_role_simulation(
    *,
    role_meta: dict,
    output_dir: str,
    holland_fn: AnswerHollandFn,
    gallup_fn: AnswerGallupFn,
    profile_summary: str,
) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    user = ensure_user(role_meta["username"], role_meta["password"], role_meta["display_name"])
    token = user["access_token"]
    user_id = user["user_id"]

    holland_qs = get_questions(token, "holland")
    gallup_qs = get_questions(token, "gallup")
    hol_answers, gal_answers, hol_log, gal_log = build_answers(
        holland_qs, gallup_qs, holland_fn, gallup_fn
    )

    hol_result = submit_holland(token, hol_answers)
    gal_result = submit_gallup(token, gal_answers)
    prof_report = get_professional_report(user_id)

    _save_json(os.path.join(output_dir, "answers_holland.json"), {"answers": hol_answers})
    _save_json(os.path.join(output_dir, "answers_gallup.json"), {"answers": gal_answers})
    _save_json(os.path.join(output_dir, "monologues_holland.json"), {"items": hol_log})
    _save_json(os.path.join(output_dir, "monologues_gallup.json"), {"items": gal_log})
    _save_json(os.path.join(output_dir, "assessment_result.json"), {
        "user_id": user_id,
        **role_meta,
        "holland_result": hol_result,
        "gallup_result": gal_result,
    })
    _save_json(os.path.join(output_dir, "professional_report.json"), prof_report)
    if prof_report.get("report_html"):
        _save_text(os.path.join(output_dir, "professional_report.html"), prof_report["report_html"])

    summary = {
        **role_meta,
        "user_id": user_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "holland_code": hol_result.get("holland_code"),
        "holland_scores": hol_result.get("holland_scores"),
        "gallup_domain": gal_result.get("gallup_domain"),
        "gallup_top5": gal_result.get("gallup_top5"),
        "gallup_secondary_domain": gal_result.get("gallup_secondary_domain"),
        "careers": [c.get("career_name") for c in (prof_report.get("careers") or [])],
        "tension": prof_report.get("tension"),
        "output_dir": output_dir,
    }
    _save_json(os.path.join(output_dir, "summary.json"), summary)

    rationale = _build_rationale(role_meta, profile_summary, hol_result, gal_result, prof_report)
    _save_text(os.path.join(output_dir, "role_rationale.md"), rationale)

    return summary


def _build_rationale(role_meta, profile_summary, hol_result, gal_result, prof_report) -> str:
    top5 = gal_result.get("gallup_top5") or []
    careers = prof_report.get("careers") or []
    return f"""# {role_meta.get("label")} — 假设验证记录

> 生成时间：{datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
> 报告类型：**专业版 only**

## 角色画像

{profile_summary}

## 实测结果

| 维度 | 结果 |
|------|------|
| Holland 三码 | `{hol_result.get("holland_code")}` |
| Holland 得分 | {json.dumps(hol_result.get("holland_scores"), ensure_ascii=False)} |
| Gallup 主导领域 | {gal_result.get("gallup_domain")} |
| Gallup 次要领域 | {gal_result.get("gallup_secondary_domain")} |
| Gallup Top 5 | {", ".join(top5)} |
| 张力分析 | {prof_report.get("tension", "")[:200]}… |

## 推荐职业（专业版，{len(careers)} 条）

{chr(10).join(f"- {c.get('career_name')}" for c in careers[:8])}

## 作答材料

- 逐题内心独白：`monologues_holland.json`（60 题）、`monologues_gallup.json`（180 题）
- 专业版报告：`professional_report.html`

## 账号

- 用户名：`{role_meta.get("username")}`
- 密码：`{role_meta.get("password")}`
"""


def _save_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _save_text(path: str, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
