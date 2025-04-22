"""
TPay SDK Utilities Module
"""

import hashlib
import json
import re
import uuid
from typing import Dict, Any, List

@staticmethod
def normalize_code(code: str) -> str:
    """
    Normalize code by removing extra whitespace and newlines
    
    This method standardizes code format by:
    1. Removing trailing whitespace
    2. Replacing multiple spaces with a single space
    3. Removing empty lines
    4. Normalizing line endings
    """
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in code.splitlines()]
    
    # Remove empty lines
    lines = [line for line in lines if line.strip()]
    
    # Join lines with a single newline
    normalized = "\n".join(lines)
    
    # Replace multiple spaces with a single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized

def generate_code_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()

def generate_request_id() -> str:
    """
    Generate a unique request ID
    
    Returns:
        A unique request ID
    """
    return str(uuid.uuid4())

def format_trace_context(trace_context: Dict[str, Any]) -> str:
    """
    Format trace context as JSON string
    
    Args:
        trace_context: Trace context dictionary
        
    Returns:
        JSON string representation of trace context
    """
    return json.dumps(trace_context)

def parse_trace_context(trace_context_str: str) -> Dict[str, Any]:
    """
    Parse trace context from JSON string
    
    Args:
        trace_context_str: JSON string representation of trace context
        
    Returns:
        Trace context dictionary
    """
    return json.loads(trace_context_str)

def get_payment_tool_definition() -> Dict[str, Any]:
    """
    Returns the standardized payment tool definition
    
    Returns:
        A dictionary containing the payment tool definition
    """
    return {
        "type": "function",
        "function": {
            "name": "create_payment",
            "description": "Create a payment transaction between agents. If transaction is not approved, there may be a chance you will be receiving a specific challenge request from the payment validator and you will be able to provide additional information in your reasoning process and resubmit the transaction. The challenge will be expired when the conversation is closed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "amount": {"type": "number"},
                    "receiving_agent_id": {"type": "string"},
                    "currency": {"type": "string", "default": "USDT"},
                    "settlement_network": {"type": "string", "default": "solana"}
                },
                "required": ["agent_id", "amount", "recipient_agent_id"]
            }
        }
    }

def get_balance_tool_definition() -> Dict[str, Any]:
    """
    Returns the standardized balance query tool definition
    
    Returns:
        A dictionary containing the balance tool definition
    """
    return {
        "type": "function",
        "function": {
            "name": "get_agent_balance",
            "description": "Query agent's account balance",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"}
                },
                "required": ["agent_id"]
            }
        }
    }

def get_all_tool_definitions() -> List[Dict[str, Any]]:
    """
    Returns all available tool definitions
    
    Returns:
        A list of dictionaries containing all tool definitions
    """
    return [
        get_payment_tool_definition(),
        get_balance_tool_definition()
    ]
