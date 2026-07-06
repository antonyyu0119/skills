---
name: frontend-code-component-standard
description: Standardize frontend implementation and component usage for project development. Use when building or refactoring frontend pages/components, especially around UI library selection, visibility state control, form handling, and reducing custom HTML/CSS usage by prioritizing UI-library components.
---

# Frontend Code Component Standard

## Scope

Use this skill for frontend project implementation that needs consistent component usage and code style.

## Workflow

1. Identify UI library first.
2. Prefer UI components over raw HTML/CSS unless user explicitly requests custom styles.
3. Implement interaction visibility with `v-model` + `defineModel`.
4. Implement user-input submission flows with UI form components.

## 1) Identify UI library first

Before coding, inspect the project for UI library signals:

- `package.json` dependencies/devDependencies
- Existing page/component usage patterns (e.g. `t-`, `el-`, `a-`, `n-` component prefixes)
- Project docs/rules (`CLAUDE.md`, team conventions)

Output a short conclusion:

- Primary UI library
- Secondary UI libraries (if any)
- Main component prefixes in this codebase (e.g. `t-` or `a-`)

## 2) Prefer UI components over raw HTML/CSS

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

### Inline and horizontal layout priority

For inline or horizontal (non-block) layouts, prefer UI-library layout components:

- `a-row` / `t-row` with `a-col` / `t-col` for row-column structure
- `a-space` / `t-space` for inline spacing between labels, text, tags, buttons, and actions

Use these patterns first for:

- Horizontally aligned form items
- Horizontally aligned cards/stat blocks
- Horizontal action bars
- Inline metadata/tag/button groups with spacing requirements

If row/col/space can solve layout and spacing, do not replace them with ad-hoc `div + flex + custom gap` by default.

## 3) Visibility control standard (`v-model` + `defineModel`)

For interactive show/hide state (drawer, dialog, popover, modal-like components), prefer:

- Parent: `v-model:visible="xxx"` (or the component-specific model key)
- Child: `const visible = defineModel<boolean>('visible', { required: true })`

Avoid legacy pattern unless required by old code compatibility:

- `props.visible` + `emit('update:visible', ...)`

Preferred close behavior:

- `visible.value = false`

For nested interactive components, keep the same pattern consistently.

Example:

```vue
<!-- Parent.vue -->
<template>
  <t-button @click="visible = true">Open</t-button>
  <ConfigDrawer v-model:visible="visible" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ConfigDrawer from './ConfigDrawer.vue';

const visible = ref(false);
</script>
```

```vue
<!-- ConfigDrawer.vue -->
<script setup lang="ts">
const visible = defineModel<boolean>('visible', { required: true });

function handleClose() {
  visible.value = false;
}
</script>
```

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

Example:

```vue
<template>
  <t-form ref="formRef" :data="formData" :rules="rules" @submit="handleSubmit">
    <t-row :gutter="[16, 12]">
      <t-col :span="6">
        <t-form-item name="name" label="Name">
          <t-input v-model="formData.name" />
        </t-form-item>
      </t-col>
      <t-col :span="6">
        <t-form-item name="channel" label="Channel">
          <t-select v-model="formData.channel" />
        </t-form-item>
      </t-col>
    </t-row>

    <div v-for="(owner, index) in formData.owners" :key="owner.id">
      <t-form-item :name="`owners[${index}].name`" label="Owner">
        <t-input v-model="owner.name" />
      </t-form-item>
    </div>

    <t-space>
      <t-button theme="default" variant="outline">Cancel</t-button>
      <t-button theme="primary" type="submit">Submit</t-button>
    </t-space>
  </t-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const formRef = ref();
const formData = ref({
  name: '',
  channel: '',
  owners: [{ id: 1, name: '' }],
});

const rules = {
  name: [{ required: true, message: 'Please input name' }],
  channel: [{ required: true, message: 'Please select channel' }],
};

function handleSubmit() {
  // submit request
}
</script>
```

## Implementation Checklist

- [ ] UI library identified
- [ ] UI components preferred over raw HTML/CSS
- [ ] Visibility state uses `v-model` + `defineModel`
- [ ] Input/submit areas use UI form components
- [ ] Dynamic form items use path-style `name`
- [ ] Inline/horizontal layout uses row/col/space components first
- [ ] New custom CSS minimized
- [ ] Existing project style conventions preserved
