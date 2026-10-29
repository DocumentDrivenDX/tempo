# Tempo: an example HELIX project

Tempo is a time-tracking web app meant to replace Everhour at Synaptiq. This repository holds no application code yet. It holds the **governed documents** that came out of one working session with [HELIX](https://github.com/DocumentDrivenDX) and Claude Code: a vision, a PRD, feature specs, user stories, architecture decisions, a data model, a security design, and an API contract.

It is published as an example of how a person can use HELIX to go from a one-paragraph idea to an implementable design in a single conversation, mostly by answering questions and correcting course. The conversation is quoted below, because the person's side of it is the point. They never wrote a spec by hand.

> **Status:** a draft produced in one session on 2026-10-29. The documents have not been through HELIX template validation, SPIKE-001 (Entra roles) has not been run, and pricing figures come from third-party sites and need checking against vendor pages. Treat it as a worked example, not an approved plan.

## What came out of it

| Activity | Artifacts | Where |
|----------|-----------|-------|
| Discover | Research note on prior art and Azure options; product vision | [`docs/helix/00-discover/`](docs/helix/00-discover) |
| Frame | PRD (27 numbered requirements), 6 feature specs, 17 user stories with given/when/then criteria, parking lot, project concerns | [`docs/helix/01-frame/`](docs/helix/01-frame), [`docs/helix/parking-lot.md`](docs/helix/parking-lot.md) |
| Design | 7 ADRs, architecture with module boundaries, data design, security architecture, HTTP API contract, UMF table specs (YAML) with a schema browser build, one technical spike plan | [`docs/helix/02-design/`](docs/helix/02-design) |

The project marker is [`.helix.yml`](.helix.yml). It tells HELIX which flow governs the repo and where its documents live.

**Tempo in one paragraph.** Staff log time with a timer or by hand against projects and tasks. Every entry records its time zone and is split at local midnight, so month-end totals are exact. Project managers approve entries one by one. Accountants close accounting periods. Admins can override either when the process breaks. Reports group by day, week, or month and export to CSV. It runs on Azure Static Web Apps, a linked Azure Functions app (Node.js), and Azure SQL serverless, signs in through Entra ID, and is designed to cost under $30 a month.

## The conversation

Each step below shows what the person said, in their words, and what HELIX and Claude did with it. Quoted text is verbatim. Where the person answered a multiple-choice question, the choices are summarized.

### 1. The opening prompt

> Let's create a new helix project. It should be a simple task management system, to replace everhour. It will have a concept of projects, users, time tracked per project, and must integrate with entra id for authentication and run in a low cost serverless environment with good persistent storage. Ask me what you need to know to complete this project.

This is HELIX's *genesis* mode: bootstrap a project from bare intent. The last sentence matters. Asking to be interviewed, instead of writing requirements up front, is what made the rest of the session work.

### 2. Answering the interview

Claude asked two rounds of questions. The person picked from options, with a recommendation marked on each:

- Cloud: Azure (because Entra ID fits it)
- Stack: TypeScript and React
- v1 features: live timer and manual entry, tasks per project, reports and CSV export, budgets, rates and approvals
- Size and roles: small team, two roles
- Name: Tempo
- Data and integrations: Everhour import plus Teams/Slack reminders
- Research: yes, survey the prior art first

HELIX then researched Everhour, Clockify, Toggl, Harvest, and the Azure serverless options, wrote the findings with sources, drafted the vision from them, and scaffolded the repository. Nothing was written before the research.

### 3. Challenging a technical choice

Claude had recorded Node.js instead of the HELIX default, Bun, because Azure Functions runs Node.

> Do we have to use node on azure, can't we use bun?

Claude laid out three options with trade-offs and recommended keeping Node. The person decided:

> No stick with node I want to stay serverless.

The constraint went into the project's concerns file as the operator's decision, and later shaped the hosting ADR (no containers).

### 4. Noticing what the tool left out

> What concerns did we add for SDLC and code quality?

Claude admitted it had recorded only stack and product concerns, and listed eight quality concerns from the HELIX library (testing, verification, end-to-end tests, module boundaries, code-size limits, observability, accessibility, relational data modeling).

> yes. those should have been defaults

They were added, and a note was saved so future bootstraps include them without asking. This is the feedback loop in miniature: say what should have been the default, and it changes.

### 5. Committing as you go

> commit everything

The repository got a commit at each stage, so every step of the project's evolution is in the history.

### 6. Framing the requirements

> yes

HELIX's *frame* mode needed product decisions the person had to make. Claude asked four questions (how approval works, how budgets and rates work, timer rules, which chat platform) and the answers were:

- Approval: weekly, with each project's manager approving that project's entries
- Budgets and rates: hours or dollar budget per project, rate per user with per-project override
- Timer: one running timer per user, minute precision
- Reminders: "skip reminders for now"

Claude then wrote the PRD, feature specs and user stories, and checked with a script that every requirement was covered by at least one story. Open questions were left visible in the PRD instead of guessed.

### 7. Settling the open questions, and changing the model

The person answered the PRD's open questions in one message, adding new requirements and removing old scope:

> Week's start on Sunday, but it should probably be configurable. We need time zone support, and we need to track the time zone along with tracked entries so we can know things like what time people are working in their local time zones and handle end of month shear, etc. Managers approve their own time. I can get an everhour export but I don't have one right now and the import is not a high priority issue. Drop the references to everhour import and teams/slack reminders for now. Do not mark them as deprecated, clean up all references.

Claude added time-zone capture on every entry, splitting at local midnight, a configurable week start, and self-approval by managers. It deleted the import feature and the reminders everywhere, with no "deprecated" markers, and checked that no references were left.

### 8. Replacing a whole concept with one sentence

> Submitted weeks shouldn't matter -- approval should happen at the hourly level and reporting will be configurable by week or month at time of reporting, so the "week" concept is really just a ui affordance.

This removed the weekly submit step from the PRD, features, stories and vision, and made approval work per entry. While Claude was working on it, the person interrupted with:

> Is there some scenario where that doesn't work?

Claude answered honestly before carrying on: premature approval of half-finished entries, no hard cutoff for payroll or billing, reports mixing pending and approved hours, and weak control over self-approval. It then built mitigations for the cheap ones (only stopped entries are approvable, an approval-status filter on reports) and raised the cutoff as a question. Asking the tool to critique your own decision, mid-flight, is cheap and worked well.

### 9. Introducing a role from a business need

> Hard period close should be driven by accounting. We may need a role for that.

Claude added an Accountant role and an accounting period-close requirement, with a new persona and story, and left two follow-up questions in the PRD. The person closed them:

> Period close should be while entries remain unapproved. Accountants should not approve time entries. Admin will need all operations and can unblock either of the above in case of process breakdown.

The PRD, features, stories and security model were updated together. A closed period still blocks direct edits by every role, Admins included, until the period is reopened; Claude pointed this out as its own reading, and said how to change it.

### 10. Design

> yes

HELIX's *design* mode produced seven ADRs, the architecture (with named modules and allowed and forbidden dependencies), the data design, the security architecture, and the API contract. Two judgment calls are worth reading:

- **Linked Functions instead of managed Functions.** Research showed managed Functions cannot use managed identity, so Claude recommended a linked Functions app to avoid storing a database password, flagged it prominently, and updated the earlier concern. See [ADR-001](docs/helix/02-design/adr/ADR-001-hosting-swa-linked-functions.md).
- **An unproven assumption became a spike.** The Entra roles design depends on behavior the docs did not confirm, so ADR-004 is marked Proposed and [SPIKE-001](docs/helix/02-design/spikes/SPIKE-001-entra-roles-claim.md) says how to test it, with a fallback.

### 11. Publishing

> Create a repo named "tempo" and push it to DocumentDrivenDX

and then

> Make it public.

Claude created the repository privately first, because the visibility had not been stated, then made it public on request after scanning the tracked files for secrets.

## What this shows

- **Interview first.** The person never drafted a requirement. They answered questions and reacted to drafts.
- **Decisions are cheap to change.** Reversals (drop imports, replace weekly submission, add a role) propagated through the vision, PRD, features, stories, concerns, and design, and each change was checked for leftover references and requirement coverage.
- **Questions stay visible.** Unknowns lived in the PRD's open-questions list until the person answered them, and unproven technical bets became a spike.
- **Governed documents trace to each other.** Every requirement (`FR-n`) maps to a story with numbered acceptance criteria; stories map to features; design artifacts link back to requirements and ADRs.
- **Pushback works.** Challenging a choice (Bun), asking what was missed (quality concerns), and asking "is there a scenario where that doesn't work?" each improved the result.

## What is not here yet

The test plan, the build plan with work items, and any code. The next HELIX steps would be to run SPIKE-001, then plan the tests and the build.

## Using HELIX to do something similar

1. Install the HELIX plugin for Claude Code.
2. Describe the product in a paragraph and end with "Ask me what you need to know."
3. Answer the questions, push back when something looks wrong, and ask for commits as you go.

The repository's `AGENTS.md` points an AI agent at the vision and the current next step.
