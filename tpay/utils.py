"""
TPay SDK Utilities Module
"""

import hashlib
import json
import re
import uuid
from typing import Dict, Any

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
