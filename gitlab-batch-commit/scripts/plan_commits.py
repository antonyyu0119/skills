#!/usr/bin/env python3
"""Plan batched git commits for GitLab uploads with line-count limits."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PACK_LIMIT = 700
HARD_LIMIT = 800
EXCLUDE_NAMES = {".DS_Store"}

TEST_PATH_RE = re.compile(r"(^|/)(test|tests|__tests__)(/|$)")
TEST_FILE_RE = re.compile(
    r"(\.test\.|\.spec\.|_test\.go$|^Test[^/]*\.java$)", re.IGNORECASE
)


def line_count(path: Path) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def is_test_file(path: Path) -> bool:
    s = path.as_posix()
    if TEST_PATH_RE.search(s):
        return True
    return bool(TEST_FILE_RE.search(path.name))


def collect_files(root: Path, paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        fp = root / p
        if fp.is_file():
            if fp.name not in EXCLUDE_NAMES:
                files.append(fp.resolve())
        elif fp.is_dir():
            for f in sorted(fp.rglob("*")):
                if f.is_file() and f.name not in EXCLUDE_NAMES:
                    files.append(f.resolve())
    return sorted(set(files), key=lambda x: x.as_posix())


def branch_prefix_type(branch: str, is_test_batch: bool) -> str:
    if is_test_batch:
        return "test"
    if "fix" in branch.lower():
        return "fix"
    return "feat"


def co_author_type(is_test_batch: bool, is_ai_fix: bool = False) -> str:
    if is_test_batch:
        return "test"
    if is_ai_fix:
        return "fix"
    return "code"


def title_commit_type(
    lines: int, branch: str, is_test_batch: bool
) -> str:
    if lines > HARD_LIMIT:
        return "skip"
    return branch_prefix_type(branch, is_test_batch)


def make_batches(files: list[Path], limit: int = PACK_LIMIT) -> list[list[Path]]:
    batches: list[list[Path]] = []
    batch: list[Path] = []
    total = 0

    for f in files:
        n = line_count(f)
        if n > limit:
            if batch:
                batches.append(batch)
                batch, total = [], 0
            batches.append([f])
            continue
        if total + n > limit and batch:
            batches.append(batch)
            batch, total = [], 0
        batch.append(f)
        total += n

    if batch:
        batches.append(batch)
    return batches


def batch_lines(files: list[Path]) -> int:
    return sum(line_count(f) for f in files)


def plan_commits(
    root: Path,
    paths: list[str],
    ticket: str,
    branch: str = "main",
    limit: int = PACK_LIMIT,
) -> list[dict]:
    all_files = collect_files(root, paths)
    test_files = [f for f in all_files if is_test_file(f)]
    nontest_files = [f for f in all_files if not is_test_file(f)]

    plans: list[dict] = []
    batch_num = 0

    for group_name, group_files, is_test in [
        ("test", test_files, True),
        ("nontest", nontest_files, False),
    ]:
        if not group_files:
            continue
        for file_batch in make_batches(group_files, limit):
            batch_num += 1
            lines = batch_lines(file_batch)
            title_type = title_commit_type(lines, branch, is_test)
            ai_type = co_author_type(is_test)
            rel_files = [str(f.relative_to(root)) for f in file_batch]
            plans.append(
                {
                    "batch": batch_num,
                    "group": group_name,
                    "lines": lines,
                    "file_count": len(rel_files),
                    "title_type": title_type,
                    "ai_type": ai_type,
                    "is_test_batch": is_test,
                    "exceeds_hard_limit": lines > HARD_LIMIT,
                    "files": rel_files,
                    "suggested_subject": f"{ticket} {title_type} <简短标题>",
                    "suggested_co_author": f"Co-Authored-By: <工具名> | <模型名> | {ai_type}",
                }
            )
    return plans


def format_markdown(plans: list[dict]) -> str:
    lines_out = [f"## 提交计划（共 {len(plans)} 批）\n"]
    for p in plans:
        flag = " ⚠️超800" if p["exceeds_hard_limit"] else ""
        lines_out.append(
            f"### 第 {p['batch']} 批{flag}\n"
            f"- 行数: {p['lines']} | 文件: {p['file_count']}\n"
            f"- 标题类型: `{p['title_type']}` | AI类型: `{p['ai_type']}`\n"
            f"- Test批次: {'是' if p['is_test_batch'] else '否'}\n"
            f"- 建议标题: `{p['suggested_subject']}`\n"
            f"- 文件: {', '.join(p['files'][:5])}"
            + (f" ... +{len(p['files']) - 5}" if len(p['files']) > 5 else "")
            + "\n"
        )
    return "\n".join(lines_out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan batched git commits")
    parser.add_argument("--root", required=True, help="Repository root")
    parser.add_argument("--ticket", required=True, help="Task ticket number")
    parser.add_argument("--paths", nargs="+", required=True, help="Paths to include")
    parser.add_argument("--branch", default="main", help="Current branch name")
    parser.add_argument("--limit", type=int, default=PACK_LIMIT, help="Pack limit")
    parser.add_argument(
        "--format", choices=["json", "markdown"], default="json", help="Output format"
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: root not found: {root}", file=sys.stderr)
        return 1

    plans = plan_commits(root, args.paths, args.ticket, args.branch, args.limit)

    if args.format == "json":
        print(json.dumps(plans, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(plans))

    return 0


if __name__ == "__main__":
    sys.exit(main())
