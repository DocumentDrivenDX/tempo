---
ddx:
  id: FEAT-004
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-004 — Budgets and Rates

**Feature ID**: FEAT-004
**Priority**: P1
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Budgets and Rates
**Covered PRD Requirements**: FR-12, FR-13, FR-14
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

Project budgets, billable rates, and budget consumption display. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

BUD-01. Optional hours and dollar budgets with alert threshold (FR-12).
BUD-02. Rates per user with per-project override, effective-dated (FR-13).
BUD-03. Consumed and remaining shown and flagged (FR-14).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-007](../user-stories/US-007.md)
- [US-008](../user-stories/US-008.md)

## Edge Cases and Error Handling

- No rate set: entry has hours but no dollars and is flagged.
- Rate change after approval does not alter approved entries.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: FEAT-001 (identity)
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-12, FR-13, FR-14

## Out of Scope

- Invoicing; task-level budgets (parking lot).
