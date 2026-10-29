<!-- helix:publish audience=data page=index kind=explanation voice=onboarding budget=900 written=agent-opus reviewed=2026-10-29/agent-sonnet/018f1bac01698db6 -->
<!-- helix:gap artifact:data-architecture -->
<!-- helix:source docs/helix/00-discover/product-vision.md sha256:9b53a7d443020c1a -->
<!-- helix:source docs/helix/02-design/data-design.md sha256:4e13adc8da5cf9ab -->
<!-- helix:source docs/helix/02-design/adr/ADR-002-datastore-azure-sql-serverless.md sha256:79361fa47dbd952a -->
<!-- helix:source docs/helix/02-design/adr/ADR-006-period-close-enforcement.md sha256:1421b1e3bd0196b8 -->
<!-- helix:source docs/helix/02-design/adr/ADR-007-audit-trail.md sha256:79cf8135cdce7ac3 -->
<!-- helix:source docs/helix/02-design/architecture.md#quality-attributes sha256:5259ef0a45408ec1 -->
<!-- helix:source docs/helix/02-design/contracts/CONTRACT-001-tempo-api.md#normative-surface sha256:48280f533acd0647 -->
<!-- helix:source docs/helix/01-frame/prd.md sha256:bed0e3e775aa06a6 -->
# Data overview

## What the data is for

Tempo's data answers one question: where did Synaptiq's hours go? Staff log time against projects and tasks. Managers approve that time, and Accountants close accounting periods. Reports turn the result into billing and payroll inputs without re-keying.

All of the data lives in one Azure SQL Database serverless instance in Synaptiq's own subscription (ADR-002). That database is the system of record. Tempo has no warehouse, no copies, and no pipelines.

The repository has no job, DLT, dbt, or notebook definitions, and it has no application code yet. The schema exists as design: `docs/helix/02-design/data-design.md` and one UMF TableSpec per table in `docs/helix/02-design/umf/tables/`.

```sh
ls -1 docs/helix/02-design/umf/tables
```

Expected result:

```text
audit_log.yaml
project_members.yaml
projects.yaml
rates.yaml
running_timers.yaml
settings.yaml
tasks.yaml
time_entries.yaml
users.yaml
```

## The datasets

Tempo has nine tables and three read paths built on them. Most questions about hours are answered by `time_entries`, joined to `projects`, `users`, and `tasks`.

**Tables**

| Table | What it holds | Size |
|-------|---------------|------|
| `time_entries` | Logged time: duration in minutes, local date, billable flag, approval status | About 60k rows in 5 years |
| `projects` | Projects with client, billable default, and optional hours or amount budgets | Hundreds |
| `tasks` | Labels for time within a project | Thousands |
| `users` | People, their global role, and their time zone | Under 50 |
| `project_members` | Who belongs to each project, as `manager` or `contributor` | Thousands |
| `rates` | Effective-dated billable rates per user, optionally per project | Hundreds |
| `running_timers` | At most one live timer per user | Under 50 |
| `settings` | One row: week start, `closed_through`, currency | 1 row |
| `audit_log` | Approvals, rejections, reopenings, period closes, and Admin overrides | Thousands per year |

**Read paths**

| Endpoint | What it returns | Who may call it |
|----------|-----------------|-----------------|
| `GET /api/reports/hours` | Minutes and, where permitted, amounts, grouped by project, user, task, day, week, or month | Any user, limited by membership |
| `GET /api/reports/time-of-day` | Minutes per local hour of the day | Admin, Accountant, project Manager |
| `GET /api/audit` | Audit rows filtered by entity and date range | Admin, Accountant |

Add `format` to the hours report to get CSV. The CSV must have the same filters and totals as the on-screen report (FR-20).

**Which dataset answers which question**

| Question | Use |
|----------|-----|
| Hours by project, person, task, or period | Hours report, or `time_entries` grouped on `local_date` |
| Billable amount | Hours report with amounts, which needs a rate-visible role |
| How much of a project budget is used | `time_entries` against `projects.hours_budget_minutes` or `amount_budget_minor` |
| When people work during the day | Time-of-day report |
| Who approved, reopened, or closed something | `audit_log` or `GET /api/audit` |
| Which periods are locked | `settings.closed_through` |
| Who is tracking time right now | `running_timers` |

Some rules change the meaning of a query:

- Day and month buckets use each entry's `local_date` by default. A reporting time zone (`tz`) can bucket everything in one zone instead (FR-26).
- An approved entry carries its frozen rate in `rate_minor_snapshot`. A pending entry uses the most specific rate in force on its `local_date`.
- A closed period can hold entries that stay unapproved. An approved-only report misses them, so filter on `status` deliberately.
- The time-of-day report excludes entries with no start time.
- Rates and amounts are confidential. Only Admins, Accountants, and Managers of the project concerned may see them (FR-21). Members see only their own hours.

<details>
<summary>Units and formats the data uses</summary>

Durations are integer minutes. Money is integer minor units (cents) in the organization currency. Local dates are `YYYY-MM-DD`, and instants are ISO 8601 UTC strings ending in `Z`.

Time zones are IANA names. These units come from the API contract, `docs/helix/02-design/contracts/CONTRACT-001-tempo-api.md`.

</details>

## Freshness and ownership

Every dataset is current as of the last committed transaction, because reports query the system of record directly. A logged hour shows up in reports and budget bars the same day, which is the product's goal. The first request after the database auto-pauses may take several seconds while it resumes.

Each kind of data has one writer:

- The API writes every table through use cases, each in one transaction. It connects with the Functions app's managed identity, not SQL logins.
- Only Accountants and Admins change `settings.closed_through` (ADR-006). A database trigger rejects any write to a `time_entries` row dated on or before that date, whatever the code path.
- The API writes `audit_log` in the same transaction as the change it records. Its identity has no `UPDATE` or `DELETE` grant on the table (ADR-007).
- Nothing is physically deleted except pending or rejected entries and memberships. Users, projects, and tasks are deactivated or archived instead.

Azure SQL automated backups with point-in-time restore give a recovery point objective of 1 day and a recovery time objective of 1 day.

Schema changes ship as forward-only versioned SQL migrations, run in CI and at deploy. The prose tables in `docs/helix/02-design/data-design.md` and the UMF YAML must stay identical. When they disagree, fix whichever is wrong.

The repository has no data-architecture artifact. The architecture owner supplies anything beyond the data design, such as analytical copies or retention rules.

## Where to go next

To browse the schema with its columns, keys, and relationships, build the UMF schema browser:

```sh
node docs/helix/02-design/umf/build-browser.mjs
python3 -m http.server -d docs/helix/02-design/umf/browser 8099
```

Expected result: the server listens on port 8099, and `http://localhost:8099/assets/index.html` opens the browser. The build output is about 18 MB and is git-ignored.

- [Overview](../developer/index.md) describes what Tempo is and its parts.
- [Architecture](../developer/architecture.md) describes the containers, the database's place among them, and the decisions behind them.
- `docs/helix/02-design/data-design.md` holds the access patterns, indexes, and constraints.
