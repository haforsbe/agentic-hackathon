# Optional Weather-agent GitHub delivery lab

Offer this lab after Weather checkpoint 07, including CH01, and before
Cultural checkpoint 08. It is an optional extension, not a numbered core
checkpoint, and does not change the 5-6-hour core estimate.

## Goal and teaching story

Participants finish building and testing a Weather agent in Microsoft Foundry,
then experience a simple GitHub-based promotion:

**Foundry Dev agent -> capture workflow -> pull request and checks -> reviewed
merge -> approved GitHub Actions deployment -> Foundry Prod agent.**

Use one Microsoft Foundry Project as the workshop shortcut, with two distinct
agent resources: one manually edited Dev agent and one existing Prod agent.
The deployment workflow never writes to the Dev agent. This demonstrates
configuration history, review, automated checks, and controlled promotion
without requiring a second project. Explain that production environments
normally separate projects/resources and access more strongly.

The participant does not need to make an extra Dev edit just to begin this
lab. The capture uses the exact saved Dev version they select. If they want a
visible change to review, make and test it during the normal Weather lesson,
not as a new CI/CD prerequisite.

## Participant flow

### Coach opening and readiness

The Workshop Coach says:

> You've built and tested your Weather agent in Microsoft Foundry. Now you'll
> keep its configuration in Git and use GitHub to deliver it to a separate
> Prod agent, without manually copying settings. You'll capture it, review a
> pull request, and approve deployment. Dev stays unchanged.
>
> Capture -> review and checks -> merge -> approve deployment -> verify Prod.
>
> CI means continuous integration: automated checks on a proposed change.
> CD means continuous delivery: preparing and delivering an accepted change
> through a controlled process. This lab uses a manual capture and deployment
> approval so you can see those decisions.

Before asking the participant to run anything, confirm the exact repository,
default branch, Microsoft Foundry Project, existing Dev/Prod names, saved Dev
version and participant authorized to start deployment. Reuse earlier verified evidence
only while its identity, resource and operation scope remain unchanged.
Check the facilitator setup below, including PR checks and manual deployment
confirmation. No GitHub Environment is needed. Distinguish **configured**, **access verified** and
**live-rehearsed**; an existing setting alone proves neither of the latter.
If a prerequisite is missing, explain the specific blocker and offer setup
assistance, pause or an explicit skip. Never quietly weaken a gate to proceed.

The participant does not write JSON, create folders, configure a pipeline,
or copy a token during this promotion. The workflow creates
`student/weather-delivery/` automatically inside their repository. Its
`agent-definition.json` holds the captured configuration; `manifest.json`
records its source, intended destination and file fingerprint (SHA-256).
These are ordinary reviewable files, not a second cloud environment.

### Guided hands-on steps

1. **Capture Dev.** From the repository's default branch, manually run
   [Capture Weather Dev configuration](../../.github/workflows/weather-delivery-cloud.yml)
   and enter the exact saved Dev version. GitHub Actions reads that version
   from the configured Dev agent, writes the sanitized definition and a small
   source/target manifest into a unique branch, and opens a pull request.
2. **Review the proposed configuration.** The first PR adds the captured files
   to Git. Later PRs show changes since the previous capture. Participants
   inspect the instructions, model reference, and tool configuration in the
   diff. Merging the PR is their approval to make this captured configuration
   the desired version for Prod; it does not change Dev.
3. **See automated PR checks.** The capture workflow dispatches the offline
   check on the PR branch. It runs the repository's standard-library tests
   and verifies the captured JSON, credential exclusion, Dev/Prod separation,
   and definition hash. These are automated contract checks, not an AI review
   and not proof that the model or tools work in Foundry. The participant
   remains responsible for reviewing and merging the diff.
4. **Start deployment deliberately.** Merge does not deploy. Manually run
   [Deploy Weather configuration to Prod](../../.github/workflows/weather-delivery-deploy.yml)
   on the default branch. Enter its full reviewed commit SHA as
   `expected_commit` and check `deploy_approved`. The job refuses an unchecked
   confirmation or a different commit before Azure login. It then creates a
   new version on the existing Prod agent, reads it back and pins the Prod
   stable endpoint to it. No GitHub Environment or separate reviewer is used.
