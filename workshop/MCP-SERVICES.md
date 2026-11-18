# Agreed MCP services and the shared travel story

This is the connection reference for Workshop Coach, not a participant
infrastructure assignment. Use these selected public, free-to-use,
no-authentication MCP services for the core workshop. Participants build two
Foundry agents and then a hosted workflow; they do not build, host, or choose
replacement MCP servers. The final workflow calls the two released agents,
not the MCP servers directly.

An MCP server is a remote service exposing callable operations called tools.
Connecting a server to the GitHub Copilot app does not connect it to a
Microsoft Foundry agent. The core teaches
[direct MCP connections](MCP-CONNECTIONS.md): attach Weather's public server
with only its forecast tool at 04, expand the allowlist at 05 and verify the
binding at 07. Repeat independently for Cultural at 11/12. No Toolbox or
upstream authentication connection is required, and no planned Weather
migration is needed at 14. Local discovery, saved attachment and actual
execution are separate evidence boundaries.

## Selected services

| Specialist | MCP Server Endpoint | Provider's server name | Suggested Foundry server label | First allowed tool |
|------------|---------------------|------------------------|-------------------------------|--------------------|
| Weather Research Agent | `https://weather.datakoot.com/mcp` | `weather-intel` | `weather_intelligence` | `weather_forecast` |
| Cultural Travel Agent | `https://mcp.travel.art/` | `travel.art` | `cultural_travel` | `find_museum_guide` |

Both use **Streamable HTTP**: the client sends MCP requests to the exact URL
above. Do not append a guessed `/sse` or `/mcp` path. No API key, authorization
header, OAuth sign-in, or credential connection is needed for these services.
Authentication and permissions are still required for the participant's
Microsoft Foundry Project. Foundry model calls, memory, telemetry, and hosted
workflow resources can incur charges; a free MCP service does not make the
workshop free. Public-service availability, terms, and limits can change.

**Verification dated 2026-10-27:** both endpoints accepted MCP `initialize`
and `tools/list` requests without credentials, negotiated protocol
`2025-03-26`, and reported the tools below. Server versions were
`weather-intel 1.0.0` and `travel.art 1.6.0`. One read-only
`find_museum_guide` request with `{"country":"US"}` returned guides for the
Metropolitan Museum of Art and MoMA in New York, with source `travel.art`,
`guideUrl`, and `lastVerified` fields. These were local authoring checks, not
Foundry runtime tests, student passes, or guarantees of future free access.
No weather retrieval or model request was made for these checks.

