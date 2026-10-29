---
ddx:
  id: SPIKE-001
  authoring:
    home: repo
  links:
    - ADR-004
---

# Technical Spike: Entra app roles through SWA to a linked Functions API

**Spike ID**: SPIKE-001 | **Lead**: Implementer | **Time Budget**: 0.5 day | **Status**: Not started

## Objective

**Technical Question**: Does the SWA roles function receive the Entra `roles` claim, and does it work when the API is a linked bring-your-own Functions app?

**Goals**:
- [ ] Deploy a minimal SWA with custom Entra authentication and a linked Functions app.
- [ ] Assign an Entra app role to a test user and confirm it reaches `x-ms-client-principal.userRoles`.
- [ ] Confirm the Functions app rejects calls that bypass SWA.

**Success Criteria**: Evidence gathered, recommendation with rationale, risks identified.

**Out of Scope**: Production implementation.

## Hypothesis

**Primary**: The roles function receives the `roles` claim and works with a linked backend.
**Assumptions**: SWA Standard plan; tenant admin can create app roles.
**Expected Outcome**: ADR-004 accepted as written.

## Approach

**Method**: Integration testing.

| Day | Activity | Objective |
|-----|----------|-----------|
| 1 | Minimal SWA, Entra app registration, roles function, linked Functions app | Observe principal and claims |

## Recommendations

**RECOMMENDATION**: If the hypothesis fails, use the fallback in ADR-004 (role column managed by Admins, bootstrap Admin from a setting) and update FR-2 wording.
- **Concern Impact**: None expected; ADR-004 would be amended.
