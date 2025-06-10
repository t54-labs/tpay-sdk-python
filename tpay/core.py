"""
TPay SDK Core Module
"""

import os
import json
import time
import logging
import traceback
import requests
from typing import Dict, Any, Optional, Callable, List
from dotenv import load_dotenv

# Async imports
try:
    import httpx
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
from .exceptions import TPayAPIError, TPayConfigError
from .trace import trace_store

logger = logging.getLogger(__name__)

if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.WARNING)
    
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)
        root_logger.setLevel(logging.WARNING)

# global configuration
_config = {
    "api_key": None,
    "api_secret": None,
    "base_url": "http://127.0.0.1:4000/api/v1",
    "timeout": 30,
}

# List of callback functions to be executed after initialization
_init_callbacks: List[Callable] = []

def register_init_callback(callback: Callable) -> None:
    """
    Register a callback function to be executed after initialization
    
    Args:
        callback: Callback function
    """
    _init_callbacks.append(callback)

def tpay_initialize(
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    base_url: Optional[str] = None,
    project_id: Optional[str] = None,
    timeout: Optional[int] = None
) -> None:
    """
    Initialize TPay SDK with API credentials
    
    Args:
        api_key: API key for authentication
        api_secret: API secret for authentication
        base_url: Base URL for API requests
        project_id: Project ID for audit
        timeout: Request timeout in seconds
    """
    # use the provided parameters first
    if api_key:
        _config["api_key"] = api_key
    elif os.getenv("TLEDGER_API_KEY"):
        _config["api_key"] = os.getenv("TLEDGER_API_KEY")
    
    if api_secret:
        _config["api_secret"] = api_secret
    elif os.getenv("TLEDGER_API_SECRET"):
        _config["api_secret"] = os.getenv("TLEDGER_API_SECRET")
    
    if base_url:
        _config["base_url"] = base_url
    elif os.getenv("TLEDGER_API_BASE_URL"):
        _config["base_url"] = os.getenv("TLEDGER_API_BASE_URL")
    
    if not _config["base_url"]:
        _config["base_url"] = "http://127.0.0.1:4000/api/v1"

    if timeout:
        _config["timeout"] = timeout
    else:
        _config["timeout"] = 30
    
    if project_id:
        _config["project_id"] = project_id
    elif os.getenv("TLEDGER_PROJECT_ID"):
        _config["project_id"] = os.getenv("TLEDGER_PROJECT_ID")
    
    # verify the configuration
    if not _config["api_key"] or not _config["api_secret"]:
        raise TPayConfigError("API credentials not provided")

    if not _config["project_id"]:
        raise TPayConfigError("Project ID not provided, you can obtain it from https://portal.t54.ai/dashboard")
    
    # Execute all callbacks after initialization
    for callback in _init_callbacks:
        try:
            callback()
        except Exception as e:
            logger.warning(f"Init callback failed: {e}")
    
    logger.info("tPay SDK initialized successfully")

def get_config() -> Dict[str, Any]:
    """
    Get current configuration
    
    Returns:
        Current configuration dictionary
    """
    return _config.copy()

