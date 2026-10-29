---
ddx:
  id: CONTRACT-001
  authoring:
    home: repo
  links:
    - ADR-004
    - ADR-005
    - ADR-006
---

# Contract

**Contract ID**: CONTRACT-001
**Type**: HTTP API
**Version**: v1
**Related**: ADR-004, ADR-005, ADR-006, FEAT-001 to FEAT-006

## Purpose

Governs the HTTP API between the Tempo SPA and the Functions API. Feature specs and stories reference this contract instead of defining endpoints inline.

## Scope and Boundaries

- In scope: JSON endpoints under `/api`, authorization outcomes, error format, CSV export.
- Out of scope: SWA sign-in routes (`/.auth/*`), database schema (data-design), UI.
- Owning system: Tempo API.

## Normative Surface

All requests MUST be authenticated through SWA; the API reads the principal from `x-ms-client-principal`. Bodies and responses are `application/json` (UTF-8) except CSV. Identifiers are UUID strings. Dates are `YYYY-MM-DD` (local dates). Instants are ISO 8601 UTC strings ending in `Z`. Durations are integer minutes. Money is integer minor units (cents) with the organization currency. Time zones are IANA names. Roles in the Access column: A=Admin, C=Accountant, M=project Manager, U=any authenticated user (further limited by membership).

| Endpoint | Request | Response | Access | Rules |
|----------|---------|----------|--------|-------|
| `GET /api/me` | none | `{id,email,displayName,role,tzId,settings:{weekStart,closedThrough,currency}}` | U | Upserts user on first call (FR-2) |
| `PATCH /api/me` | `{tzId}` | user | U | Valid IANA name; existing entries unchanged (FR-22, FR-23) |
| `GET /api/users` | none | `[{id,email,displayName,role,active}]` | A, C | |
| `PATCH /api/users/{id}` | `{active}` | user | A | Deactivation only; role comes from Entra |
| `GET /api/projects` | query `includeArchived` | `[Project]` | U | Members see their projects; A, C see all (FR-3) |
| `POST /api/projects` | `{name,client?,billableDefault}` | Project | A, any M | Creator becomes Manager unless Admin |
| `PATCH /api/projects/{id}` | `{name?,client?,billableDefault?,archived?}` | Project | A, M | Archive stops a running timer on it |
| `PUT /api/projects/{id}/members/{userId}` | `{projectRole}` (`manager`\|`contributor`) | member | A, M | |
| `DELETE /api/projects/{id}/members/{userId}` | none | 204 | A, M | History kept |
| `GET /api/projects/{id}/tasks` | none | `[Task]` | U (member) | |
| `POST /api/projects/{id}/tasks` | `{name}` | Task | A, M | Unique name per project |
| `PATCH /api/tasks/{id}` | `{name?,status?}` | Task | A, M | status `active`\|`completed`\|`archived` |
| `GET /api/timer` | none | `{timer:null}` or `{timer:{projectId,taskId,startedAtUtc,tzId,note}}` | U | Server-held (FR-11) |
| `POST /api/timer/start` | `{projectId,taskId?}` | timer | U (member) | Stops and saves any running timer first (FR-7) |
| `POST /api/timer/stop` | `{note?}` | `{entries:[Entry]}` | U | Splits at local midnight (FR-24); 409 `PERIOD_CLOSED` if any segment is closed |
| `GET /api/entries` | query `from,to,userId?,projectId?,status?` | `[Entry]` | U | Members only their own; M their projects; A, C all |
| `POST /api/entries` | `{projectId,taskId?,localDate,durationMinutes,startTime?,tzId?,note?,billable}` | `{entries:[Entry]}` | U (member) | `startTime` is `HH:mm` local; `tzId` defaults to profile; may split (FR-8, FR-24) |
| `PATCH /api/entries/{id}` | `{durationMinutes?,note?,billable?,projectId?,taskId?,localDate?,startTime?}` | `{entries:[Entry]}` | owner | Only while `pending` or `rejected` and not in a closed period (FR-9) |
| `DELETE /api/entries/{id}` | none | 204 | owner | Same rule |
| `GET /api/approvals` | query `projectId?,userId?,from?,to?` | `[Entry]` | A, M | Pending, stopped entries of managed projects (FR-15) |
| `POST /api/approvals/approve` | `{entryIds:[uuid]}` | `{approved:[uuid],failed:[{id,code}]}` | A, M | Not C. Freezes rate snapshot. Per-entry audit rows; Admin use logged as override (FR-16, FR-18) |
| `POST /api/approvals/reject` | `{entryIds,comment}` | same shape | A, M | `comment` required |
| `POST /api/entries/{id}/reopen` | `{reason}` | Entry | A | Approved to pending; refused in a closed period (FR-17) |
| `PUT /api/projects/{id}/budget` | `{hoursBudgetMinutes?,amountBudgetMinor?,alertThresholdPct?}` | Project with `consumed` and `remaining` | A, M | Null removes a budget (FR-12, FR-14) |
| `GET /api/rates` | query `userId?,projectId?` | `[Rate]` | A, C | |
| `POST /api/rates` | `{userId,projectId?,rateMinor,effectiveFrom}` | Rate | A | Never alters approved entries (FR-13) |
| `GET /api/reports/hours` | query `from,to,groupBy,tz?,billable?,status?,projectId?,userId?,format?` | `{groups:[{key,label,minutes,amountMinor?}],totalMinutes,totalAmountMinor?}` or CSV | U | `groupBy` is `project`\|`user`\|`task`\|`day`\|`week`\|`month`; `tz` buckets by that zone (FR-19, FR-20, FR-26) |
| `GET /api/reports/time-of-day` | query `from,to,userId?,projectId?` | `{hours:[{hour,minutes}]}` per entry local hour | A, C, M | Excludes entries with no start time (FR-26) |
| `GET /api/settings` | none | `{weekStart,closedThrough,currency}` | U | |
| `PATCH /api/settings` | `{weekStart}` | settings | A | 0=Sunday to 6=Saturday (FR-25) |
| `PUT /api/period-close` | `{closedThrough,reason}` | settings | A, C | Date or null; audit row; works with pending entries present (FR-27) |
| `GET /api/audit` | query `entityType?,entityId?,from?,to?` | `[AuditRow]` | A, C | |

