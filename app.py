from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import random
import datetime
from typing import TypedDict, Annotated, Literal
import operator

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

app = Flask(__name__)
CORS(app)

# In-memory data store
items = [
    {"id": 1, "name": "Item 1", "description": "A high-performance laptop for professional use.", "category": "Electronics"},
    {"id": 2, "name": "Item 2", "description": "Freshly baked sourdough bread, artisanal quality.", "category": "Food"}
]

# --- LangChain Setup ---
google_api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=google_api_key, temperature=0.7)

# Simple categorization chain
categorization_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert categorizer. Categorize the following item description into one of these categories: Electronics, Food, Apparel, Home Goods, Tools, Books, Software, Other. Respond with only the most relevant category name."),
    ("user", "Description: {description}")
])
categorization_chain = categorization_prompt | llm | StrOutputParser()

# --- Define Tools ---

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression. Example: '2 + 2' returns '4'"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

@tool
def random_fact_generator() -> str:
    """Generates a random interesting fact."""
    facts = [
        "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible.",
        "Octopuses have three hearts and blue blood.",
        "Bananas are berries, but strawberries aren't.",
        "A group of flamingos is called a 'flamboyance'.",
        "The shortest war in history lasted 38 minutes between Britain and Zanzibar in 1896.",
        "Venus is the only planet that rotates clockwise.",
        "A single strand of spaghetti is called a 'spaghetto'.",
        "Wombat poop is cube-shaped.",
        "The human brain uses about 20% of the body's energy despite being only 2% of body weight.",
        "There are more stars in the universe than grains of sand on all Earth's beaches."
    ]
    return random.choice(facts)

@tool
def current_datetime() -> str:
    """Returns the current date and time."""
    now = datetime.datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def word_counter(text: str) -> str:
    """Counts the number of words in the provided text."""
    word_count = len(text.split())
    return f"Word count: {word_count}"

@tool
def reverse_text(text: str) -> str:
    """Reverses the provided text."""
    return f"Reversed text: {text[::-1]}"

@tool
def coin_flip() -> str:
    """Simulates a coin flip and returns either 'Heads' or 'Tails'."""
    result = random.choice(["Heads", "Tails"])
    return f"Coin flip result: {result}"

@tool
def dice_roll(sides: int = 6) -> str:
    """Rolls a dice with the specified number of sides (default is 6)."""
    if sides < 2:
        return "Error: Dice must have at least 2 sides."
    result = random.randint(1, sides)
    return f"Rolled a {sides}-sided dice: {result}"

