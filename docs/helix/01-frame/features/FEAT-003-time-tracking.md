---
ddx:
  id: FEAT-003
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-003 — Time Tracking

**Feature ID**: FEAT-003
**Priority**: P0
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Time Tracking
**Covered PRD Requirements**: FR-7, FR-8, FR-9, FR-10, FR-11, FR-22, FR-23, FR-24, FR-25
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

Server-held timer, manual entries, editing until approval, the week view, time zone capture on every entry, and a configurable week start. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

TIME-01. One running timer per user, held server-side (FR-7, FR-11).
TIME-02. Manual entries in whole minutes (FR-8).
TIME-03. Edit and delete own entries until approved (FR-9).
TIME-04. A week view with daily and weekly totals as a UI affordance, using the configured week start (FR-10, FR-25).
TIME-05. Each user has a time zone, defaulted from the browser and changeable (FR-22).
TIME-06. Every entry records its start instant, IANA time zone, UTC offset, and local date (FR-23).
TIME-07. Entries crossing local midnight are split at midnight in the entry time zone (FR-24).
TIME-08. Admins configure the week start; the default is Sunday (FR-25).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-005](../user-stories/US-005.md)
- [US-006](../user-stories/US-006.md)
- [US-014](../user-stories/US-014.md)
- [US-015](../user-stories/US-015.md)

## Edge Cases and Error Handling

- Timer left running overnight: user can stop and correct the duration.
- Entry on an archived project is refused.
- Daylight-saving change inside an entry: duration is the elapsed time; start and offset are stored.
- User changes profile time zone: past entries keep their recorded zone.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: FEAT-001 (identity)
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-7, FR-8, FR-9, FR-10, FR-11, FR-22, FR-23, FR-24, FR-25

## Out of Scope

- Idle detection, screenshots, concurrent timers.
