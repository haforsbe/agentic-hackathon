# Daily Operations Planner

Build a Microsoft Foundry prompt agent that turns current tasks, deadlines, dependencies,
and available capacity into a realistic daily plan. You build the solution yourself with
GitHub Copilot.

## Before you begin

- Complete the shared [Lab 06 prerequisites](../README.md#prerequisites).
- Review [sample-data.json](sample-data.json), which contains synthetic tasks.

## When to use the sample data

Use [sample-data.json](sample-data.json) at two stages:

1. **During local testing in Step 2:** adapt the Responses quickstart so it reads the JSON
  file and includes its task data in the model input. This lets you test planning behavior
  before connecting Todoist. The agent must describe this as supplied sample data, not as
  live Todoist data.
2. **Before adding Todoist MCP in Step 4:** use the JSON file as a blueprint and manually
  create the `Hackathon Operations` project and sample tasks in the workshop Todoist
  account. After MCP is connected, Todoist becomes the authoritative source and the agent
  should no longer use the local JSON file for current task status.

The JSON file is not imported into Todoist automatically.

## 1. Create the agent in VS Code with GitHub Copilot

Start from these existing examples:

- [01-quickstart-responses.py](../../02-microsoft-foundry-agents/01-quickstart-responses.py)
  for local model testing.
- [02-quickstart-create-agent.py](../../02-microsoft-foundry-agents/02-quickstart-create-agent.py)
  for creating the prompt-agent version.

Ask Copilot to explain both examples, then create your own copies in this folder. Leave the
originals unchanged.

Create a Markdown file named `agent-instructions.md`. It must define the planner's user
and purpose, the factors used to prioritize work, the interruption buffer, how blocked
tasks are handled, how over-capacity is explained, and which Todoist actions require
explicit confirmation. Do not hard-code a plan for the sample tasks.

Review generated changes for secrets, invented task data, and unapproved side effects.

**Checkpoint:** You have two quickstart copies and one instruction file that Copilot can
explain. The instructions would still work with a different task list.

## 2. Test it locally

1. Adapt your copy of
  [01-quickstart-responses.py](../../02-microsoft-foundry-agents/01-quickstart-responses.py).
2. Load [sample-data.json](sample-data.json) with Python's JSON support. Resolve it relative
  to the script, not the terminal's current folder.
3. Load the instruction file from Step 1 and pass it as the request's instructions.
4. Include the sample tasks and one test question in the request input. Label them as
  supplied sample data rather than live Todoist data.
5. Run one question at a time: a six-hour plan, an impossible four-hour workload, and a
  request to put overdue blocked tasks first.

The agent should reject impossible capacity, expose tradeoffs, and schedule unblock
actions. Improve its instructions rather than hard-coding expected answers.

**Checkpoint:** The script runs without errors, refers to IDs from the JSON, respects the
available capacity, identifies an unblock action, and never claims to have used Todoist.

## 3. Deploy it to Foundry

1. Adapt your copy of
  [02-quickstart-create-agent.py](../../02-microsoft-foundry-agents/02-quickstart-create-agent.py)
  so it loads the tested instruction file.
2. Set a unique `AGENT_NAME` in `.env`, run the script, and record the printed agent name
  and version.
3. Copy and adapt
  [03-quickstart-chat-with-agent.py](../../02-microsoft-foundry-agents/03-quickstart-chat-with-agent.py)
  to invoke that agent by name. Replace its questions about France with one planning
  question from Step 2.
4. Open it under **Microsoft Foundry > Build > Agents** and compare its displayed
  instructions with the local file.

**Checkpoint:** The prompt agent appears in Foundry and produces the expected planning
behavior when invoked through the chat quickstart.

## 4. Tweak and add tools in Foundry

### Prepare Todoist

Create a free Todoist workshop account and a project named `Hackathon Operations`. Use
[sample-data.json](sample-data.json) as a blueprint and manually create its tasks. Include
each sample ID, such as `T-201`, in the task title or description. Do not add real employee
tasks or confidential information.

### Add Todoist MCP

| Setting | Value |
|---------|-------|
| Tool type | Remote MCP |
| Server label | `todoist-operations` |
| Server URL | `https://ai.todoist.net/mcp` |
| Authentication | OAuth through a Foundry project connection |
| Account | Synthetic workshop account only |
| Approval for reads | During development |
| Approval for writes | Always |

1. Open the agent version and choose **Add tool > MCP**.
2. Add the label and URL above, then create the OAuth project connection.
3. Allow-list project and task read operations first.
4. Ask the agent to list tasks in `Hackathon Operations`. Confirm a Todoist MCP read call
  appears in the trace and sample tasks such as T-201 and T-202 are returned.
5. Add only required create, update, reschedule, and complete operations.
6. Require **Always** approval for every write operation.

If OAuth is blocked by tenant policy, continue with local sample data rather than embedding
a token. Once MCP works, Todoist becomes the authoritative source instead of the JSON file.

### Add Code Interpreter

**Code Interpreter** lets the agent run Python in a managed, isolated environment. Here it
can apply priority weights, total task durations and buffers, verify that work fits available
hours, calculate over-capacity, and produce a schedule without overlaps.

For example, a six-hour day with a 15% interruption buffer has 5 hours and 6 minutes of
planned-task capacity. Code Interpreter can calculate and verify that limit.

Todoist MCP retrieves and updates tasks. Code Interpreter does not access Todoist or decide
which task matters. It only makes the numeric work reproducible and visible in the trace.

Code Interpreter is recommended, not required. Without it, manually verify all scores,
duration totals, buffers, and capacity calculations.

1. Choose **Add tool > Code Interpreter**.
2. Tell the agent to use it for scores, duration totals, buffers, and capacity validation.
3. Require input values and calculations in the response.
4. Test one plan that fits and one that exceeds capacity.

Use synthetic task fields only. Do not upload real employee exports or sensitive files.

### Test the tools

In the Microsoft Foundry agent playground:

1. Ask for a six-hour plan. Open the trace and confirm a Todoist read call occurred before
  the agent described current tasks.
2. Ask it to fit all work into four hours. Confirm it explains the shortfall instead of
  silently shortening or dropping tasks.
3. Ask it to prioritize a blocked task. Confirm it recommends an unblock action.
4. Ask it to reschedule T-206 and complete T-204. Confirm it shows both proposed changes
  and that Foundry pauses the MCP call for approval. Inspect the server, tool name, and
  arguments in the approval view.
5. Deny the tool call, then check Todoist and confirm both tasks remain unchanged.

Save the tested configuration as a new version.

## 5. Publish and Test in website

Publish the tested version as a managed Agent Application, wait for **Running**, grant
testers `Foundry User` if required, and choose **Test in website**. Repeat all five tests.

If tools fail only after publishing, repair application identity or connection permissions.
Never disable approval to solve authentication.

## Done when

- The plan uses current task data and fits available capacity.
- Blocked work becomes an unblock action.
- Scores and tradeoffs are visible.
- No Todoist write occurs without approval.
- The same controls work through **Test in website**.