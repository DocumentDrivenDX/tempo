---
ddx:
  id: FEAT-005
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-005 — Entry Approval

**Feature ID**: FEAT-005
**Priority**: P0
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Entry Approval
**Covered PRD Requirements**: FR-15, FR-16, FR-17, FR-18, FR-27
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

Entry-level approval: pending entries, per-project manager approval or rejection, locking, reopening, accounting period close, and audit trail. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

APPR-01. Entries are pending from creation; managers list pending entries for their projects, filtered by user, project, and date range (FR-15).
APPR-02. Managers approve or reject stopped entries individually or in bulk, with a comment on rejection; Admins may do so for any entry; Accountants may not (FR-16).
APPR-03. Approved entries lock; Admin reopens (FR-17).
APPR-04. Audit trail of every action (FR-18).
APPR-05. Accountants and Admins close and reopen accounting periods, even while entries are unapproved; a closed period blocks all entry changes in it (FR-27).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-009](../user-stories/US-009.md)
- [US-010](../user-stories/US-010.md)
- [US-011](../user-stories/US-011.md)
- [US-017](../user-stories/US-017.md)

## Edge Cases and Error Handling

- Entries on several projects: each project's managers approve only their own project's entries.
- Entry with a running timer: not approvable until stopped.
- The two halves of a midnight-split entry can be approved together or separately.
- Entry in a closed period: no create, edit, delete, approve, reject, or reopen by any role; an Admin or Accountant must reopen the period first.
- Unapproved entries in a period at close are locked as they are and stay unapproved.
- Project with no Manager: Admins approve.
- A Manager approves their own entries; the audit trail records the actor and that it was a self-approval.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: FEAT-001 (identity)
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-15, FR-16, FR-17, FR-18, FR-27

## Out of Scope

- Delegated or automatic approval; payroll integration; per-project or per-client period close.
