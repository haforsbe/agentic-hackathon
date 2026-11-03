# Optional Weather-agent GitHub delivery lab

This is an optional lab **after Weather checkpoint 07 and before Cultural
checkpoint 08**. It is not a numbered core checkpoint. Skipping it or
completing it returns directly to checkpoint 08; the core stays 00-16 and
remains planned for 5-6 hours.

## What this lab does—and does not do

The lab practices a reviewed Git configuration change, offline CI checks,
evidence-linked validation, and an explicitly gated release for the Weather
Research Agent only. Its capture, manifest, and evidence checks are supported
offline. The current GitHub Actions workflow runs offline contract tests only.
It has no Azure identity, cloud calls, tool approvals, or deployment steps.
The live Foundry validation, per-call MCP approval, stable consumer-path
verification, and release remain separate participant-approved actions.

This uses **one Microsoft Foundry Project as a training compromise**, not as a
production pattern or best practice. The validation candidate and released
Weather agent must be separate resources with explicitly separate memory
scopes. This reduces accidental changes to the released agent; it does not
isolate quotas, permissions, project-wide resources, audit scope, or blast
radius. Never infer memory isolation from using separate Conversations.

GitHub CI's short-lived workload identity, the participant/runtime identity,
and any agent identity are different principals. A GitHub Environment approval
or a successful CI run is **not** per-call MCP approval. Keep the actual
`weather_forecast` request visible and require a human to approve or deny that
specific call in the supported Microsoft Foundry prompt-agent runtime. If the
runtime cannot surface the exact request and preserve its Conversation for
continuation, stop: do not auto-approve, switch to direct MCP, or claim a pass.

## Route

1. **Capture** the reviewed Weather configuration and release dependencies
   from service read-back. Record the instructions and model policy; exact
   released-agent/version and Stable Agent Endpoint; Toolbox name, pinned
   version-specific MCP URL, and discovered qualified tool mapping; distinct
   upstream and Toolbox-authentication connection references; skill revision
   and delivery method; and memory configuration hash and separate candidate/
   release scopes. Include no tool credentials, private Conversations,
   transcripts, memory contents, or bearer tokens. Do not construct a URL from
   a display name or substitute the project endpoint for the Stable Agent
   Endpoint.
2. **Review in Git.** Put only the sanitized manifest, agent-definition file,
   instructions source, and synthetic/public test cases in the participant's
   `student/weather-delivery/` folder. The manifest pins the agent-definition
   and instructions file hashes; offline CI checks those hashes against the
   reviewed files. Open a normal GitHub pull request and review the diff. The
   manifest contract rejects unknown fields, missing dependency references,
   shared connections, unverified bindings, and non-pinned Toolbox endpoints;
   it does not silently remove unsupported fields.
3. **Run offline CI.** The
   [Weather delivery check](../../.github/workflows/weather-delivery-check.yml)
   runs standard-library tests with no secrets, Azure login, network calls,
   model usage, MCP invocation, or `id-token` permission. A passing check proves
   only that the local contract and progress-state tests passed. It does not
   prove Foundry access or runtime behavior.
4. **Validate the separate candidate.** After reviewing the exact commit,
   create/use a separate validation agent in the same project and keep its
   Toolbox version, effective allowlist, model policy, skill revision, and
   other dependencies pinned to the reviewed manifest. Verify the candidate
   identity and memory scope independently; never modify the released agent or
   its dependencies during validation. Run a fresh managed Conversation with
   the real Weather MCP server exposed through the verified Toolbox. Capture
   only returned evidence IDs and hashes, including one actual approved call
   and a separate denied call. Do not save raw arguments, prompts, replies, or
   memory content in shared files.
5. **Gate and release manually.** Do not release until the same reviewed
   configuration commit and manifest hash match the passing offline CI run,
   candidate version, dependency references, explicit approval/denial traces,
   and isolated memory evidence. Use the supported Foundry release action only
   after a separate current-step approval. Read back the service-returned
   version/Stable Agent Endpoint, then test through that consumer path and
   retain its evidence IDs. If any identity, dependency version, permission,
   approval, or endpoint differs, block release and preserve the failed
   evidence. A project endpoint or Toolbox MCP URL is not the consumer path.

The standard-library validator can check internal consistency:

```text
python -S -m workshop.weather_delivery.contract check-manifest student/weather-delivery/manifest.json
python -S -m workshop.weather_delivery.contract check-validation student/weather-delivery/manifest.json .workshop/evidence/weather-validation.json --repository haforsbe/agentic-hackathon --default-branch FY27 --current-commit "$CURRENT_SHA" --latest-sha "$LATEST_DEFAULT_BRANCH_SHA" --latest-attempt "$LATEST_RUN_ATTEMPT"
python -S -m workshop.weather_delivery.contract check-release student/weather-delivery/manifest.json .workshop/evidence/weather-validation.json .workshop/evidence/weather-release.json --repository haforsbe/agentic-hackathon --default-branch FY27 --current-commit "$CURRENT_SHA" --latest-sha "$LATEST_DEFAULT_BRANCH_SHA" --latest-attempt "$LATEST_RUN_ATTEMPT"
```

Evidence belongs in ignored `.workshop/evidence/`, not in the Git PR. The
validator checks hashes, pinned dependencies, exact CI run/artifact linkage,
actual evidence-ID presence, and the approval outcome shape; it cannot prove
that a human-reported ID came from Microsoft Foundry. The facilitator must
independently inspect required live evidence. Failed or blocked attempts stay
available for diagnosis and never authorize release. The shell variables in
the examples must come from an independent read of the current commit and
latest default-branch workflow attempt; never fill them from participant-
reported or stale values.

## Before any live rehearsal

This repository currently has **no** CI/CD Azure variables, GitHub Environment,
OIDC federated credential, role assignment, workflow dispatch, or live
Foundry/tool call configured or verified for this lab. Do not create these as
part of the offline exercise. A later facilitator-approved rehearsal must
separately establish:

- the exact GitHub repository/workflow/branch OIDC subject and a short-lived,
  least-privilege CI identity, distinct from the participant/runtime identity;
- the exact existing one-project scope and permitted create/read operations,
  without write-probing, role broadening, or creating another model deployment;
- a supported way for the prompt-agent runtime—not a developer client—to use
  the version-pinned Toolbox while preserving human per-call approval and the
  same managed Conversation for approval continuation;
- explicit cost/spend agreement for each model/tool call, private artifact
  retention, a separate human release gate, and read-only consumer-path
  verification; and
- an observed full failure/recovery rehearsal on synthetic/public data.

The current official Microsoft documentation describes prompt-agent MCP
configuration, Toolbox endpoints, and approval continuation, but this lab has
not verified that complete workflow against a live project/runtime. Until it
has, **CI is offline-only and cloud validation/deployment are manual, gated,
and potentially blocked**. Never configure a GitHub Environment or workflow
identity as a substitute for the missing runtime evidence.

The optional lab is not included in the core time estimate. Do not reduce or
skip any 00-16 approval, evidence, test, or teach-back gate to fit it in.

## Official references

- [Connect agents to MCP server endpoints](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Create and manage a Toolbox](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/toolbox)
- [GitHub OIDC in Azure](https://docs.github.com/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure)
- [GitHub OIDC subject claims](https://docs.github.com/actions/reference/security/oidc#immutable-subject-claims)
