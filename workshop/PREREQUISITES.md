# Before the Agentic Workshop: participant prerequisites

Build two Microsoft Foundry agents and a coordinating workflow, guided by
**Workshop Coach in the GitHub Copilot app**. No prior agent development
experience is required. Prepare the following before attending; contact your
facilitator if anything is blocked.
You will also publish and use Weather before building Cultural Travel, and
the completed workflow afterward, in **Microsoft Teams and/or Microsoft 365
Copilot**. Choose at least one surface for each milestone; the GitHub Copilot
app remains the separate coaching application.

Plan for **5-6 hours including breaks** for the guided two-agent-and-workflow
build. A capstone using your own scenario is an optional follow-on. Ready
prerequisites help protect hands-on time; access problems may require separate
facilitator support.

## 1. Prepare your device and Copilot access

Bring a computer with a web browser and permission to run organization-approved
tools. Install:

| Tool | What it is and why you need it |
|------|-------------------------------|
| [GitHub Copilot app](https://github.com/features/ai/github-app) | Your AI-assisted workspace, where Workshop Coach guides you through building agents and reviewing results. |
| [Git](https://git-scm.com/install/) | A version-control tool that lets the app retrieve workshop files and track your changes. |

Sign in to the app with a GitHub account that has the required Copilot access.
Open the repository link and exact revision supplied by your facilitator.
Your network must allow GitHub, Microsoft sign-in, Foundry, and the approved
Azure services; do not disable security controls.

The coach supplies the two selected public
[MCP services](MCP-SERVICES.md) during the lessons. These provide callable
weather and cultural-travel tools without a service account or API key. You
do not need a Cloudflare account or to build or host an MCP server. Your
network must allow `weather.datakoot.com` and `mcp.travel.art`; ask your
facilitator for help if either is blocked. Foundry still requires the Microsoft
account and Azure access below.

**Other required tools are checked in the coach's execution environment:**
Azure Command-Line Interface (CLI) is required before the first Foundry check;
Python and Foundry software development kit (SDK) packages run workshop code
and connect to Foundry; Azure Developer CLI (`azd`) deploys the later hosted
workflow. They may already be available. A facilitator can help prepare an
isolated environment in advance to avoid installations during teaching;
otherwise the coach guides missing-tool setup when needed.
**VS Code is not required.**

An optional advance readiness session checks installed tools and, after you
confirm your account/project and agree to read-only checks, access and later
lesson prerequisites. It does not build your agents, send paid test prompts
or authorize resource changes. The live workshop still confirms your account
and exact project. Flag missing memory, release or hosting support early rather
than discovering it near the end.

## 2. Prepare your Microsoft account and Azure access

Sign in to [Microsoft Foundry](https://ai.azure.com/) with your intended
Microsoft account, which may differ from your GitHub account. Arrange an
approved Azure subscription with access, permissions, and quota for projects,
models, and agents; ask your facilitator or administrator for access help.

**Signing in alone is not enough.** Ask your administrator to arrange Azure
roles at the appropriate resource scope:

| Activity | Access needed |
|----------|---------------|
| Build and test agents | **Foundry User** on the Foundry resource or appropriate project scope. |
| Release agents through stable endpoints | Operation-specific agent management and consumer access, checked at the project/agent scope; project management access alone does not prove consumer invocation permission. |
| Publish Weather and the hosted workflow to Microsoft Teams/Microsoft 365 Copilot | Current project publishing permission (the official guide names **Foundry User**) and allowed/licensed tenant access to the chosen channel. Microsoft Foundry manages direct-publishing bot registration; no separate Azure Bot Service resource or Bot Service Contributor role is required for that route. See [PUBLISHING.md](PUBLISHING.md) for scope, approval and runtime requirements. |
| Create a project or deploy models | Additional management permissions, such as **Foundry Account Owner** on the Foundry resource; creating the resource itself requires permissions on the target resource group. |
| Inspect traces and query logs | **Log Analytics Reader** on connected telemetry resources; protected tables may require additional read access. |
| Deploy the hosted workflow | Permissions for supporting Azure resources and runtime identities, checked during deployment preparation. |

For a prepared environment, request **Foundry Project Manager** on your
dedicated Foundry resource plus telemetry-read access; an administrator can
prepare model deployments and supporting resources. Subscription-wide Owner
or Microsoft 365 Global Administrator access is not required. Azure
**Contributor alone does not grant Foundry agent data access**.
You may see the older role names **Azure AI User**, **Azure AI Project Manager**,
and **Azure AI Account Owner** in the portal. See
[Microsoft's Foundry role reference](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).

Use **one dedicated Foundry Project**, the workspace for your agents and
connections, not a production project. Prepare your own project in advance or
create it yourself with coach guidance during checkpoint 00 (setup), after
confirming costs. The facilitator does not assign its name or endpoint.
If it exists, have its name and **Project Endpoint** (service address) ready;
the coach can help you locate it.

**Do not create a model deployment just for preparation.** A deployment makes
a model available to your agents. The coach checks existing deployments first;
you choose whether to reuse one or approve a new model deployment and its cost.

## 3. Prepare Application Insights for trace inspection

**Connect Application Insights to your project and arrange telemetry-read
access.** This Azure service stores execution records called **traces**, which
show what an agent actually did.

For an existing project, arrange this before attending; for a project created
during setup, plan it with the coach then. Follow
[Microsoft's tracing setup guidance](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup).
Ask your administrator about **Log Analytics Reader** access and any extra
permissions needed for protected log tables.

The coach checks readiness on the first project connection and before trace
exercises. A working model reply does not prove tracing is enabled.
Connecting or creating telemetry resources requires explicit approval and can
incur storage and ingestion costs; earlier executions may not appear afterward.

## 4. Prepare Microsoft Teams or Microsoft 365 Copilot access

Arrange access/licensing to at least one of these applications with your
organization's Microsoft account. Your facilitator must rehearse the chosen
surface(s), tenant app policies, installation and publication permissions, and
the hosted workflow's compatible channel adapter before delivery. Ask your
administrator for help; do not bypass app policies or request broad roles.

Microsoft Foundry manages bot registration for direct publishing; a separate
Azure Bot Service resource or `Microsoft.BotService` provider registration is
not a blanket prerequisite for that route. Publishing enables channel
protocol/authorization settings and needs explicit approval.
**Just you** is the preferred workshop scope;
organization-wide distribution requires separate approval and Microsoft 365
administrator review. Personal publication does not remove Azure permission,
licensing or tenant-policy requirements.

Messages and app metadata pass through Microsoft 365 services and their data
handling commitments, separately from Microsoft Foundry. Agree on this flow
and any channel costs before publishing. Private-network projects need a
separately approved, rehearsed supported route; do not relax security settings.
See [publication readiness and steps](PUBLISHING.md#required-channel-publication-at-07-and-16).
A missing required channel/runtime or tool-approval capability leaves the
affected checkpoint blocked, not passed with a screenshot or endpoint-only test.
No agents need to be published in advance.

## 5. Agree on costs and safe practice data

Agree on an approved spending arrangement: models, memory, hosted compute,
and telemetry can incur charges, even with existing resources. The coach asks
for approval before changes or paid tests and shows available Foundry model
usage and cost estimates, excluding Copilot coaching and other service charges.

Use only **public or synthetic data**; traces may capture prompts and replies.
Never share credentials or confidential files. Agree on resource cleanup;
pausing a lesson does not stop paid Azure resources.

## 6. Be ready to start in the GitHub Copilot app

After cloning the repository provided by your facilitator (downloading a local
copy), open it as a project in the **GitHub Copilot app**, start a session,
type **`/agent`** in the message box, select **Workshop Coach**, and send:

> Start the workshop.

The coach welcomes you and explains the workshop, then asks how experienced
you feel with **Microsoft Foundry** and the **GitHub Copilot app**, separately.
Choose Beginner, Intermediate or Expert, or describe it in your own words.
The answers tailor explanations and navigation, not the goals or safety checks.
Setup starts next without another start command. You can say "explain more"
or "keep it brief" at any time; saved preferences are reused when you resume.
During the workshop, occasional short check-ins let you keep or adjust the
explanation level and the balance between coach-executed and hands-on steps.
You can defer a check-in; it is not an assessment and does not change approvals
or required learning evidence.

The core includes reusable **Foundry tool connections** and **Toolboxes**
(managed collections of tools). Your project must support their management
and your agents' runtime access; the facilitator checks this before delivery.
Public Weather/travel.art services require no keys, but that does not remove
Foundry permissions or possible costs. No VS Code setup is required.

You can also request coaching in your preferred language, for example:

> Start the workshop. Guide me in Swedish, and explain technical terms in
> Swedish with their English names in parentheses.

Replace Swedish with your preferred language. Keep resource names, commands,
code, and portal labels unchanged so you can match them to the actual tools.
The coaching language does not automatically change your Foundry agents'
instructions or test prompts. Ask your facilitator which languages have been
rehearsed for this workshop.

The documented alternative is the agent picker dropdown inside the prompt box,
if visible; it is not the model picker. If neither selection route is available,
use normal repository Chat. If selection works but Workshop Coach is missing,
use the [start guide](START.md) or ask
your facilitator; availability depends on the app build and configuration.

Workshop Coach is a supplied GitHub Copilot custom-agent profile; you do not
need to create one to begin. The coach runs in the GitHub Copilot app; your
Weather and Cultural Travel agents run in Microsoft Foundry. The coach states when
to use the portal for inspection or testing. Do not duplicate tests in both places.

## Final readiness check

- [ ] I can sign in to the GitHub Copilot app and open the supplied repository revision.
- [ ] Git is installed, and I can install approved additional tools when needed.
- [ ] I know which Microsoft account and approved Azure subscription I will use.
- [ ] I can access my dedicated Foundry Project, or have arranged to create it during setup.
- [ ] Application Insights and telemetry-read access are ready, or I have flagged the setup needed with my facilitator.
- [ ] I can access Microsoft Teams and/or Microsoft 365 Copilot, with project publishing permissions, channel/runtime support and tenant policies prepared or flagged with my facilitator.
- [ ] I understand that Azure usage can incur costs and will use only public or synthetic data.

If any item is blocked, contact your facilitator before the workshop. You do
not need to create agents, run paid model tests, or deploy a workflow in advance.
