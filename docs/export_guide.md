# TPay SDK Export Guide

## Build Complete ✅

TPay SDK has been successfully built! Version: 0.1.1

## Method 1: Using Built Package (Recommended)

### 1. Copy Distribution Package
Copy the following files to your target project:
```
dist/tpay-0.1.1-py3-none-any.whl    # wheel package (recommended)
or
dist/tpay-0.1.1.tar.gz              # source package
```

### 2. Install in Target Project
```bash
# Method A: Install wheel package directly
pip install tpay-0.1.1-py3-none-any.whl

# Method B: Install source package
pip install tpay-0.1.1.tar.gz
```

## Method 2: Copy Source Code Directly

### Required Files and Folders to Copy:
```
tpay/                          # Entire tpay folder
├── __init__.py               # SDK entry file
├── core.py                   # Core functionality (initialization, API calls)
├── agent.py                  # Agent class
├── tools.py                  # Payment tools and decorators
├── utils.py                  # Utility functions
├── exceptions.py             # Exception definitions
├── trace.py                  # Tracing functionality
└── openai_wrapper.py         # OpenAI wrapper

examples/                      # Example files (optional)
├── __init__.py
├── test_agent.py             # Complete agent usage example
└── create_agent_example.py   # Agent creation example

README.md                      # Usage documentation (optional)
setup.py                       # For repackaging if needed (optional)
```

### Manually Install Dependencies in Target Project:
```bash
# Basic dependencies
pip install requests>=2.25.1 python-dotenv>=0.19.0

# For async functionality (optional)
pip install httpx>=0.24.0
```

## Usage

### 1. Basic Usage
```python
import tpay

# Initialize SDK
tpay.tpay_initialize(
    api_key="your_api_key",
    api_secret="your_api_secret",
    project_id="your_project_id",
    base_url="https://api.t54.ai/api/v1"
)

# Use payment tools
@tpay.tradar_verifier
def my_payment_function():
    return tpay.tpay_toolkit_payment(
        receiving_agent_id="agent123",
        payment_amount=100.0,
        currency="USDT",
        settlement_network="solana"
    )
```

### 2. Create New Agent
```python
import tpay

# Initialize SDK
tpay.tpay_initialize(
    api_key="your_api_key",
    api_secret="your_api_secret",
    project_id="your_project_id"
)

# Create agent using standalone function
agent_data = tpay.create_agent(
    name="My Test Agent",
    description="This is a test agent created via TPay SDK",
    agent_daily_limit=200.0,
    agent_type="autonomous_agent"
)

# Or using TPayAgent class
agent = tpay.TPayAgent()
agent_data = agent.create_agent(
    name="My Second Test Agent",
    description="Another test agent"
)
```

### 3. Use Agent Functionality
```python
from tpay import TPayAgent

agent = TPayAgent()

# Create payment
payment_result = agent.create_payment(
    agent_id="your_agent_id",
    receiving_agent_id="recipient_agent_id",
    amount=100.0,
    currency="USDT"
)

# Check balance
balance = agent.get_agent_balance("your_agent_id")

# Get specific asset balance
asset_balance = agent.get_agent_asset_balance(
    agent_id="your_agent_id",
    network="solana",
    asset="USDC"
)
```

### 4. Get Agent Asset Balance
```python
import tpay

# Initialize SDK
tpay.tpay_initialize(
    api_key="your_api_key",
    api_secret="your_api_secret",
    project_id="your_project_id"
)

# Method 1: Using standalone function
balance_data = tpay.get_agent_asset_balance(
    agent_id="agent_123",
    network="solana",
    asset="USDC"
)

# Method 2: Using TPayAgent class
agent = tpay.TPayAgent()
balance_data = agent.get_agent_asset_balance(
    agent_id="agent_123",
    network="xrpl",
    asset="XRP"
)

if balance_data:
    print(f"Balance: {balance_data['balance']} {balance_data['asset']}")
    print(f"USD Value: ${balance_data['balance_usd']}")
```

### 5. Async Functionality (Advanced)

**Installation with async support:**
```bash
pip install tpay-0.1.1.tar.gz[async]
# or
pip install tpay-0.1.1.tar.gz[all]
```

**Basic async usage:**
```python
import asyncio
import tpay

async def main():
    # Initialize SDK (same as sync)
    tpay.tpay_initialize(
        api_key="your_api_key",
        api_secret="your_api_secret",
        project_id="your_project_id"
    )
    
    # Method 1: Using async standalone functions
    agent_data = await tpay.async_create_agent(
        name="Async Agent",
        description="Created asynchronously"
    )
    
    balance = await tpay.async_get_agent_asset_balance(
        agent_id="agent_id",
        network="solana",
        asset="USDC"
    )
    
    # Method 2: Using AsyncTPayAgent class
    async_agent = tpay.AsyncTPayAgent()
    
    payment = await async_agent.create_payment(
        agent_id="sender_id",
        receiving_agent_id="receiver_id",
        amount=100.0
    )
    
    # Concurrent operations
    results = await asyncio.gather(
        tpay.async_create_agent("Agent 1", "Desc 1"),
        tpay.async_create_agent("Agent 2", "Desc 2"),
        tpay.async_get_agent_asset_balance("id", "solana", "USDC")
    )

# Run async code
asyncio.run(main())
```

**Available async functions:**
- `async_make_request()` - Core async HTTP requests
- `async_create_agent()` - Create agent asynchronously
- `async_get_agent_asset_balance()` - Get balance asynchronously
- `AsyncTPayAgent` class with all async methods

### 6. Use Audit Functionality
```python
@tpay.taudit_verifier
def my_audited_function():
    # This function will be automatically audited
    pass
```

## Important Notes

1. **Must Initialize First**: Call `tpay_initialize()` before using any tpay functionality
2. **API Credentials**: Ensure correct api_key, api_secret, and project_id are configured in target project
3. **Environment Variables**: You can use .env file for configuration:
   ```
   TLEDGER_API_KEY=your_api_key
   TLEDGER_API_SECRET=your_api_secret
   TLEDGER_PROJECT_ID=your_project_id
   TLEDGER_API_BASE_URL=https://api.t54.ai/api/v1
   ```

## Complete Examples

Refer to the `examples/` folder for complete usage examples, including:
- `test_agent.py`: Complete agent usage example
- `create_agent_example.py`: Agent creation example
- `async_example.py`: Async functionality demonstration

Examples include:
- SDK initialization
- Tool function definitions
- LLM calls
- Conversation management
- Audit submission
- Agent creation
- Async operations and concurrent execution

## Supported Features

### Synchronous API
✅ Payment processing (`tpay_toolkit_payment`)
✅ Balance inquiry (`tpay_toolkit_balance`) 
✅ Asset-specific balance inquiry (`get_agent_asset_balance`)
✅ Agent creation (`create_agent`)
✅ Agent conversation management (`TPayAgent`)
✅ Function tracing (`@tradar_verifier`)
✅ Code auditing (`@taudit_verifier`)
✅ Context management and tracing
✅ Error handling and logging

### Asynchronous API (New!)
✅ Async HTTP requests (`async_make_request`)
✅ Async agent creation (`async_create_agent`)
✅ Async balance inquiry (`async_get_agent_asset_balance`)
✅ Async agent management (`AsyncTPayAgent`)
✅ Async payment processing
✅ Async payment status checking
✅ Concurrent operation support
✅ Compatible with asyncio ecosystem

Build time: $(Get-Date)
SDK version: 0.1.1 