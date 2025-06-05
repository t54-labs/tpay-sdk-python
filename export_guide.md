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
pip install requests>=2.25.1 python-dotenv>=0.19.0
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
```

### 4. Use Audit Functionality
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

Examples include:
- SDK initialization
- Tool function definitions
- LLM calls
- Conversation management
- Audit submission
- Agent creation

## Supported Features

✅ Payment processing (`tpay_toolkit_payment`)
✅ Balance inquiry (`tpay_toolkit_balance`) 
✅ Function tracing (`@tradar_verifier`)
✅ Code auditing (`@taudit_verifier`)
✅ Agent conversation management (`TPayAgent`)
✅ Agent creation (`create_agent`)
✅ Context management and tracing
✅ Error handling and logging

Build time: $(Get-Date)
SDK version: 0.1.1 