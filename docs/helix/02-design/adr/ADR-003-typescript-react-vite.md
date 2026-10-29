---
ddx:
  id: ADR-003
  authoring:
    home: repo
  links:
    - ADR-001
---

# ADR-003: TypeScript on Node.js with a React and Vite single-page app

## Problem

HELIX defaults to TypeScript on Bun with React/Next.js. Azure Functions runs Node.js, and the app is a static SPA behind SWA, so Bun at runtime and Next.js server rendering do not fit.

## Decision

We will write the API and the SPA in TypeScript (strict) on Node.js 22, build the SPA with Vite and React, and keep one repository with pnpm workspaces. Shared request and response types live in a contracts package used by both sides.

## Why We Chose This

### Over Bun at runtime
Functions does not run Bun without a custom handler or containers, which the operator ruled out in favor of pure serverless.

### Over Next.js
There is no server-rendering need; SWA serves static assets and `/api` already exists.

## Consequences

**Good**: One language end to end; shared types prevent client/server drift; simple static hosting.

**Trade-offs**: Client-side rendering only; no Bun speed in tooling.

**Drift signals to watch**: Duplicate hand-written API types in the SPA; server-rendering dependencies.

## Concern Impact

- **Override / deviation**: Ratifies the `language-runtime` and `frontend-framework` overrides in `concerns.md` Project Overrides.