# List of all tools
tools = [
    calculator,
    random_fact_generator,
    current_datetime,
    word_counter,
    reverse_text,
    coin_flip,
    dice_roll
]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# --- LangGraph Agent State ---
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# --- Agent Functions ---
def call_model(state: AgentState):
    """Call the LLM with tools."""
    print("\n=== CALL_MODEL: Starting ===")
    messages = state["messages"]
    print(f"CALL_MODEL: Number of messages in state: {len(messages)}")
    print(f"CALL_MODEL: Last message type: {type(messages[-1]).__name__}")
    print(f"CALL_MODEL: Last message content preview: {str(messages[-1])[:200]}...")
    
    # Check if the last message is a ToolMessage - if so, we need to prompt for a final answer
    if isinstance(messages[-1], ToolMessage):
        # Add a system message to prompt for a final response
        messages_with_prompt = messages + [
            HumanMessage(content="Based on the tool results above, please provide a clear and complete answer to my original question.")
        ]
        response = llm_with_tools.invoke(messages_with_prompt)
    else:
        response = llm_with_tools.invoke(messages)
    
    print(f"CALL_MODEL: Response type: {type(response).__name__}")
    print(f"CALL_MODEL: Response has tool_calls: {hasattr(response, 'tool_calls') and bool(response.tool_calls)}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"CALL_MODEL: Number of tool calls: {len(response.tool_calls)}")
        for i, tc in enumerate(response.tool_calls):
            print(f"CALL_MODEL: Tool call {i+1}: {tc.get('name', 'unknown')}")
    print(f"CALL_MODEL: Response content preview: {str(response.content)[:200] if response.content else 'No content'}")
    print("=== CALL_MODEL: Complete ===\n")
    
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine if we should use tools or end."""
    print("\n=== SHOULD_CONTINUE: Starting ===")
    messages = state["messages"]
    last_message = messages[-1]
    
    print(f"SHOULD_CONTINUE: Total messages: {len(messages)}")
    print(f"SHOULD_CONTINUE: Last message type: {type(last_message).__name__}")
    
    # If there are tool calls, continue to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print(f"SHOULD_CONTINUE: Tool calls detected: {len(last_message.tool_calls)}")
        print("SHOULD_CONTINUE: Decision -> 'tools'")
        print("=== SHOULD_CONTINUE: Complete ===\n")
        return "tools"
    # Otherwise, end
    print("SHOULD_CONTINUE: No tool calls detected")
    print("SHOULD_CONTINUE: Decision -> 'end'")
    print("=== SHOULD_CONTINUE: Complete ===\n")
    return "end"

# --- Build LangGraph Workflow ---
print("\n=== Building LangGraph Workflow ===")
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))
print("Workflow nodes added: agent, tools")

# Set entry point
workflow.set_entry_point("agent")
print("Entry point set: agent")

# Add conditional edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)
print("Conditional edges added: agent -> tools/end")

# Add edge from tools back to agent
workflow.add_edge("tools", "agent")
print("Edge added: tools -> agent")

# Compile the graph
agent_executor = workflow.compile()
print("=== LangGraph Workflow Compiled Successfully ===\n")

# --- Flask Routes ---

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API with AI Agent!"})

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": items})

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        "id": len(items) + 1,
        "name": data.get("name"),
        "description": data.get("description"),
        "category": data.get("category", "Uncategorized")
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    item["name"] = data.get("name", item["name"])
    item["description"] = data.get("description", item["description"])
    item["category"] = data.get("category", item["category"])
    return jsonify(item)

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

@app.route('/api/ai/categorize', methods=['POST'])
def categorize_description():
    print("\n=== CATEGORIZE: Request received ===")
    if not google_api_key:
        print("ERROR: Google API key is not configured")
        return jsonify({"error": "Google API key is not configured."}), 503

    data = request.get_json()
    description = data.get("description")
    
    print(f"CATEGORIZE: Description: '{description}'")

    if not description:
        print("ERROR: No description provided")
        return jsonify({"error": "Description is required."}), 400

    try:
        print("CATEGORIZE: Invoking categorization chain...")
        suggested_category = categorization_chain.invoke({"description": description})
        print(f"CATEGORIZE: Suggested category: '{suggested_category.strip()}'")
        print("=== CATEGORIZE: Complete ===\n")
        return jsonify({"description": description, "suggested_category": suggested_category.strip()})
    except Exception as e:
        print(f"ERROR in categorization: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to categorize: {str(e)}"}), 500

@app.route('/api/agent/query', methods=['POST'])
def agent_query():
    print("\n" + "="*60)
    print("=== AGENT_QUERY: New request received ===")
    print("="*60)
    
    if not google_api_key:
        print("ERROR: Google API key is not configured")
        return jsonify({"error": "Google API key is not configured."}), 503

    data = request.get_json()
    user_query = data.get("query")
    
    print(f"AGENT_QUERY: User query: '{user_query}'")

    if not user_query:
        print("ERROR: No query provided")
        return jsonify({"error": "Query is required."}), 400

    try:
        # Create initial state with user message
        print("AGENT_QUERY: Creating initial state...")
        initial_state = {
            "messages": [HumanMessage(content=user_query)]
        }
        print(f"AGENT_QUERY: Initial state created with {len(initial_state['messages'])} message(s)")
        
        # Run the agent
        print("AGENT_QUERY: Invoking agent executor...")
        result = agent_executor.invoke(initial_state)
        print("AGENT_QUERY: Agent executor completed")
        
        # Extract final response
        messages = result.get("messages", [])
        print(f"AGENT_QUERY: Total messages in result: {len(messages)}")
        
        final_response = ""
        
        for i, msg in enumerate(reversed(messages)):
            print(f"AGENT_QUERY: Examining message {len(messages) - i} (type: {type(msg).__name__})")
            if isinstance(msg, AIMessage) and msg.content:
                final_response = msg.content
                print(f"AGENT_QUERY: Found final AI response: '{final_response[:100]}...'")
                break
        
        if not final_response:
            print("WARNING: No final response found in messages")
        
        print("AGENT_QUERY: Returning response to client")
        print("="*60 + "\n")
        
        return jsonify({
            "query": user_query,
            "response": final_response,
            "message_count": len(messages)
        })
    except Exception as e:
        print(f"ERROR in agent query: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Agent error: {str(e)}"}), 500

@app.route('/api/tools/execute', methods=['POST'])
def execute_tool():
    print("\n=== EXECUTE_TOOL: Direct tool execution request ===")
    data = request.get_json()
    tool_name = data.get("tool_name")
    tool_args = data.get("args", {})
    
    print(f"EXECUTE_TOOL: Tool name: '{tool_name}'")
    print(f"EXECUTE_TOOL: Tool args: {tool_args}")

    tool_map = {tool.name: tool for tool in tools}
    
    if tool_name not in tool_map:
        print(f"ERROR: Tool '{tool_name}' not found")
        print(f"EXECUTE_TOOL: Available tools: {list(tool_map.keys())}")
        return jsonify({"error": f"Tool '{tool_name}' not found. Available: {list(tool_map.keys())}"}), 400

    try:
        tool = tool_map[tool_name]
        print(f"EXECUTE_TOOL: Executing tool '{tool_name}'...")
        result = tool.invoke(tool_args)
        print(f"EXECUTE_TOOL: Tool execution successful")
        print(f"EXECUTE_TOOL: Result: {result}")
        
        return jsonify({
            "tool": tool_name,
            "result": result
        })
    except Exception as e:
        print(f"ERROR: Tool execution failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Tool execution error: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("=== Flask Application Starting ===")
    print(f"Google API Key configured: {bool(google_api_key)}")
    print(f"Number of available tools: {len(tools)}")
    print(f"Tool names: {[tool.name for tool in tools]}")
    print("="*60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5001)