5. **Verify and explain.** Participants inspect the deployment artifact and
   Foundry read-back for the Prod agent name, new version, source Dev version,
   configuration hash, and stable endpoint. Dev should remain unchanged. A
   separate prompt/tool runtime test is not part of this deployment job.

The learning outcome is a merged, versioned configuration in Git and a
GitHub-Actions-created version selected by the Prod agent. Participants can
explain which PR was reviewed, which checks ran, who approved the production
deployment, and what version is selected. Merging is the configuration
approval; manually starting the confirmed deployment is the separate delivery
decision. This is a lab confirmation, not enforced separation of duties.

### Where the participant clicks and what they should see

The Coach supplies the actual repository/project links and resource names,
not placeholder URLs. Give one action at a time; explain its purpose and
expected result before the participant acts. These are navigation cues, not
proof that a control exists or the signed-in user can access it. If the screen
differs, ask what is visible rather than inventing a route.

| Surface | Participant action | Expected evidence |
|---|---|---|
| GitHub Copilot app, current repository session with Workshop Coach | Confirm the selected saved Dev version and intended Prod target; choose to start the optional lab | One agreed source and destination; no additional Dev edit required |
| GitHub website, confirmed repository -> **Actions** -> **Capture Weather Dev configuration** -> **Run workflow** | Select the default branch, enter the exact `agent_version`, then run | A capture run; its **Summary** links to the automatically opened PR, or explains that nothing changed |
| Linked PR -> **Files changed** | Find familiar Weather instructions; inspect model/tool references and manifest source/target | A first captured configuration or a meaningful subsequent diff; no credentials or private conversation content |
| Same PR -> **Checks** | Wait for `offline-contract-tests`; inspect its run summary | Successful checks on the current PR head; explicitly no model/tool runtime claim |
| Same PR -> **Conversation** | Review, then use the available merge control when required checks pass | A merged configuration; no deployment starts from merge |
| GitHub -> repository **Code** -> default branch -> latest commit | With the Coach, confirm this is the reviewed merged configuration and copy the full commit SHA (a 40-character Git identifier) | An exact commit to deploy; if the branch changed, inspect the changes before confirming |
| GitHub -> **Actions** -> **Deploy Weather configuration to Prod** -> **Run workflow** | Select the default branch, paste `expected_commit`, check `deploy_approved`, then run | The confirmed commit matches the run SHA; no Environment, reviewer gate or extra Azure sign-in prompt |
| Completed deployment run -> **Summary** | Read the exact source version, Git commit, new Prod version, hash and endpoint | A readable receipt of the created/read-back definition and selected version |
| Microsoft Foundry, starting at https://ai.azure.com/ -> confirmed project | With Coach guidance based on the verified portal route, locate the exact Prod agent/version and selected stable version; compare its instructions with the merged PR | Independent read-back agrees with the receipt; inspect Dev to confirm it was not changed |

Do not treat viewing an arbitrary version in a test screen as proof of the
stable selector. The Coach uses the supported read-only CLI/API route when
that property is not exposed in the verified portal screen. Ask the participant
to recognize a familiar instruction and explain the two approvals in one
teach-back, not a quiz after each click. Keep this final evidence distinct from
any separately approved paid prompt/tool runtime test.

If capture reports "nothing new", no PR or deployment was created. Explain the
result; do not make a gratuitous Dev change or mark a new promotion complete.
If deployment fails, inspect the artifact and current service state before
retrying: a failed run may already have created a Prod version or changed routing.

## What capture includes—and excludes

Capture stores the selected prompt-agent **version definition** returned by
Microsoft Foundry: its instructions, model reference, and configured tools
when those fields are in the definition. It records the source agent/version,
intended Prod agent, facilitator-verified Prod Stable Agent Endpoint, and a hash
of the captured definition. It rejects credential-like fields before writing
the configuration into the PR. The endpoint is configured from the exact
service read-back; it is not guessed from an agent name.

