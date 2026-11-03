# Agentic Workshop in the GitHub Copilot App

Learn to build and test Microsoft Foundry agents with **GitHub Copilot as your
coach**. Create a **Weather Research Agent**, test it, add managed conversations,
a remote Weather MCP, skills, and memory, then release it. Next create and
enhance a separate **Cultural Travel Agent** backed by the public **travel.art
MCP server**. Both specialists use the selected free-to-use, no-authentication
[MCP services](workshop/MCP-SERVICES.md); the coach supplies connection details
and guides the same incremental process for each. Participants do not host
MCP servers. Foundry resources and model usage can still incur charges.
Learn reusable **Foundry tool connections** and a forecast-only **Toolbox**
with Weather's first tool at checkpoint 04; expand that Toolbox at 05.
Verify the existing binding before release and deepen Toolbox management
with Cultural Travel, then verify both existing releases at handoff without
a planned Weather migration or repeat release cycle. Each specialist keeps
only its own tools; a skill guides their use rather than granting access.
After both agents pass independently, deploy a hosted
**Trip Planning Workflow** that invokes them and assembles a sourced itinerary.
Each participant uses one dedicated Microsoft Foundry Project, which they may
prepare before the workshop or create themselves during checkpoint 00 with
coach guidance after confirming the target and possible costs. The facilitator
does not assign the project name or endpoint. Participants independently select
a compatible model from the Microsoft Foundry Model Catalog only if no suitable
existing deployment is chosen. Before asking for a model/version or creating a
new deployment, the coach checks for existing deployments and asks whether to
reuse a matching one; new deployments require cost acknowledgment.

Alongside agent development, learn to use the **Copilot app itself**: asking for
explanations or implementation, reviewing changes, inspecting tool calls,
working with sessions, and choosing between Chat and available visual tools.
VS Code is not required.

The core workshop is planned for **5-6 hours**, including breaks, and finishes
with the two specialists connected through the hosted workflow. Learn the
method with agent 1, then apply it with shorter reminders on agent 2. A
student-chosen capstone is an optional follow-on, outside that core time budget.
After Weather checkpoint 07, students may also choose the separate
[Weather-agent GitHub delivery lab](workshop/weather-delivery/README.md) before
checkpoint 08; it does not change the core estimate or checkpoint numbering.
Its one-project setup is an educational compromise, not a production pattern.

## Start here: select Workshop Coach

1. Open the workshop repository supplied by your facilitator as a project in
   the **GitHub Copilot app**.
2. Start a session in that project and use the app's agent selector to select
   **Workshop Coach**.
3. With **Workshop Coach** selected, type:

   > Start the workshop.

Workshop Coach will welcome you, explain how the guided lessons work, check that it can
read this repository, and help you through setup one question at a time. You do
not need to know an agent name, internal file path, or Azure command to begin.
If you already have local progress, the coach will help you resume safely.
If your app has no agent selector, use normal repository Chat and send the same
message as a fallback. If a selector exists but Workshop Coach is missing, use
the discovery troubleshooting in the start guide rather than choosing another
agent. Fresh-session picker visibility still needs validation for your app build.

**New to the app or not sure what to open?** Follow the
[participant prerequisites](workshop/PREREQUISITES.md) and
[start guide](workshop/START.md). You can also ask "How do I start
this workshop?" in the repository chat to get orientation before beginning.

The facilitator supplies the app-access instructions and the workshop repository
revision. Azure setup comes after the welcome; opening the project or sending
the starter message does not authorize creating paid resources.

## Learning path

| Stage | Agent concepts | Copilot app practice |
|-------|----------------|----------------------|
| 00 | Verify or create the participant's dedicated project, then reuse or explicitly approve a workshop model deployment | Read repository context; understand approvals and cost boundaries |
| 01-07 | Weather Research Agent: create, test, add conversations, Weather MCP, skills, memory, and release | Explain vs implement; inspect evidence; resume sessions; compare connections |
| 08-14 | Cultural Travel Agent: repeat baseline, instructions, conversations, MCP, skill, memory, and release | Reinforce the full lifecycle with separate evidence |
| 15-16 | Hosted Trip Planning Workflow: define contracts, orchestrate, trace, release, update, and roll back | Inspect generated files and nested traces; compare local/remote evidence |
| 17-19 (optional follow-on) | Choose, implement, and release a two-specialist capstone | Write a scoped brief; review changes; demonstrate and hand off |

Every capability follows **predict -> change -> test -> explain -> checkpoint**.
The coach teaches one small change at a time and introduces one app technique
plus a useful alternative. Students do not have to complete the lesson twice.

## Capstone choices

The early exercises use a shared fictional travel-planning story: one prompt
agent researches weather, another researches curated cultural evidence, and a
hosted workflow validates their versioned results and combines them into an itinerary. This
teaches boundaries and orchestration without selecting the student's capstone.

In an optional follow-on, choose **IT support**, **a documentation research assistant**,
**a fictional travel-planning assistant**, or **your own approved scenario**.
Use synthetic/public data. The [capstone guide](workshop/CAPSTONE.md) defines
equivalent acceptance criteria and what extra infrastructure each choice needs.

## Workshop material

- [Checkpoint map and student controls](workshop/README.md)
- [Participant prerequisites](workshop/PREREQUISITES.md), [setup](workshop/SETUP.md),
  and [Copilot app techniques](workshop/APP-GUIDE.md)
- [Prompt-agent lessons](workshop/01-prompt-agents.md)
- [Selected MCP services and the shared travel story](workshop/MCP-SERVICES.md)
- [Reusable Foundry tools and Toolboxes](workshop/TOOLS-AND-TOOLBOXES.md)
- [Optional Weather-agent GitHub delivery lab](workshop/weather-delivery/README.md)
- [Hosted-agent lessons](workshop/02-hosted-agents.md)
- [Tests](workshop/TESTS.md) and [stable-endpoint release](workshop/PUBLISHING.md)
- [Capstone choices](workshop/CAPSTONE.md) and [facilitator guide](workshop/FACILITATOR.md)

Student implementations live in `student/`; local progress and sanitized test
evidence live in ignored `.workshop/` files. The coach is a formative tutor, not
an independent examiner or a secure grading system.

**Foundry terminology:** new-model agents receive a stable endpoint on creation.
Release checkpoints verify version selection and consumer access, not a separate
endpoint publishing operation. Teams/Microsoft 365 distribution is optional;
legacy Agent Applications are explained in the publishing guide.

## Repository layout

| Location | Purpose |
|----------|---------|
| `workshop/` | Participant guides, lessons, coach protocol, tests, and facilitator guidance |
| `workshop/assets/` | Supporting lesson assets |
| `workshop/templates/` | Templates for local workshop progress |
| `.github/` | Workshop Coach profile and repository instructions |
| `student/` | Student implementations and reproducible agent definitions |
| `examples/support-ticket-system/` | Optional IT support example app with shared storage, web server, and local MCP tools |
| `.workshop/` | Ignored local progress and sanitized evidence; never published |

Dependencies are introduced per lesson in isolated student environments.
The optional [IT support example app](examples/support-ticket-system/README.md)
is retained. The other earlier VS Code tutorials and agent scripts remain
available in Git history.
