# Microsoft Cloud Guidance Advisor

Build a Microsoft Foundry prompt agent that answers technical questions with current,
official Microsoft documentation and code samples. Test it in Foundry without tools
first, then connect the Microsoft Learn MCP tool.

## What you will build

The finished agent can:

- search official Microsoft and Azure documentation
- fetch full documentation pages for detailed guidance
- find official code samples
- compare Microsoft services with visible evidence and caveats
- refuse invented citations and unsupported current claims

Microsoft operates this MCP endpoint and documents it for use with Microsoft Foundry.

## Before you begin

Complete the shared [Lab 04 prerequisites](../README.md#prerequisites). Confirm that you
can open the intended Foundry project, select a deployed model, and create and test agents.
Microsoft Learn MCP is public and needs no key or OAuth setup.

## Understand the two stages

| Stage | What the agent receives | Expected behavior |
|-------|-------------------------|-------------------|
| Foundry baseline | Instructions and one question | Explain its research method and disclose that official docs were not retrieved. |
| Foundry | The same instructions plus Microsoft Learn MCP | Search and fetch official sources before making current product claims. |

There is no sample-data file. Current documentation reaches the agent only through the
MCP tool after it is connected in Foundry.

## 1. Create the instructions

Create `agent-instructions.md` in this folder. Ask GitHub Copilot to draft it with a source
boundary, research workflow, response format, and integrity rules.

Confirm the instructions require:

1. documentation search for current product claims
2. full-page retrieval for detailed guidance
3. official code-sample search for implementation requests
4. titles and URLs for citations
5. visible uncertainty, conflicts, preview status, and missing evidence

Do not paste product documentation or code samples into the instruction file.

**Checkpoint:** The instructions describe a reusable research process and contain no
hard-coded product answer.

## 2. Create and test the prompt agent in Foundry

1. Open **Microsoft Foundry > Build > Agents**.
2. Select **Create agent** and choose your deployed model.
3. Name the agent `microsoft-cloud-guidance-advisor-yourname`.
4. Paste the complete contents of your `agent-instructions.md` into **Instructions**.
5. Save the first version without adding a tool.
6. Ask each baseline question in the playground:
   - `Give me current documented steps and official links for managed identity in Azure Container Apps.`
   - `How would you compare Azure Container Apps and Azure App Service after Learn tools are connected?`
   - `Provide the latest official Python SDK code for a Microsoft service.`
7. Confirm the agent discloses that documentation was not retrieved, explains a sound
   research method, and asks which service is intended rather than inventing a sample.
8. If a response fails, improve `agent-instructions.md`, update the agent in a new version,
   and repeat the same question.

**Checkpoint:** The first immutable version contains instructions and no tools.

## 3. Connect Microsoft Learn MCP

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

## 4. Publish and test in website

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

### The baseline agent invents citations

Strengthen the source-boundary rules, update the agent version, and repeat the same
playground question. Do not add URLs to the test prompt to make it pass.

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

- The student-created `agent-instructions.md` remains in the local working copy only.
- The no-tool playground check discloses that official documentation was not retrieved.
- A new Foundry version has all three read-only Learn operations.
- Traces show search, fetch, and code-sample calls where appropriate.
- The published Agent Application gives source-grounded answers in **Test in website**.