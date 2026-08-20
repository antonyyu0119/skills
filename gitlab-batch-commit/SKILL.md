---
name: gitlab-batch-commit
description: >
  Plans and executes batched git commits for company GitLab uploads with a
  800-line-per-commit limit, dual-type commit messages (feat/fix/test/skip +
  Co-Authored-By code/fix/test), and Test-file separation. Use when uploading
  a project to GitLab, batch-committing a large codebase, or when the user
  mentions 分批提交、800行、1500行、skip commit、工单号 commit、GitLab 导入。
disable-model-invocation: true
---

# GitLab Batch Commit

> **核心原则**：先梳理项目结构 → 按业务批次拆分 → 按行数打包 → 严格遵循公司 AI Commit 格式提交。  
> 默认**只 commit，不 push**（除非用户明确要求）。

## When to Use

- 首次将大型项目上传到公司 GitLab
- 需要满足单条 commit ≤ 800 行的后台校验
- 需要按模块分批提交，便于审查与追溯

**不要用于**：日常小改动提交 → 使用 `git-commit` skill。

## Quick Checklist

```
- [ ] 1. 环境检查 + 确认任务号
- [ ] 2. 梳理项目结构，确定业务批次
- [ ] 3. 运行 plan_commits.py 生成提交计划
- [ ] 4. 展示计划，等待用户确认（或批量授权）
- [ ] 5. 记录 BATCH_START=$(git rev-parse HEAD)，逐批用 batch_commit.sh 提交（禁止 git commit）
- [ ] 6. 全部完成后运行 verify_batch_messages.sh；失败则 strip_cursor_coauthor.sh 再 verify
- [ ] 7. verify 通过后才输出提交总结（禁止 push）
```

## 1. Environment Check

```bash
git rev-parse --is-inside-work-tree
git symbolic-ref --short HEAD
git status --porcelain
git log -1 --format=%B
```

规则：

- 不在 Git 仓库 → 终止
- 工作区无变更 → 终止
- 🔒 无任务号 → 询问用户（如 `304375`）
- 默认**禁止** `git push`；仅当用户明确授权时才 push

排除不应提交的文件：`node_modules/`、`dist/`、`.DS_Store`、编译产物、依赖锁定目录（遵循项目 `.gitignore`）。

## 2. Project Structure Analysis

首次导入前，输出顶层目录与模块职责，并按 [batch-template.md](batch-template.md) 给出 8 类业务批次建议。

## 3. Batching Rules

```text
打包上限：700 行/批（为 800 硬限制留缓冲）
硬限制：单条 commit 总行数 ≤ 800
超限：标题提交类型用 skip（GitLab 导入专用扩展）
暂存：git add -- <files>，严禁 git add .
推送：禁止 git push（除非用户明确授权）
```

使用脚本生成计划：

```bash
python3 scripts/plan_commits.py \
  --root <repo-root> \
  --ticket <任务号> \
  --paths <dir1> <dir2> ... \
  --format markdown
```

详见 [batch-template.md](batch-template.md) 了解推荐批次划分。

## 4. Commit Message Format

对齐公司《AI commit 提交规范》第 5.1 节统一格式 + 第 6 节提交类型规则。

### 4.1 统一结构

```text
<任务号> <提交类型> <简短标题>

- <详细说明1>
- <详细说明2>
- <详细说明3>

Co-Authored-By: <工具名> | <模型名> | <AI生成类型>
```

**格式硬性约束（后台校验敏感，不可省略空行）：**

| 位置 | 规则 |
|------|------|
| 标题行 | `<任务号>` + 空格 + `<提交类型>` + 空格 + `<简短标题>` |
| 标题后 | **必须空一行** |
| 详情 | 每条以 `- ` 开头，建议 1–4 条 |
| 详情后 | **必须空一行** |
| Co-Authored-By | `<工具名> \| <模型名> \| <AI生成类型>`，竖线两侧各有一个空格 |

提交命令使用 HEREDOC：

```bash
git commit -m "$(cat <<'EOF'
<任务号> <提交类型> <简短标题>

- <详细说明1>

Co-Authored-By: <工具名> | <模型名> | <AI生成类型>
EOF
)"
```

### 4.2 双层类型体系

**标题行 `<提交类型>`**（第二个 token）：

| 值 | 适用场景 |
|----|----------|
| `feat` | 普通业务代码（AI 闭环/纯 AI/少量人工调整） |
| `fix` | 当前分支名包含 `fix` 时的非 Test 批次 |
| `test` | Test 专用批次（第二 token **强制**为 `test`） |
| `skip` | GitLab 导入专用：单批行数 > 800 且无法拆分 |

**Co-Authored-By 第三段 `<AI生成类型>`**（与标题类型独立判定）：

| 值 | 适用场景 |
|----|----------|
| `code` | AI 闭环/纯 AI 业务代码，或少量人工调整 |
| `fix` | 修复 AI 自身错误、方案遗漏、CR 中 AI 代码问题 |
| `test` | 单元测试、集成测试、测试脚本及测试目录变更 |

**判定优先级：**

1. 批次仅含 Test 文件 → 标题 `test`，Co-Authored-By 第三段 `test`
2. 修复 AI 自身错误/CR 问题 → Co-Authored-By 第三段 `fix`（标题类型仍遵循分支约束）
3. 其余业务代码 → Co-Authored-By 第三段 `code`
4. 批次行数 > 800 且无法拆分 → 标题 `skip`（Co-Authored-By 通常仍为 `code`）

