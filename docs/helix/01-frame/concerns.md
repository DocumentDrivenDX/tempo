---
ddx:
  id: concerns
  authoring:
    home: repo
---

# Project Concerns

## Active Concerns

| Concern | Source | Areas | Why Active | Key Practices | Selection |
|---------|--------|-------|------------|---------------|-----------|
| language-runtime: TypeScript on Node.js | assumption | `area:api`, `area:ui` | Azure Functions (managed SWA API) runs Node, not Bun; one language across API and UI. Overrides the shipped `typescript-bun` default. | Strict TS; shared types for API contracts; managed Functions only (no containers) | operator-override |
| frontend-framework: react-vite | assumption | `area:ui` | SPA served as static content on Azure Static Web Apps; Next.js SSR adds hosting complexity with no stated need. Overrides shipped `react-nextjs` default. | SPA, client-side routing, timer state in-browser | assumption (validate in design) |
| deploy-target: Azure Static Web Apps + managed Functions | operator-override (cloud = Azure, serverless, low cost) | `area:infra` | Operator chose Azure; SWA Standard supports custom Entra registration and custom roles. | IaC for all resources; scale-to-zero | operator-override |
| auth-provider: Microsoft Entra ID (OIDC) | operator-override | `area:api`, `area:data` | Operator requires Entra ID. Overrides shipped `auth-local-sessions`. Project-local filler; no library concern exists. | Single-tenant app registration; Admin/Member as Entra app roles or group claims; no local passwords | operator-override |
| datastore: Azure SQL Database serverless (free offer) | assumption | `area:data` | Relational data (projects, tasks, time entries, rates, approvals) and aggregate reports; free offer + auto-pause fits low cost. Cosmos DB serverless and PostgreSQL Flexible Server remain alternatives for an ADR. | Migrations in repo; backups verified; tolerate cold-start resume | assumption (ADR required) |
| scope-discipline | library | all | Replacing a commercial tool invites feature creep. | Hold v1 to named Everhour-parity features | assumption |
| security-owasp | library | `area:api`, `area:ui` | Authenticated business data incl. billing rates. | Server-side authorization on every call | assumption |
| authorization-model | library | `area:api` | Admin, Member, and Accountant roles plus per-project membership, approvals, and period close. | Central policy checks | assumption |
| auth | library | `area:api`, `area:ui` | Account-based product: sign-in, sessions, server-side RBAC through the principal (FR-1 to FR-3). Mechanism is the Entra ID filler above. | Resolve principal on every call; no hardcoded provider | assumption (Frame selection) |
| admin-console | library | `area:ui` | Admins and Managers manage mutable domain objects (users, projects, members, rates, approvals) through the UI. | Primary operator workflow (create project, approve week) covered by whole-stack e2e | assumption (Frame selection) |
| testing | library | all | Timer logic, rate and budget math, and approvals need a deliberate test strategy. | Unit tests for domain rules; API tests against a real database schema | operator-override |
| verification | library | all | Evidence-based completion and a pre-merge gate. | Tests and checks pass in CI before merge | operator-override |
| e2e-playwright (e2e-framework slot) | shipped-default | `area:ui` | Core flows: sign in, timer, entry approval. | Playwright against a deployed preview with a test Entra identity | operator-override |
| modularity-and-encapsulation | library | `area:api`, `area:ui` | Handwritten TypeScript needs clear module boundaries; detailed boundaries are decided in Design. | Narrow public interfaces; boundary checks in CI | operator-override |
| code-shape-ceilings | library | all | Keeps files and functions small and reviewable. | Size ceilings enforced by lint/CI | operator-override |
| o11y-otel | library | `area:api`, `area:infra` | Serverless cold starts and errors are hard to see otherwise. | OpenTelemetry to Application Insights; trace each request | operator-override |
| a11y-wcag-aa | library | `area:ui` | Staff use the app daily. | WCAG 2.1 AA; keyboard-operable timer | operator-override |
| relational-data-modeling | library | `area:data` | Azure SQL schema for projects, tasks, entries, rates, approvals. | Versioned migrations; constraints in the schema | operator-override |

## Project Overrides

| Concern | Practice | Override | Authority |
|---------|----------|----------|-----------|
| language-runtime | typescript-bun default | Node.js runtime on managed Functions (operator wants fully serverless) | Operator instruction; ADR to record |
| frontend-framework | react-nextjs default | react-vite | Needs ADR |
| auth-provider | auth-local-sessions default | Entra ID | Operator instruction |

## Area Labels

- `area:ui` — React SPA
- `area:api` — Azure Functions endpoints
- `area:data` — Azure SQL schema and migrations
- `area:infra` — Azure resources, CI/CD, Entra app registration

## Concern Conflicts

| Conflict | Resolution |
|----------|------------|
| Low cost (auto-pause) vs. timer responsiveness | Accept cold-start latency on first request; revisit in design if it harms UX. |

## Source-Code Boundaries

`modularity-and-encapsulation`: active (see table); module boundaries and checker design are decided in Design.
