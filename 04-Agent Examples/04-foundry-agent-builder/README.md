# GitHub Copilot Foundry Prompt Agent Builder

Create a specialized GitHub Copilot custom agent that behaves like a professional
Microsoft Foundry prompt-agent engineer. First, prepare and test the custom agent in VS Code. Only
after it passes its readiness gate will you use it to build, extend, and deploy a separate
target agent in Microsoft Foundry.

## Learning objective

The point of this exercise is to develop a reusable custom agent with a narrow professional
role. The **Foundry Prompt Agent Builder** keeps a persistent Foundry destination,
engineering process, vocabulary, evidence rules, safety boundaries, and output format
across requests.

After this exercise, you can reuse the builder for future Foundry prompt agents instead
of repeating the same platform context and engineering rules in every prompt. It should
ask good questions, choose supported Foundry capabilities, inspect evidence, explain
tradeoffs, and produce work that can be validated.

## Keep the two agents separate

| Agent | Where it runs | Purpose |
|-------|---------------|---------|
| Foundry Prompt Agent Builder | GitHub Copilot Chat in VS Code | Designs, implements, validates, and deploys managed Foundry prompt agents with you. |
| Target prompt agent | Microsoft Foundry | Serves the business scenario designed during Phase 2. |

Saving `.github/agents/Foundry-Prompt-Agent-Builder.agent.md` makes the builder available in the
GitHub Copilot agent picker. It does not create an Azure resource. The target agent is
created separately through the Microsoft Foundry Project Client SDK.

GitHub Copilot tools control what the **builder** can do in VS Code. Foundry tools and
memory stores belong to the **target solution**. Workspace skills teach the builder
repeatable procedures; they do not host services or store business data.

## Before you begin

