---
ddx:
  id: product-vision
  authoring:
    home: repo
---

# Product Vision

## Mission Statement

Tempo lets Synaptiq's team track time against projects and tasks, with Entra ID sign-in, budgets and approvals, at near-zero hosting cost, so the company owns its time data instead of renting it from Everhour.

## Positioning

For Synaptiq staff and project managers who log billable and internal hours against client projects,
Tempo is a time-tracking and light task-management web app that records, budgets, approves, and reports time.
Unlike Everhour, Tempo signs users in with the company's Entra ID tenant, runs on serverless Azure with scale-to-zero cost, and keeps all data in Synaptiq's own subscription.

## Vision

Every hour worked is attributed to a project and task in seconds, approved without chasing anyone, and visible in budget reports the same day. No per-seat subscription, separate identity, or data export is needed to answer "where did the hours go?"

**North Star**: Percentage of working hours logged to a project within 24 hours of being worked.

## User Experience

Priya signs in with her Synaptiq Entra account, opens Tempo, picks a project and task, and presses start. The timer keeps running while she switches tabs; she stops it after the client call and adds a note. Friday she sees a prompt in Teams, opens her week, fills a missed Tuesday entry by hand, and submits the timesheet. Her project manager sees it in an approval queue, approves it, and watches the project's budget bar move from 62% to 68%. At month end an admin exports hours by project and user to CSV.

## Target Market

| Attribute | Description |
|-----------|-------------|
| Who | Synaptiq employees (under about 50) and the project managers and admins who run their projects |
| Pain | Paying per seat for Everhour, maintaining a second identity, and having time data outside company control |
| Current Solution | Everhour (Team plan, roughly $8.50-$10 per seat per month) |
| Why They Switch | Entra single sign-on, data ownership, and no per-seat licence cost |

## Key Value Propositions

| Value Proposition | Customer Benefit |
|-------------------|------------------|
| Timer and manual entry per project and task | Hours get logged in seconds, so reports are accurate |
| Entra ID sign-in with Admin and Member roles | No new passwords; access follows company directory |
| Budgets, rates, and timesheet approval | Managers see overruns and approve hours without spreadsheets |
| Reports and CSV export | Billing and payroll inputs without re-keying |
| Teams/Slack reminders | Fewer missing timesheets |
| Serverless Azure hosting | Hosting cost near zero when idle |

## Success Definition

| Metric | Target |
|--------|--------|
| Primary KPI: hours logged within 24 hours of work | 90% within 3 months of launch |
| Everhour retired, subscription cancelled | Within 6 months of launch |
| Historical Everhour data imported | 100% of projects, users, and entries from the last 24 months |
| Monthly Azure hosting cost at current team size | Under $30 |
| Timesheets approved within 3 working days of submission | 90% |

## Why Now

Entra ID is already Synaptiq's identity provider, and Azure Static Web Apps with managed Functions plus Azure SQL's free serverless tier make a small authenticated app cheap to run. Peer tools charge roughly $5-$18 per seat per month, so Synaptiq's per-seat spend recurs every month while Tempo's hosting cost stays flat as headcount grows.
