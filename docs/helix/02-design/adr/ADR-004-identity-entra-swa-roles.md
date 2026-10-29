---
ddx:
  id: ADR-004
  authoring:
    home: repo
  links:
    - ADR-001
    - SPIKE-001
---

# ADR-004: Entra ID through SWA custom authentication, roles from Entra app roles

## Problem

The PRD requires Entra-only sign-in (FR-1), a global role of Admin, Member, or Accountant from Entra (FR-2), and server-side authorization (FR-3). The Functions API must trust the identity without validating tokens itself.

## Decision

We will register a single-tenant Entra application and configure SWA custom authentication for it. The SWA roles function (`rolesSource`) maps the Entra `roles` claim values (`Admin`, `Member`, `Accountant`) to SWA roles; users with no app role receive `Member`. The API reads the `x-ms-client-principal` header supplied by SWA, upserts the user row on each authenticated request, and applies the authorization policy in the domain module. The API accepts requests only from the linked SWA. The user's global role is cached in `users.role` for reports and display; the request principal remains authoritative.

## Why We Chose This

### Over validating Entra tokens in the API
It duplicates what SWA already does at the edge and adds MSAL and JWKS code and failure modes.

### Over a role table maintained in Tempo
Admins would manage roles in two places. Entra already holds the directory and group assignments.

## Consequences

**Good**: No auth code in the SPA beyond redirects; roles follow the company directory.

**Trade-offs**: The principal header lacks the full claims array ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/user-information)), so roles rely on the roles function. Role changes take effect at next sign-in. Whether the roles function receives the `roles` claim and works with a linked Functions app is unproven; SPIKE-001 must confirm it. Fallback: a `users.role` column managed by Admins and seeded from a bootstrap Admin setting.

**Drift signals to watch**: Local passwords; role checks in the SPA only; trusting a client-supplied role.

## Concern Impact

- **Override / deviation**: Ratifies the `auth-provider` override (Entra ID in place of local sessions) in `concerns.md`.
