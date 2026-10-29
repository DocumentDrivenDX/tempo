---
ddx:
  id: ADR-007
  authoring:
    home: repo
  links:
    - ADR-002
---

# ADR-007: Append-only audit log in the database

## Problem

FR-18 and FR-27 require approvals, rejections, reopenings, period closes, and Admin overrides to be recorded with actor, time, and comment, in a way the application cannot quietly alter.

## Decision

We will keep an `audit_log` table written in the same transaction as the change it records. The API's database identity has `INSERT` and `SELECT` on it but not `UPDATE` or `DELETE`. Each row records time (UTC), actor user, actor global role, action, entity type and id, a JSON detail, and an optional comment. Admin overrides carry the action suffix `.override`.

## Why We Chose This

### Over logging to Application Insights
Logs are sampled and expire; the audit trail must be complete and queryable by reports.

### Over event sourcing
It is more machinery than the PRD needs.

## Consequences

**Good**: Transactional consistency; tamper resistance from permissions; easy to query.

**Trade-offs**: Table grows with activity (small at 50 users); detail JSON schema needs discipline.

**Drift signals to watch**: Audit writes outside the transaction; grants of update or delete on the table.

## Concern Impact

- **No concern impact**.
