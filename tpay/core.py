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
