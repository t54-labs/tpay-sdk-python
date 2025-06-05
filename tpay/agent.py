"""
TPay SDK Agent Module
"""

import time
import json
import traceback
from typing import Dict, Any, List, Optional
from .exceptions import TPayError, TPayTimeoutError
from .trace import trace_store
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

def serialize_to_json(obj: Any) -> str:
    """
    Serialize an object to JSON string, handling non-serializable objects.
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON string representation of the object
    """
    def custom_serializer(item):
        # Handle common non-serializable types
        if hasattr(item, '__dict__'):
            # For objects with __dict__ attribute, convert to dict
            return {k: custom_serializer(v) for k, v in item.__dict__.items()}
        elif hasattr(item, 'model_dump'):
            # For Pydantic models
            return custom_serializer(item.model_dump())
        elif isinstance(item, (list, tuple)):
            # For lists and tuples
            return [custom_serializer(i) for i in item]
        elif isinstance(item, dict):
            # For dictionaries
            return {k: custom_serializer(v) for k, v in item.items()}
        elif hasattr(item, '__str__'):
            # For other objects, convert to string
            return str(item)
        else:
            # For basic types, return as is
            return item
    
    try:
        # First try to serialize with custom serializer
        serialized_obj = custom_serializer(obj)
        return json.dumps(serialized_obj)
    except Exception as e:
        # If serialization fails, use a simplified version
        logger.warning(f"Failed to serialize object: {e}")
        # Create a simplified version with only serializable data
        if isinstance(obj, dict):
            simplified_obj = {
                k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v
                for k, v in obj.items()
            }
            return json.dumps(simplified_obj)
        else:
            return json.dumps(str(obj))


class PaymentRequest(BaseModel):
    request_id: str | None = Field(
        default=None,
        description="Optional request ID for idempotency. If not provided, one will be generated.",
    )
    sending_agent_id: str = Field(
        ..., description="Unique ID of the sending agent."
    )
    receiving_agent_id: str = Field(
        ..., description="Unique ID of the receiving agent."
    )
    payment_amount: float = Field(
        ..., gt=0, description="The amount for the payment, must be positive."
    )
    settlement_network: str = Field(
        default="solana", description="network used for settlement."
    )
    currency: str = Field(
        ...,
        description="Currency used in the crypto bridge (e.g., USDT, USDC, BTC, ETH).",
    )
    trace_context: str = Field(
        default="{}", description="JSON string containing agent runtime environment state and parameters"
    )
    func_stack_hashes: str = Field(
        default="[]", description="JSON string containing the hashes of the functions in the call stack"
    )
    debug_mode: bool = Field(
        default=False, description="Debug mode for testing"
    )

class TPayAgent:
    """
    TPay Agent for payment processing and tracking
    """
    
    def __init__(self):
        """
        Initialize TPay Agent
        """
        pass
    
    def create_payment(
        self,
        agent_id: str,
        receiving_agent_id: str,
        amount: float,
        currency: str = "USDT",
        settlement_network: str = "solana",
        trace_context: Optional[Dict[str, Any]] = None,
        func_stack_hashes: Optional[str] = None,
        debug_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Create a payment
        
        Args:
            agent_id: ID of the agent
            receiving_agent_id: ID of the receiving agent
            payment_amount: Payment amount
            currency: Payment currency (default: USDT)
            settlement_network: Settlement network (default: solana)
            trace_context: Trace context for tracking
            func_stack_hashes: JSON string containing function hashes
            debug_mode: Debug mode for testing
        Returns:
            Payment information
        """
        from .core import make_request
        
        logger.debug("Creating payment request")

        # If trace_context is not provided, try to get it from the current context
        if trace_context is None:
            trace_context = trace_store.get_all()
        
        try:
            # Convert trace_context to JSON string using the utility function
            trace_context_str = serialize_to_json(trace_context) if trace_context else "{}"
            # func_stack_hashes is already a string, no need to serialize
            func_stack_hashes_str = func_stack_hashes if func_stack_hashes else "[]"

            # Create PaymentRequest object
            payment_request = PaymentRequest(
                sending_agent_id=agent_id,
                receiving_agent_id=receiving_agent_id,
                payment_amount=amount,
                currency=currency,
                settlement_network=settlement_network,
                trace_context=trace_context_str,
                func_stack_hashes=func_stack_hashes_str,
                debug_mode=debug_mode
            )
        except Exception as e:
            traceback.print_exc()
            raise TPayError(f"Error creating payment request: {e}")
        
        # Send request using the PaymentRequest model
        return make_request("POST", "/payment", data=payment_request.model_dump())
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """
        Get payment status
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment status information
        """
        from .core import make_request
        return make_request("GET", f"/payment/{payment_id}")
    
    def get_agent_balance(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent balance
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            Agent balance information
        """
        from .core import make_request
        return make_request("GET", f"/balance/agent/{agent_id}")
    
    def wait_for_payment_success(
        self,
        payment_id: str,
        timeout: int = 60,
        check_interval: int = 2
    ) -> Dict[str, Any]:
        """
        Wait for payment to succeed
        
        Args:
            payment_id: Payment ID
            timeout: Maximum time to wait in seconds
            check_interval: Time between status checks in seconds
            
        Returns:
            Final payment status
            
        Raises:
            TPayTimeoutError: If payment does not succeed within timeout
        """
        start_time = time.time()
        while True:
            status = self.get_payment_status(payment_id)
            if status["status"] == "success":
                return status
            elif status["status"] in ["failed", "cancelled"]:
                return False
                
            if time.time() - start_time > timeout:
                raise TPayTimeoutError(
                    f"Payment {payment_id} did not succeed within {timeout} seconds"
                )
                
            time.sleep(check_interval)
    
    def create_agent(
        self,
        name: str,
        description: str,
        project_id: Optional[str] = None,
        agent_daily_limit: float = 100.0,
        agent_type: str = "autonomous_agent"
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new agent using API key and secret authentication
        
        Args:
            name: Agent name
            description: Agent description
            project_id: Project ID (optional, will use config default if not provided)
            agent_daily_limit: Daily spending limit for the agent (default: 100.0)
            agent_type: Type of agent (default: "autonomous_agent")
            
        Returns:
            Dictionary containing agent information, or None if creation fails
        """
        from .core import make_request, get_config
        
        # Get project_id from config if not provided
        if project_id is None:
            config = get_config()
            project_id = config.get("project_id")
            if not project_id:
                logger.error("Project ID not provided and not found in configuration")
                return None
        
        logger.info(f"Creating agent: {name}")
        
        payload = {
            "name": name,
            "project_id": project_id,
            "description": description,
            "agent_daily_limit": agent_daily_limit,
            "agent_type": agent_type
        }
        
        try:
            # Use the make_request function which handles API key/secret authentication
            agent_data = make_request("POST", "/agent_profiles", data=payload)
            logger.info(f"Agent creation successful: {agent_data.get('id', 'Unknown ID')}")
            print("\n=== Agent Creation Response ===")
            print(json.dumps(agent_data, indent=2))
            print("="*30)
            return agent_data
        except Exception as e:
            logger.error(f"Agent creation failed: {str(e)}")
            return None
