---
name: frontend-project-structure
description: Enforces modular frontend project structure for page and component development in Vue/TypeScript projects. Use when creating new pages, refactoring page architecture, organizing components, or when the user mentions componentization, modularization, enums, interfaces/types, constants, API modules, tabs, modules, or folder conventions.
---

# Frontend Project Structure

## Purpose

Apply a consistent, scalable structure for frontend page development with clear module boundaries, complete supporting artifacts, and predictable component placement.

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

### 2) API Integration and Joint-Debugging

During API integration and joint-debugging in Rule 2, the modularization and artifact requirements defined in Rule 1 must still be followed. At the same time, the integration process should follow a backend-interface-first standardization principle.

For all API-related module artifacts (enums, types/interfaces, constants, and API definitions):

- Prefer backend contract standards over ad-hoc frontend naming or temporary mappings
- Keep names, value domains, and field semantics aligned with backend interfaces
- Consolidate duplicated local variants into unified backend-aligned definitions
- If display adaptation is needed, still prioritize backend fields. Only when the gap is substantial (for example, completely incompatible types), use explicit transformation logic, while preserving the integrity of base definitions as much as possible

### 3) Component Development

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

### 4) Complex Page Structure

For complex pages, split by component nature and place files in purpose-specific folders:

- General/simple business components:
  - `views/<page>/components`
- Multi-tab pages:
  - `views/<page>/tabs`
- Page sections with actual module-level business meaning:
  - `views/<page>/modules`

Examples of module-level units include:

- Header module
- Filter module
- List module
- Detail module
- Step modules for multi-step flows

For example, if a page contains a header module, list module, filter module, and detail module, place these modules under `views/<page>/modules`. For pages completed through multiple steps, place each step module under `views/<page>/modules`.

The goal is to keep page architecture discoverable: structure should reveal responsibility.

## Execution Checklist

Use this checklist whenever you implement or refactor a page:

- [ ] Confirm componentized and modularized page plan before coding
- [ ] Add/update module-level enums
- [ ] Add/update module-level types/interfaces (TypeScript projects)
- [ ] Add/update module-level constants
- [ ] Add/update module-level API definitions
- [ ] During API integration, prioritize backend contract standards and unify enums/types/constants/APIs accordingly
- [ ] Ensure `src/enums`, `src/interface`, `src/constants`, `src/api` exist
- [ ] Classify components into `components/public` or `components/private`
- [ ] Use folder-first component creation pattern
- [ ] For complex pages, place units into `components`, `tabs`, and `modules` as appropriate
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
4. Does it represent a business module (list/detail/step/etc.)?
   - Yes -> `views/<page>/modules`

Prefer explicit module boundaries over large mixed files.
