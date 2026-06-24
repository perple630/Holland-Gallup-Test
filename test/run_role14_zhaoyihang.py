"""运行角色十四 · 赵一航 假设验证（专业版报告 + 逐题内心独白）。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from characters.zhaoyihang import (
    OUTPUT_DIR_NAME,
    PROFILE_SUMMARY,
    ROLE_META,
    answer_gallup,
    answer_holland,
)
from role_runner import run_role_simulation


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "roles", OUTPUT_DIR_NAME)
    print(f"=== {ROLE_META['label']} ({ROLE_META['display_name']}) ===")
    print("模式：逐题内心独白 · 仅专业版报告")

    summary = run_role_simulation(
        role_meta=ROLE_META,
        output_dir=output_dir,
        holland_fn=answer_holland,
        gallup_fn=answer_gallup,
        profile_summary=PROFILE_SUMMARY.strip(),
    )

    print("\n=== 完成 ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n内心独白：{output_dir}/monologues_holland.json, monologues_gallup.json")
    print(f"专业版报告：{output_dir}/professional_report.html")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"失败: {e}", file=sys.stderr)
        sys.exit(1)
