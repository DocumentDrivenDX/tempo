---
ddx:
  id: prd
  authoring:
    home: repo
  links:
    - product-vision
kind: product
---

# Product Requirements Document

## Summary

Tempo is a web app where Synaptiq staff track time against projects and tasks, project managers set budgets and approve entries, admins manage the system, and accountants close periods and report and export hours. It replaces Everhour, signs users in with Entra ID, and runs on serverless Azure for under $30 a month. v1 covers sign-in, projects and tasks, a timer and manual entry, budgets and rates, weekly approval, and reports with CSV export. Every entry records its time zone so local working hours and month ends are exact. Success is 90% of hours logged within 24 hours, Everhour cancelled within 6 months, and approvals within 3 working days.

## Problem and Goals

### Problem

Synaptiq pays Everhour roughly $8.50-$10 per seat per month, manages a second identity for time tracking, and keeps time data in a vendor's system. Project managers cannot see budget burn alongside company identity and access.

### Goals

1. Staff log time in seconds, by timer or by hand, against a project and task.
2. Managers approve hours entry by entry and see budget burn without spreadsheets.
3. Synaptiq owns its data and retires Everhour.

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Hours logged within 24 hours of work | 90% by 3 months after launch | Entry `created_at` vs entry date, monthly SQL report |
| Entries approved within 3 working days of being logged | 90% | Entry creation and approval timestamps |
| Monthly Azure cost at current team size | Under $30 | Azure Cost Management |
| Everhour subscription cancelled | Within 6 months of launch | Finance confirmation |

### Non-Goals

- Invoicing, payments, or expense tracking.
- Screenshots, activity monitoring, or idle detection.
- Resource planning, capacity forecasting, or Gantt charts.
- Full task management (assignees, due dates, boards, comments); tasks are labels for time.
- Multi-tenant or external-customer access; Tempo serves one Entra tenant.
- Native mobile apps; the web app is responsive.
- Third-party integrations such as Jira, Asana, or GitHub.

Deferred items tracked in `docs/helix/parking-lot.md`.

## Users and Scope

### Primary Persona: Priya, Member

**Role**: Consultant or engineer at Synaptiq working on client projects
**Goals**: Log hours fast and get her hours approved
**Pain Points**: Forgotten entries, re-keying time, another login

### Secondary Persona: Marcus, Project Manager

**Role**: Member who is a Manager on one or more projects
**Goals**: Approve hours, watch budget burn, catch overruns early
**Pain Points**: Chasing people for hours, building budget reports by hand

### Secondary Persona: Alex, Admin

**Role**: Operations administrator
**Goals**: Manage users, projects, rates, and settings
**Pain Points**: Maintaining the same data in several tools

### Secondary Persona: Dana, Accountant

**Role**: Finance or accounting staff
**Goals**: Close periods so billed and paid hours are final; report and export hours and amounts for billing
**Pain Points**: Hours that change after they have been invoiced or paid

Roles: Entra app roles give each user a global role of Admin, Member, or Accountant. Manager is a per-project membership role held by a Member, not a global role.

## Requirements

### Must Have (P0)

1. Entra ID sign-in with Admin, Member, and Accountant roles and server-side authorization.
2. Projects, project membership, and tasks.
3. Timer and manual time entry with editing, with the time zone recorded on every entry.
4. Per-project manager approval of entries, with locking.
5. Reports by project, user, and date range, with CSV export.
6. Accounting period close, owned by the Accountant role.

### Should Have (P1)

1. Project hour and dollar budgets with consumption display and alert threshold.
2. Billable rates per user, overridable per project.

### Nice to Have (P2)

1. Task-level budgets.
2. Saved report filters.

## Functional Requirements

### Subsystem: Identity and Access

- **FR-1** — Users sign in only through the company Entra ID tenant; Tempo stores no passwords.
- **FR-2** — A user is created on first sign-in with the global role from their Entra app role (Admin, Member, or Accountant; default Member); Admins can deactivate users.
- **FR-3** — Every data access is authorized server-side: Members see only projects they belong to; Admins and Accountants see all.

### Subsystem: Projects and Tasks

- **FR-4** — Admins and project Managers create, edit, and archive projects (name, client, default billable flag); archived projects accept no new time.
- **FR-5** — Admins and project Managers assign project members with the project role Manager or Contributor.
- **FR-6** — Managers and Admins create, rename, complete, and archive tasks within a project.

### Subsystem: Time Tracking

- **FR-7** — A user starts and stops a timer on a project, optionally on a task; starting a second timer stops the first, so a user has at most one running timer.
- **FR-8** — A user adds a manual entry with date, duration in whole minutes, project, optional task, optional note, and billable flag.
- **FR-9** — A user edits or deletes their own entries until the entry is approved; approved entries are read-only.
- **FR-10** — A user sees a week view of their entries by day and project, with daily and weekly totals; the week is a display affordance only and does not affect approval or storage.
- **FR-11** — A running timer is held server-side, so it survives page reloads and shows on other devices.
- **FR-22** — Each user has a profile time zone (IANA name), proposed from the browser on first sign-in and changeable by the user.
- **FR-23** — Every entry stores its start instant in UTC when known, the IANA time zone and UTC offset in force when it was logged, and its local date in that zone; a later change to the profile zone does not alter existing entries.
- **FR-24** — An entry that crosses local midnight in its time zone is split at midnight, so each resulting entry belongs to exactly one local day and month.
- **FR-25** — Admins configure the first day of the week for the organization, default Sunday; it sets the week view and weekly report grouping.

