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

Tempo is a web app where Synaptiq staff track time against projects and tasks, project managers set budgets and approve weekly timesheets, and admins report and export hours. It replaces Everhour, signs users in with Entra ID, and runs on serverless Azure for under $30 a month. v1 covers sign-in, projects and tasks, a timer and manual entry, budgets and rates, weekly approval, reports with CSV export, and a one-time Everhour CSV import. Success is 90% of hours logged within 24 hours, Everhour cancelled within 6 months, and approvals within 3 working days.

## Problem and Goals

### Problem

Synaptiq pays Everhour roughly $8.50-$10 per seat per month, manages a second identity for time tracking, and keeps time data in a vendor's system. Project managers cannot see budget burn alongside company identity and access.

### Goals

1. Staff log time in seconds, by timer or by hand, against a project and task.
2. Managers approve hours weekly and see budget burn without spreadsheets.
3. Synaptiq owns its data and retires Everhour.

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| Hours logged within 24 hours of work | 90% by 3 months after launch | Entry `created_at` vs entry date, monthly SQL report |
| Timesheets approved within 3 working days of submission | 90% | Submission and approval timestamps |
| Everhour history imported | 100% of last 24 months of projects, users, entries | Import dry-run vs commit counts |
| Monthly Azure cost at current team size | Under $30 | Azure Cost Management |
| Everhour subscription cancelled | Within 6 months of launch | Finance confirmation |

### Non-Goals

- Invoicing, payments, or expense tracking.
- Screenshots, activity monitoring, or idle detection.
- Resource planning, capacity forecasting, or Gantt charts.
- Full task management (assignees, due dates, boards, comments); tasks are labels for time.
- Multi-tenant or external-customer access; Tempo serves one Entra tenant.
- Native mobile apps; the web app is responsive.
- Chat reminders (Teams or Slack) and third-party integrations such as Jira, Asana, or GitHub; deferred to `docs/helix/parking-lot.md`.

Deferred items tracked in `docs/helix/parking-lot.md`.

## Users and Scope

### Primary Persona: Priya, Member

**Role**: Consultant or engineer at Synaptiq working on client projects
**Goals**: Log hours fast and get her timesheet approved
**Pain Points**: Forgotten entries, re-keying time, another login

### Secondary Persona: Marcus, Project Manager

**Role**: Member who is a Manager on one or more projects
**Goals**: Approve hours, watch budget burn, catch overruns early
**Pain Points**: Chasing timesheets, building budget reports by hand

### Secondary Persona: Alex, Admin

**Role**: Operations or finance administrator
**Goals**: Manage users and projects, report hours by project and user, export for billing
**Pain Points**: Reconciling exports across tools

Roles: Entra app roles give each user a global role of Admin or Member. Manager is a per-project membership role held by a Member, not a third global role.

## Requirements

### Must Have (P0)

1. Entra ID sign-in with Admin and Member roles and server-side authorization.
2. Projects, project membership, and tasks.
3. Timer and manual time entry with editing.
4. Weekly timesheet submission, per-project manager approval, and locking.
5. Reports by project, user, and date range, with CSV export.

### Should Have (P1)

1. Project hour and dollar budgets with consumption display and alert threshold.
2. Billable rates per user, overridable per project.
3. Everhour CSV import.

### Nice to Have (P2)

1. Task-level budgets.
2. Saved report filters.

## Functional Requirements

### Subsystem: Identity and Access

- **FR-1** — Users sign in only through the company Entra ID tenant; Tempo stores no passwords.
- **FR-2** — A user is created on first sign-in with the global role from their Entra app role (Admin or Member, default Member); Admins can deactivate users.
- **FR-3** — Every data access is authorized server-side: Members see only projects they belong to; Admins see all.

### Subsystem: Projects and Tasks

- **FR-4** — Admins and project Managers create, edit, and archive projects (name, client, default billable flag); archived projects accept no new time.
- **FR-5** — Admins and project Managers assign project members with the project role Manager or Contributor.
- **FR-6** — Managers and Admins create, rename, complete, and archive tasks within a project.

### Subsystem: Time Tracking

