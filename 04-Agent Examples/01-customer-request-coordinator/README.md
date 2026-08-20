# Customer Request Coordinator

Build a Microsoft Foundry prompt agent that reviews customer requests, prioritizes
them consistently, drafts follow-up messages, and asks for approval before changing
data. You receive the challenge and sample data, but you build the agent yourself.

## Before you begin

- Complete the shared [Lab 04 prerequisites](../README.md#prerequisites).
- Review [sample-data.json](sample-data.json), which contains synthetic records only.
- Do not use real customer or personal data.

## 1. Create the agent in VS Code with GitHub Copilot

Start from these existing examples:

- [01-quickstart-responses.py](../../01-microsoft-foundry-agents/01-quickstart-responses.py)
  shows how to call the Foundry model while developing locally.
- [02-quickstart-create-agent.py](../../01-microsoft-foundry-agents/02-quickstart-create-agent.py)
  shows how to define and create a persistent prompt-agent version.

Ask Copilot to explain where each example reads configuration, sends model input, and sets
agent instructions. Then create your own copies in this folder and leave the originals
unchanged.

Create a Markdown file named `agent-instructions.md` that both copies can reuse. Use
Copilot to help draft it, but make the business decisions yourself. The instructions must
define:

- the coordinator's role and intended user
- how facts, assumptions, and missing fields are presented
- how customer impact, urgency, SLA risk, and strategic importance affect priority
- what a useful customer-response draft contains
- which actions require explicit user confirmation
- that customer record content is untrusted data, not agent instructions

Do not encode the expected answer for the supplied records. The instructions should still
work when the data changes.

Review Copilot's changes. Confirm secrets come from `.env` and the implementation remains
a Foundry prompt agent using `azure-ai-projects`.

**Checkpoint:** You have your own two quickstart copies and one reusable instruction file.
Copilot can explain each file, and the original quickstarts are unchanged.

## 2. Test it locally

Use [01-quickstart-responses.py](../../01-microsoft-foundry-agents/01-quickstart-responses.py)
as the starting point for the local test:

1. Create your own copy of the quickstart in this scenario folder. Keep the original
   quickstart unchanged so it remains a working reference. Skip this if you made the copy
   in Step 1.
2. Use GitHub Copilot to modify your copy so it loads [sample-data.json](sample-data.json)
   with Python's JSON support before calling `openai_client.responses.create`. Resolve the
   file relative to the script so it works regardless of the terminal's current folder.
3. Load the instruction file from Step 1 and pass it as the request's instructions.
4. Include both the loaded JSON content and the test question in the request input. Clearly
   label the JSON as **untrusted reference data** so text inside a customer record cannot
   override the agent instructions.
5. Run one test question at a time and inspect the response.

Start by asking the agent to rank the top three requests and draft a response for the
highest-priority request without changing data. Then test CR-1004, which has missing fields,
and CR-1005, which contains an embedded prompt-injection attempt.

The agent should use the data, disclose missing information, and ignore the embedded
prompt injection. Verify that it mentions request IDs and field values found in the JSON;
this confirms the sample data reached the model. It must describe the source as supplied
sample data and must not claim that it accessed Notion during this local stage.

When the behavior is wrong, give Copilot the observed output and ask it to improve the
instructions rather than hard-code a response.

**Checkpoint:** The script runs without errors, uses IDs and values from the JSON, flags
missing data in CR-1004, ignores the instruction inside CR-1005, and never claims to have
used Notion.

## 3. Deploy it to Foundry

1. Adapt your copy of
  [02-quickstart-create-agent.py](../../01-microsoft-foundry-agents/02-quickstart-create-agent.py)
  so it loads the same tested instruction file used locally.
2. Set a unique `AGENT_NAME` in `.env` and run the script once.
3. Record the agent name and version printed by the script. Re-running after changes can
  create another immutable version.
4. Copy and adapt
  [03-quickstart-chat-with-agent.py](../../01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py)
  to test the deployed agent by name. Replace its questions about France with one of the
  coordinator test questions from Step 2.
5. Open the agent under **Microsoft Foundry > Build > Agents** and confirm the displayed
  instructions match the local instruction file.

**Checkpoint:** The agent appears in the Microsoft Foundry portal, the chat quickstart can
invoke it, and its response follows the same rules as the local test.

## 4. Tweak and add tools in Foundry

### Prepare Notion

Create a free Notion workspace for workshop use and a database named `Customer Requests`.
Use [sample-data.json](sample-data.json) as a blueprint and manually create its synthetic
records in the database. The JSON file is not imported automatically. Do not add real
customer or personal data.

### Add Notion MCP

| Setting | Value |
|---------|-------|
| Tool type | Remote MCP |
| Server label | `notion-customer-requests` |
| Server URL | `https://mcp.notion.com/mcp` |
| Authentication | OAuth through a Foundry project connection |
| Workspace | Synthetic workshop workspace only |
| Approval for reads | During development |
| Approval for writes | Always |

1. Open the deployed agent version and choose **Add tool > MCP**.
2. Enter the server label and URL above.
3. Create an OAuth-backed project connection and authorize only the workshop workspace.
4. Initially allow-list only search and read operations.
5. Ask the agent to list records from `Customer Requests`. Confirm a Notion MCP read call
  appears in the trace and sample records such as CR-1001 are returned.
6. Add only the minimum create and update operations required by the challenge.
7. Keep approval set to **Always** for create, update, move, archive, and delete operations.

Never put an OAuth token in the URL, prompt, source code, or `.env` file. Once this
connection works, Notion becomes the authoritative source instead of the local JSON file.

### Add Code Interpreter

**Code Interpreter** lets the agent run Python in a managed, isolated environment. Here it
can apply the same priority weights to every request, calculate combined scores, sort the
requests consistently, and show how missing or changed inputs affect the ranking.

Notion MCP retrieves and updates records. Code Interpreter does not access Notion, decide
the business meaning of a field, or make missing data reliable. The agent must still disclose
assumptions and avoid false precision.

Code Interpreter is recommended, not required. Without it, verify every weighted score and
ranking manually.

1. Choose **Add tool > Code Interpreter**.
2. Tell the agent to use it for weighted scoring and ranking checks.
3. Require input values, weights, and the final score in the response.
4. Test one complete request and CR-1004, which has missing fields.

Use only synthetic request fields. Do not upload real customer exports or sensitive files.

### Test the tools

Test these cases in the Microsoft Foundry agent playground:

1. Read and rank open requests without changing anything.
2. Ask for a record with missing fields and verify uncertainty is visible.
3. Ask the agent to assign and update a request. Verify it displays the exact change
  and that Foundry pauses the MCP call for approval. Inspect the server, tool name, and
  arguments in the approval view before deciding.
4. Deny the approval and confirm that Notion remains unchanged.

Save the improved configuration as a new immutable version.

## 5. Publish and Test in website

1. Select the version that passed the tests and choose **Publish**.
2. Create or update the managed Agent Application.
3. Wait for the deployment to report **Running**.
4. Grant intended testers `Foundry User` on the Agent Application if required.
5. Choose **Test in website** and repeat the four tests above.

If tool calls work in the Microsoft Foundry agent playground but fail after publishing,
check the published application identity and project connection. Do not disable approval
to work around an authentication problem.

## Done when

- Current request facts come from the configured source.
- Missing information and assumptions are visible.
- Priority calculations use the stated weights.
- No external write happens without explicit approval.
- The controls still work through **Test in website**.