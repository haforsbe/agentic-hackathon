# Microsoft Cloud Guidance Advisor

Build a Microsoft Foundry prompt agent that answers technical questions with current,
official Microsoft documentation and code samples. Test its instructions locally first,
then connect the Microsoft Learn MCP tool in Foundry.

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
virtual environment is active, `az login` has completed, and the root `.env` contains:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=your-project-endpoint
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=your-model-deployment
AGENT_NAME=microsoft-cloud-guidance-advisor-yourname
```

Keep real values private. Microsoft Learn MCP is public and needs no key or OAuth setup.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| Local test | Instructions and one question | Explain its research method and disclose that official docs were not retrieved. |
| Foundry | The same instructions plus Microsoft Learn MCP | Search and fetch official sources before making current product claims. |

There is no sample-data file. Current documentation reaches the agent only through the
MCP tool after it is connected in Foundry.

## 1. Review the instructions

Open [agent-instructions.md](agent-instructions.md). Ask GitHub Copilot to explain the
source boundary, research workflow, response format, and integrity rules.

Confirm the instructions require:

1. documentation search for current product claims
2. full-page retrieval for detailed guidance
3. official code-sample search for implementation requests
4. titles and URLs for citations
5. visible uncertainty, conflicts, preview status, and missing evidence

Do not paste product documentation or code samples into the instruction file.

**Checkpoint:** The instructions describe a reusable research process and contain no
hard-coded product answer.

## 2. Test only the instructions locally

[local_test.py](local_test.py) loads the instructions and sends a question directly to
the model. It has no documentation tool and no sample data.

Run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\local_test.py" --test no-tool
```

The response should disclose that it did not retrieve current Microsoft Learn pages. It
must not invent links or claim that a documentation search occurred.

Run the other tests:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\local_test.py" --test method
& .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\local_test.py" --test code
```

The code test should ask which Microsoft service is intended instead of inventing a
sample. Use `--test all` to run all three.

If a test fails, improve `agent-instructions.md` and rerun it. Do not add documentation,
URLs, or expected answers to the Python runner.

**Checkpoint:** The agent is honest about missing tools, explains a defensible research
method, and asks for material missing context.

## 3. Create the prompt agent in Foundry

1. Set a unique `AGENT_NAME` in `.env`.
2. Run:

   ```powershell
   & .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\02-quickstart-create-agent.py"
   ```

3. Record the printed agent name and version.
4. Open **Microsoft Foundry > Build > Agents**.
5. Select the agent and confirm its instructions match
   [agent-instructions.md](agent-instructions.md).
6. Ask for current official guidance once. Confirm the agent discloses that no
   documentation tool is connected.

**Checkpoint:** The first immutable version contains instructions and no tools.

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

## 5. Test with the Python chat client

The Python script has no interactive approval handler. After inspecting the three
allow-listed read operations in the playground, edit the agent, change approval for only
those operations to **Never**, and save a new runtime version. Do not expand the allow-list.

[03-quickstart-chat-with-agent.py](03-quickstart-chat-with-agent.py) sends only the
technical question; it does not embed documentation.

Confirm `AGENT_NAME` names the MCP-backed agent, then run:

```powershell
& .\.venv\Scripts\python.exe ".\04-Agent Examples\03-microsoft-cloud-guidance-advisor\03-quickstart-chat-with-agent.py"
```

Open the run trace in Foundry. Confirm it contains documentation search and full-page
fetch calls before detailed current guidance.

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

### The local test invents citations

Strengthen the source-boundary rules and rerun `--test no-tool`. Do not add URLs to the
test prompt to make it pass.

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

- Local tests use only instructions and questions.
- The no-tool test discloses that official documentation was not retrieved.
- A new Foundry version has all three read-only Learn operations.
- Traces show search, fetch, and code-sample calls where appropriate.
- The published Agent Application gives source-grounded answers in **Test in website**.