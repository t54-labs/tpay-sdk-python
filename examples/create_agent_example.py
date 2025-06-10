"""
TPay SDK - Create Agent Example

This example shows how to create a new agent using the TPay SDK.
"""

import tpay


def create_agent_example():
    """Example of creating a new agent"""
    
    # Method 1: Initialize SDK first, then create agent
    print("=== Method 1: Using SDK initialization ===")
    
    # Initialize the SDK with your credentials
    tpay.tpay_initialize(
        api_key="your_api_key_here",
        api_secret="your_api_secret_here",
        project_id="your_project_id_here",
        base_url="https://api.t54.ai/api/v1"  # or your API base URL
    )
    
    # Create agent using the standalone function
    agent_data = tpay.create_agent(
        name="My Test Agent",
        description="This is a test agent created via TPay SDK",
        agent_daily_limit=200.0,  # Optional: daily spending limit
        agent_type="autonomous_agent"  # Optional: agent type
    )
    
    if agent_data:
        print(f"Successfully created agent with ID: {agent_data['id']}")
        print(f"Agent name: {agent_data['name']}")
    else:
        print("Failed to create agent")
    
    print("\n" + "="*50 + "\n")
    
    # Method 2: Using TPayAgent class
    print("=== Method 2: Using TPayAgent class ===")
    
    # Create TPayAgent instance
    agent = tpay.TPayAgent()
    
    # Create agent using the class method
    agent_data2 = agent.create_agent(
        name="My Second Test Agent",
        description="Another test agent created via TPay SDK",
        project_id="your_project_id_here"  # Optional: override default project_id
    )
    
    if agent_data2:
        print(f"Successfully created agent with ID: {agent_data2['id']}")
        print(f"Agent name: {agent_data2['name']}")
    else:
        print("Failed to create agent")
    
    print("\n" + "="*50 + "\n")
    
    # Method 3: Get agent asset balance
    print("=== Method 3: Get Agent Asset Balance ===")
    
    if agent_data:
        agent_id = agent_data['id']
        
        # Using standalone function
        print("Using standalone function:")
        balance_data = tpay.get_agent_asset_balance(
            agent_id=agent_id,
            network="solana",
            asset="USDC"
        )
        
        print("\nUsing TPayAgent class:")
        balance_data2 = agent.get_agent_asset_balance(
            agent_id=agent_id,
            network="solana", 
            asset="SOL"
        )


if __name__ == "__main__":
    create_agent_example() 