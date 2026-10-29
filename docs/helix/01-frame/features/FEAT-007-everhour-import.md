---
ddx:
  id: FEAT-007
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-007 — Everhour Import

**Feature ID**: FEAT-007
**Priority**: P1
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Everhour Import
**Covered PRD Requirements**: FR-22, FR-23
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

One-time CSV import of Everhour history with dry run and idempotent commit. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

IMP-01. Dry run reports counts and unmatched rows (FR-22).
IMP-02. Commit is idempotent (FR-22).
IMP-03. Imported entries approved and locked; users matched by email (FR-23).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-014](../user-stories/US-014.md)

## Edge Cases and Error Handling

- Unmatched user email: row reported, nothing created for it.
- Malformed CSV: rejected with line numbers.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: FEAT-001 (identity)
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-22, FR-23

## Out of Scope

- Ongoing sync with Everhour.
