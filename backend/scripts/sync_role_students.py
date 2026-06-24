"""导出/导入模拟角色学生（role* 账号）的 users + assessments 数据。"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
from typing import Any, Dict, List

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "data", "assessment.db")


def _connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def export_role_students(db_path: str, out_path: str) -> Dict[str, Any]:
    conn = _connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username LIKE 'role%' ORDER BY username"
    )
    users = [dict(row) for row in cur.fetchall()]
    user_ids = [u["id"] for u in users]
    assessments: List[dict] = []
    if user_ids:
        placeholders = ",".join("?" * len(user_ids))
        cur.execute(
            f"SELECT * FROM assessments WHERE user_id IN ({placeholders})",
            user_ids,
        )
        assessments = [dict(row) for row in cur.fetchall()]
    conn.close()
    payload = {"users": users, "assessments": assessments}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return {"users": len(users), "assessments": len(assessments), "out": out_path}


def import_role_students(db_path: str, in_path: str) -> Dict[str, int]:
    with open(in_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    users = payload.get("users", [])
    assessments = payload.get("assessments", [])

    conn = _connect(db_path)
    cur = conn.cursor()
    imported_users = 0
    imported_assessments = 0

    for user in users:
        username = user["username"]
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        existing = cur.fetchone()
        if existing:
            old_id = existing["id"]
            cur.execute("DELETE FROM assessments WHERE user_id = ?", (old_id,))
            cur.execute("DELETE FROM users WHERE id = ?", (old_id,))

        cur.execute(
            """
            INSERT INTO users (id, username, display_name, role, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user["id"],
                user["username"],
                user["display_name"],
                user["role"],
                user["password_hash"],
                user.get("created_at"),
            ),
        )
        imported_users += 1

    for row in assessments:
        cur.execute("DELETE FROM assessments WHERE user_id = ?", (row["user_id"],))
        cur.execute(
            """
            INSERT INTO assessments (
                id, user_id, holland_done, holland_scores, holland_code,
                gallup_done, gallup_top5, gallup_top10, gallup_domain,
                gallup_secondary_domain, gallup_scores, status,
                completed_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["user_id"],
                row["holland_done"],
                row["holland_scores"],
                row["holland_code"],
                row["gallup_done"],
                row.get("gallup_top5"),
                row["gallup_top10"],
                row["gallup_domain"],
                row["gallup_secondary_domain"],
                row["gallup_scores"],
                row["status"],
                row.get("completed_at"),
                row.get("updated_at"),
            ),
        )
        imported_assessments += 1

    conn.commit()
    conn.close()
    return {"users": imported_users, "assessments": imported_assessments}


def main():
    parser = argparse.ArgumentParser(description="同步 role* 模拟学生数据")
    parser.add_argument("action", choices=["export", "import"])
    parser.add_argument("--db", default=DEFAULT_DB, help="SQLite 数据库路径")
    parser.add_argument("--file", default="role_students.json", help="JSON 文件路径")
    args = parser.parse_args()

    db_path = os.path.abspath(args.db)
    if args.action == "export":
        result = export_role_students(db_path, args.file)
        print(json.dumps(result, ensure_ascii=False))
    else:
        result = import_role_students(db_path, args.file)
        print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
