"""
Example of a complete agent implementation using tPay
"""
import logging
import sys
import os
from typing import Dict, Any, List, Optional, Callable
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from tpay import tpay_initialize, tradar_verifier, create_payment_tool
from tpay.tools import create_balance_tool, taudit_verifier
from tpay.utils import get_all_tool_definitions
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


load_dotenv()

TLEDGER_API_KEY = os.getenv("TLEDGER_API_KEY")
TLEDGER_API_SECRET = os.getenv("TLEDGER_API_SECRET")
TLEDGER_PROJECT_ID = os.getenv("TLEDGER_PROJECT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")
RECEIVING_AGENT_ID = os.getenv("RECEIVING_AGENT_ID")

# Check if all required environment variables are set
if not all([TLEDGER_API_KEY, TLEDGER_API_SECRET, TLEDGER_PROJECT_ID, OPENAI_API_KEY, AGENT_ID, RECEIVING_AGENT_ID]):
    print("Please set all required environment variables")
    exit(1)


# ----- Register customized tool functions -----
@tradar_verifier
def search_product(query: str) -> Dict[str, Any]:
    """Search for products"""
    print("🔍 Tool Called: search_product")
    print("Keywords:", query)
    return {
        "results": [
            {"name": "Blue Yeti Microphone", "price": 58.8, "currency": "USDT", "settlement_network": "solana", "receiving_agent_id": RECEIVING_AGENT_ID, "id": "mic001"},
            {"name": "Razer Seiren", "price": 88, "currency": "USDT", "settlement_network": "solana", "receiving_agent_id": RECEIVING_AGENT_ID, "id": "mic002"}
        ]
    }

@tradar_verifier
def get_user_agent_id(user_id: str) -> Dict[str, Any]:
    """Get user agent id"""
    print("🔍 Tool Called: get_user_agent_id")
    print("User ID:", user_id)
    return {"agent_id": AGENT_ID}

# ----- Initiated tPay standard tools for agent -----
balance_tool = create_balance_tool()
payment_tool = create_payment_tool()

# ----- Tool definitions -----
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "Search for products based on user requirements",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_agent_id",
            "description": "Get the agent ID associated with a user ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"]
            }
        }
    }
]

tools.extend(get_all_tool_definitions())

# ----- Simulate conversation -----
conversation = [
    {
        "role": "system",
        "content": """You are an intelligent assistant with access to several tools. When using tools, you must:
1. Explain what you are going to do and why
2. Generate a tool_call (do not write any code or function calls in your message)
3. Wait for the tool's response before proceeding
4. Make decisions based on available information without asking for additional confirmation

Available tools:
1. get_user_agent_id(user_id: str) -> Returns the agent ID associated with a user ID
   Example: Call this tool to get the agent ID for a user
   
2. get_agent_balance(agent_id: str) -> Returns agent account balance
   Example: Call this tool to check an agent's balance
   
3. search_product(query: str) -> Returns list of matching products
   Example: Call this tool to search for products
   
4. create_payment(agent_id: str, amount: float, receiving_agent_id: str, currency: str = "USDT", settlement_network: str = "solana") -> Creates payment
   Example: Call this tool to complete a purchase

For purchasing decisions:
- First get the user's agent ID using get_user_agent_id
- Then check the agent's balance using get_agent_balance
- Search for products that match the user's requirements
- If multiple options are available and all are within budget, choose the cheapest one
- Complete the purchase without asking for additional confirmation
- Use create_payment to finalize the transaction

Please reason step by step and call appropriate tools to complete tasks. Consider user needs and context at each step, and always explain your reasoning."""
    },
    {
        "role": "user",
        "content": "My user_id is 123, I want to buy a microphone for Alice, please help me decide the most suitable choice within my current balance and complete the purchase for me."
    }
]

