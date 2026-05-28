---
name: frontend-code-component-standard
description: Standardize frontend implementation and component usage for project development. Use when building or refactoring frontend pages/components, especially around UI library selection, component visibility state control, form handling, and reducing custom HTML/CSS usage.
---

# Frontend Code Component Standard

## Scope

Use this skill for frontend project implementation that needs consistent component usage and code style.

## Workflow

1. Identify UI library first.
2. Prefer UI-library skills if available.
3. Implement interaction visibility with `v-model` + `defineModel`.
4. Implement user-input submission flows with UI form components.
5. Prefer UI components over raw HTML/CSS unless user explicitly requests custom styles.

## 1) Identify UI library first

Before coding, inspect the project for UI library signals:

- `package.json` dependencies/devDependencies
- Existing page/component usage patterns (e.g. `t-`, `el-`, `a-`, `n-` component prefixes)
- Project docs/rules (`CLAUDE.md`, team conventions)

Output a short conclusion:

- Primary UI library
- Secondary UI libraries (if any)
- Whether there is a matching UI-specific skill to follow

## 2) Load matching UI-library skill when available

If there is a skill matching the detected UI library, load and follow it first.

Examples:

- TDesign project -> load TDesign skill (if available)
- Element Plus project -> load Element Plus skill (if available)
- Ant Design Vue project -> load Ant Design Vue skill (if available)

If no matching skill exists, continue with this standard.

## 3) Visibility control standard (`v-model` + `defineModel`)

For interactive show/hide state (drawer, dialog, popover, modal-like components), prefer:

- Parent: `v-model:visible="xxx"` (or the component-specific model key)
- Child: `const visible = defineModel<boolean>('visible', { required: true })`

Avoid legacy pattern unless required by old code compatibility:

- `props.visible` + `emit('update:visible', ...)`

Preferred close behavior:

- `visible.value = false`

For nested interactive components, keep the same pattern consistently.

## 4) Form standard for user-input and submit flows

For any UI that collects user input and submits to backend (or mock API), use UI form components:

- Wrap input area with `t-form` / project-equivalent form container
- Use `t-form-item` / equivalent for each field
- Always provide `name` for form items that map to submitted data

### Array / dynamic form fields

When fields are rendered with `v-for`:

- Place `t-form` outside the `v-for` container
- Use path-style `name` in each item, e.g.:
  - `` `owners[${index}].name` ``
  - `` `strategies[${index}].eventId` ``
  - `` `items[${i}].children[${j}].value` ``

This keeps validation/data-path behavior predictable and consistent.

## 5) Prefer UI components over raw HTML/CSS

Unless the user explicitly requests custom visuals:

- Use existing UI-library components for layout and interaction
- Use project shared components first (if available)
- Keep raw HTML and custom CSS minimal

Priority order:

1. Existing project business components
2. UI library components
3. Utility classes / design tokens
4. New custom CSS as last resort

Especially avoid reinventing:

- Form layout / spacing
- Cards / section containers
- Dialog/Drawer headers and footers
- Button/link style variants

## Implementation Checklist

- [ ] UI library identified
- [ ] Matching UI skill checked/loaded (if exists)
- [ ] Visibility state uses `v-model` + `defineModel`
- [ ] Input/submit areas use UI form components
- [ ] Dynamic form items use path-style `name`
- [ ] New custom CSS minimized
- [ ] Existing project style conventions preserved
