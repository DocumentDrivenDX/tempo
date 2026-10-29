---
ddx:
  id: ADR-001
  authoring:
    home: repo
  links:
    - prd
---

# ADR-001: Host on Static Web Apps with a linked Azure Functions app

## Problem

The PRD requires a fully serverless, low-cost Azure deployment (under $30 per month) with Entra ID sign-in and Node.js. Static Web Apps (SWA) managed Functions are the cheapest option, but they cannot use managed identity or Key Vault references, so the API would need a database password stored in app settings. Managed Functions also limit the Node.js versions available.

## Decision

We will host the SPA on Azure Static Web Apps (Standard plan) and link a bring-your-own Azure Functions app (Node.js 22, HTTP triggers, Flex Consumption or Consumption plan) as the API behind `/api`. The Functions app uses a system-assigned managed identity to reach Azure SQL (ADR-002).

## Why We Chose This

### Over SWA managed Functions
Managed Functions have no managed identity and no Key Vault references ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/static-web-apps/apis-functions)). That forces a SQL password into app settings. Passwordless access is worth one more deployment pipeline.

### Over Azure Container Apps or App Service
Both need containers or an always-on plan. The operator wants pure serverless with scale-to-zero cost.

## Consequences

**Good**: No stored database secret; current Node.js runtime; same `/api` routing and SWA user-principal header as managed Functions; scales to zero.

**Trade-offs**: Two deploy targets (SPA and Functions app) and a storage account for the Functions app; cold starts on first request; SWA Standard plan cost is required for custom Entra registration and linked backends. Monthly cost must be confirmed against the $30 target during deployment (Deploy activity).

**Drift signals to watch**: Database passwords in app settings; containers appearing in infrastructure; API code assuming non-HTTP triggers.

## Concern Impact

- **Override / deviation**: Refines the `deploy-target` selection in `concerns.md` (managed Functions becomes linked Functions). Still serverless; no container.