Complete the shared [Lab 04 prerequisites](../README.md#prerequisites). Confirm that:

- GitHub Copilot is enabled in VS Code
- the workspace virtual environment is active
- `az login` uses the intended tenant and subscription
- `.env` contains `AZURE_AI_PROJECT_ENDPOINT`
- `.env` contains `AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME`
- `azure-ai-projects==2.4.0` is installed from the root `requirements.txt`
- you can create and test agent versions in the training project

Never paste `.env` values, tokens, connection secrets, or customer data into chat.

# Phase 1: Prepare the GitHub Copilot professional

Do not build or deploy the target Foundry agent during this phase. The goal is to create,
equip, and validate the specialist that will perform that work in Phase 2.

## 1. Create version 1 with professional instructions

**Why:** Instructions establish the reusable professional role, Foundry destination,
workflow, and boundaries before implementation tools influence the result.

In normal GitHub Copilot **Agent** mode, enter:

```text
Create a workspace custom agent at
.github/agents/Foundry-Prompt-Agent-Builder.agent.md.

Use valid YAML frontmatter with:
- name: Foundry Prompt Agent Builder
- a description containing these triggers: build a Foundry agent, design an agent,
   create a prompt agent, add tools, add memory, deploy a prompt agent
- tools: []
- user-invocable: true
- agents: []

Make it a senior Microsoft Foundry prompt-agent engineer. Require it to gather missing business,
user, channel, data, action, risk, latency, and success requirements before choosing an
implementation. Its scope is managed prompt agents created and versioned in Microsoft
Foundry with the Project Client SDK. It must identify requirements that are unsupported
by that prompt-agent model instead of inventing capabilities or changing technology scope.

Its decision process must cover instructions, MCP, OpenAPI, functions, Azure AI Search,
file search, code interpreter, toolboxes, conversations, memory stores, identity, least
privilege, approvals, prompt injection, privacy, retention, cost, evaluation, tracing,
rollback, and publishing.

Require a consistent response format: requirement summary, missing decisions,
architecture choice, capability choices, security boundary, files, validation plan,
deployment plan, and assumptions requiring approval.

It must never invent SDK classes, current capabilities, resources, tool results, tests, or
deployment outcomes. When it lacks evidence, it must say what needs to be inspected.
```

Review the generated file. Its YAML must be between `---` markers, the description must
be specific, and the body must consistently target Microsoft Foundry.

At this stage `tools: []` makes the builder conversational only. It cannot inspect or
change the workspace. That limitation is intentional.

**Checkpoint:** The custom agent appears as **Foundry Prompt Agent Builder** in the agent picker
and contains no endpoints, credentials, project IDs, or customer-specific design.

## 2. Add repository read and search tools

**Why:** A Foundry professional should reuse the project's templates, versions, and
conventions. Read-only repository access grounds advice without granting modification or
execution rights yet.

In normal **Agent** mode, ask GitHub Copilot to update only the custom-agent frontmatter:

```text
Change the Foundry Prompt Agent Builder tools to ['read', 'search']. Make no other changes.
```

Select **Foundry Prompt Agent Builder** and ask:

```text
Inspect this repository and identify the exact templates, SDK versions, authentication
pattern, and environment variables for a Foundry prompt agent. Do not edit or execute.
```

The builder should cite inspected files, find the Lab 01 Project Client examples, and
separate confirmed repository facts from recommendations.

**Checkpoint:** The builder grounds its answer in local files and remains unable to edit
or execute commands.

## 3. Add official web research

**Why:** Repository evidence proves how this training project works, but Foundry services
change. Web access lets the builder verify unresolved or current facts against official
Microsoft documentation.

Update only the frontmatter:

```text
Change the Foundry Prompt Agent Builder tools to ['read', 'search', 'web']. Make no other changes.
```

Test it with:

```text
Compare the installed Foundry SDK capabilities with current official Microsoft guidance.
Use repository evidence first and official Microsoft sources only where needed.
```

It should identify whether a fact comes from local code, the pinned SDK, or current
documentation. It must flag preview APIs and version differences.

**Checkpoint:** Web research is selective, uses official sources, and does not override
verified local behavior with examples from a different SDK version.

## 4. Add editing, execution, and structured questions

**Why:** These tools move the builder from advice to implementation. Add them only after
students have observed its professional reasoning and evidence hierarchy. Human review
is still required before code or resources change.

Update only the frontmatter:

```text
Change the Foundry Prompt Agent Builder tools to
['vscode/askQuestions', 'read', 'search', 'web', 'edit', 'execute'].
Make no other changes.
```

Ask the builder to inspect one Lab 01 script, propose a harmless documentation comment,
and wait for approval before editing. Then ask it to validate only that file. This tests
the plan, approval, edit, and validation behavior without creating an Azure resource.

**Checkpoint:** The builder can ask structured questions, edit reviewed files, and run
focused checks, but pauses before resource-changing commands.

## 5. Add workspace skills for consistent tool usage

**Why:** Frontmatter grants access to tools but does not guarantee when or how they are
used. Skills package repeatable procedures that load only for matching tasks.

Ask **Foundry Prompt Agent Builder** to create:

| Skill | Purpose |
|-------|---------|
| `.github/skills/foundry-prompt-agent-lifecycle/SKILL.md` | Design instructions, create immutable prompt-agent versions, test them, and separate versioning from publishing. |
| `.github/skills/foundry-tool-integration/SKILL.md` | Choose and validate MCP, OpenAPI, function, search, file, code, or toolbox integrations. |
| `.github/skills/foundry-memory-design/SKILL.md` | Choose conversation context, memory store, workflow state, or application data and enforce lifecycle controls. |

Use this prompt:

```text
Create the three workspace skills defined in this exercise. Use valid SKILL.md
frontmatter. Each lowercase hyphenated name must match its folder. Give each skill a
keyword-rich description stating when it loads. Each procedure must clarify requirements,
inspect repository evidence, verify installed SDK support, use official documentation for
remaining current facts, apply security and lifecycle checks, and define validation.
Show the proposed files and wait for review before editing.
```

Test skill discovery with three separate prompts:

```text
Plan the lifecycle for a managed Foundry prompt agent from instructions through publishing.
```

```text
Choose a tool for an agent that reads and cancels orders.
```

```text
Decide whether an employee assistant should remember preferences across conversations.
```

Ask which skill was used and inspect whether its procedure was followed. Skills improve
how the builder uses tools; they do not add an external service or create memory.

**Checkpoint:** All three skills have valid names and descriptions, load for matching
requests, and produce consistent evidence, security, and validation steps.

## 6. Pass the builder readiness gate

**Why:** The builder should prove its professional behavior before it is allowed to create
a target agent or change Foundry resources.

Test these requests without permitting implementation:

1. A managed FAQ assistant with supported Foundry tools.
2. A prompt agent that needs current documentation, user preferences, and uploaded files.
3. A refund agent requested without authentication, limits, logging, or rollback.

The builder passes when it:

- asks for missing requirements
- remains within the managed Foundry prompt-agent scope
- identifies unsupported or out-of-scope runtime requirements instead of changing frameworks
- challenges the unsafe refund design
- identifies required tools, identity, approvals, tests, traces, and rollback
- distinguishes verified facts from assumptions
- proposes a staged plan and waits for approval

**Checkpoint:** Phase 1 is complete. Do not continue until the builder passes all criteria.

# Phase 2: Use the builder to create a Foundry agent

The Foundry Prompt Agent Builder is now ready. In this phase it creates a target agent through
successive Foundry versions. Each version adds one capability so its effect remains
testable.

## 7. Define the target scenario

**Why:** Tools and memory must follow a business requirement. Starting from a scenario
prevents technology from becoming the goal.

Use this default scenario or define an equivalent one:

```text
Design a Microsoft Foundry Delivery Advisor for engineers. It must answer current Foundry
questions from approved Microsoft sources, cite evidence, remember each engineer's
preferred language and experience level across conversations, analyze uploaded evaluation
results, and search approved internal agent standards. It must never deploy, publish, or
change Azure resources without explicit approval.
```

Ask the builder for requirements and architecture only. Resolve users, data, actions,
risk, identity, retention, evaluation, and success criteria before code is generated.

**Checkpoint:** The approved design maps every proposed capability to a requirement and
identifies assumptions that still need a human decision.

## 8. Create target version 1: instructions only

**Why:** An instructions-only baseline proves whether the target respects its role and
admits that current or private information is unavailable before tools and memory exist.

Ask the builder to create a `target-agent` folder containing reusable instructions plus
Project Client create and chat scripts based on the Lab 01 templates. Require:

- `AIProjectClient` and `PromptAgentDefinition`
- `AzureCliCredential`
- existing environment-variable names
- no tools, memory, credentials, endpoints, or expected answers in source
- local syntax validation before deployment
- review before running the creation script

After approval, run only the reviewed creation script. Record the returned target-agent
name and immutable version. Test requests for current documentation, remembered
preferences, uploaded analysis, and internal standards. The baseline must disclose that
those capabilities are unavailable.

**Checkpoint:** Version 1 exists in Foundry with instructions only and passes its boundary
tests without inventing tool calls or memory.

## 9. Create target version 2: add Tool 1

**Why:** Add grounding first because current Foundry guidance requires authoritative
evidence. One tool at a time makes failures and behavior changes easy to attribute.

Ask the builder to use its `foundry-tool-integration` skill to select and add a read-only
official documentation tool. For the default scenario, Microsoft Learn MCP is a suitable
candidate. Require it to verify:

- the service endpoint and hosting owner
- authentication and Foundry connectivity
- available operations and approval behavior
- input, output, timeout, and error handling
- prompt-injection treatment of returned content
- citation and trace acceptance tests

Creating or attaching a tool definition does not host the underlying service. Review the
tool configuration and create a new immutable target-agent version. Keep Version 1.

**Checkpoint:** Version 2 uses visible tool results before current claims, cites returned
sources, and still refuses unsupported actions.

## 10. Add a Foundry memory store

**Why:** Cross-conversation preferences justify durable memory in the default scenario,
but memory introduces consent, retention, isolation, deletion, and cost obligations. It
must not be treated as generic chat history or authoritative business data.

Ask the builder to use its `foundry-memory-design` skill. It must first confirm that
conversation context is insufficient and then define:

- the target-agent use case and allowed memory kinds
- a non-sensitive stable scope identifier
- compatible chat and embedding model deployments
- consent, tenant isolation, retention or TTL, inspection, and deletion
- tests for cross-user isolation, stale data, conflicts, and deletion

In this repository, `azure-ai-projects==2.4.0` exposes memory-store operations under
`project_client.beta.memory_stores`. The builder must inspect the installed SDK before
generating constructors or arguments, pin the version, and state that beta APIs may
change. Creating a memory store does not automatically attach it to every agent; verify
the supported integration for the selected target-agent type.

Review the design and generated code before allowing the memory-store creation command.
Record the store name and validation evidence, never credentials or raw personal data.

**Checkpoint:** The intended user preference persists across conversations, another scope
cannot retrieve it, deletion works, and current facts still come from Tool 1 rather than memory.

## 11. Create target versions 3 and 4: add Tools 2 and 3

**Why:** Add capabilities separately so each version has a clear purpose, test, and
rollback point. Multiple tools added together make routing and failure diagnosis harder.

For the default scenario:

1. Add **Tool 2** for analyzing uploaded evaluation results, considering code interpreter
   and file boundaries. Test supported formats, size limits, privacy, malformed input,
   output validation, and prohibited network access.
2. Add **Tool 3** for approved internal agent standards, considering file search or Azure
   AI Search. Test source allow-listing, citations, access isolation, stale content, and
   missing evidence.

Use the builder's tool-integration skill for each addition. Require a new immutable version
and focused acceptance tests before adding the next tool. Tool choice depends on actual
project resources; the builder must not invent an index, connection, vector store, file,
or hosted service.

**Checkpoint:** Version 3 proves Tool 2 routing and boundaries. Version 4 proves Tool 3
routing and grounding without regressing Tool 1 or memory isolation.

## 12. Use the skills to harden combined tool usage

**Why:** Individual tools may pass alone while the agent still chooses the wrong tool,
uses memory as evidence, or combines results unsafely. The skills provide a repeatable
review after the full capability set exists.

Ask the builder to review the target agent with all three skills and improve its
instructions so that it:

- searches current documentation with Tool 1
- analyzes only uploaded evaluation artifacts with Tool 2
- retrieves only approved internal standards with Tool 3
- uses memory only for consented preferences
- never treats memory as current product evidence
- asks before high-impact or resource-changing actions
- reports missing, conflicting, stale, or failed sources

Run prompts that require one tool, each pair of tools, all three tools, no tool, and a
tool failure. Inspect traces to confirm routing and result order.

**Checkpoint:** The target selects the minimum necessary capabilities, keeps source roles
separate, and degrades safely when one capability fails.

## 13. Evaluate and publish

**Why:** Successful SDK calls prove that resources exist, not that the target is useful,
safe, or ready for users. Stable evaluations and traces provide release and rollback
evidence.

Run the same acceptance suite against every version:

1. current Foundry question requiring official sources
2. preference recall in the same and a different user scope
3. uploaded evaluation analysis
4. internal-standard retrieval
5. ambiguous request
6. prompt injection inside tool content
7. missing or conflicting evidence
8. prohibited deployment or permission change

Compare quality, tool routing, safety, latency, and token use. Keep previous immutable
versions for rollback. Publish only the version that passes:

1. Select the tested version in Microsoft Foundry.
2. Choose **Publish**.
3. Create or update the managed Agent Application.
4. Wait for **Running**.
5. Grant only intended testers access.
6. Repeat the acceptance suite in **Test in website**.

Publishing is separate from `project_client.agents.create_version(...)`. Project
connections and externally hosted services also have separate management and deployment
lifecycles.

**Checkpoint:** The published application uses the tested version and reproduces its
approved behavior with trace evidence.

## Done when

- The Foundry Prompt Agent Builder passed its Phase 1 readiness gate before target work began.
- The builder can be reused for future managed Foundry prompt-agent projects.
- Builder tools were added progressively: read/search, web, then edit/execute.
- Prompt-agent lifecycle, tool-integration, and memory-design skills load for matching requests.
- Target Version 1 contains instructions only.
- Target Version 2 adds one grounded documentation tool.
- The memory store passes consent, isolation, persistence, and deletion tests.
- Target Versions 3 and 4 add and validate Tools 2 and 3 separately.
- Combined tool and memory routing passes the acceptance suite.
- The tested immutable target version is published with rollback evidence.
