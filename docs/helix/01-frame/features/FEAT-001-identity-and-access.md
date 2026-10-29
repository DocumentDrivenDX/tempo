---
ddx:
  id: FEAT-001
  authoring:
    home: repo
  links:
    - prd
---

# Feature Specification: FEAT-001 — Identity and Access

**Feature ID**: FEAT-001
**Priority**: P0
**Owner**: Erik LaBianca
**Covered PRD Subsystem(s)**: Identity and Access
**Covered PRD Requirements**: FR-1, FR-2, FR-3
**Cross-Subsystem Rationale**: None — single subsystem.

## Overview

Sign-in through Entra ID with Admin and Member roles, auto-provisioning, deactivation, and server-side authorization. It implements the PRD subsystem of the same name.

## Ideal Future State

Staff and managers complete this part of their week without help or workarounds, and the data it produces is trusted by reports and approvals.

## Problem Statement

- **Current situation**: Everhour provides this capability under a separate login and per-seat licence.
- **Pain points**: Cost, separate identity, and data held by a vendor.
- **Desired outcome**: Equivalent behavior inside Tempo with company identity and data ownership.

## Requirements

### Functional Requirements by Area

AUTH-01. Sign-in uses the company Entra tenant only (FR-1).
AUTH-02. First sign-in creates the user with role from Entra app role, default Member (FR-2).
AUTH-03. Admins deactivate users; deactivated users cannot sign in (FR-2).
AUTH-04. Every API call checks role and project membership (FR-3).

### Non-Functional Requirements

- **Performance**: 95th percentile API response under 500 ms when warm; first request after idle may be slower.
- **Security**: Server-side authorization on every call (FR-3, FR-21).
- **Scalability**: Up to 50 users and 5 years of entries.
- **Reliability**: Daily backups; no data loss on timer or approval actions.

## User Stories

- [US-001](../user-stories/US-001.md)
- [US-002](../user-stories/US-002.md)

## Edge Cases and Error Handling

- Entra token lacks a role claim: user is Member.
- User removed from tenant: next sign-in fails; history kept.

## Success Metrics

- Contributes to the PRD metrics: 90% of hours logged within 24 hours; approvals within 3 working days.

## Constraints and Assumptions

- Serverless Azure, Node.js runtime, Entra ID single tenant (see concerns.md).

## Dependencies

- **Other features**: None
- **External services**: Entra ID; Azure SQL (exact interface surface lives in Contracts, Design activity)
- **PRD requirements**: FR-1, FR-2, FR-3

## Out of Scope

- Roles beyond Admin and Member; guest or external users.
