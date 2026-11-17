# Repository guidance

This repository is an incremental workshop delivered in the GitHub Copilot app.
The current entry point is README.md and the curriculum is workshop/README.md.
The numbered example folders are reference material from the earlier workshop.
Use full product names in teaching and documentation: **GitHub Copilot** or
**GitHub Copilot app**, **Microsoft Foundry**, **Microsoft Teams** and
**Microsoft 365 Copilot**. Keep exact UI labels, role names and API identifiers
unchanged; never confuse Microsoft 365 Copilot with the GitHub Copilot app.

## Instruction routing

This file is the repository-wide entry point. Keep detailed coaching rules in
the linked protocol, not duplicated in the GitHub Copilot instructions or the
Workshop Coach profile.

| Request | Required guidance |
|---------|-------------------|
| How to begin or select Workshop Coach | [Participant start guide](workshop/START.md); orientation is not a lesson or cloud approval |
| Start, resume or participate | [Coach protocol](workshop/COACH.md), including welcome, setup, teaching, approvals, progress and recovery |
| Current checkpoint and required tests | [Curriculum](workshop/README.md), current lesson and [acceptance cases](workshop/TESTS.md) |
| Edit the workshop, examples or coach | Perform the repository task; read only the guidance relevant to the edit; do not start/resume a participant or deploy resources |

Load the full coach protocol when entering coaching or when it changes, then
reuse loaded context and its fast operating checklist. Read the current lesson
and only the additional sections needed for the current step. Do not reload
the entire curriculum or scan all chat history every turn. Both the Workshop
Coach profile and the normal repository Chat fallback follow that same
protocol; profile selection alone never starts a lesson.
If required guidance cannot be loaded, report the blocker instead of
reconstructing a reduced protocol from these entry-point instructions.

## Coaching reference ownership

Follow these authoritative references when their topic is needed, rather than
maintaining shortened copies of their rules in entry-point instructions:

| Topic | Reference |
|-------|-----------|
| Welcome order, experience preferences, pacing, teaching, usage summaries and approvals | [Coach protocol](workshop/COACH.md) |
| Participant input, chat-led progress, pauses and missing-history recovery | [Startup/resume](workshop/COACH.md#session-startup-and-resume) and [progress/evidence](workshop/COACH.md#progress-and-evidence); no routine `progress.json` I/O |
| Verified participant navigation and GitHub Copilot app techniques | [App guide](workshop/APP-GUIDE.md) |
| Microsoft Foundry setup, identity, project access and permissions | [Setup sequence](workshop/COACH.md#checkpoint-00-setup-sequence) and [setup references](workshop/SETUP.md) |
| Direct MCP bindings, selected public servers and first/expanded tool sets | [MCP connections](workshop/MCP-CONNECTIONS.md) and [MCP services](workshop/MCP-SERVICES.md) |
| Supported prompt-agent execution and recovery artifacts | [Shared runner](workshop/runner/README.md) |
| Release, consumer access, CH01/CH02 publication and channel evidence | [Publishing](workshop/PUBLISHING.md) |
| Optional Weather GitHub delivery lab | [Delivery lab](workshop/weather-delivery/README.md) |
| Hosted workflow preparation and intended G/W tests | [Hosted lesson](workshop/02-hosted-agents.md) and [facilitator readiness](workshop/FACILITATOR.md#hosted-workflow-readiness-before-the-cohort) |

References preserve the full requirements, not optional alternatives. Retain
checkpoint order, independent evidence, participant learning, explicit scope/
cost approval and every native human tool decision. Never infer approvals or
passes from a summary, bypass a blocked gate, or migrate/resume a paused
participant during authoring.

## Implementation boundaries

- Keep the main learning path in the Copilot app; do not require VS Code.
- Keep this repository focused on the current Copilot app workshop.
- Create student implementations in student/; introduce dependencies per lesson.
- Never commit credentials, tokens, .env files, conversation transcripts, or
  student progress. Keep sanitized local evidence in .workshop/.
- For Foundry operations, use the installed microsoft-foundry skill if available
  and follow its applicable workflow. Otherwise read the current official
  references in workshop/SETUP.md before using the SDK, CLI, or REST API.
- Check actual tool availability and SDK versions. Do not invent tool names,
  Canvas actions, resource IDs, endpoints, or preview feature support.
- Never turn a curriculum-authoring request into a live Azure deployment.
