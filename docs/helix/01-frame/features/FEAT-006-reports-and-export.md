---
ddx:
  id: FEAT-006
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-006 — Reports and Export

**Feature ID**: FEAT-006
**Priority**: P0
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Reports and Export
**Covered PRD Requirements**: FR-19, FR-20, FR-21
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

Hours and amount reports with CSV export and rate visibility rules. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

REP-01. Group by project, user, task, or day over a date range (FR-19).
REP-02. CSV export matches on-screen totals (FR-20).
REP-03. Rates and amounts visible only to Admins and project Managers (FR-21).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-012](../user-stories/US-012.md)
- [US-013](../user-stories/US-013.md)

## Edge Cases and Error Handling

- Empty range: empty report and header-only CSV.
- Member requests another user's hours: denied.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: FEAT-001 (identity)
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-19, FR-20, FR-21

## Out of Scope

- Scheduled reports, saved filters (parking lot), invoices.