# ----- Tool execution functions -----
def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool by name with the given arguments
    
    Args:
        tool_name: Name of the tool to execute
        args: Arguments for the tool
        
    Returns:
        Result of the tool execution
    """
    if tool_name == "search_product":
        return search_product(**args)
    elif tool_name == "get_user_agent_id":
        return get_user_agent_id(**args)
    elif tool_name == "get_agent_balance":
        return balance_tool(**args)
    elif tool_name == "create_payment":
        # Set default values for currency and settlement_network if not provided
        if "currency" not in args:
            args["currency"] = "USDT"
        if "settlement_network" not in args:
            args["settlement_network"] = "solana"
        return payment_tool(**args)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

@taudit_verifier
def call_llm_with_tools(
    messages: List[Dict[str, Any]], 
    tools: List[Dict[str, Any]], 
    model: str = "gpt-4",
    tool_choice: str = "auto"
) -> Dict[str, Any]:
    # Call the LLM
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice=tool_choice
    )
    
    # Get the model's message
    msg = response.choices[0].message
    print("🤖 Model Reasoning Process (content):", msg.content)
    
    # Add the model's message to the conversation
    updated_conversation = messages.copy()
    updated_conversation.append(msg)
    
    # Handle tool calls if any
    if msg.tool_calls:
        print(f"🔧 Model requested {len(msg.tool_calls)} tool calls")
        for call in msg.tool_calls:
            fn_name = call.function.name
            args = eval(call.function.arguments)
            print(f"🔨 Executing tool: {fn_name}")
            
            # Execute the tool
            result = execute_tool(fn_name, args)
            
            # Add tool response to conversation
            updated_conversation.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })
            
            # If this is a payment tool, we're done
            if fn_name == "create_payment":
                print("✅ Payment completed, ending conversation")
                return updated_conversation

    return updated_conversation

@taudit_verifier
def run_agent_conversation(
    initial_messages: List[Dict[str, Any]], 
    tools: List[Dict[str, Any]], 
    max_iterations: int = 10
) -> List[Dict[str, Any]]:
    conversation = initial_messages.copy()
    
    for i in range(max_iterations):
        print(f"\n🔄 Starting iteration {i+1}/{max_iterations}")
        
        # Call the LLM with tools
        conversation = call_llm_with_tools(conversation, tools)
        
        # Check if the last message was from a tool
        last_message = conversation[-1]
        print(f"🔍 Last message: {last_message}")
        if isinstance(last_message, dict):
            if last_message.get("role") == "tool":
                # If the last tool was a payment, we're done
                if "create_payment" in str(last_message):
                    print("✅ Task completed, exiting loop")
                    break
            else:
                # If the last message was from the model and had no tool calls, we're done
                print("🔍 No tool calls requested, exiting loop")
                break
        
        if isinstance(last_message, ChatCompletionMessage):
            if last_message.role == "assistant" and not last_message.tool_calls:
                print("🔍 No tool calls requested, exiting loop")
                break

    return conversation

def main():
    # Run the agent conversation
    final_conversation = run_agent_conversation(conversation, tools)
    
    print("\n📝 Final Conversation:")
    for msg in final_conversation:
        if isinstance(msg, dict):
            if msg["role"] == "user":
                print(f"👤 User: {msg['content']}")
            elif msg["role"] == "assistant":
                print(f"🤖 Assistant: {msg['content']}")
            elif msg["role"] == "tool":
                print(f"🔧 Tool Response: {msg['content']}")
        elif isinstance(msg, ChatCompletionMessage):
            if msg.role == "user":
                print(f"👤 User: {msg.content}")
            elif msg.role == "assistant":
                print(f"🤖 Assistant: {msg.content}")
            elif msg.role == "tool":
                print(f"🔧 Tool Response: {msg.content}")

# Initialize tpay sdk
tpay_initialize(api_key=TLEDGER_API_KEY, api_secret=TLEDGER_API_SECRET, project_id=TLEDGER_PROJECT_ID, timeout=1000)

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

if __name__ == "__main__":
    main() 