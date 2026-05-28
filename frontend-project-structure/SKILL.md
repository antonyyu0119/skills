---
name: frontend-project-structure
description: Enforces modular frontend project structure for page and component development in Vue/TypeScript projects. Use when creating new pages, refactoring page architecture, organizing components, or when the user mentions componentization, modularization, enums, interfaces/types, constants, API modules, tabs, modules, or folder conventions.
---

# Frontend Project Structure

## Purpose

Apply a consistent, scalable structure for frontend page development with clear module boundaries, complete supporting artifacts, and predictable component placement.

## Core Rules

### 1) Page Requirement Development

When implementing a page feature, always follow componentized and modularized development.

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
- Semantically independent business modules:
  - `views/<page>/modules`

Examples of module-level units include:

- List module
- Detail module
- Step modules for multi-step flows

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