def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an API request
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        data: Request data
        params: Query parameters
        headers: Request headers
        
    Returns:
        API response
    """
    config = get_config()
    
    if not headers:
        headers = {}
    
    headers.update({
        "X-API-Key": config["api_key"],
        "X-API-Secret": config["api_secret"],
        "Content-Type": "application/json",
    })
    
    url = f"{config['base_url']}/{endpoint.lstrip('/')}"
    
    try:
        response = requests.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=headers,
            timeout=config["timeout"]
        )
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        raise TPayAPIError(f"API request failed: {str(e)}", 
                          status_code=getattr(e.response, 'status_code', None),
                          response=getattr(e.response, 'json', lambda: None)())

def create_agent(
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
        return agent_data
    except Exception as e:
        logger.error(f"Agent creation failed: {str(e)}")
        return None

def get_agent_asset_balance(
    agent_id: str,
    network: str,
    asset: str
) -> Optional[Dict[str, Any]]:
    """
    Get the balance for a specific asset on a specific network for an agent
    
    Args:
        agent_id: ID of the agent
        network: Network (e.g., solana, xrpl)
        asset: Asset type (e.g., USDC, XRP, SOL)
        
    Returns:
        Dictionary containing asset balance information, or None if retrieval fails
    """
    logger.info(f"Getting {asset} balance on {network} for agent {agent_id}")
    
    endpoint = f"/balance/agent/{agent_id}/{network}/{asset}"
    
    try:
        # Use the make_request function which handles API key/secret authentication
        balance_data = make_request("GET", endpoint)
        balance_data["balance"] = float(balance_data["balance"])
        return balance_data["balance"]
    except Exception as e:
        logger.error(f"Asset balance retrieval failed: {str(e)}")
        return None

# ===============================================
# ASYNC VERSIONS
# ===============================================

async def async_make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make an async API request
    
    Args:
        method: HTTP method
        endpoint: API endpoint
        data: Request data
        params: Query parameters
        headers: Request headers
        
    Returns:
        API response
        
    Raises:
        ImportError: If httpx is not installed
        TPayAPIError: If API request fails
    """
    if not ASYNC_AVAILABLE:
        raise ImportError("httpx is required for async functionality. Install with: pip install httpx")
    
    config = get_config()
    
    if not headers:
        headers = {}
    
    headers.update({
        "X-API-Key": config["api_key"],
        "X-API-Secret": config["api_secret"],
        "Content-Type": "application/json",
    })
    
    url = f"{config['base_url']}/{endpoint.lstrip('/')}"
    
    try:
        async with httpx.AsyncClient(timeout=config["timeout"]) as client:
            response = await client.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            )
            
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        traceback.print_exc()
        raise TPayAPIError(f"Async API request failed: {str(e)}")
    except httpx.HTTPStatusError as e:
        traceback.print_exc()
        raise TPayAPIError(f"Async API request failed: {str(e)}", 
                          status_code=e.response.status_code,
                          response=e.response.json() if e.response.headers.get('content-type', '').startswith('application/json') else None)

async def async_create_agent(
    name: str,
    description: str,
    project_id: Optional[str] = None,
    agent_daily_limit: float = 100.0,
    agent_type: str = "autonomous_agent"
) -> Optional[Dict[str, Any]]:
    """
    Async version: Create a new agent using API key and secret authentication
    
    Args:
        name: Agent name
        description: Agent description
        project_id: Project ID (optional, will use config default if not provided)
        agent_daily_limit: Daily spending limit for the agent (default: 100.0)
        agent_type: Type of agent (default: "autonomous_agent")
        
    Returns:
        Dictionary containing agent information, or None if creation fails
    """
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
        # Use the async_make_request function which handles API key/secret authentication
        agent_data = await async_make_request("POST", "/agent_profiles", data=payload)
        logger.info(f"Agent creation successful: {agent_data.get('id', 'Unknown ID')}")
        return agent_data
    except Exception as e:
        logger.error(f"Agent creation failed: {str(e)}")
        return None

async def async_get_agent_asset_balance(
    agent_id: str,
    network: str,
    asset: str
) -> Optional[float]:
    """
    Async version: Get the balance for a specific asset on a specific network for an agent
    
    Args:
        agent_id: ID of the agent
        network: Network (e.g., solana, xrpl)
        asset: Asset type (e.g., USDC, XRP, SOL)
        
    Returns:
        Float balance value, or None if retrieval fails
    """
    logger.info(f"Getting {asset} balance on {network} for agent {agent_id}")
    
    endpoint = f"/balance/agent/{agent_id}/{network}/{asset}"
    
    try:
        # Use the async_make_request function which handles API key/secret authentication
        balance_data = await async_make_request("GET", endpoint)
        balance_data["balance"] = float(balance_data["balance"])
        return balance_data["balance"]
    except Exception as e:
        logger.error(f"Asset balance retrieval failed: {str(e)}")
        return None
