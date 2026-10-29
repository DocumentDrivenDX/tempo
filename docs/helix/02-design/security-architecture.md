---
ddx:
  id: security-architecture
  authoring:
    home: repo
  links:
    - ADR-004
    - ADR-006
    - ADR-007
---

# Security Architecture

**Scope**: Tempo SPA, linked Functions API, Azure SQL database.

## Decision

Authentication is delegated to Entra ID through SWA. Authorization is enforced in the API by a single domain `Policy`, with period close and audit integrity enforced again in the database. The API holds no secrets: database access uses managed identity.

## Trust Boundaries

| Boundary | Assets | Trust Change | Control |
|----------|--------|--------------|---------|
| Browser to SWA | Session cookie | Untrusted client to edge | HTTPS only; SWA route rules require authentication on every path except the sign-in pages |
| SWA to API | User principal header | Edge to application | API accepts calls only from the linked SWA; header parsed, never client-supplied |
| API to database | All data | Application to data | Managed identity; least-privilege database roles |

## Control Mapping

| Threat / Risk | Control | Implementation Surface | Verification |
|---------------|---------|-------------------------|--------------|
| Member reads another project's data | Project-membership checks in `Policy` and in query filters | `domain/policy`, repositories | Authorization matrix test (every endpoint by every role) |
| Rates exposed to Members | Rate fields omitted unless Admin, Accountant, or the project's Manager | Response mappers | Contract tests on field presence |
| Edit inside a closed period | Service check plus database trigger | `application`, migration trigger | Trigger test; use-case test |
| Audit tampering | No update/delete grant; same-transaction writes | Migration grants | Permission test |
| Forged principal header | API restricted to SWA; no public Functions endpoint | Functions access restriction | Deployment check |
| Excess Admin power unnoticed | Admin overrides audited with `.override` | Audit writer | Audit test |

## Identity and Access

- Authentication: Entra ID, single tenant, via SWA custom authentication.
- Authorization: global roles Admin, Member, Accountant; per-project roles Manager and Contributor. Matrix: Admin may do everything. Accountant may read everything (including amounts), close and reopen periods, and run reports, but not approve or reject. Manager may manage their projects, members, tasks, budgets, and approve or reject their project's stopped entries. Member may manage their own entries and timer and see projects they belong to.
- Session or token handling: SWA manages the session cookie; the API receives no tokens.

## Data Protection

- Data at rest: Azure SQL transparent data encryption; backups encrypted.
- Data in transit: TLS everywhere, including the database connection.
- Secrets and key handling: none stored; the Entra app client secret (SWA custom auth) is kept in SWA application settings.

## Logging and Monitoring

- Security events: failed authorization decisions logged to Application Insights without personal data beyond user id.
- Alerting: alert on spikes of denied requests and on `.override` audit actions.
- Audit trail: `audit_log` (ADR-007).

## Residual Risk

- Role changes in Entra take effect only at next sign-in; accepted for a small trusted team.
- Admins hold broad power by design; mitigated by audit and alerting.

## Security Test Hooks

- Role-by-endpoint authorization matrix test.
- Database test proving the closed-period trigger and the audit permission denial.
- Check that the Functions app rejects requests that do not come through SWA.