### Subsystem: Budgets and Rates

- **FR-12** — A project may have an hours budget, a dollar budget, or both, with an alert threshold percentage.
- **FR-13** — Admins set a billable rate per user and may override it per project; a rate change applies to entries from its effective date forward and never alters approved entries.
- **FR-14** — A project shows budget consumed and remaining, and flags when the alert threshold or budget is exceeded.

### Subsystem: Entry Approval

- **FR-15** — Entries are pending approval from creation; Managers list pending entries on their projects, filtered by user, project, and date range.
- **FR-16** — Each project's Managers approve or reject that project's stopped entries, individually or in bulk, with a comment on rejection; rejected entries return to editable. A Manager may approve their own entries on a project they manage.
- **FR-17** — Approved entries are locked; an Admin can reopen them unless their period is closed (FR-27), and the reopening is recorded.
- **FR-18** — Approval, rejection, and reopening are recorded in an audit trail with actor, time, and comment.
- **FR-27** — Accountants close accounting periods by setting a close-through date and reopen them by moving it earlier; no entry with a local date on or before the date can be created, edited, deleted, approved, rejected, or reopened while closed, by any role; closing and reopening are recorded in the audit trail.

### Subsystem: Reports and Export

- **FR-19** — Users run reports of hours, and of billable amounts where permitted, grouped by project, user, task, day, week, or month chosen at report time, over a date range, filtered by billable flag and approval status.
- **FR-20** — Any report exports to CSV with the same filters and totals.
- **FR-21** — Rates and dollar amounts are visible only to Admins, Accountants, and Managers of the project concerned; Members see their own hours only.
- **FR-26** — Reports group days and months by each entry's local date by default, can instead bucket by one chosen reporting time zone, and include a time-of-day view of when people work in their local time.

## Acceptance Test Sketches

| Requirement | Scenario | Input | Expected Output |
|-------------|----------|-------|-----------------|
| FR-1 | Unauthenticated visit | Open app without session | Redirect to Entra sign-in; no data returned |
| FR-3 | Member opens another project | Member not in project P requests P | Denied; P absent from lists |
| FR-7 | Second timer | Timer running on A; start timer on B | A stopped with duration; only B running |
| FR-9 | Edit approved entry | Entry approved; user edits duration | Rejected; entry unchanged |
| FR-16 | Reject entry | Manager rejects with comment | Entry editable by user; comment visible |
| FR-20 | Export | Report for May by project | CSV rows and totals equal on-screen report |
| FR-23 | Time zone captured | User in America/Chicago logs a timer | Entry stores UTC start, zone, offset, local date |
| FR-27 | Closed period | Close-through 31 May; Admin edits an entry dated 30 May | Edit denied; audit trail unchanged |
| FR-24 | Midnight split | Timer 23:00 31 May to 01:00 1 June local | Two entries, 60 minutes each, one in May and one in June |

## Technical Context

Stack decisions are recorded in `01-frame/concerns.md`; rationale belongs in ADRs (Design).

- **Language/Runtime**: TypeScript on Node.js (Azure Functions managed runtime)
- **Key Libraries**: React with Vite (SPA)
- **Data/Storage**: Azure SQL Database serverless (leading candidate; ADR required)
- **Auth**: Microsoft Entra ID, single tenant, via Azure Static Web Apps custom registration
- **Platform Targets**: Azure Static Web Apps (Standard) with managed Functions; current Chrome, Edge, Firefox, Safari

## Constraints, Assumptions, Dependencies

### Constraints

- **Technical**: Fully serverless on Azure; no containers (operator decision).
- **Business**: Hosting under $30 per month at current team size.
- **Legal/Compliance**: Time and rate data is internal business data; access follows FR-3 and FR-21.

### Assumptions

- Under about 50 users, one Entra tenant.
- Entra app roles or group claims can carry the Admin role.
- Cold-start latency on the first request after idle is acceptable.

### Dependencies

- Entra app registration and tenant admin consent.

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Azure SQL auto-pause makes the first request slow | High | Med | Accept at launch; measure; spec a keep-warm option in Design |
| Time zone and DST handling produces wrong day or month totals | Med | High | Store zone, offset, and local date per entry (FR-23); split at local midnight (FR-24); test month boundaries and DST |
| Rate history complicates budgets and reports | Med | Med | Effective-dated rates (FR-13), decided in Design |
| Scope creep toward full task management | Med | Med | Non-goals above; `scope-discipline` concern |

## Open Questions

- [ ] When an Accountant closes a period that still has pending entries, should the close be blocked, or should pending entries be auto-approved — blocks FR-27 design, ask Erik.
- [ ] Should an Accountant also be allowed to approve entries, or only close periods and report — blocks FR-27 and FR-16 design, ask Erik.

## Success Criteria

- Everhour is cancelled.
- 90% of hours are logged within 24 hours and 90% of entries approved within 3 working days.
- Monthly Azure cost stays under $30.