### 4.3 分支约束（第 7 节）

- 分支名包含 `fix` → 非 Test 批次标题第二 token 必须为 `fix`
- 分支名不包含 `fix` → 非 Test 批次**禁止**使用 `fix`
- Test 批次不受上述约束，标题第二 token 固定为 `test`

### 4.4 Test 强约束（第 6.4 节）

- Test 文件**必须**与非 Test 文件**拆分提交**
- 同一批次**禁止**混入 Test 与非 Test 文件
- Test 批次：标题 `test`，Co-Authored-By 第三段 `test`

**Test 文件识别：**

- 路径含：`test/`、`tests/`、`__tests__/`
- 文件名：`*.test.*`、`*.spec.*`、`*_test.go`、`Test*.java`

### 4.5 Co-Authored-By 自动填充

- `<工具名>`：实际 AI-IDE 原始大小写（Cursor、Claude Code 等）
- `<模型名>`：实际模型标识符（如 `claude-opus-4-6`、`DeepSeek-V3`），禁止泛称
- 无法判断时输出预览并请用户确认

## 5. Examples

**普通代码提交：**

```text
168985 feat add OAuth2 login

- Implement Google and GitHub OAuth2 flows
- Add token validation and user session handling

Co-Authored-By: Cursor | DeepSeek-V3 | code
```

**修复提交：**

```text
168985 feat handle callback null exception

- Fix null pointer in callback processing
- Add fallback for missing auth state

Co-Authored-By: Claude Code | claude-opus-4-6 | fix
```

**测试提交：**

```text
BBYFXN-123 test add OAuth2 login tests

- Cover normal login flow
- Cover auth failure and token expiration
- Cover callback parameter validation

Co-Authored-By: Cursor | DeepSeek-V3 | test
```

**GitLab 导入超限提交（本 skill 扩展）：**

```text
304375 skip 添加 LLM Token 计数 BPE 分词数据

- 添加 cl100k_base.tiktoken 分词数据文件
- 用于 LLM 请求的 Token 用量估算

Co-Authored-By: Cursor | Composer-2.5 | code
```

## 6. Execution Workflow

1. 梳理项目结构，确定业务批次（见 [batch-template.md](batch-template.md)）
2. 对每个业务批次运行 `plan_commits.py` 生成子计划
3. 合并展示全局提交计划（批次号、文件数、行数、标题类型、AI 生成类型）
4. 🔒 等待用户确认首批，或用户授权后连续执行
5. 记录起点并逐批执行（**禁止直接使用 `git commit`**，Cursor 会注入 `cursoragent@cursor.com`）：

```bash
BATCH_START=$(git rev-parse HEAD)
MSG=$(mktemp)
cat > "$MSG" <<'EOF'
<任务号> <提交类型> <简短标题>

- <详细说明1>

Co-Authored-By: <工具名> | <模型名> | <AI生成类型>
EOF
bash <skill-root>/scripts/batch_commit.sh -F "$MSG" -- <file1> <file2>
rm -f "$MSG"
```

6. 每批报告：`hash`、标题类型、行数、文件数
7. 全部批次完成后，**必须**校验 message（未通过不得输出总结）：

```bash
bash <skill-root>/scripts/verify_batch_messages.sh --since "$BATCH_START" \
  || bash <skill-root>/scripts/strip_cursor_coauthor.sh --since "$BATCH_START"
bash <skill-root>/scripts/verify_batch_messages.sh --since "$BATCH_START"
```

8. verify 通过后输出总结，**不执行 push**

## 7. Post-Commit Summary

```text
=== 提交总结 ===
共完成 X 次提交（feat: A, fix: B, test: C, skip: D）
  1. <hash> - <任务号> <类型> <标题>
  ...
Message 校验：verify_batch_messages 已通过（无 cursoragent 注入）
工作区状态：<clean / 剩余未提交文件>
推送状态：未 push（由用户统一推送）
```

## 8. 禁止注入 Cursor 邮箱

**首选预防**：使用 [scripts/batch_commit.sh](scripts/batch_commit.sh)（`git commit-tree`）替代 `git commit`，从源头避免注入。

**兜底清理**：若误用 `git commit` 或仍有注入，使用 [scripts/strip_cursor_coauthor.sh](scripts/strip_cursor_coauthor.sh)。

在 **Cursor Agent 终端**执行 `git commit` 时，提交完成后可能被自动追加以下行（**不属于公司规范，禁止保留**）：

```text
Co-authored-by: Cursor <cursoragent@cursor.com>
```

规范 message **仅允许**末尾一行公司格式：`Co-Authored-By: <工具名> | <模型名> | <AI生成类型>`。

**注意：**

- `--no-verify` **无法**阻止该行注入（非本地 hook，而是 Cursor 提交链路行为）
- 全部批次完成后**必须**运行 [scripts/verify_batch_messages.sh](scripts/verify_batch_messages.sh)；失败则**必须**运行 `strip_cursor_coauthor.sh` 并再次 verify，通过后才能输出总结
- verify 示例：`bash scripts/verify_batch_messages.sh --since "$BATCH_START"`
- strip 示例：`bash scripts/strip_cursor_coauthor.sh --since "$BATCH_START"` 或 `bash scripts/strip_cursor_coauthor.sh <批次数>`

## Related Skills

- **日常提交 + 自动推送** → `git-commit`
- **GitLab 大批量首次导入、800 行限制** → `gitlab-batch-commit`（本 skill）
