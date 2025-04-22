"""
OpenAI Wrapper Module for TPay SDK
"""

import copy
from typing import Dict, Any, List, Optional
from openai import OpenAI
from openai.resources.chat.completions import Completions
from .trace import trace_store

def wrap_openai_client(client: Optional[OpenAI] = None) -> None:
    """
    Wrap OpenAI client to track and audit LLM calls
    
    Args:
        client: OpenAI client instance (optional)
    """
    # Save the original create method
    _orig_create = Completions.create
    
    def wrapped_create(self, *args, **kwargs):
        messages = kwargs.get("messages", [])
        tools = kwargs.get("tools", [])

        trace_store.set("messages", copy.deepcopy(messages))
        trace_store.set("tools", copy.deepcopy(tools))

        response = _orig_create(self, *args, **kwargs)

        trace_store.set("response", response)
        return response

    # ✅ Replace the method of the Completions class itself, not an instance
    Completions.create = wrapped_create