Capture does not export or recreate project resources that the definition
references. In this one-project lab, the Prod agent reuses the same project
model deployment, tool connections, Toolboxes, and other project-level
dependencies. External skill files and memory contents/configuration are not
exported as part of this simple capture. Participants must understand that a
configuration diff is not a complete infrastructure backup. The capture does
not include credentials, private Conversations, transcripts, or memory
contents.

The Foundry-to-Toolbox runtime authentication path is being investigated
separately. A successful capture, PR check, or deployment proves configuration
delivery only; it does not prove that the Prod agent can invoke its Weather
tool. Do not claim a tool-runtime pass until that path has independent live
evidence.

## Facilitator setup before the cohort

The cloud workflows are repository code, not a connected deployment. Before
any live run, configure and rehearse all of the following in the dedicated
workshop repository and project:

- Confirm an existing Dev agent and an existing, separate Prod agent in the
  same Microsoft Foundry Project. Set repository Actions variables
  `WEATHER_DEV_AGENT_NAME`, `WEATHER_PROD_AGENT_NAME`,
  `WEATHER_FOUNDRY_PROJECT_ENDPOINT`, and `WEATHER_PROD_STABLE_ENDPOINT` to
  their exact values.
- Configure `WEATHER_AZURE_CLIENT_ID`, `WEATHER_AZURE_TENANT_ID`, and
  `WEATHER_AZURE_SUBSCRIPTION_ID` as repository Actions variables. Configure
  `WEATHER_CAPTURE_OIDC_SUBJECT` for the default-branch subject used by both
  capture and deployment. Add the matching federated credential in Microsoft Entra ID; do not use a
  client secret.
- Give the CI identity only the Foundry permissions needed to read the
  selected Dev agent/version and create/read a version and update/read the
  version selector on the existing Prod agent. Verify the current permission
  mapping in the target project; do not test it by creating a throwaway
  resource.
- Confirm the participant has repository access to manually dispatch the
  deployment. Rehearse its unchecked-confirmation and wrong-commit rejection
  before Azure login. GitHub Environments and their approval features are not
  required. The same person may review/merge and start deployment in this lab.
- Protect the default branch with a rule/ruleset requiring a pull request and
  the `offline-contract-tests` check from GitHub Actions before merge.
  Confirm the dispatched check on the actual PR head satisfies the rule and
  a pending/failed check prevents merge for the participant (no bypass).
  Do not require this path-filtered workflow for unrelated PRs without
  accounting for skipped checks: scope the rule to a dedicated delivery-lab
  repository or adjust the required-check strategy. Rehearse any requirement
  for branches to be up to date with the manually dispatched check.
  Deployment also reruns the offline suite and package validation before
  Azure login; this is not a replacement for PR protection.
- In repository Actions settings, allow GitHub Actions to create pull
  requests. The capture workflow uses the repository `GITHUB_TOKEN` with
  `contents`, `pull-requests`, and `actions` permissions; it does not need a
  personal access token.
- Rehearse capture, PR opening, the dispatched offline check, PR merge,
  manual deployment confirmation, Prod version creation/read-back, and endpoint pinning
  in an approved test project before teaching it live.

Both jobs use the default-branch federated subject, normally
`repo:OWNER/REPOSITORY:ref:refs/heads/DEFAULT_BRANCH`. Confirm the actual subject
claims and configure an exact match. An old Environment-based subject cannot
authenticate this branch-based flow; the facilitator must approve and configure
the branch trust before use. `WEATHER_PRODUCTION_OIDC_SUBJECT` is no longer used.
The same CI identity is used for both
jobs as a workshop simplification; it therefore needs the union of their
permissions. Separate identities and narrower environment-specific rights
are preferable in production.

No Azure variables, federated credentials, repository protection rules, or
live workflow results are configured by this repository change. Until a
facilitator completes the setup and live rehearsal, the flow is implemented
but not ready to run against a Foundry project.

### Authentication: sign in once, do not carry a user session into CI

The recommended lab route is **facilitator-prepared automation identity plus
participant-owned interactive sign-in**. A personal sign-in alone cannot
authenticate a job running later on a GitHub-hosted runner.

