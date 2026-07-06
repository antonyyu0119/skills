---
name: markdown-to-confluence
description: "Convert Markdown files to Confluence Wiki markup format (.wiki). Use this skill whenever the user mentions Confluence, wiki format, .wiki files, converting docs to Confluence, or wants to put content into Confluence. Also trigger when users say 'confluence格式', 'wiki格式', '转Confluence', or reference Confluence macros like panels, expand, or toc. Covers full Confluence macro support including panels, info/note/warning boxes, table of contents, expand sections, Mermaid diagrams, and image handling."
---

# Markdown → Confluence Wiki Converter

Convert any Markdown document into Confluence Wiki markup that can be pasted directly into the Confluence editor.

## How to use

1. Read the source Markdown file(s)
2. Apply the conversion rules below
3. Save the output as `<original-name>.wiki` in the same directory
4. Tell the user to copy-paste into Confluence editor (Insert → Markup or Ctrl+Shift+D)

## Conversion Rules

### Headers

Markdown headers become Confluence wiki headers. No `#` symbols — use the `h` prefix notation.

```
# Title        →  h1. Title
## Section      →  h2. Section
### Subsection  →  h3. Subsection
#### Level 4    →  h4. Level 4
##### Level 5   →  h5. Level 5
###### Level 6  →  h6. Level 6
```

### Text Formatting

```
**bold**            →  *bold*
_italic_            →  _italic_
***bold italic***   →  *_bold italic_*
~~strikethrough~~   →  -strikethrough-
`inline code`       →  {{inline code}}
```

### Links

```
[text](url)     →  [text|url]
[text](url "t") →  [text|url|title=t]
[url](url)      →  [url]
```

### Images

```
![alt](url)            →  !url|alt=alt!
![alt](url "title")    →  !url|title=title|alt=alt!
![alt](url =300x200)   →  !url|width=300,height=200|alt=alt!
```

For images with size specifications, extract width/height and use the Confluence image parameters syntax.

### Lists

**Unordered lists** — use `*` with indentation for nesting:
```
- Item            →  * Item
  - Sub-item      →    ** Sub-item
    - Deep item   →      *** Deep item
```

**Ordered lists** — use `#` with indentation:
```
1. First          →  # First
   1. Sub-first   →    ## Sub-first
2. Second         →  # Second
```

**Task lists / Checkboxes:**
```
- [ ] unchecked   →  [] ( ) unchecked
- [x] checked     →  [ ] checked
```

Note: Confluence wiki has limited native checkbox support. If the document has extensive task lists, consider using the `{tasklist}` macro instead — but for simple cases, the basic checkbox syntax works.

### Tables

Markdown tables use `|` for both headers and rows. Confluence wiki distinguishes headers (`||`) from data rows (`|`).

```
| Col A | Col B |       →  ||Col A||Col B||
| --- | --- |           →  (remove — separator row is not needed in Confluence)
| val 1 | val 2 |       →  |val 1|val 2|
```

Key rules:
- The first row of a Markdown table is always the header → wrap each cell in `||`
- Remove the separator row (`|---|---|`)
- Alignment (left/center/right) is not supported in Confluence wiki tables — ignore alignment markers (`:---`, `:---:`, `---:`)
- Empty cells should be preserved as `|  |` or `|| ||`

### Code Blocks

```
```language
code here
```       →  {code:language=language}
             code here
             {code}
```

Language mapping (some Markdown language names differ from Confluence):
- `js` / `javascript` → `javascript`
- `ts` / `typescript` → `typescript`
- `py` / `python` → `python`
- `java` → `java`
- `bash` / `sh` / `shell` → `bash`
- `sql` → `sql`
- `json` → `json`
- `xml` / `html` → `xml` (or `html` for HTML)
- `yaml` / `yml` → `yaml`
- `text` / `plaintext` / no language → omit the language parameter: `{code}`

