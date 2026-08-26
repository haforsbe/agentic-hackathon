# Microsoft Cloud Guidance Advisor

Build a Microsoft Foundry prompt agent that answers technical questions with current,
official Microsoft documentation and code samples. Use GitHub Copilot in VS Code to create
the agent files from the Foundry quickstart tasks, then connect Microsoft Learn MCP.

## What you will build

The finished agent can:

- search official Microsoft and Azure documentation
- fetch full documentation pages for detailed guidance
- find official code samples
- compare Microsoft services with visible evidence and caveats
- refuse invented citations and unsupported current claims

Microsoft operates this MCP endpoint and documents it for use with Microsoft Foundry.

## Before you begin

Complete the shared [Lab 04 prerequisites](../README.md#prerequisites). Confirm that the
virtual environment is active, `az login` has completed, and `.env` contains the project
endpoint, model deployment, and `AGENT_NAME=microsoft-cloud-guidance-advisor-yourname`.
Microsoft Learn MCP is public and needs no key or OAuth setup.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| VS Code baseline | Student-created instructions and chat script, without tools | Explain its research method and disclose that official docs were not retrieved. |
| Foundry | The same instructions plus Microsoft Learn MCP | Search and fetch official sources before making current product claims. |

There is no sample-data file. Current documentation reaches the agent only through the
MCP tool after it is connected in Foundry.

## 1. Create the instructions

In VS Code, open GitHub Copilot Chat in **Agent** mode. Ask it to create
`agent-instructions.md` in this folder with a source boundary, research workflow, response
format, and integrity rules.

Confirm the instructions require:

1. documentation search for current product claims
2. full-page retrieval for detailed guidance
3. official code-sample search for implementation requests
4. titles and URLs for citations
5. visible uncertainty, conflicts, preview status, and missing evidence

Do not paste product documentation or code samples into the instruction file.

**Checkpoint:** The instructions describe a reusable research process and contain no
hard-coded product answer.

## 2. Create the Python tasks with GitHub Copilot

Use these options in order:

1. **Try it yourself first:** Write your own prompt for GitHub Copilot Agent mode. Think
   about which Lab 01 files are templates, which files Copilot must create, what behavior
   is unique to this scenario, and what must not be hard-coded.
2. **Use the example second:** After your own attempt, compare it with the prompt below.
   You can refine your prompt or use the example as is if you need more guidance.

Whichever option you use, review Copilot's plan before accepting changes.

```text
Use 01-microsoft-foundry-agents/02-quickstart-create-agent.py as a template to create
04-Agent Examples/03-microsoft-cloud-guidance-advisor/02-quickstart-create-agent.py.
Preserve the template's Microsoft Foundry SDK, AzureCliCredential, model, endpoint, and
AGENT_NAME environment-variable pattern. Load instructions from agent-instructions.md
beside the new script instead of hard-coding them. Do not add tools or credentials.

Use 01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py as a template to create
04-Agent Examples/03-microsoft-cloud-guidance-advisor/03-quickstart-chat-with-agent.py.
Keep the agent-reference conversation pattern. Ask for current managed-identity guidance,
a method for comparing Container Apps and App Service, and the latest official Python SDK
sample without naming a service. Do not provide documentation or code samples in the script.
```

Review both generated files. They must read the existing `.env` values and contain no
endpoint, credential, product documentation, expected answers, or MCP implementation.

## 3. Create and test the no-tool agent from VS Code

From the workspace root, run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\02-quickstart-create-agent.py"
& .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\03-quickstart-chat-with-agent.py"
```

Confirm the agent discloses that documentation was not retrieved, explains a sound
research method, and asks which service is intended rather than inventing a sample. If a
response fails, improve `agent-instructions.md`, rerun the creation script, and repeat the
chat script.

**Checkpoint:** The student-created scripts run in VS Code, and the first immutable
Foundry version contains instructions and no tools.

## 4. Connect Microsoft Learn MCP

### Create the tool

1. In Microsoft Foundry, open **Build > Tools**.
2. Select **Connect a tool**.
3. Select the custom **MCP** tool option.
4. Enter:

   | Setting | Value |
   |---------|-------|
   | Name | `microsoft-learn` |
   | Remote MCP server endpoint | `https://learn.microsoft.com/api/mcp` |
   | Authentication | **Unauthenticated** |

5. Select **Connect** or **Create**.
6. Open the tool and confirm Foundry discovers the Microsoft Learn operations.

Do not select **Key-based** or **OAuth Identity Passthrough**. Do not append a key, token,
or query string to the endpoint.

### Add the tool to a new agent version

1. Return to **Build > Agents** and open the guidance agent.
2. Choose **Edit** or create a new version from the existing one.
3. Select **Add tool** and choose `microsoft-learn`.
4. Allow these read-only operations:
   - `microsoft_docs_search`
   - `microsoft_docs_fetch`
   - `microsoft_code_sample_search`
5. Require approval during development so each search is visible.
6. Save the configuration as a new immutable version.

Keep the first no-tool version as a behavioral baseline.

### Test the connected tool

In the agent playground, ask:

```text
Compare Azure Container Apps and Azure App Service for a public Python API. Use current
official Microsoft documentation, state the deciding constraints, and cite sources.
```

When an approval appears:

1. verify the server is `microsoft-learn`
2. inspect the search query
3. approve only the expected read call
4. confirm the agent fetches important pages before detailed recommendations
5. open the completed trace and inspect each tool result

Also test:

- `Find the current steps for configuring managed identity in Azure Container Apps.`
- `Show an official Python code sample for DefaultAzureCredential.`
- `Tell me a product limit, but do not search the documentation.`

The final request should not bypass the source requirement for a current limit.

**Checkpoint:** Current claims and code are grounded in visible Microsoft Learn results,
and citations use returned titles and URLs.

## 5. Test the MCP-backed agent from VS Code

The generated chat script cannot approve a tool call interactively. After inspecting the
three allow-listed read operations in the playground, edit the agent again, set approval
to **Never** for only those operations, and save a new runtime version.

Rerun `03-quickstart-chat-with-agent.py` from Step 3. Inspect the trace and confirm current
claims use Learn MCP results with returned titles and URLs.

## 6. Publish and test in website

1. Select the tested MCP-backed version and choose **Publish**.
2. Create or update the managed Agent Application.
3. Wait until the deployment reports **Running**.
4. Grant intended testers `Foundry User` if required.
5. Choose **Test in website**.
6. Repeat the service-comparison and managed-identity tests.
7. Open source links and confirm they support the response.

Saving an agent version does not publish it. Publish the MCP-backed version that passed
the playground checks.

## Troubleshooting

### A generated script fails before reaching Foundry

Compare it with the corresponding task in `01-microsoft-foundry-agents`. Confirm the
virtual environment is active, `az login` uses the intended tenant, and all three `.env`
values are present. Never paste `.env` contents into Copilot Chat.

### The baseline agent invents citations

Strengthen the source-boundary rules, rerun the creation script, and repeat the chat
script. Do not add URLs to the test prompt to make it pass.

### Foundry cannot discover Microsoft Learn tools

Confirm the endpoint is exactly `https://learn.microsoft.com/api/mcp` and authentication
is **Unauthenticated**. Remove any headers, keys, or query parameters.

### The agent searches but does not fetch pages

Confirm `microsoft_docs_fetch` is allow-listed and the instructions require fetching
high-value pages before detailed guidance.

### Citations do not support the answer

Inspect the trace and retrieved page content. Refine the search query or instructions;
do not rely on a search snippet for a detailed claim.

### Playground works but Test in website fails

Confirm the Agent Application uses the tested version and can reach Microsoft Learn MCP.
Do not add credentials because the endpoint is unauthenticated.

## Done when

- GitHub Copilot created `agent-instructions.md` and both Python tasks in VS Code.
- The generated files contain no secrets, endpoints, documentation, or expected answers.
- The no-tool chat check discloses that official documentation was not retrieved.
- A new Foundry version has all three read-only Learn operations.
- The student-created chat script works with the MCP-backed runtime version.
- Traces show search, fetch, and code-sample calls where appropriate.
- The published Agent Application gives source-grounded answers in **Test in website**.