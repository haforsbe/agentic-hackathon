# Get started with GitHub Copilot in VS Code

> **Note:** This readme has been adapted from https://code.visualstudio.com/docs/copilot/getting-started.

GitHub Copilot transforms how you write code in Visual Studio Code. In this hands-on tutorial, you build a complete IT support ticketing system while discovering VS Code's AI capabilities: autonomous agents that implement features across multiple files, intelligent inline suggestions, precise editing with inline chat, integrated smart actions, and powerful customization options.

By the end of this tutorial, you'll have both a working web application and a personalized AI coding setup that adapts to your development style.

## Prerequisites

* VS Code installed on your machine. Download it from the [Visual Studio Code website](https://code.visualstudio.com/).

* Access to GitHub Copilot. Follow these steps to [Set up GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/setup).

    > **Tip:** If you don't have a Copilot subscription, you can sign up to use Copilot for free directly from within VS Code and get a monthly limit of inline suggestions and chat interactions.

## Step 1: Experience inline suggestions

AI-powered inline suggestions appear as you type, helping you write code faster and with fewer errors. Let's start building the foundation of your IT support ticketing system.

1. Create a new folder for your project and open it in VS Code.

1. Create a new file called `index.html`.

1. Start typing the following and, as you type, VS Code provides inline suggestions (_ghost text_):

    ```html
    <!DOCTYPE html>
    ```

    ![Screenshot showing Copilot suggesting HTML structure inline suggestion.](https://code.visualstudio.com/assets/docs/copilot/getting-started/html-completion.png)

    You might see different suggestions because large language models are [nondeterministic](https://code.visualstudio.com/docs/copilot/concepts/language-models#key-characteristics).

1. Press `Tab` to accept the suggestion.

    Congratulations! You've just accepted your first AI-powered inline suggestion.

1. Continue building your HTML structure. Inside the `<body>` tag, start typing:

    ```html
    <div class="container">
        <h1>IT Support Tickets</h1>
        <form id="ticket-form">
    ```

    Notice how VS Code continues suggesting relevant HTML elements as you build your application structure.

1. If you see multiple suggestions, hover over the ghost text to see navigation controls, or use `Alt+]` and `Alt+[` to cycle through options.

    ![Screenshot showing inline suggestion navigation controls.](https://code.visualstudio.com/assets/docs/copilot/getting-started/inline-suggestion-navigation.png)

Inline suggestions work automatically as you type, learning from your patterns and the context of your project. They're particularly helpful for writing boilerplate code, HTML structures, and repetitive patterns.

## Step 2: Build complete features with agents

AI Agents are VS Code's most powerful AI capability. Given a natural language prompt, they autonomously plan and implement complex features across multiple files. Let's use them to create the core functionality of your IT support ticketing application.

1. Open the Chat view by pressing `Ctrl+Shift+I` or by selecting the chat icon in the VS Code title bar.

    The Chat view is where you interact with the AI by using natural language prompts. You can have an ongoing conversation and iteratively refine your requests to get better results.

1. Select **Agent** in the agent dropdown menu to let the AI independently implement your request end-to-end.

    ![Screenshot showing the agent picker in the Chat view.](https://code.visualstudio.com/assets/docs/copilot/getting-started/agent-mode-selection.png)

    > **Important:** If you don't see the agent option, make sure agents are enabled in your VS Code settings (`chat.agent.enabled`). Your organization might also have disabled agents - contact your admin to enable this functionality.

1. Enter the following prompt and press `Enter`. The agent analyzes your request and begins implementing the solution.

    ```text
    Create a directory called `app`. Within that directory, create a demo IT support ticketing system web application. Each ticket should have a title, description, priority level (Low, Medium, High, Critical), status (Open, In Progress, Resolved, Closed), and an assigned technician field. Include the ability to create, edit, and close tickets. Populate the app with several existing tickets. Include modern CSS styling and make it responsive. Use semantic HTML and ensure it's accessible. Separate markup, styles, and scripts into their own files. Provide instructions on how to serve the app on localhost.
    ```

    Watch as the agent generates the necessary files and code to implement your request. You should see it update the `index.html` file, create a `styles.css` file for styling, and a `script.js` file for functionality.

    > **Tip:** Different language models might have different strengths. Use the model dropdown in the Chat view to switch between language models.

1. Review the generated files and select **Keep** to accept all the changes.

1. Open your `index.html` file in the integrated browser VS Code by right-clicking the file and selecting **Show Preview**. You can create new tickets, update their status, and close them.

1. Now, let's add an extra feature. Enter the following prompt in the chat input box:

    ```text
    Add a filter system with buttons to filter tickets by status (All, Open, In Progress, Resolved, Closed) and by priority (All, Low, Medium, High, Critical). Update the styling to match the existing design.
    ```

    Notice how the agent coordinates changes across multiple files to implement this feature completely.

Agents excel at understanding high-level requirements and translating them into working code. They're perfect for implementing new features, refactoring large sections of code, or building entire applications from scratch.

## Step 3: Make precise adjustments with inline chat

While agents handle large features, editor inline chat is perfect for targeted improvements to specific code sections within a file. Let's use it to enhance the ticketing app.

1. Open your JavaScript file and locate the code that creates new tickets.

1. Select the code block and then press `Ctrl+I` to open editor inline chat.

    ![Screenshot showing inline chat starting for selected code block.](https://code.visualstudio.com/assets/docs/copilot/getting-started/inline-chat-start.png)

    > **Note:** The exact code might vary because large language models are nondeterministic.

1. Enter the following prompt:

    ```text
    Add input validation to prevent submitting tickets with empty titles, ensure a priority is selected, and trim whitespace from all text fields.
    ```

    Notice how inline chat focuses specifically on the selected code and makes targeted improvements.

    ![Screenshot showing inline chat adding validation to selected function.](https://code.visualstudio.com/assets/docs/copilot/getting-started/inline-chat-validation.png)

1. Review the changes and select **Keep** to apply them.

Editor inline chat is ideal for making small, focused changes without affecting the broader codebase, like adding error handling, refactoring individual functions, or fixing bugs.

## Step 4: Personalize your AI experience

Customizing chat makes it work better for your specific needs and coding style. You can set up custom instructions and build specialized custom agents. Let's create a complete personalization setup for your project.

### Create custom instructions

Custom instructions tell the AI about your coding preferences and standards. These apply automatically to all chat interactions.

1. Create a new folder called `.github` in your project root.

1. Inside the `.github` folder, create a file called `copilot-instructions.md`.

1. Add the following content:

    ```markdown
    # Project general coding guidelines

    ## Code Style
    - Use semantic HTML5 elements (header, main, section, article, etc.)
    - Prefer modern JavaScript (ES6+) features like const/let, arrow functions, and template literals

    ## Naming Conventions
    - Use PascalCase for component names, interfaces, and type aliases
    - Use camelCase for variables, functions, and methods
    - Prefix private class members with underscore (_)
    - Use ALL_CAPS for constants

    ## Code Quality
    - Use meaningful variable and function names that clearly describe their purpose
    - Include helpful comments for complex logic
    - Add error handling for user inputs and API calls
    ```

1. Save the file. These instructions now apply to all your chat interactions in this project.

1. Test the custom instructions by asking the agent to add a new feature:

    ```text
    Add a dark mode toggle button to the ticketing system.
    ```

    Notice how the generated code follows the guidelines you specified. VS Code supports more advanced custom instructions like applying instructions for specific file types.

> **Tip:** Use the `/init` slash command in chat to automatically generate custom instructions based on your project's structure and coding patterns. This is useful if you have an existing codebase and want to prepare it for AI assistance.

### Create a custom agent for code reviews

Custom agents create specialized AI personas for specific tasks. Let's create a "Code Reviewer" agent that focuses on analysis and providing feedback on code. In the custom agent definition, you can define the AI's role, specific guidelines, and which tools it can use.

1. Open the Command Palette and run the **Chat: New Custom Agent** command.

1. Select `.github/agents` as the location.

    This option adds the custom agent to your workspace, enabling other team members to use it when they open the project.

1. Name the custom agent "Reviewer". This creates a new file called `Reviewer.agent.md` in the `.github/agents` folder.

1. Replace the file contents with the following content. Note that this custom agent doesn't allow code changes.

    ```markdown
    ---
    name: 'Reviewer'
    description: 'Review code for quality and adherence to best practices.'
    tools: ['vscode/askQuestions', 'vscode/vscodeAPI', 'read', 'agent', 'search', 'web']
    ---
    # Code Reviewer agent

    You are an experienced senior developer conducting a thorough code review. Your role is to review the code for quality, best practices, and adherence to project standards without making direct code changes.

    When reviewing code, structure your feedback with clear headings and specific examples from the code being reviewed.

    ## Analysis Focus
    - Analyze code quality, structure, and best practices
    - Identify potential bugs, security issues, or performance problems
    - Evaluate accessibility and user experience considerations

    ## Important Guidelines
    - Ask clarifying questions about design decisions when appropriate
    - Focus on explaining what should be changed and why
    - DO NOT write or suggest specific code changes directly
    ```

1. Save the file. In the Chat view, you can now select this custom agent from the agent picker.

    ![Screenshot showing the Reviewer custom agent in the agent picker.](https://code.visualstudio.com/assets/docs/copilot/getting-started/custom-mode-dropdown.png)

1. Test your custom agent by selecting **Reviewer** from the agent picker and entering the following prompt:

    ```text
    Review my full project
    ```

   Notice how the AI now behaves as a code reviewer, providing analysis and suggestions for improvements.

    ![Screenshot showing custom reviewer agent analyzing code.](https://code.visualstudio.com/assets/docs/copilot/getting-started/custom-reviewer-mode.png)

## Step 5: Use smart actions for pre-built AI assistance

Smart actions provide AI functionality directly integrated within VS Code's interface, seamlessly plugging into your development workflow. Unlike chat interactions, smart actions appear contextually where you need them most. Let's explore commit message generation as an example.

1. Open the **Source Control** view by pressing `Ctrl+Shift+G` or selecting the Source Control icon in the Activity Bar.

1. If you haven't yet initialized a Git repository for your project, do so by selecting **Initialize Repository** in the Source Control view.

1. Stage your changes by selecting the **+** button next to the files you want to commit.

1. Select the **sparkle icon** to generate a commit message based on your staged changes.

    The AI analyzes your staged changes and generates a descriptive commit message that follows conventional commit standards. The AI considers:

    * What files were changed
    * The nature of the changes (added features, bug fixes, refactoring)
    * The scope and impact of modifications

    ![Screenshot showing generated commit message in Source Control view.](https://code.visualstudio.com/assets/docs/copilot/getting-started/generated-commit-message.png)

1. Review the generated message. If you're satisfied with it, proceed with your commit. If you want a different style or focus, select the sparkle icon again to generate an alternative message.

Smart actions like commit message generation demonstrate how AI integrates naturally into your existing workflow without requiring you to context-switch to chat interfaces. VS Code has many other smart actions to help you with debugging, testing, and more.

## Step 6: Add an MCP interface to the ticketing app

The [Model Context Protocol (MCP)](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) lets AI agents interact with external tools and services. In this step, you'll use GitHub Copilot to add an MCP server to your ticketing app, so that Copilot (or any MCP-compatible agent) can create, query, and update tickets programmatically.

1. Open the Chat view and make sure **Agent** is selected.

1. Enter the following prompt:

    ```text
    Add an MCP server to the ticketing app that exposes the ticketing system as tools via streamable HTTP and stdio. Use the Model Context Protocol SDK for TypeScript or Python (whichever fits the project). The MCP server should expose these tools:
    - list_tickets: List all tickets, with optional filters for status and priority
    - get_ticket: Get details of a specific ticket by ID
    - create_ticket: Create a new ticket with title, description, priority, and assignee
    - update_ticket: Update a ticket's status or assignee
    - close_ticket: Close a ticket by ID
    Modify the README to explain how to start the MCP server and configure it in VS Code.
    ```

1. Review the generated code. The agent should create an MCP server file that imports your app's ticket data and exposes it through MCP tool definitions.

1. Accept the changes and follow the generated README instructions to start the MCP server.

1. Configure VS Code to use your new MCP server. Create or update `.vscode/mcp.json` in your project with the connection details from the generated README. For example:

    ```json
    {
    "servers": {
        "ticketing": {
        "command": "${workspaceFolder}/.venv/Scripts/python.exe",
        "args": ["${workspaceFolder}/05-github-copilot/example_app/mcp_server.py"],
        "env": {}
        }
    }
    }
    ```

    > **Note:** The exact configuration depends on the language and transport the agent chose. Refer to the generated README for the correct command and arguments.

1. Test the MCP tools by asking the agent a question that requires interacting with your tickets:

    ```text
    List all open high-priority tickets and create a new critical ticket titled "Email server down" assigned to Alice.
    ```

    The agent should use the MCP tools to read from and write to your ticketing system directly from chat.

MCP bridges the gap between your AI assistant and your application's data. Once configured, any agent in VS Code can use these tools to interact with your ticketing system without you having to copy-paste data or switch contexts.

## Step 7: Integrate the MCP server with a custom agent using Agent Framework

Now that your ticketing system is exposed via MCP, you can connect it to an AI agent built with the [Microsoft Agent Framework](https://github.com/microsoft/agent-framework). This lets you create a standalone Python agent that can manage tickets autonomously — outside of VS Code.

1. Review the example in [`01-agent-framework/06_remote_mcp.py`](../01-agent-framework/06_remote_mcp.py). It shows how to connect an Agent Framework agent to a remote MCP server using `MCPStreamableHTTPTool`:

    ```python
    async with (
        MCPStreamableHTTPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        ) as mcp_server,
    ):
        agent = Agent(
            client=client,
            name="DocsAgent",
            instructions="You are a helpful assistant that answers questions using Microsoft documentation.",
            tools=[mcp_server],
        )
    ```

1. Using that example as a reference, create a new file called `agent_with_mcp.py` in the `05-github-copilot/example_app/` folder. Enter the following prompt in the Chat view with **Agent** selected:

    ```text
    Create a Python script called agent_with_mcp.py that uses the Microsoft Agent Framework to build
    an AI agent connected to the local ticketing MCP server at http://localhost:8000/mcp.
    Use 01-agent-framework/06_remote_mcp.py as a reference for how to set up MCPStreamableHTTPTool.
    The agent should:
    - Connect to the ticketing MCP server via streamable HTTP
    - Accept user input in a loop (multi-turn conversation)
    - Be able to list, create, update, and close tickets using the MCP tools
    - Have instructions that describe it as an IT support assistant
    ```

1. Make sure the MCP server is running in HTTP mode before starting the agent. Refer to the app's readme for details.

1. Try interacting with the agent:

    ```text
    User: List all open high-priority tickets
    User: Create a new critical ticket titled "Database backup failing" assigned to Carol Davis
    User: Close ticket #4
    ```

    The agent will use the MCP tools to read from and write to your ticketing system, just like the VS Code agent does — but running as a standalone Python application.

This step demonstrates how MCP creates a universal interface: the same ticketing server you configured for VS Code can also power custom agents, chatbots, or automation scripts built with the Agent Framework.

## Next steps

Congratulations! You've built a complete IT support ticketing system and learned how to work effectively with AI across VS Code's core capabilities.

You can further enhance your AI's capabilities by exploring other customization options:

* Add more specialized agents for different tasks like planning, debugging, or documentation.
* Create custom instructions for specific programming languages or frameworks.
* Extend the AI's capabilities with extra tools from MCP (Model Context Protocol) servers or VS Code extensions.

## Related resources

* [How GitHub Copilot works](https://code.visualstudio.com/docs/copilot/concepts/overview): Core concepts, terminology, and the architecture behind Copilot's features

* [Agents tutorial](https://code.visualstudio.com/docs/copilot/agents/agents-tutorial): Hands-on tutorial for working with different agent types

* [Cheat sheet for using AI features](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features) - Quick reference for all GitHub Copilot features in VS Code

* [Chat documentation](https://code.visualstudio.com/docs/copilot/chat/copilot-chat) - Deep dive into autonomous coding in VS Code

* [Customization guide](https://code.visualstudio.com/docs/copilot/customization/overview) - Advanced personalization techniques

* [MCP tools](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) - Extend agents with external APIs and services