| Who/where | Authentication and responsibility |
|---|---|
| Participant, GitHub website | Sign into their own GitHub account themselves. That account needs the agreed repository permissions to start capture, review/merge and manually dispatch the confirmed deployment. |
| Participant, Microsoft Foundry portal | Sign into their chosen Microsoft account themselves. Confirm the exact project and access; earlier portal sign-in does not prove the automation identity has access. |
| Coach execution context, only if CLI operations are needed | Check `gh auth status` for GitHub or Azure CLI availability/sign-in for Microsoft Foundry. If absent or expired, explain which service needs sign-in, ask permission for its supported interactive/device sign-in flow, and let the participant complete it themselves. Recheck the actual identity, repository/project and operation permission afterward. |
| GitHub Actions | Use the built-in short-lived `GITHUB_TOKEN` for the PR and an Azure workload identity trusted through OpenID Connect (OIDC) for Microsoft Foundry. OIDC lets GitHub prove which repository/job is running without a stored Azure password or client secret. |

Prepare the automation identity/trust and scoped project role assignment once
per participating repository/project before the promotion exercise, preferably
before the cohort. Explain the exact application identity, project, trusted
default-branch GitHub subject, intended access and possible costs. Obtain separate explicit
approval before creating an identity, adding trust/roles, editing repository
settings or creating Prod. If the participant lacks the required administrator
rights, involve the facilitator; repeated sign-ins do not fix missing permission.
This lab documents preparation but does not automatically provision that access.

For local Azure sign-in, preserve the account-selection and process-scoped
`AZURE_CONFIG_DIR` isolation rules in COACH.md; never change the global profile
or sign out unrelated accounts. No password, device code, access token or
client secret belongs in chat, Git, an artifact, or a workflow variable.
The participant completes authentication in the service's own sign-in UI;
do not automate credential entry. An MCP server's separate sign-in uses the
GitHub Copilot app's server-specific Sign in action, not an assumed CLI session.

After setup, participants normally need no Azure CLI login for each capture
or deployment. GitHub Actions obtains fresh short-lived credentials for each
run; manual deployment still requires the explicit commit confirmation. Authentication is not
permission: read/write authorization remains independently checked.
None of this fixes or bypasses the agent-to-Toolbox authentication blocker.

## What this shortcut is—and is not

This lab demonstrates CI/CD concepts with one project, two agents, a manually
started capture, a pull request, automated checks, and a gated deployment.
It is a teaching path, not production-grade infrastructure-as-code or a
complete backup/restore solution. In particular:

- Dev and Prod share project-level identity, permissions, quotas, model
  deployment, connections, Toolboxes, and audit boundary.
- The CI identity has access to both agents and can update the Prod version
  selector.
- Offline checks validate package consistency, not live model quality,
  Toolbox authentication, tool approvals, or production behavior.
- The deployment job creates and pins a Prod version but does not run a paid
  model/tool smoke test. Verify runtime separately under its own approval.
- Production practice would use stronger environment isolation, narrower
  identities, protected branches and required reviews, dependency/config
  management, runtime tests, monitoring, and a rehearsed rollback policy.

Close with the benefit before the limitations:

> You now have a reviewable configuration history, automated checks, and a
> record of exactly which Git change produced the selected Prod version.
> You did not need to copy the agent's settings by hand.

Then compare the observed lab with production:

| This lab | A typical production improvement |
|---|---|
| Two agents sharing one project | Separate environment/resource and audit boundaries |
| One automation identity for capture and deployment | Separate narrowly scoped identities |
| Manual deployment with a commit confirmation, no GitHub Environment | Enforced reviewer separation and deployment policy |
| Existing shared model and tool dependencies | Explicit dependency versions and infrastructure management |
| Offline package checks and definition read-back | Quality, safety and runtime integration checks |
| A deliberately approved version selection | Monitoring, change policy and rehearsed rollback |

The lab is complete when the reviewed PR is merged, its automated check has
passed, the production deployment is approved, and Foundry read-back confirms
the new Prod version and selector. If live setup or runtime verification is
blocked, record the exact blocker; never count a mock test or successful
configuration write as runtime proof.
