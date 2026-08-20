# Market Opportunity Researcher

Build a Microsoft Foundry prompt agent that gathers current market evidence, handles
conflicting sources, and ranks commercial opportunities without hiding uncertainty.

## Before you begin

- Complete the shared [Lab 04 prerequisites](../README.md#prerequisites).
- Review the synthetic research brief in [sample-data.json](sample-data.json).

## 1. Create the agent in VS Code with GitHub Copilot

Start from these existing examples:

- [01-quickstart-responses.py](../../01-microsoft-foundry-agents/01-quickstart-responses.py)
  for local model testing.
- [02-quickstart-create-agent.py](../../01-microsoft-foundry-agents/02-quickstart-create-agent.py)
  for creating the prompt-agent version.

Ask Copilot to explain both examples, then create your own copies in this folder. Leave the
originals unchanged.

Create a Markdown file named `agent-instructions.md`. It must define the research audience
and scope, source-quality expectations, how facts and assumptions are separated, how
opportunities are scored, how financial scenarios show uncertainty, and how contradictory
evidence is handled. The agent must never invent evidence or claim research it did not
perform.

**Checkpoint:** You have two quickstart copies and one instruction file that Copilot can
explain. The instructions describe a research method, not answers to the supplied brief.

## 2. Test it locally

Use [01-quickstart-responses.py](../../01-microsoft-foundry-agents/01-quickstart-responses.py)
as the starting point for the local test:

1. Create your own copy of the quickstart in this scenario folder and leave the original
  quickstart unchanged. Skip this if you made the copy in Step 1.
2. Use GitHub Copilot to make your copy load [sample-data.json](sample-data.json) with
  Python's JSON support. Resolve it relative to the script.
3. Load the instruction file from Step 1 and pass it as the request's instructions.
4. Include both the loaded research brief and the test question in the request input.
  Label the brief as reference data, not as verified market evidence.
5. Run one question at a time and inspect which brief fields the response uses.

First ask for a research plan for three Nordic retail AI opportunities and the evidence
still needed. Then request an exact 2027 forecast despite missing reliable market-size data.

Without a web tool, the agent should design research and refuse fabricated findings.
It should mention constraints and scoring weights from the JSON, confirming that the brief
reached the model, but it must not claim that it performed live web research.

**Checkpoint:** The script runs without errors, uses constraints and scoring weights from
the JSON, refuses false precision, and clearly says that live evidence is still needed.

## 3. Deploy it to Foundry

1. Adapt your copy of
  [02-quickstart-create-agent.py](../../01-microsoft-foundry-agents/02-quickstart-create-agent.py)
  so it loads the tested instruction file.
2. Set a unique `AGENT_NAME` in `.env`, run the script, and record the printed agent name
  and version.
3. Copy and adapt
  [03-quickstart-chat-with-agent.py](../../01-microsoft-foundry-agents/03-quickstart-chat-with-agent.py)
  to invoke that agent by name. Replace its questions about France with one research
  question from Step 2.
4. Open it under **Microsoft Foundry > Build > Agents** and verify its displayed
  instructions match the local file.

**Checkpoint:** The agent appears in Foundry, the chat quickstart invokes it, and it still
distinguishes a research plan from completed research.

## 4. Tweak and add tools in Foundry

### Add Tavily MCP

| Setting | Value |
|---------|-------|
| Tool type | Remote MCP |
| Server label | `tavily-market-research` |
| Server URL | `https://mcp.tavily.com/mcp/` |
| Authentication | OAuth or free-tier API key in a Foundry project connection |
| Allowed tools | Web search and page extraction only |
| Approval | Enabled during development |

1. Create a free Tavily workshop account.
2. Open the agent version and choose **Add tool > MCP**.
3. Add the server label and URL above.
4. Create the supported Foundry project connection and store credentials only there.
5. Allow-list only search and extraction operations.
6. Keep approval required during development. Test one search and confirm Foundry pauses
  before execution. Inspect the server, tool name, arguments, URLs, dates, and extracted
  content, then approve only the expected read call.

Verify authentication guidance and free-tier limits before the event. Never append an API
key to a committed URL or place it in agent instructions.

### Add Code Interpreter

**Code Interpreter** lets the agent run Python in a managed, isolated environment. Here it
can apply opportunity-scoring weights, compare opportunities with the same formula, calculate
financial scenario ranges, check conversions and percentages, and expose how inputs affect
the result.

For example, it can compare conservative, expected, and optimistic scenarios instead of
inventing one exact forecast. Each scenario should show customer count, price, adoption
assumption, currency, period, and formula.

Tavily MCP finds current evidence. Code Interpreter does not search the web, validate a
source, or turn an unsupported assumption into a fact. Reliable arithmetic applied to weak
evidence still produces a weak conclusion.

Code Interpreter is recommended, not required. Without it, manually verify opportunity
scores, financial calculations, conversions, and scenarios.

1. Choose **Add tool > Code Interpreter**.
2. Tell the agent to use it for weighted scores and financial scenarios.
3. Require formulas, inputs, currency, period, assumptions, and ranges in responses.
4. Test one evidence-backed calculation and one request with missing market-size data.

Use only public or synthetic inputs. Do not upload licensed reports, confidential forecasts,
customer lists, or sensitive files.

### Test the tools

In the Microsoft Foundry agent playground:

1. Ask for current evidence about Nordic retail AI adoption. Confirm the trace shows a
  Tavily search before the response makes current claims.
2. Open several cited URLs and confirm the pages support the claims and publication dates.
3. Ask for an exact forecast without enough market-size evidence. Confirm the agent labels
  assumptions and avoids false precision.
4. Ask for evidence both supporting and opposing rapid adoption. Confirm both sides remain
  visible in the answer.
5. Ask what changed during the last 90 days. Confirm older sources are not presented as new.

Save the tested configuration as a new version.

## 5. Publish and Test in website

Publish the tested version as a managed Agent Application, wait for **Running**, grant
testers `Foundry User` if required, and choose **Test in website**. Repeat all tests and
confirm source links survive in the website experience.

## Done when

- Current claims have dated, resolvable sources.
- Important claims are corroborated or marked as single-source.
- Facts, assumptions, and estimates are distinct.
- Opportunity scores expose their inputs.
- Grounded behavior works through **Test in website**.