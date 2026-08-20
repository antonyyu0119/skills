# GitLab 导入业务批次模板

将大型项目拆为 8 个业务批次，再在每个批次内按行数（≤700 行/批）进一步拆分 commit。

## 推荐批次顺序

| 批次 | 范围 | 说明 |
|------|------|------|
| 1. 基础骨架 | LICENSE、README*、go.mod、go.sum、Makefile、.gitignore | 项目元信息与构建基础 |
| 2. Go 核心 | cmd/、internal/ | 按 internal 子包继续拆（agent、diff、llm、tool 等） |
| 3. CLI 分发 | bin/、scripts/、npm/、package.json、install.sh | NPM 安装与跨平台二进制 |
| 4. VSCode 扩展 | extensions/vscode/ | 独立子项目，排除 node_modules/out |
| 5. 官网 | pages/src/、pages/public/、构建配置 | 排除 node_modules/、dist/ |
| 6. CI 集成 | action.yml、examples/、.github/ | GitHub Action + GitLab CI 示例 |
| 7. 插件生态 | plugins/、skills/、.claude/、.claude-plugin/ | Agent 集成 |
| 8. 资源与文档 | imgs/、docs/、CONTRIBUTING*、治理文档 | 图片、报告、合规文档 |

## 行内拆分原则

1. **打包上限 700 行**（为 800 硬限制留缓冲）
2. **单文件超大** → 独占一批；若 > 800 行 → 标题类型 `skip`
3. **Test 文件** → 必须独立批次，不得与业务代码混合
4. **多语言 README** → 每种语言单独 commit；单文件 > 800 行 → `skip`
5. **internal 子包** → 按包拆分；大包（llm、tool、agent）继续按文件拆

## 常见超大文件处理

| 文件类型 | 处理方式 |
|----------|----------|
| `.tiktoken`、大型数据文件 | 单独 `skip` commit |
| 超大单文件源码（如 TUI > 800 行） | 单独 `skip` commit |
| 图片/二进制（PNG/JPG/SVG） | 按文本统计可能虚高；大图单独 `skip` commit |
| `yarn.lock` / `package-lock.json` / `pnpm-lock.yaml` | 通常 > 800 行 → `skip` commit |

## OpenCodeReview 实践参考

以下为实际导入时的 commit 数量参考（非硬性要求）：

| 批次 | 约 commit 数 | 备注 |
|------|-------------|------|
| 1. 基础骨架 | 6 | 每种语言 README 单独提交 |
| 2. Go 核心 | ~46 | internal 按子包 + cmd 按文件组 |
| 3. CLI 分发 | ~5 | |
| 4. VSCode 扩展 | ~8 | ConfigView.tsx 等超大文件 skip |
| 5. 官网 | ~19 | 文档按语言拆分 |
| 6. CI 集成 | 4 | |
| 7. 插件生态 | 3 | |
| 8. 资源与文档 | 8 | benchmark 图片各 skip |

## 排除清单

以下路径/文件**不应提交**：

- `node_modules/`
- `dist/`、`out/`、编译产物
- `.DS_Store`
- 本地配置：`.env`、credentials
- 项目 `.gitignore` 中已声明忽略的文件

## 使用脚本

对每个业务批次分别运行：

```bash
python3 scripts/plan_commits.py \
  --root /path/to/repo \
  --ticket 304375 \
  --paths cmd internal \
  --branch feat-0728 \
  --format markdown
```

将输出的子计划合并为全局计划后，再逐批执行 commit。