Provider references: [Weather & Geo](https://datakoot.com/weather-geo) and
[travel.art MCP](https://mcp.travel.art/). Use this reference for the planned
connection; resolve current schema details needed during configuration or
recovery without adding standalone connectivity tests or a participant
`initialize`/`tools/list` exercise. The first useful agent request establishes
runtime access. Use actual returned fields, not website sample outputs, as
runtime evidence.

### Explain the Weather service when using it

Whenever introducing, using or revisiting Weather MCP, give a short relevant
reminder: it is a **free public online service used for workshop learning and
testing**, not a production or future-pricing guarantee. It covers US
locations, forecasts only within returned periods and potentially cached
results. Inspect the returned source and weather timestamps; `served_at` is
the server response time. Availability, terms and limits can change. Use public
locations, not participant home addresses. Microsoft Foundry model execution
and telemetry can still incur charges.

This reminder explains the limitations; it is not a request for participants
to test service reachability or investigate infrastructure.

## Weather tools and boundaries

| Tool | Inputs from the verified schema | Workshop use |
|------|---------------------------------|--------------|
| `weather_forecast` | Required numeric `lat`, `lon`; optional boolean `hourly`, default `false` | Checkpoint 04: sole allowed tool; retrieve daily forecast periods |
| `geocode` | Required string `address`; US address or city | Checkpoint 05: resolve a supplied public location before weather retrieval |
| `weather_current` | Required numeric `lat`, `lon` | Checkpoint 05: latest station observation, not an exact measurement at a landmark |
| `weather_alerts` | Required string `area`, normally a two-letter US state code | Checkpoint 05: relevant official alerts when requested |
| `earthquakes`, `elevation` | Discover their schemas if needed for a separately approved extension | Not part of the core weather allowlist |

The provider describes US coverage for forecasts, observations, alerts, and
geocoding. Forecasts and observations come from NWS/NOAA; geocoding uses US
Census data. Confirm provenance from each result. A response may be cached:
`provenance.served_at` is the server response time, not necessarily the weather
observation time. Preserve units, station, source timestamps, and forecast
period meanings; never turn a period's start into an inferred end.

At checkpoint 04, supply public coordinates directly. Do not enable `geocode`
early merely because it appears in discovery. At 05, separately approve the
expanded four-tool allowlist and skill. The skill resolves text locations only
when necessary, chooses forecast/current/alerts according to the question, and
does not call all tools routinely. Weather evidence does not establish museum
facts, booking availability, or emergency safety.

## Cultural tools and boundaries

| Tool | Inputs from the verified schema | Workshop use |
|------|---------------------------------|--------------|
| `find_museum_guide` | Optional strings `query`, `city`, `country` (two-letter country code) | Checkpoint 11: sole allowed tool; retrieve published museum guidance |
| `find_art_events` | Optional strings `query`, `country`, `type`, `activeOn`, `startsAfter`, `endsBefore`; `type` is `biennale`, `art-fair`, `festival`, or `museum-exhibition` | Checkpoint 12: find relevant art events using the requested dates |
| `find_layover_itinerary` | Optional strings `query`, `city`, `country`, `airport`; optional numeric `maxDurationHours` | Checkpoint 12: published short art-focused layovers where catalogue coverage exists |
| `recommend_art_trip` | Required string `city`; optional date strings `startDate`, `endDate` | Checkpoint 12: published cultural trip suggestions, not the final two-agent workflow |

Date inputs use `YYYY-MM-DD`. The source is travel.art's published, curated
guides, not a live reservation system, unrestricted web search, or an official
venue feed. Include each returned canonical `guideUrl` in the answer and retain
`lastVerified` or other freshness fields when present. Do not claim a dataset
version if none is supplied. Attribute and summarize; do not copy whole guides
into repository fixtures or claim an unverified dataset license.

The server does not expose tools named `get_attractions`,
`get_cultural_guidance`, `get_accessibility_notes`, or `search_destinations`.
Do not invent them. Accessibility or etiquette advice can be attributed only
when actually returned; missing information remains unknown. Opening hours,
prices, event dates, transit timing, and accessibility require appropriate
freshness caveats. Never claim a booking, purchase, or live availability check.

At checkpoint 12 the skill selects museum, event, layover, or recommendation
tools according to the request and actual coverage. It preserves empty results
and failures rather than inventing venues or calling unrelated tools. A
provider-supplied cultural itinerary is only one evidence source: it does not
prove that our hosted workflow invoked the Weather Agent.

## First-tool configuration

These are the **direct-MCP tool fragments for the v10 core**. They specify
the selected public endpoints, upstream tool names and native approval policy.
Keep `server_url`; do not add `project_connection_id`, credentials or a
Toolbox endpoint for either anonymous upstream service. Resolve any current
schema details needed as part of configuration, not a separate learner test.

These fragments are not complete agent definitions or
permission to create versions. After project access, current API support,
required tool metadata, and participant approval, attach only the fragment for the
current specialist. Keep the chosen model and existing
versions unchanged. Do not attach both servers to one specialist.

Weather checkpoint 04:

```json
{
  "type": "mcp",
  "server_label": "weather_intelligence",
  "server_url": "https://weather.datakoot.com/mcp",
  "allowed_tools": ["weather_forecast"],
  "require_approval": "always"
}
```

Cultural checkpoint 11:

```json
{
  "type": "mcp",
  "server_label": "cultural_travel",
  "server_url": "https://mcp.travel.art/",
  "allowed_tools": ["find_museum_guide"],
  "require_approval": "always"
}
```

Use the installed Foundry skill and currently supported client to create and
independently read back the approved candidate. SDKs may normalize allowlists;
verify equivalent semantics and no additional tools. Do not create a credential
connection for an authless server or weaken approvals. Follow
[first-use Playground permissions](APP-GUIDE.md#first-tool-use-in-the-playground):
the participant sends the useful prompt, learns the permission choices when
they appear, selects Auto approve for the displayed permitted-tool scope and
continues to the answer and trace. Explain Deny without adding a denial drill.
This portal choice does not authorize SDK/runner continuations; those still
require an exact participant decision and separately approved continuation.

## Build-up story the coach teaches

Use a fictional art-and-weather trip to **New York, US**, as the shared example.
The cultural catalogue check above establishes museum coverage; verify usable
weather results during the approved lesson. Select travel dates within the
actual returned forecast horizon. A guide's verification date is not a travel
date, and a forecast cannot establish weather months in advance.

Existing participants keep their approved targets, versions, and historical
test inputs. Do not repeat an earlier Washington, DC or other valid test merely
to switch this example or balance the coach/participant sending ratio.

| Checkpoints | Small learning steps and evidence |
|-------------|-----------------------------------|
| 01-03 Weather foundation | Create the tool-free agent; test a stable concept such as why rain forms. Improve only instructions and compare the same inputs. Prove follow-up context in one managed Conversation and isolation in a new one. It cannot retrieve a forecast yet. |
| 04 Weather first tool | Connect only `weather_forecast`. Participant sends: "For New York, US, latitude 40.7128 and longitude -74.0060, retrieve the daily forecast with hourly=false. Use those coordinates exactly." At first permission prompt, explain Approve/Deny/Auto approve and let the participant select Auto approve for the permitted Weather-tool scope. Continue to the result, grounded answer and matching trace; no separate denial drill. |
| 05 Weather skill | Add the approved geocoding/current/alerts tools and a versioned research procedure. Practice a public museum address, appropriate weather-tool choice, restraint, and partial failure. |
| 06 deferred; 07 Weather release | Skip persistent memory for now; retain its lesson for later. Retest applicable tools, Conversations and skill; release only a passing independent weather specialist. |
| 08-10 Cultural foundation | Create a separate tool-free agent; test a stable question such as how an art museum differs from an art fair. Refine its instructions and independently prove Conversation continuity and isolation. Do not copy Weather state. |
| 11 Cultural first tool | Connect only `find_museum_guide`. Participant sends: "Use the museum-guide tool to find the Metropolitan Museum of Art in New York, US. Summarize the returned guidance, cite its guide URL, and state its verification date if supplied." Briefly repeat the first-use permission explanation and let the participant select Auto approve for the permitted Cultural-tool scope. Inspect actual arguments, result, attribution and trace. |
| 12 Cultural skill | Expand only to the four verified cultural tools. Use museum-plus-event questions for multi-tool practice; use a covered European city for a separate layover test, not a US weather request. Demonstrate missing catalogue/accessibility data and a controlled partial failure. |
| 13 deferred; 14 Cultural release | Skip persistent memory for now; retain its lesson for later. Prove applicable regressions and independent release as for Weather. |
| 15-16 Final workflow | After both releases pass, define result contracts and implement a hosted Agent Framework workflow. One trip request invokes both released specialists, validates both results, and assembles a sourced itinerary with weather-aware choices, guide links, uncertainties, and explicit partial failures. Correlated traces must prove both calls; two manual replies or `recommend_art_trip` alone do not pass. |

Follow the lesson files and tests for each gate; this table is the fixed teaching
story, not authorization to skip steps or run the whole workshop at once.
Keep the planned 50/50 coach/participant test mix, exact navigation, copy-ready
prompts, cost boundaries, approval stops, actual evidence, and teach-backs.
Students choose their own capstone only after this shared workflow.

Follow the five-to-six-hour core agenda: teach the method with Weather and
use shorter reminders for Cultural Travel. Supply MCP details and require
independent evidence for both without repeating the full explanation or trace
tour. The student-chosen capstone is an optional separate follow-on.

## Coach recovery when connection details appear missing

1. Read this file before asking a participant for an MCP endpoint. Both core
   addresses and tool progressions are already selected.
2. Use the documented connection and inputs for configuration. Resolve any
   missing metadata within that operation's approved scope; do not run
   standalone connectivity probes or ask the participant to predict
   reachability. Discovery is not proof of Microsoft Foundry execution.
3. Explain and approve the current one-tool or multi-tool change, then use the
   first useful agent request for runtime evidence. Never attach every
   advertised tool automatically.
4. If blocked, report the exact endpoint, operation, and error, distinguishing
   missing local tooling, public-service availability, and Foundry access or
   runtime failure. Preserve progress and involve the facilitator. Do not ask a
   beginner to design infrastructure, request an API key, deploy a substitute,
   disable approval, or fabricate an unavailable result.
