---
name: frontend-project-structure
description: Enforces modular frontend page and component folder architecture in Vue/TypeScript projects. Use when creating pages, splitting complex pages, organizing components/public-private boundaries, or defining components/tabs/steps/modules directory conventions. Not for backend contract alignment or API joint-debugging decisions.
---

# Frontend Project Structure

## Purpose

Apply a consistent, scalable structure for frontend page development with clear module boundaries, complete supporting artifacts, and predictable component placement.

## Trigger Boundary

Use this skill for folder architecture and component/module placement.

Do not use this skill as the primary rule set for:

- Backend contract alignment
- API field/domain reconciliation
- Joint-debugging process with backend

For those tasks, use `frontend-api-integration-joint-debugging`.

## Core Rules

### 1) Page Feature Development

During page feature development, always follow componentized and modularized development.

For each feature/module, make sure the following are defined and organized by module:

- Enums
- Types/Interfaces (if the project supports TypeScript)
- Constants
- API layer definitions

If the project does not already have these directories under `src`, create them immediately:

- `src/enums`
- `src/interface`
- `src/constants`
- `src/api`

Do not leave these artifacts implicit inside page files when they belong to reusable module definitions.

### 2) Component Development

#### Vue implementation baseline

For all Vue component implementation details, fully follow the existing skill: `vue-best-practices`.

#### Public vs private components

Classify components by reuse scope:

- Reusable shared components (for example, headers used across multiple pages) go to:
  - `components/public`
- Page- or feature-private components go to:
  - `components/private`

Always choose location based on actual reuse intent, not temporary convenience.

#### Component folder-first rule

Create a dedicated folder for each component before creating the component file, so the component can evolve with internal subcomponents without restructuring later.

Recommended pattern:

- `Layout/Layout.vue`
- `Layout/components/Header.vue`
- `Layout/components/Content.vue`

Use this folder-first pattern for both shared and private components.

### 3) Complex Page Structure

For complex pages, split by component nature and place files in purpose-specific folders:

- General/simple business components:
  - `views/<page>/components`
- Multi-tab pages:
  - `views/<page>/tabs`
- Multi-step pages:
  - `views/<page>/steps`
- Page sections with actual module-level business meaning:
  - `views/<page>/modules`

Examples of module-level units include:

- Header module
- Filter module
- List module
- Detail module

For example, if a page contains a header module, list module, filter module, and detail module, place these modules under `views/<page>/modules`. For pages completed through multiple steps, place each step component under `views/<page>/steps`.

Structure examples:

Example A: Standard complex page (components + modules)

```text
src/views/agent-center/
  index.vue
  components/
    SearchBar.vue
    BatchActionBar.vue
  modules/
    HeaderModule/
      HeaderModule.vue
    FilterModule/
      FilterModule.vue
    ListModule/
      ListModule.vue
    DetailModule/
      DetailModule.vue
```

Example B: Multi-tab page

```text
src/views/evaluation-center/
  index.vue
  tabs/
    OverviewTab.vue
    CasesTab.vue
    MetricsTab.vue
  components/
    PageToolbar.vue
```

Example C: Multi-step page (step components)

```text
src/views/evaluation-set/create/
  index.vue
  steps/
    BasicConfigStep/
      BasicConfigStep.vue
    FieldMappingStep/
      FieldMappingStep.vue
    ConfirmSubmitStep/
      ConfirmSubmitStep.vue
  components/
    StepProgress.vue
```

The goal is to keep page architecture discoverable: structure should reveal responsibility.

## Execution Checklist

Use this checklist whenever you implement or refactor a page:

- [ ] Confirm componentized and modularized page plan before coding
- [ ] Add/update module-level enums
- [ ] Add/update module-level types/interfaces (TypeScript projects)
- [ ] Add/update module-level constants
- [ ] Add/update module-level API definitions
- [ ] Ensure `src/enums`, `src/interface`, `src/constants`, `src/api` exist
- [ ] Classify components into `components/public` or `components/private`
- [ ] Use folder-first component creation pattern
- [ ] For complex pages, place units into `components`, `tabs`, `steps`, and `modules` as appropriate
- [ ] Validate no cross-scope placement mistakes remain

## Decision Rules

When uncertain where code belongs, decide in this order:

1. Is it cross-page reusable?
   - Yes -> `components/public`
   - No -> continue
2. Is it a page-specific view piece?
   - Yes -> `components/private` or `views/<page>/components`
   - No -> continue
3. Is it a tab-level section?
   - Yes -> `views/<page>/tabs`
   - No -> continue
4. Is it a step in a multi-step flow?
   - Yes -> `views/<page>/steps`
   - No -> continue
5. Does it represent a business module (list/detail/etc.)?
   - Yes -> `views/<page>/modules`

Prefer explicit module boundaries over large mixed files.
