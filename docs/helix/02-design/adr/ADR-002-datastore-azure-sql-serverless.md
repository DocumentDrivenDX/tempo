---
ddx:
  id: ADR-002
  authoring:
    home: repo
  links:
    - ADR-001
---

# ADR-002: Use Azure SQL Database serverless as the datastore

## Problem

Tempo's data is relational (projects, members, tasks, entries, rates, audit) and its core outputs are aggregations over date ranges, plus integrity rules such as period close. The datastore must be near-zero cost when idle and durable.

## Decision

We will use Azure SQL Database in the serverless General Purpose tier, starting on the free offer while its monthly allowance covers usage, with auto-pause enabled. The API authenticates with the Functions app's managed identity (Entra authentication; no SQL logins). Schema changes ship as versioned migrations.

## Why We Chose This

### Over Cosmos DB serverless
Reports group and sum across many entries, and period close needs multi-row constraints and triggers. A document store makes both harder and costlier.

### Over PostgreSQL Flexible Server
It is not serverless; the burstable tier costs roughly $12-15 per month even when idle ([Mark Heath](https://markheath.net/post/which-azure-database-serverless)).

## Consequences

**Good**: Strong integrity (foreign keys, check constraints, triggers); low idle cost; Entra-based access.

**Trade-offs**: Auto-pause adds seconds of resume latency on the first request after idle (PRD risk). The free offer has a monthly vCore-second cap, so usage must be measured; fall back to paid serverless if exceeded.

**Drift signals to watch**: SQL logins or passwords; business rules only in the SPA; keep-warm hacks added without measurement.

## Concern Impact

- **Override / deviation**: Resolves the `datastore` assumption in `concerns.md`.
