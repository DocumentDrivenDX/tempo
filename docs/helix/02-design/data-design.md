---
ddx:
  id: data-design
  authoring:
    home: repo
  links:
    - ADR-002
    - ADR-005
    - ADR-006
    - ADR-007
---

# Data Design

## Data Summary

- Scope: all Tempo data for FR-1 to FR-27.
- Storage systems: Azure SQL Database serverless.
- Main concerns: exact local-date totals, closed-period integrity, audit tamper resistance, cost at idle.

## Entities and Stores

| Entity or Store | Purpose | Key Fields | Volume / Growth | Notes |
|-----------------|---------|------------|-----------------|-------|
| `users` | People known to Tempo | `id` (uuid), `entra_oid` (unique), `email` (unique), `display_name`, `role` (`admin`/`member`/`accountant`), `tz_id`, `active` | Under 50 | Upserted on sign-in; role cached from the principal |
| `projects` | Units of time, budget, approval | `id`, `name`, `client`, `billable_default`, `hours_budget_minutes` (null), `amount_budget_minor` (null), `alert_threshold_pct`, `archived` | Hundreds | Archived projects accept no time |
| `project_members` | Membership | `project_id`, `user_id`, `project_role` (`manager`/`contributor`) | Thousands | Composite key |
| `tasks` | Labels for time | `id`, `project_id`, `name`, `status` (`active`/`completed`/`archived`) | Thousands | Unique name per project |
| `time_entries` | Logged time | `id`, `user_id`, `project_id`, `task_id` (null), `started_at_utc` (null), `ended_at_utc` (null), `duration_minutes`, `tz_id`, `utc_offset_minutes`, `local_date`, `billable`, `note`, `status` (`pending`/`approved`/`rejected`), `approved_by`, `approved_at`, `rate_minor_snapshot` (null), `split_group_id` (null) | About 250 per user per year; 60k in 5 years | Core table; see ADR-005 |
| `running_timers` | One per user | `user_id` (PK), `project_id`, `task_id` (null), `started_at_utc`, `tz_id`, `note` | Under 50 | Server-held timer (FR-11) |
| `rates` | Effective-dated billable rates | `id`, `user_id`, `project_id` (null = default), `rate_minor`, `effective_from` (date) | Hundreds | Most specific rate in force on an entry's `local_date` wins |
| `settings` | Organization singleton | `week_start` (0-6, default 0 = Sunday), `closed_through` (date, null), `currency` (default USD) | 1 row | Period close lives here (ADR-006) |
| `audit_log` | Append-only history | `id`, `at_utc`, `actor_user_id`, `actor_role`, `action`, `entity_type`, `entity_id`, `detail` (JSON), `comment` | Thousands per year | No update or delete permission (ADR-007) |

## Relationships

| From | To | Type | Cardinality | On Delete |
|------|----|------|-------------|-----------|
| `project_members` | `projects`, `users` | N:M | Required | RESTRICT |
| `tasks` | `projects` | 1:N | Required | RESTRICT |
| `time_entries` | `users`, `projects` | N:1 | Required | RESTRICT |
| `time_entries` | `tasks` | N:1 | Optional | RESTRICT |
| `running_timers` | `users`, `projects`, `tasks` | 1:1 / N:1 | Required / optional | RESTRICT |
| `rates` | `users`, `projects` | N:1 | Required / optional | RESTRICT |

Nothing is physically deleted except pending or rejected entries and members; users, projects, and tasks are deactivated or archived.

## Access Patterns and Constraints

| Access Pattern | Frequency | Performance Need | Supporting Index or Cache |
|----------------|-----------|------------------|---------------------------|
| Entries for a user and date range (week view) | High | p95 under 200 ms | Index `(user_id, local_date)` |
| Pending entries per project (approval queue) | Daily | p95 under 300 ms | Filtered index `(project_id, local_date) WHERE status='pending'` |
| Report sums by project, user, task, day, week, month | Daily | Under 2 s for 5 years of data | Index `(project_id, local_date)` including `duration_minutes`, `billable`, `status` |
| Time-of-day report | Occasional | Under 2 s | Scan of `started_at_utc` and `tz_id` for the range |
| Project budget consumption | On project view | Under 300 ms | Same covering index |

Constraints: `duration_minutes >= 1`; `local_date` consistent with `started_at_utc` and `tz_id` when start is present (checked by the domain function and a check on offset); `ended_at_utc - started_at_utc` equals `duration_minutes` when both present; `status = 'approved'` requires `approved_by` and `approved_at`; one timer per user (PK); `alert_threshold_pct` between 1 and 100; trigger rejecting writes to entries with `local_date <= settings.closed_through` (ADR-006).

## Validation and Security

| Field or Data Type | Rules / Classification | Protection or Error Handling |
|--------------------|------------------------|------------------------------|
| `rates.rate_minor`, `time_entries.rate_minor_snapshot` | Confidential (pay-related) | Returned only to Admin, Accountant, and the project's Managers (FR-21) |
| `tz_id` | IANA name, validated against the runtime's list | Reject unknown names |
| `note` | Up to 500 characters, internal | Output-encoded in the SPA |
| Emails, names | Personal data | Standard Azure SQL encryption at rest and in transit |
| `audit_log` | Integrity-critical | No update or delete grant |

Approval freezes `rate_minor_snapshot` (FR-13); pending entries use the rate in force on their `local_date`.

## Migration Strategy

- Tooling: plain versioned SQL migration files run by a small script in CI and at deploy.
- Approach: forward-only, additive where possible; each migration applied inside a transaction; a test applies all migrations to an empty database and runs the schema tests.
- Backfill or cleanup: none initially.
