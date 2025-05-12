"""
TPay SDK Tools Module
"""

import functools
import inspect
import hashlib
import logging
import os
import linecache
import json
import traceback

from tpay.utils import normalize_code
from .trace import trace_store

from typing import Dict, Any, Callable, List, Tuple
from .agent import TPayAgent
from .core import make_request, register_init_callback, get_config
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Global registry for audited functions
AUDITED_ENTITIES: List[Tuple[Callable, Dict[str, Any]]] = []
AUDIT_SNAPSHOT: Dict[str, Dict[str, Any]] = {}

# Audit snapshot file path
AUDIT_SNAPSHOT_FILE = "audit_snapshot.txt"

class FunctionInfo(BaseModel):
    """Function information model"""
    function_name: str = Field(..., description="Function name")
    function_code: str = Field(..., description="Function code")


class CodeAuditRequest(BaseModel):
    """Request model for code audit"""
    functions: List[FunctionInfo] = Field(..., description="List of functions")
    project_id: str = Field(..., description="Project ID")


def taudit_verifier(func: Callable) -> Callable:
    """
    Decorator for core functions to enable code auditing.
    Collects function location and source code hash for verification.
    
    Args:
        func: Function to be audited
        
    Returns:
        Decorated function
        
    Raises:
        TypeError: If the decorator is applied to a non-function
    """
    if not inspect.isfunction(func):
        raise TypeError(f"[t54_audit] Error: @taudit_verifier can only be used on functions, not on classes ({func})")

    try:
        # Get source code and location information
        src_lines, start_line = inspect.getsourcelines(func)
        src = ''.join(src_lines).strip()

        file_path = inspect.getsourcefile(func)
        code_hash = hashlib.sha256(src.encode("utf-8")).hexdigest()

        # Create unique function identifier
        func_id = f"{os.path.abspath(file_path)}:{func.__name__}:{start_line}"

        # Collect metadata
        metadata = {
            "file": os.path.abspath(file_path),
            "name": func.__name__,
            "line": start_line,
            "hash": code_hash,
            "source": src
        }

        # Register the function for auditing
        AUDITED_ENTITIES.append((func, metadata))
        AUDIT_SNAPSHOT[func_id] = metadata

    except Exception as e:
        logger.error(f"Unable to get metadata for function {func.__name__}: {e}")

    return func


def get_current_stack_function_hashes():
    """Get file paths, function signatures, and code hashes of all functions in the call stack"""
    stack = inspect.stack()
    result = []

    for frame_info in stack:
        code = frame_info.frame.f_code
        filename = os.path.abspath(code.co_filename)
        lineno = code.co_firstlineno
        func_name = code.co_name

        # Get source code text (get the entire function, not just the first line)
        try:
            # Use inspect.getsourcelines to safely get the entire function body
            lines, _ = inspect.getsourcelines(code)
            source = ''.join(lines).strip()
            source = normalize_code(source)
        except Exception:
            # fallback: use linecache to get a single line
            traceback.print_exc()
            source = linecache.getline(filename, lineno).strip()

        code_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
        result.append(code_hash)

    # 将哈希列表转换为 JSON 字符串
    result_str = json.dumps(result)
    return result_str


def submit_audit(project_id: str = "default") -> Dict[str, Any]:
    """
    Submit all audited functions to the backend /audit endpoint
    
    Args:
        project_id: Project ID for the audit
        
    Returns:
        Response from the audit endpoint
    """
    if not AUDITED_ENTITIES:
        logger.warning("No functions have been audited")
        return {"status": "no_entities", "message": "No functions have been audited"}
    
    # Prepare function information list
    functions = []
    for func, metadata in AUDITED_ENTITIES:
        functions.append(
            FunctionInfo(
                function_name=metadata["name"],
                function_code=metadata["source"]
            )
        )
    
    # Create audit request
    audit_request = CodeAuditRequest(
        functions=functions,
        project_id=project_id
    )
    
    # Submit to backend
    try:
        response = make_request("POST", "/radar/audit", data=audit_request.model_dump())
        return response
    except Exception as e:
        logger.error(f"Failed to finish taudit: {str(e)}")
        return {"status": "error", "message": f"Failed to submit audit: {str(e)}"}


def tradar_verifier(func: Callable) -> Callable:
    """
    Decorator for tool functions to enable verification and tracking
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get function name and arguments
        func_name = func.__name__
        
        # Get current tool call history, initialize as empty list if not exists
        tool_history = trace_store.get("tool_history") or []
        
        # Add current tool call to history
        tool_history.append({
            "name": func_name,
            "args": {"args": args, "kwargs": kwargs}
        })
        
        # Update tool call history
        trace_store.set("tool_history", tool_history)
        
        # Set current tool call (maintain backward compatibility)
        trace_store.set("tool_invoked", func_name)
        trace_store.set("tool_args", {"args": args, "kwargs": kwargs})
                
        # Call original function
        return func(*args, **kwargs)
         
    return wrapper


class PaymentTool:
    """
    Payment tool class for creating payments
    """
    
    def __init__(self):
        """Initialize payment tool"""
        self.agent = TPayAgent()
    
    @tradar_verifier
    def __call__(
        self,
        agent_id: str,
        receiving_agent_id: str,
        amount: float,
        currency: str = "USDT",
        settlement_network: str = "solana",
        debug_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Create a payment
        
        Args:
            agent_id: ID of the sending agent
            receiving_agent_id: ID of the receiving agent
            payment_amount: Payment amount
            currency: Payment currency (default: USDT)
            settlement_network: Settlement network (default: solana)
            debug_mode: Debug mode for testing
            
        Returns:
            Payment information
        """
        # Get current tool call and arguments
        trace_context = trace_store.get_all()
        logger.info(f"Creating payment from {agent_id} to {receiving_agent_id} with amount {amount} {currency} on {settlement_network}")

        func_stack_hashes = get_current_stack_function_hashes()

        # Create payment
        return self.agent.create_payment(
            agent_id=agent_id,
            receiving_agent_id=receiving_agent_id,
            amount=amount,
            currency=currency,
            settlement_network=settlement_network,
            trace_context=trace_context,
            func_stack_hashes=func_stack_hashes,
            debug_mode=debug_mode
        )


class BalanceTool:
    """
    Balance tool class for checking agent balances
    """
    
    def __init__(self):
        """Initialize balance tool"""
        self.agent = TPayAgent()
    
    @tradar_verifier
    def __call__(
        self,
        agent_id: str
    ) -> Dict[str, Any]:
        """
        Get agent balance
        
        Args:
            agent_id: ID of the agent to check balance for
            
        Returns:
            Agent balance information
        """
        return self.agent.get_agent_balance(agent_id)


def tpay_toolkit_payment() -> PaymentTool:
    """
    Create a payment tool instance
    
    Returns:
        Payment tool instance
    """
    return PaymentTool()


def tpay_toolkit_balance() -> BalanceTool:
    """
    Create a balance tool instance
    
    Returns:
        Balance tool instance
    """
    return BalanceTool()


def get_current_agent_trace():
    return trace_store.get_all()


def _init_tools():
    """Initialize tools module"""
    try:
        from .openai_wrapper import wrap_openai_client
        logger.info("Initializing agent reasoning tracking module...")
        wrap_openai_client()
    except Exception as e:
        logger.error(f"Failed to wrap OpenAI client: {e}")

    try:
        config = get_config()
        logger.info("Initializing taudit module...")
        submit_audit(project_id=config["project_id"])
    except Exception as e:
        logger.error(f"Failed to submit audit: {e}")

# Register initialization callback
register_init_callback(_init_tools)