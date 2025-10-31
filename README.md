
# Basic Agentic App Demo: A Beginner's Guide to Full-Stack AI

Welcome! This project is a comprehensive, hands-on guide designed for students and beginners. It walks you through the fundamentals of application development, from building a simple frontend and backend to integrating powerful Large Language Models (LLMs) and creating a sophisticated AI agent with LangGraph.

Think of this as more than just a project; it's a complete, self-contained course that will take you from zero to building your first AI-powered web application.

## 📚 Table of Contents

1.  [What is This Project?](#-what-is-this-project)
2.  [Core Concepts Explained (The Knowledge Base)](#-core-concepts-explained-the-knowledge-base)
    *   [What is a Frontend? (The User Interface)](#1-what-is-a-frontend-the-user-interface)
    *   [What is a Backend? (The Brains of the Operation)](#2-what-is-a-backend-the-brains-of-the-operation)
    *   [How Frontend and Backend Communicate (API Calls)](#3-how-frontend-and-backend-communicate-api-calls)
    *   [What are Large Language Models (LLMs)?](#4-what-are-large-language-models-llms)
    *   [What is LangChain? (Giving LLMs Superpowers)](#5-what-is-langchain-giving-llms-superpowers)
    *   [What is an AI Agent? (An Autonomous Problem-Solver)](#6-what-is-an-ai-agent-an-autonomous-problem-solver)
    *   [What is LangGraph? (Building AI Agents)](#7-what-is-langgraph-building-ai-agents)
3.  [Project Structure](#-project-structure)
4.  [Setup and Installation (Let's Get Building!)](#-setup-and-installation-lets-get-building)
5.  [How to Run the Application](#-how-to-run-the-application)
6.  [Exploring the Application (A Guided Tour)](#-exploring-the-application-a-guided-tour)
7.  [Code Deep Dive](#-code-deep-dive)
    *   [`app.py` (The Backend)](#apppy-the-backend)
    *   [`index.html` (The Frontend)](#indexhtml-the-frontend)
8.  [Conclusion and Next Steps](#-conclusion-and-next-steps)

---

## 🚀 What is This Project?

This project is a simple web-based "Items Manager" application. You can add, view, update, and delete items. But it's much more than that. It's a playground for learning how modern applications are built and how AI can be integrated into them.

It demonstrates:
*   A **frontend** built with HTML, CSS, and JavaScript that you can interact with in your browser.
*   A **backend** API built with Python and Flask that manages the data and business logic.
*   **API communication** that allows the frontend to talk to the backend.
*   **AI-powered categorization** using a Large Language Model (LLM) via LangChain.
*   A fully-featured **AI Agent** built with LangGraph that can use "tools" (like a calculator or a random fact generator) to answer your questions.

---

## 🧠 Core Concepts Explained (The Knowledge Base)

This section is the heart of the documentation. We'll break down every core concept from scratch.

### 1. What is a Frontend? (The User Interface)

The **frontend** is what you, the user, see and interact with in your browser. It's the visual part of the web application—the buttons, text, forms, and layout.

*   **Core Technologies:**
    *   **HTML (HyperText Markup Language):** The skeleton of the page. It defines the structure and content, like headings, paragraphs, and input fields. In our project, `index.html` is the HTML file.
    *   **CSS (Cascading Style Sheets):** The styling. It controls the colors, fonts, spacing, and layout, making the application look good. In our project, the CSS is inside the `<style>` tag in `index.html`.
    *   **JavaScript:** The interactivity. It makes the application dynamic. When you click a button, submit a form, or fetch data, JavaScript is what makes it happen. In our project, the JavaScript is inside the `<script>` tag in `index.html`.

**In this project:** `index.html` is our frontend. It provides the user interface for managing items and interacting with the AI agent.

### 2. What is a Backend? (The Brains of the Operation)

The **backend** is the server-side of the application. It's the part you don't see. It runs on a server and is responsible for:
*   **Storing and managing data** (like our list of items).
*   **Executing business logic** (like creating a new item or categorizing a description).
*   **Responding to requests** from the frontend.
*   **Security and authentication**.

An **API (Application Programming Interface)** is a key part of the backend. It's a set of rules and endpoints that the frontend uses to communicate with the backend. For example, the frontend can send a request to the `/api/items` endpoint to get a list of all items.

**In this project:** `app.py` is our backend. It's a Python script using the **Flask** framework to create a web server and define our API endpoints.

### 3. How Frontend and Backend Communicate (API Calls)

The frontend and backend are separate, but they need to talk to each other. This communication happens through **API calls**, which are essentially HTTP requests.

*   **The Process:**
    1.  **User Action:** The user clicks a button on the frontend (e.g., "Refresh List").
    2.  **JavaScript Request:** The frontend's JavaScript code uses the `fetch()` function to send an HTTP request to a specific URL on the backend (e.g., `http://localhost:5001/api/items`).
    3.  **Backend Processing:** The backend server (our Flask app) receives the request, finds the matching route (`@app.route('/api/items')`), and executes the corresponding Python function (`get_items()`).
    4.  **Backend Response:** The backend function gathers the data (the list of items) and sends it back to the frontend, usually in a format called **JSON (JavaScript Object Notation)**.
    5.  **Frontend Update:** The frontend's JavaScript receives the JSON data and uses it to update the HTML, displaying the new list of items to the user.

This request-response cycle is the foundation of all modern web applications.

### 4. What are Large Language Models (LLMs)?

LLMs are a type of artificial intelligence trained on vast amounts of text data. They are incredibly good at understanding and generating human-like text. You've probably heard of models like GPT-4 or Google's Gemini.

They can perform a wide range of tasks, including:
*   Answering questions.
*   Writing essays and code.
*   Translating languages.
*   Summarizing text.
*   Categorizing information (which is what we do in this project!).

### 5. What is LangChain? (Giving LLMs Superpowers)

While LLMs are powerful, they are just text-in, text-out systems. **LangChain** is a framework that makes it easier to build applications powered by LLMs. It provides tools and abstractions to:

*   **Connect to different LLM providers** (like Google, OpenAI, etc.).
*   **Manage prompts** using templates.
*   **Chain multiple LLM calls together** to perform more complex tasks.
*   **Integrate external tools** that the LLM can use.

**In this project:** We use `langchain-google-genai` to connect to the Gemini LLM. We create a `categorization_chain` that combines a prompt template with the LLM to create a simple, reusable AI tool for categorizing item descriptions.

### 6. What is an AI Agent? (An Autonomous Problem-Solver)

An AI Agent is a more advanced application of an LLM. Instead of just responding to a prompt, an agent can:

1.  **Reason:** Decide what steps to take to accomplish a goal.
2.  **Use Tools:** Access external tools (like a calculator, a database, or another API) to get information it doesn't have.
3.  **Observe:** Take the results from the tools.
4.  **Iterate:** Repeat the process until it has a final answer.

For example, if you ask an agent, "What is the sum of the first 5 prime numbers?", it might:
1.  **Decide:** "I need to find the first 5 prime numbers and then add them. I don't know them offhand, so I need a way to calculate or find them."
2.  **Decide:** "I don't have a 'prime number' tool, but I can use my reasoning. The first few primes are 2, 3, 5, 7, 11."
3.  **Decide:** "Now I need to add them. I'll use the `calculator` tool."
4.  **Use Tool:** Call the `calculator` tool with the expression "2 + 3 + 5 + 7 + 11".
5.  **Observe:** The tool returns "28".
6.  **Respond:** "The sum of the first 5 prime numbers is 28."

### 7. What is LangGraph? (Building AI Agents)

**LangGraph** is a library built on top of LangChain that is specifically designed for creating robust, stateful AI agents. It allows you to define the agent's logic as a **graph**, which is a collection of nodes and edges.

*   **Nodes:** These are the steps in the agent's workflow. A node can be a function that calls the LLM, or a function that executes a tool.
*   **Edges:** These are the connections between the nodes. They define the path the agent takes. An edge can be conditional, meaning the path changes based on the current state (e.g., "if the LLM decided to use a tool, go to the 'tools' node, otherwise, end").
*   **State:** LangGraph agents are **stateful**. This means they have a memory that is passed between each node. In our project, the state is the history of messages in the conversation.

**In this project:** We use LangGraph to build our AI agent.
*   `AgentState`: Defines the structure of our agent's memory.
*   `call_model` node: Calls the LLM to decide what to do next.
*   `ToolNode`: A special node that automatically executes any tools the LLM decides to use.
*   `should_continue` edge: A conditional edge that checks if the LLM's last response included a tool call.

This graph structure makes the agent's logic clear, predictable, and easy to debug.

---

## 📁 Project Structure

Here's a breakdown of the files in this project:

*   `app.py`: The Python backend server built with Flask. It contains all the API logic, the LangChain setup, and the LangGraph agent.
*   `index.html`: The single HTML file that acts as our frontend. It includes all the necessary HTML, CSS, and JavaScript for the user interface.
*   `requirements.txt`: A list of all the Python packages this project needs to run.
*   `.env` (You will create this): A file to store your secret API key.

---

## 🛠️ Setup and Installation (Let's Get Building!)

Follow these steps to get the project running on your local machine.

### Prerequisites

*   **Python:** Make sure you have Python 3.8 or newer installed. You can download it from [python.org](https://www.python.org/).
*   **Google AI API Key:** This project uses Google's Gemini model. You'll need an API key.
    *   Go to [Google AI Studio](https://aistudio.google.com/).
    *   Sign in with your Google account.
    *   Click "Get API key" and create a new API key in a new project.
    *   **Important:** Keep this key safe and private!

### Step-by-Step Guide

1.  **Clone the Repository**
    Open your terminal or command prompt and run:
    ```bash
    git clone https://github.com/pranaydeep139/Basic-Agentic-App-Demo.git
    cd Basic-Agentic-App-Demo
    ```

2.  **Create a Virtual Environment**
    It's a best practice to create a virtual environment for each Python project to keep dependencies separate.
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
    You should see `(venv)` at the beginning of your terminal prompt.

3.  **Install Dependencies**
    Install all the required Python packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the .env File**
    Create a new file in the project directory named `.env`. Open this file and add your Google API key like this:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
    Replace `"YOUR_API_KEY_HERE"` with the actual key you got from Google AI Studio.

You're all set up!

---

## ▶️ How to Run the Application

1.  **Start the Backend Server**
    In your terminal (make sure your virtual environment is still active), run the Flask application:
    ```bash
    python app.py
    ```
    You should see output indicating that the server is running, usually on `http://127.0.0.1:5001`.

2.  **Open the Frontend**
    This project uses a simple setup where you open the HTML file directly in your browser.
    *   Navigate to the project folder in your file explorer.
    *   **Right-click on `index.html` and choose "Open with" your favorite web browser** (like Chrome, Firefox, or Edge).

You should now see the "Items Manager with AI Agent" application in your browser!

---

## 🗺️ Exploring the Application (A Guided Tour)

The UI is divided into four main sections:

1.  **AI Agent with Tools**
    *   This is the most powerful part of the app. You can ask the agent complex questions.
    *   **Try these queries:**
        *   `What is 123 * 456?` (It will use the `calculator` tool).
        *   `Tell me a random fact.` (It will use the `random_fact_generator` tool).
        *   `What time is it?` (It will use the `current_datetime` tool).
        *   `Reverse the text 'hello world'` (It will use the `reverse_text` tool).
    *   Notice the chat history that appears, showing your message and the agent's response.

2.  **Test Tools Directly**
    *   This section lets you bypass the agent and trigger each tool directly. It's great for understanding what each tool does on its own.
    *   Click any of the buttons to see the raw output from that tool.

3.  **Manage Items**
    *   This is the basic CRUD (Create, Read, Update, Delete) part of the application.
    *   You can add new items, and they will appear in the list below.
    *   Click "Refresh List" to load all items.
    *   Use the "Update" and "Delete" buttons to manage existing items.

4.  **AI Categorization Tool**
    *   This section demonstrates a simpler AI integration using a LangChain chain.
    *   Enter a description for an item (e.g., "A delicious, freshly baked apple pie").
    *   Click "Get AI Category Suggestion". The backend will call the LLM to suggest a category (e.g., "Food").
    *   You can then click "Apply to New Item" to copy the suggested category into the "Manage Items" form.

---

## 💻 Code Deep Dive

Let's look at the key parts of the code.

### `app.py` (The Backend)

*   **Flask Setup & CORS:**
    ```python
    app = Flask(__name__)
    CORS(app) # Allows the frontend (on a different origin) to talk to the backend.
    ```

*   **API Endpoints (e.g., Get Items):**
    ```python
    @app.route('/api/items', methods=['GET'])
    def get_items():
        return jsonify({"items": items})
    ```
    This defines an API endpoint. When the frontend sends a `GET` request to `/api/items`, this function runs and returns the `items` list as JSON.

*   **LangChain Categorization Chain:**
    ```python
    categorization_prompt = ChatPromptTemplate.from_messages([...])
    categorization_chain = categorization_prompt | llm | StrOutputParser()
    ```
    This is a simple chain. The `|` (pipe) operator sends the output of one component as the input to the next. So, the user's description goes into the prompt, the prompt goes to the LLM, and the LLM's output is parsed into a simple string.

*   **Defining a Tool:**
    ```python
    @tool
    def calculator(expression: str) -> str:
        """Evaluates a mathematical expression..."""
        # ... implementation ...
    ```
    The `@tool` decorator from LangChain is what turns a regular Python function into a tool that the AI agent can use. The function's docstring is very important, as the LLM uses it to understand what the tool does.

*   **LangGraph Workflow:**
    ```python
    # Define the state
    class AgentState(TypedDict):
        messages: Annotated[list, operator.add]

    # Define the nodes
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))

    # Define the edges
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, ...)
    workflow.add_edge("tools", "agent")

    # Compile the graph
    agent_executor = workflow.compile()
    ```
    This is the core of the agent setup. It defines the structure of the agent's logic: start at the `agent` node, conditionally go to the `tools` node if needed, and then always return from the `tools` node back to the `agent` node to continue the process.

### `index.html` (The Frontend)

*   **API URLs:**
    ```javascript
    const API_URL = 'http://localhost:5001/api/items';
    const AGENT_API_URL = 'http://localhost:5001/api/agent/query';
    ```
    These constants define the backend endpoints that the JavaScript will call.

*   **Fetching Data (e.g., Loading Items):**
    ```javascript
    async function loadItems() {
        const response = await fetch(API_URL); // Send GET request
        const data = await response.json();   // Parse JSON response
        displayItems(data.items);             // Update the UI
    }
    ```
    This is a classic example of an asynchronous `fetch` call to get data from the backend.

*   **Sending Data (e.g., Querying the Agent):**
    ```javascript
    async function queryAgent() {
        const query = document.getElementById('agentQuery').value;

        const response = await fetch(AGENT_API_URL, {
            method: 'POST', // Use POST to send data
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }) // The data we're sending
        });

        const data = await response.json();
        // ... update UI with agent's response ...
    }
    ```
    This function shows how to send data *to* the backend. We use the `POST` method and include the user's query in the `body` of the request, formatted as a JSON string.

---

## 🎉 Conclusion and Next Steps

Congratulations! You've just set up and explored a full-stack application with a sophisticated AI agent. You've learned about frontends, backends, APIs, LLMs, LangChain, and LangGraph.

This project is a starting point. Here are some ideas for how you can expand on it:

*   **Add More Tools:** Create new Python functions with the `@tool` decorator. For example, a tool that can search the web, or a tool that can read and write to a file.
*   **Persistent Storage:** The current item list is in-memory and resets when the server restarts. Try modifying the backend to store the items in a database like SQLite.
*   **Give the Agent Access to Items:** Create tools that allow the agent to interact with the `items` list. For example, a `list_items` tool or a `find_item_by_id` tool. Then you could ask the agent: "How many items are in the list?" or "What is the description of item 2?".
*   **Improve the UI:** Make the chat interface more advanced, perhaps with streaming responses so you can see the agent "thinking".

Happy coding!
