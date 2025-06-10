"""
TPay SDK - Async Usage Example

This example shows how to use the asynchronous functionality of the TPay SDK.
"""

import asyncio
import tpay


async def async_example():
    """Example of using async TPay SDK functionality"""
    
    print("=== Async TPay SDK Example ===")
    
    # Initialize the SDK with your credentials (same as sync version)
    tpay.tpay_initialize(
        api_key="your_api_key_here",
        api_secret="your_api_secret_here",
        project_id="your_project_id_here",
        base_url="https://api.t54.ai/api/v1"  # or your API base URL
    )
    
    print("\n1. Creating agent asynchronously...")
    
    # Method 1: Using async standalone function
    agent_data = await tpay.async_create_agent(
        name="Async Test Agent",
        description="This is a test agent created via async TPay SDK",
        agent_daily_limit=300.0,
        agent_type="autonomous_agent"
    )
    
    if agent_data:
        print(f"✅ Successfully created agent with ID: {agent_data['id']}")
        print(f"   Agent name: {agent_data['name']}")
        agent_id = agent_data['id']
    else:
        print("❌ Failed to create agent")
        return
    
    print("\n2. Using AsyncTPayAgent class...")
    
    # Method 2: Using AsyncTPayAgent class
    async_agent = tpay.AsyncTPayAgent()
    
    # Create another agent
    agent_data2 = await async_agent.create_agent(
        name="Second Async Agent",
        description="Another async test agent"
    )
    
    if agent_data2:
        print(f"✅ Successfully created second agent with ID: {agent_data2['id']}")
    
    print("\n3. Getting asset balance asynchronously...")
    
    # Method 3: Get agent asset balance
    try:
        # Using standalone async function
        balance = await tpay.async_get_agent_asset_balance(
            agent_id=agent_id,
            network="solana",
            asset="USDC"
        )
        
        if balance is not None:
            print(f"✅ Agent USDC balance: {balance}")
        else:
            print("❌ Failed to get balance")
        
        # Using AsyncTPayAgent class method
        balance2 = await async_agent.get_agent_asset_balance(
            agent_id=agent_id,
            network="solana",
            asset="SOL"
        )
        
        if balance2 is not None:
            print(f"✅ Agent SOL balance: {balance2}")
            
    except Exception as e:
        print(f"❌ Balance retrieval error: {e}")
    
    print("\n4. Creating payment asynchronously...")
    
    # Create a payment
    try:
        payment_result = await async_agent.create_payment(
            agent_id=agent_id,
            receiving_agent_id="recipient_agent_id_here",
            amount=10.0,
            currency="USDT",
            settlement_network="solana"
        )
        
        if payment_result:
            print(f"✅ Payment created: {payment_result.get('id', 'Unknown')}")
            
            # Wait for payment success
            payment_id = payment_result.get('id')
            if payment_id:
                print("   Waiting for payment to complete...")
                final_status = await async_agent.wait_for_payment_success(
                    payment_id=payment_id,
                    timeout=30
                )
                print(f"   Payment final status: {final_status}")
        
    except Exception as e:
        print(f"❌ Payment error: {e}")
    
    print("\n5. Concurrent operations example...")
    
    # Example of running multiple async operations concurrently
    try:
        tasks = [
            tpay.async_get_agent_asset_balance(agent_id, "solana", "USDC"),
            tpay.async_get_agent_asset_balance(agent_id, "solana", "SOL"),
            async_agent.get_agent_balance(agent_id)
        ]
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print("✅ Concurrent results:")
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   Task {i+1}: Error - {result}")
            else:
                print(f"   Task {i+1}: Success - {type(result).__name__}")
                
    except Exception as e:
        print(f"❌ Concurrent operations error: {e}")
    
    print("\n🎉 Async example completed!")


def sync_vs_async_comparison():
    """Comparison between sync and async usage"""
    
    print("\n" + "="*60)
    print("SYNC vs ASYNC Comparison")
    print("="*60)
    
    print("\n📝 Synchronous Usage:")
    print("""
    import tpay
    
    # Initialize SDK
    tpay.tpay_initialize(api_key="...", api_secret="...", project_id="...")
    
    # Create agent (blocking)
    agent_data = tpay.create_agent("My Agent", "Description")
    
    # Get balance (blocking)
    balance = tpay.get_agent_asset_balance("agent_id", "solana", "USDC")
    
    # Use TPayAgent class
    agent = tpay.TPayAgent()
    payment = agent.create_payment(...)
    """)
    
    print("\n⚡ Asynchronous Usage:")
    print("""
    import asyncio
    import tpay
    
    async def main():
        # Initialize SDK (same as sync)
        tpay.tpay_initialize(api_key="...", api_secret="...", project_id="...")
        
        # Create agent (non-blocking)
        agent_data = await tpay.async_create_agent("My Agent", "Description")
        
        # Get balance (non-blocking)
        balance = await tpay.async_get_agent_asset_balance("agent_id", "solana", "USDC")
        
        # Use AsyncTPayAgent class
        agent = tpay.AsyncTPayAgent()
        payment = await agent.create_payment(...)
        
        # Run multiple operations concurrently
        results = await asyncio.gather(
            tpay.async_create_agent("Agent 1", "Desc 1"),
            tpay.async_create_agent("Agent 2", "Desc 2"),
            tpay.async_get_agent_asset_balance("id", "solana", "USDC")
        )
    
    asyncio.run(main())
    """)
    
    print("\n💡 Key Benefits of Async:")
    print("   • Non-blocking operations")
    print("   • Better performance for I/O-bound tasks")
    print("   • Concurrent execution with asyncio.gather()")
    print("   • Same API interface as sync version")
    print("   • Fully compatible with existing code")


if __name__ == "__main__":
    print("🚀 Starting async example...")
    try:
        asyncio.run(async_example())
    except KeyboardInterrupt:
        print("\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
    finally:
        sync_vs_async_comparison() 