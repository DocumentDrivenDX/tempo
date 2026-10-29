---
ddx:
  id: research-plan
  authoring:
    home: repo
---

# Research Plan: Prior art for Tempo (Everhour replacement)

**Research Lead**: Genesis (Claude), for Erik LaBianca
**Time Budget**: one pass, four web searches
**Created**: 2026-10-29

## Research Objectives

### Primary Research Questions

1. **Question**: What do Everhour and its peers offer, and at what price?
   - **Why Important**: Sets the cost bar Tempo must beat.
   - **Success Criteria**: Per-seat price range for Everhour, Clockify, Toggl Track, Harvest.
2. **Question**: Is Azure Static Web Apps + managed Functions a fit for Entra ID auth with roles?
   - **Why Important**: Validates the operator's Azure serverless constraint.
   - **Success Criteria**: Entra and custom-role support identified by plan tier.
3. **Question**: Which Azure datastore is cheapest and sound for a small relational workload?
   - **Why Important**: Datastore is an exclusive concern slot.
   - **Success Criteria**: Ranked options with cost drivers.

### Knowledge Gaps
| Gap | Impact | Current Confidence |
|-----|--------|--------------------|
| Current Everhour Team price and exact budget/approval features | Med | Low |
| SWA Standard monthly price | Med | Low |
| Cosmos DB serverless per-unit cost | Low | Low |

## Scope

**In Scope**: Competitor pricing, Azure hosting/auth/datastore options.
**Out of Scope**: Market sizing, detailed feature comparison (competitive-analysis).
**Assumptions**: Third-party aggregator figures are indicative only.
**Decision Enabled**: Vision positioning; ADRs for datastore and hosting in Design.

## Findings

Sources are third-party pages and Microsoft Learn; verify prices on vendor pages before relying on them.

- **Everhour**: Free (up to 5 users), Team, and Custom plans. Team is listed at roughly $8.50-$10 per seat per month; sources conflict ([Capterra](https://www.capterra.com/p/133409/Everhour/pricing/), [Digital Project Manager](https://thedigitalprojectmanager.com/tools/everhour-review/)). Core value: billable hours, budgets, and add-ons for Asana, ClickUp, Trello, Basecamp, GitHub, Jira. Approval-workflow detail not confirmed.
- **Peers**: Clockify is cheapest (paid roughly $5-$15 per seat); Toggl Track about $9-$18; Harvest about $9-$14 and invoicing-centred ([Kimai comparison](https://www.kimai.org/en/blog/2025/price-comparison), [CostBench](https://costbench.com/software/time-tracking/)). Clockify's free-tier user cap reports conflict.
- **Azure Static Web Apps**: Managed Functions are on Free and Standard. Custom Entra registrations and function-assigned custom roles require the Standard plan ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)). Standard price (one blog cites about $9/month) is unconfirmed.
- **Datastores**: Azure SQL Database free offer (100,000 vCore-seconds per month, auto-pauses) is the cheapest relational option; PostgreSQL Flexible Server B1ms is about $12-15/month and is not serverless; Cosmos DB serverless suits sporadic NoSQL ([Mark Heath](https://markheath.net/post/which-azure-database-serverless)).

## Disposition

- Azure fits the Entra constraint; plan on SWA Standard for custom roles.
- Lead datastore candidate: Azure SQL serverless (relational reporting, lowest cost). Final choice needs an ADR in Design.
- Per-seat SaaS cost for a small team is low, so Tempo's case rests on ownership, Entra-native identity, and near-zero hosting cost, not on beating price per seat alone.