Entry: `{id,userId,projectId,taskId,startedAtUtc,endedAtUtc,durationMinutes,tzId,utcOffsetMinutes,localDate,billable,note,status,approvedBy,approvedAt,rateMinor?,amountMinor?,splitGroupId}`. `rateMinor` and `amountMinor` appear only for A, C, and the project's M.

Authorization outcomes: unauthenticated requests receive 401; requests for another user's or non-member project data receive 404 (no existence leak); role violations receive 403 `FORBIDDEN`.

## Precedence and Compatibility

- Versioning: v1 is implicit in the path; breaking changes introduce `/api/v2`.
- Ordering: list endpoints return entries by `localDate`, then `startedAtUtc`, then `id`.
- Backward-compatibility rules: adding optional response fields and optional query parameters is compatible; removing or retyping a field is breaking.
- Deprecation rules: none yet.

## Error Semantics

Errors use `application/problem+json` with `{type,title,status,code,detail,errors?}`.

| Condition | Error / Outcome | Retry | Recovery Expectation |
|-----------|------------------|-------|----------------------|
| Validation failure | 400 `VALIDATION` with `errors` | no | Fix input |
| Not authenticated | 401 | no | Sign in |
| Role not allowed | 403 `FORBIDDEN` | no | Ask an Admin |
| Not found or no access | 404 | no | |
| Entry date on or before `closedThrough` | 409 `PERIOD_CLOSED` | no | Accountant or Admin reopens the period |
| Entry not editable (approved) | 409 `ENTRY_LOCKED` | no | Admin reopens the entry |
| Timer not running | 409 `NO_TIMER` | no | |
| Project archived | 409 `PROJECT_ARCHIVED` | no | |
| Unknown time zone | 400 `INVALID_TIMEZONE` | no | |
| Database resuming | 503 with `Retry-After` | yes | Client retries with backoff |

## Examples

```text
POST /api/timer/stop   {"note":"client call"}
200 {"entries":[
 {"localDate":"2026-05-31","durationMinutes":60,"tzId":"America/Chicago","status":"pending"},
 {"localDate":"2026-06-01","durationMinutes":60,"tzId":"America/Chicago","status":"pending"}]}

PUT /api/period-close  {"closedThrough":"2026-05-31","reason":"May close"}
409 on later PATCH /api/entries/{id} with localDate 2026-05-30:
{"status":409,"code":"PERIOD_CLOSED","title":"Period is closed"}
```

## Non-Normative Notes

Bulk approval is not atomic: each entry succeeds or fails on its own, reported in `failed`. Shapes here are implemented once in `packages/contracts` and imported by both the API and the SPA.
