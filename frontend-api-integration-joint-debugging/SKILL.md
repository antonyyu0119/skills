---
name: frontend-api-integration-joint-debugging
description: Standardizes frontend API contract alignment and backend joint-debugging, including enum/type/constant/API consistency and explicit transformation boundaries. Use when integrating APIs, reconciling response fields/domains, or handling interface joint-debugging and contract mismatches. Not for page/component folder structure decisions.
---

# Frontend API Integration and Joint-Debugging

## Purpose

Keep frontend API integration consistent, backend-aligned, and maintainable during implementation and joint-debugging.

## Trigger Boundary

Use this skill for API contract alignment and joint-debugging behavior.

Do not use this skill as the primary rule set for:

- `views/<page>/components|tabs|modules` placement
- `components/public` vs `components/private` placement
- Folder-first component creation conventions

For those tasks, use `frontend-project-structure`.

## Core Rules

### 1) Contract-First Integration

During API integration and joint-debugging, always follow a backend-interface-first standardization principle.

For all API-related module artifacts:

- Enums
- Types/Interfaces
- Constants
- API definitions

Apply these rules:

- Prefer backend contract standards over ad-hoc frontend naming or temporary mappings
- Keep names, value domains, and field semantics aligned with backend interfaces
- Consolidate duplicated local variants into unified backend-aligned definitions
- If display adaptation is required, still preserve backend-aligned base definitions and place adaptation in explicit transformation logic

### 2) Transformation Boundaries

When backend fields do not directly match UI display needs:

- Keep raw backend model definitions intact in base types/interfaces
- Add explicit adapters/transformers at module boundaries (for example, mapper functions)
- Do not silently mutate base enums/types/constants into UI-only semantics

Prefer this flow:

1. Define backend-aligned base model
2. Define UI view model only when needed
3. Map base -> view model in explicit transformation layer

### 3) Debugging Checklist in Joint Sessions

During backend-frontend joint-debugging:

- Validate field names and value domains against backend docs or contract outputs
- Confirm optional/nullable fields are reflected in types
- Verify enum domains match backend real responses
- Remove temporary compatibility hacks once contract is stable

## Execution Checklist

- [ ] Backend contract is identified before coding API layer
- [ ] Enums/types/constants/APIs are backend-aligned
- [ ] No duplicated local variants remain after alignment
- [ ] UI adaptation uses explicit transformation logic
- [ ] Base definitions remain contract-faithful
- [ ] Joint-debugging findings are merged back into module artifacts

## Relationship with Other Skills

Use this skill together with `frontend-project-structure`:

- `frontend-project-structure` defines where artifacts should live
- This skill defines how API artifacts should align with backend contracts during integration and joint-debugging
