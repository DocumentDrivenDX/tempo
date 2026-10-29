---
ddx:
  id: FEAT-002
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-002 — Projects and Tasks

**Feature ID**: FEAT-002
**Priority**: P0
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Projects and Tasks
**Covered PRD Requirements**: FR-4, FR-5, FR-6
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

Projects, project membership with Manager or Contributor roles, and tasks used to label time. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

PROJ-01. Create, edit, archive projects (FR-4).
PROJ-02. Assign members as Manager or Contributor (FR-5).
PROJ-03. Create, rename, complete, archive tasks (FR-6).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-003](../user-stories/US-003.md)
- [US-004](../user-stories/US-004.md)

## Edge Cases and Error Handling

- Archiving a project with a running timer stops the timer.
- Removing a member keeps their past entries.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: FEAT-001 (identity)
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-4, FR-5, FR-6

## Out of Scope

- Assignees, due dates, boards, comments.
