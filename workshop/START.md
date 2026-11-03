# Participant start guide

Build two AI agents and a coordinating workflow in Microsoft Foundry, guided
by Workshop Coach in the GitHub Copilot app. Complete the
[prerequisites](PREREQUISITES.md) before attending. VS Code is not required.
You will publish and use the Weather agent in Microsoft Teams and/or
Microsoft 365 Copilot before building Cultural Travel, then publish and use
the completed workflow there to observe both agents' contributions.

## 1. Start the GitHub Copilot app

Open the app, select **Sign in to GitHub** if prompted, and sign in with your
workshop-approved account. You should see **Projects** in the sidebar.

## 2. Choose your owned repository, then clone it

Use a participant-owned fork or template copy for changes, pull requests and
GitHub Actions. The upstream `haforsbe/agentic-hackathon` is the curriculum
source, not a repository where every participant has administrator access.
Cloning downloads files; it does not grant GitHub permissions or copy Actions
variables, identity trust or Azure access.

1. In a browser, open https://github.com/haforsbe/agentic-hackathon and confirm
   the facilitator's revision is **`FY27`**. If you already have a fork, use
   it: inspect its branches and unmerged work before syncing. Do not delete,
   replace, force-push or reset it to get a clean start.
2. If you need a copy, use GitHub's **Fork** control to create one under your
   approved account/organization, including `FY27`. A facilitator may instead
   supply a template route if **Use this template** is available; confirm that
   the copy includes the intended branch and workshop files. Do not assume
   template controls are available or that fork-only work is in a new copy.
3. Record your exact `OWNER/REPOSITORY` and intended default branch. For this
   revision use `FY27`, unless the facilitator explicitly establishes another
   branch containing the same reviewed curriculum. In your owned repository,
   confirm administrator access and that **Actions** lists **Weather delivery
   offline checks** and **Weather delivery cloud stages**. Confirm policy
   permits the required actions. A fork may require enabling Actions with
   owner approval. Do not dispatch a cloud stage.

Use the [read-only repository preflight](weather-delivery/README.md#read-only-github-preflight)
to distinguish missing configuration from denied/unknown access. If Settings
or workflows are inaccessible, stop and ask the repository owner/facilitator;
do not navigate into upstream Settings, grant roles, or paste credentials.
Missing cloud variables block the optional cloud delivery lab, not reading
the curriculum or starting the core workshop. Repository checks do not prove
Microsoft Foundry access or make the workshop delivery-ready.

Now clone **your owned repository** in the GitHub Copilot app:

1. Click **+** beside **Projects**, then **GitHub repository**.
2. Find your recorded **`OWNER/REPOSITORY`** and follow the prompts to clone it.
3. Use the facilitator-confirmed **`FY27`** branch
   (the named workshop revision), not an unconfirmed default branch.

If branch selection is unavailable, ask your facilitator for help, or run this
in a terminal from a folder where you keep projects:

```text
git clone --branch FY27 https://github.com/OWNER/REPOSITORY.git
```

Replace `OWNER/REPOSITORY` with your actual owned copy, not the upstream name.
Then choose **Projects → + → Local folder or repository** and select the newly
created repository folder. If you already have the correct checkout, add that
folder instead of cloning again. Preserve its student files and ignored
`.workshop/` progress; switching revisions is not consent to migrate progress.

## 3. Open the workshop

Under **Projects**, find your cloned repository and click **+** beside it to
start a session. Choose a local execution location unless your facilitator
specifies otherwise. Use this repository session, not the general **Chats** area.

## 4. Select Workshop Coach and start

**Workshop Coach is your teaching profile in the GitHub Copilot app.** A custom
agent profile is a reusable set of instructions for a specialist role. This
repository already supplies it in `.github/agents/workshop-coach.agent.md`;
you do not need to create your own profile to begin.

This is different from the Weather Research Agent and Cultural Travel Agent
you will build in **Microsoft Foundry**. Selecting Workshop Coach does not
create, deploy, or select either of those cloud agents.

1. Below the prompt field, set the session mode to **Interactive** so you stay
   involved in decisions.
2. In the same repository session's message box, type **`/agent`** to open
   custom-agent selection, then choose **Workshop Coach**. The official
   documentation also describes an agent picker dropdown inside the prompt
   box; use it if visible. You do not need to locate that dropdown first.
3. Confirm the selected profile is **Workshop Coach** using the selection
   interface exposed by your app, then send:

   > Start the workshop.

The **model picker** chooses the AI model, not the custom-agent role.
**Interactive / Plan / Autopilot** controls how the session works, not which
profile it uses. You do not need to change your model to select Workshop Coach.

**If the dropdown is missing, try `/agent` before using the fallback.** If
neither selection route is available in your build, use the repository session's
normal Chat and send the same starter message. Repository instructions provide
the same coaching protocol. If selection works but **Workshop Coach** is
missing, ask your facilitator to check the revision and profile discovery;
do not select an unrelated agent, delete progress, or restart the workshop.
The profile file and official documentation do not prove discovery in your
installed build.

**Expected result:** the coach says "Hi!", explains the workshop's four stages
(checkpoint 00 setup, Weather with channel publication/use, Cultural Travel,
and the hosted workflow with channel publication/use then optional capstone).
It asks the two quick Microsoft Foundry/GitHub Copilot app experience questions,
then asks which signed-in Microsoft account you want to use for Microsoft Foundry,
then asks for your Foundry Project Endpoint. If you do not know it or do not
yet have a project, the coach guides you to locate or create your own dedicated
project. The coach confirms the account used by its Foundry request, connects
to that exact project, and verifies the permission needed for the current
approved step.
Read-only access is not enough when a resource must be created. The coach
checks for an existing model deployment before proposing one and pauses if
identity, project access, or required permission cannot be verified. The
facilitator does not assign the project name or endpoint. Never share
passwords or tokens. No resource is created or deployed without your explicit
approval for that step.
You can say
**"Explain without editing"**, **"Give me a hint"**, or **"Pause the workshop"**
at any time.

For more on selecting an existing profile and the distinction between profiles,
models and Microsoft Foundry agents, see
[custom agents in the app guide](APP-GUIDE.md#select-custom-agents).
Keep Workshop Coach selected during the lessons. Participants do not need to
create or edit an agent profile.

## If something looks different

Show your facilitator what you see rather than guessing controls. If the coach
gives a generic answer, first confirm the repository contains `AGENTS.md` and
`workshop/COACH.md`, then send:

> Read AGENTS.md and workshop/COACH.md from this repository and start the
> guided workshop at checkpoint 00. Ask one question at a time.

If those files are missing, request the correct workshop revision. Do not delete
old progress to restart; let the coach explain safe recovery.

**Facilitators:** distribute a committed/pushed revision or prepared checkout;
fresh clones do not include uncommitted edits. Verify Workshop Coach discovery
in the participant app build. See [facilitator guidance](FACILITATOR.md).

App navigation follows the official
[quickstart](https://docs.github.com/en/copilot/get-started/quickstart-copilot-app)
and [session guide](https://docs.github.com/en/copilot/how-tos/github-copilot-app/agent-sessions).
Custom-agent selection follows
[Using custom agents](https://docs.github.com/en/copilot/how-tos/github-copilot-app/customize-github-copilot-app#using-custom-agents)
and the [`/agent` command reference](https://docs.github.com/en/copilot/reference/github-copilot-app-reference/slash-commands).
These are documented routes, not a claim that a participant's controls have
been observed.