Additional code block options (when context suggests they'd be useful):
```
{code:title=filename.java|borderStyle=solid|language=java}
{code:linenumbers=true|language=python}
{code:title=Server Log|collapse=true}
```

### Blockquotes

Simple blockquotes become the `{quote}` macro. If the blockquote is multi-paragraph or appears to be a callout/admonition, use `{panel}` instead.

```
> Simple quote
→
{quote}
Simple quote
{quote}
```

For multi-line or structured blockquotes that read like callout boxes:
```
> **Note**
> This is important info.
→
{panel:title=Note|borderColor=#0052CC}
This is important info.
{panel}
```

### Horizontal Rules

```
---   →  ----
***   →  ----
___   →  ----
```

### Table of Contents

```markdown
## Table of Contents
<!-- TOC -->
```
or any heading like "目录", "Table of Contents", "TOC":
→
```
{toc:maxLevel=3}
```

Use `maxLevel=3` by default. If the document is very flat (mostly h2/h3), use `maxLevel=2`. If deeply nested, `maxLevel=4`.

### Footnotes

Confluence wiki doesn't have native footnote support. Convert footnote references to superscript links:
```
Some text[^1] and more[^2]

[^1]: First footnote
[^2]: Second footnote
```
→
```
Some text^[(1)]^ and more^[(2)]^

h4. Footnotes
# [(1)] First footnote
# [(2)] Second footnote
```

### Admonitions / Callout Blocks

Many Markdown docs use blockquote syntax or custom containers for callouts. Map these to Confluence panels:

**Standard admonitions (GitHub/Python style):**
```
> **Note:** Some note text
→
{panel:title=Note|borderColor=#0052CC}
Some note text
{panel}

> **Warning:** Careful here
→
{panel:title=Warning|borderColor=#FFAB00}
Careful here
{panel}

> **Important:** Critical info
→
{panel:title=Important|borderColor=#FF5630}
Critical info
{panel}

> **Tip:** Helpful suggestion
→
{panel:title=Tip|borderColor=#00875A}
Helpful suggestion
{panel}
```

**MkDocs-style admonitions** (if detected):
```
!!! note "Title"
    Content here
→
{panel:title=Title|borderColor=#0052CC}
Content here
{panel}
```

### Mermaid Diagrams

```
```mermaid
graph TD
    A --> B
```
→
```
{code:mermaid}
graph TD
    A --> B
{code}
```

### Expand / Collapsible Sections

```markdown
<details>
<summary>Click to expand</summary>
Hidden content here
</details>
```
→
```
{expand:title=Click to expand}
Hidden content here
{expand}
```

Also handle HTML `<details>` tags found in GitHub-flavored Markdown.

### Nested Blockquotes for Panels

When a blockquote contains a heading-like first line (bold or capitalized followed by newline), extract it as the panel title:
```
> **需求变更说明**
> 1. First change
> 2. Second change
→
{panel:title=需求变更说明|borderColor=#326CE5}
# First change
# Second change
{panel}
```

### Special Characters

Confluence wiki has its own escaping rules. These characters may need escaping or handling:
- `\` in regular text — usually fine, leave as-is
- `{` and `}` when not part of a macro — can break rendering; if they appear in plain text (not code), consider escaping or wrapping in `{noformat}`

## Workflow

1. Read the entire Markdown file first — scan for special patterns (admonitions, mermaid, details, custom syntax)
2. Process top-to-bottom, converting each element
3. Preserve paragraph spacing — Confluence wiki is tolerant of extra blank lines
4. If the document is long (>200 lines), automatically add `{toc:maxLevel=3}` at the top
5. Save as `.wiki` extension alongside the original `.md` file
6. Remind the user: paste into Confluence using the "Wiki Markup" input mode (not the visual editor)

## Edge Cases and Judgment Calls

- **Markdown inside HTML blocks**: Confluence wiki doesn't support mixed HTML/wiki syntax well. If you encounter HTML blocks (like `<div>`, `<span>`), convert their semantic meaning to wiki macros where possible, or wrap in `{noformat}` if conversion isn't practical.
- **Nested tables**: Confluence wiki doesn't support nested tables. Flatten or restructure if possible.
- **Very wide tables** (>10 columns): Consider adding a note to the user that wide tables may not render well in Confluence.
- **Emoji shortcodes**: `:smile:` etc. — Confluence wiki supports some emoji via `(/)` etc., but coverage is spotty. Leave emoji as-is or convert to Unicode emoji where possible.
- **Math / LaTeX**: Confluence doesn't natively support LaTeX. If math blocks are detected, suggest the user install a Confluence math plugin, and leave the content as `{code}` blocks as a fallback.
