---
name: weekly-report
description: Generate weekly work reports by scanning git repositories for commits and uncommitted changes. Supports custom report templates and dual-format output (Markdown + HTML rich text for email). Use when the user asks to prepare a weekly report, generate weekly summary, write a work report, or collect progress across repositories.
disable-model-invocation: true
---

# Weekly Report Generator

## Overview

Generates structured weekly reports by:
1. Scanning specified git repositories for commits and uncommitted changes within a date range
2. Listing Cursor agent transcripts for context gathering
3. Organizing findings into a user-provided or default template
4. Outputting both Markdown (.md) and HTML rich-text (.html) files for email

## Workflow

### Phase 1: Collect Requirements

Ask the user for:

1. **Repositories** — Absolute paths to git repos to scan (e.g. `/Users/xxx/Projects/...`)
2. **Report period** — Default: last work week (Monday to Friday)
3. **Template / format** — Does the user have a specific template? If not, use the [default template](template.md)
4. **Technical share / special events** — Any talks, demos, research that should be included
5. **Target output folder** — Where to save `.md` and `.html` files (default: workspace root)

If the user says "no template, use your own", use the default template in [template.md](template.md).

### Phase 2: Gather Git Data

For each repository:

```bash
# 1. Get all authors' commits for the period
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --pretty=format:"%h|%ad|%an|%s" --date=short

# 2. Get the user's own commits with details
git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" --author="$USER_NAME" --stat --oneline

# 3. Get commit diffs for meaningful context (key commits only)
git show <hash> -p --stat

# 4. Check uncommitted changes
git status -sb
git diff HEAD --stat
git diff HEAD -p
```

For each commit, extract:
- JIRA ticket number (e.g. `#300297`) from the commit message
- What was changed (files, summary)
- Why it was changed (business purpose)

### Phase 3: Gather Context from Cursor Transcripts

Check the Cursor agent transcripts directory for relevant sessions:

```
ls ~/.cursor/projects/.../agent-transcripts/
```

Search for keywords related to the week's topics to discover technical shares, demos, or special activities.

### Phase 4: Organize Report Content

Categorize the findings into:

1. **Feature development** — New features, iterations
2. **Bug fixes** — Defect resolutions
3. **Architecture / engineering** — Refactoring, optimization, security
4. **Tech shares & research** — Technical talks, demos, learning
5. **Documentation** — Design docs, guides

### Phase 5: Generate Output Files

See [template.md](template.md) for the exact report structure.

**Step 1 — Generate Markdown (.md):**
- Use the template structure verbatim from template.md
- Fill in all sections with actual content from git data and user input
- Save to the target folder as `周报-MM.DD-MM.DD.md`

**Step 2 — Generate HTML (.html):**
- Convert the markdown to HTML rich text suitable for email paste
- Use inline styles (no external CSS) so formatting survives email clients
- Include: collapsible tables for meta info, styled section headers with colored left borders, ordered lists, table for share details
- Save as `周报-MM.DD-MM.DD.html`

### Phase 6: Present to User

Tell the user the output file paths and offer to:
- Adjust any section wording
- Change the output format
- Regenerate with different repositories or date range

## Default Template Structure

```
# 周报 MM.DD - MM.DD

| 项目     | 内容       |
|----------|------------|
| 报告人   | [name]     |
| 报告时间 | [date]     |
| 导师/主管 | [names]   |

---

## 本周总结

[Opening paragraph summarizing the week's focus, followed by numbered items]

### 1. [Title with ticket number]

[Description of what was done, why, and impact]

### 2. [Title with ticket number]

...

## 下周计划

1. ...
2. ...

## 问题 / 风险点

1. ...
2. ...

## 【聚焦】下周核心

1. ...
2. ...

## 【链接】需支持

1. ...
2. ...
```

For the complete template including the technical share detail format, see [template.md](template.md).

## HTML Output Rules

When generating `.html`:

```html
<!-- Meta info table: bordered, gray header row -->
<!-- Section headers: colored left border (blue for main, green for 聚焦, purple for 链接) -->
<!-- Share details: use a second table with theme, time, location, speaker, RSVP link -->
<!-- Tips: yellow left border block for sign-in instructions -->
<!-- Keep all styles inline for email compatibility -->
<!-- Font: Microsoft YaHei / PingFang SC, size 14px -->
```

See [template.html](template.html) for the complete HTML skeleton.

## Additional Resources

- For the default report template, see [template.md](template.md)
- For the HTML email template, see [template.html](template.html)
- For a complete example, see [examples.md](examples.md)