- **FR-7** — A user starts and stops a timer on a project, optionally on a task; starting a second timer stops the first, so a user has at most one running timer.
- **FR-8** — A user adds a manual entry with date, duration in whole minutes, project, optional task, optional note, and billable flag.
- **FR-9** — A user edits or deletes their own entries until the entry is approved; approved entries are read-only.
- **FR-10** — A user sees a weekly timesheet of their entries by day and project, with daily and weekly totals.
- **FR-11** — A running timer is held server-side, so it survives page reloads and shows on other devices.

### Subsystem: Budgets and Rates

- **FR-12** — A project may have an hours budget, a dollar budget, or both, with an alert threshold percentage.
- **FR-13** — Admins set a billable rate per user and may override it per project; a rate change applies to entries from its effective date forward and never alters approved entries.
- **FR-14** — A project shows budget consumed and remaining, and flags when the alert threshold or budget is exceeded.

### Subsystem: Timesheet Approval

- **FR-15** — A user submits a week for approval; submitted entries are read-only to the user until approved or rejected.
- **FR-16** — Each project's Managers approve or reject that project's entries in a submitted week, with a comment on rejection; rejected entries return to editable.
- **FR-17** — Approved entries are locked; an Admin can reopen them, and the reopening is recorded.
- **FR-18** — Submission, approval, rejection, and reopening are recorded in an audit trail with actor, time, and comment.

### Subsystem: Reports and Export

- **FR-19** — Users run reports of hours, and of billable amounts where permitted, grouped by project, user, task, or day over a date range, filtered by billable flag.
- **FR-20** — Any report exports to CSV with the same filters and totals.
- **FR-21** — Rates and dollar amounts are visible only to Admins and to Managers of the project concerned; Members see their own hours only.

### Subsystem: Everhour Import

- **FR-22** — An Admin imports Everhour CSV exports (projects, users, tasks, time entries), previews counts and unmatched rows in a dry run, then commits; re-importing the same file creates no duplicates.
- **FR-23** — Imported entries are stored approved and locked; users are matched by email to Entra users.

## Acceptance Test Sketches

| Requirement | Scenario | Input | Expected Output |
|-------------|----------|-------|-----------------|
| FR-1 | Unauthenticated visit | Open app without session | Redirect to Entra sign-in; no data returned |
| FR-3 | Member opens another project | Member not in project P requests P | Denied; P absent from lists |
| FR-7 | Second timer | Timer running on A; start timer on B | A stopped with duration; only B running |
| FR-9 | Edit approved entry | Entry approved; user edits duration | Rejected; entry unchanged |
| FR-16 | Reject entry | Manager rejects with comment | Entry editable by user; comment visible |
| FR-20 | Export | Report for May by project | CSV rows and totals equal on-screen report |
| FR-22 | Re-import | Same CSV imported twice | Second commit adds zero entries |

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
- Everhour exports include enough fields (project, task, user email, date, duration, billable) to import.
- Cold-start latency on the first request after idle is acceptable.

### Dependencies

- Entra app registration and tenant admin consent.
- Everhour CSV export samples for import design.

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Azure SQL auto-pause makes the first request slow | High | Med | Accept at launch; measure; spec a keep-warm option in Design |
| Everhour export lacks needed fields | Med | High | Obtain a real export before Design of FR-22 |
| Rate history complicates budgets and reports | Med | Med | Effective-dated rates (FR-13), decided in Design |
| Scope creep toward full task management | Med | Med | Non-goals above; `scope-discipline` concern |

## Open Questions

- [ ] What is Tempo's week start (Monday?) and time zone handling for entries — blocks FR-10, FR-15, ask Erik.
- [ ] Do Managers approve their own time, or does an Admin — blocks FR-16, ask Erik.
- [ ] Is a sample Everhour export available — blocks FR-22 design, ask Erik.
- [ ] Should the vision's Teams/Slack reminder proposition be removed or marked deferred — vision currently lists it, ask Erik.

## Success Criteria

- Everhour is cancelled and all 24 months of history is queryable in Tempo.
- 90% of hours are logged within 24 hours and 90% of timesheets approved within 3 working days.
- Monthly Azure cost stays under $30.
