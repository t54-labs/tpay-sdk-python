# tPay SDK for Python

## Product Intro

Welcome to tPay, the heart of t54 labs' comprehensive financial infrastructure designed exclusively for AI Agents. Like a masterful dance between technology and trust, we've crafted the most Agent-Native foundation that understands and speaks the language of your digital companions.

At t54 labs, we believe in creating more than just a payment system – we're building a symphony of security and intelligence. Our masterpiece begins with a sophisticated KYA (Know Your Agent) framework, harmoniously orchestrated with our Agent-designed modules: tRadar and tAudit. Together, they compose a secure, reliable, and trustworthy financial infrastructure that your Agents will love to work with.

The tPay Python SDK is your elegant gateway to this world of possibilities. Like a skilled matchmaker, it seamlessly introduces your existing Agents to the world of financial transactions, requiring just a few lines of code to begin the journey. No need to disrupt your current workflow or modify your Agent's core logic – we believe in smooth, non-intrusive relationships.

Built for the modern AI ecosystem, our SDK supports both synchronous and asynchronous operations, ensuring optimal performance whether you're building a single agent or orchestrating a fleet of thousands. With our async-first architecture, your agents can handle financial operations with unprecedented efficiency and scale.

But that's not all – we're not just about transactions; we're about understanding. Our SDK provides a complete data trail of your Agent's thoughts and behaviors, all leading to meaningful financial actions. Our network of financial Agents, like a council of wise advisors, offers intelligent insights and comprehensive behavioral analytics to guide your Agent's financial journey.

Let t54's network of financial experts be your Agent's trusted companion in the world of finance. Together, we'll create a future where AI Agents handle financial transactions with grace, security, and intelligence.

## Features

### Core Functionality

1. **Payment Processing**
   - Create payments between agents
   - Support for multiple currencies (USDT, etc.)
   - Multiple settlement networks (Solana, etc.)
   - Transaction tracking and verification

2. **Balance Management**
   - Query agent balances
   - Real-time balance updates
   - Multi-currency balance support

3. **Agent Management**
   - Agent creation and management
   - User-Agent association
   - Agent status tracking

4. **Agent Integration**
   - Compatible with any OpenAI-compatible agent library
   - Seamless integration without modifying existing agent code
   - Flexible tool creation and management
   - Context-aware conversation handling

### Advanced Features

1. **Asynchronous API Support** ⚡
   - Full async/await support for all operations
   - High-performance concurrent execution
   - Non-blocking I/O operations
   - Compatible with asyncio ecosystem
   - Parallel agent creation and management
   - Concurrent balance queries and payments

2. **Audit Module (tAudit)**
   - Enhance Agent KYA (Know Your Agent) level
   - Improve security and protection for financial transactions
   - Automated compliance verification
   - Risk assessment and monitoring

3. **Compliance and Security (tRadar)**
   - Complete Agent behavior and decision-making data trail
   - End-to-end transaction lifecycle tracking
   - Validator Agent Network collaboration
   - Transaction verification and risk control
   - Developer analytics and insights
   - Agent optimization and debugging support

4. **Error Handling**
   - Comprehensive error management
   - Detailed error messages
   - Error recovery mechanisms

## Installation

```bash
# Basic installation
pip install tpay

# With async support (recommended for high-performance applications)
pip install tpay[async]
```

## Requirements

### Environment
- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux

### Dependencies
The SDK has the following main dependencies:
- `requests>=2.25.1`: For synchronous HTTP requests
- `python-dotenv>=0.19.0`: For environment variable management
- `pydantic>=2.0.0`: For data validation and settings management (optional)

**For Async Support (optional):**
- `httpx>=0.24.0`: For asynchronous HTTP requests

**For OpenAI Integration (optional):**
- `openai>=1.0.0`: For OpenAI API integration

Additional dependencies will be automatically installed when you install the SDK.

## Quick Start

### SDK Initialization

First, initialize the tPay SDK in your application:

```python
from tpay import tpay_initialize

# Initialize the SDK with your credentials
tpay_initialize(
    api_key="your_api_key",
    api_secret="your_api_secret",
    project_id="your_project_id",
    timeout=1000  # Optional: timeout in milliseconds
)
```

### Agent Integration

The SDK provides seamless integration with any OpenAI-compatible agent library. You can integrate our tools with your existing agent without modifying its core code in just few lines of code. Here's how:

1. **Create Tools**

```python
from tpay import *

# Create payment tool
payment_tool = tpay_toolkit_payment()

# Create balance tool
balance_tool = tpay_toolkit_balance()
```

2. **Add Tools to Your Agent**

Simply add the tools to your existing agent's tool list:

```python
# Example with OpenAI's client
from openai import OpenAI

# Initialize your own tool list for your agent
tools = [...]

# Then add our tool defintions to the tool list
tools.extend(get_all_tool_definitions())

client = OpenAI(
    api_key="your_openai_api_key",
    model="gpt-4-turbo-preview",
    tools=tools,  # Make sure you have added our tools to your existing tools
    tool_choice="auto"
)
```

3. **Handle Tool Execution**

Implement a tool execution handler that works with your agent:

```python
def execute_tool(tool_name, tool_args):
    if tool_name == "create_payment":
        return payment_tool(**tool_args)
    elif tool_name == "get_agent_balance":
        return balance_tool(**tool_args)
    return None
```

That's it! Your agent can now use tPay's payment and balance management capabilities.

### Asynchronous Usage (Advanced)

For high-performance applications, you can use the asynchronous API:

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
    
    # Create agents asynchronously
    agent_data = await tpay.async_create_agent(
        name="Async Agent",
        description="High-performance agent"
    )
    
    # Use AsyncTPayAgent for non-blocking operations
    async_agent = tpay.AsyncTPayAgent()
    
    # Concurrent operations for better performance
    results = await asyncio.gather(
        async_agent.create_payment(...),
        async_agent.get_agent_balance("agent_id"),
        tpay.async_get_agent_asset_balance("agent_id", "solana", "USDC")
    )

# Run async code
asyncio.run(main())
```

### Error Handling

The SDK provides detailed error handling:

```python
from tpay.exceptions import TPayError

try:
    # Your code here
    pass
except TPayError as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.code}")
```

## Best Practices

1. **API Key Management**
   - Store API keys securely
   - Use environment variables
   - Rotate keys regularly

2. **Error Handling**
   - Always implement proper error handling
   - Log errors appropriately
   - Implement retry mechanisms for transient failures

3. **Transaction Management**
   - Verify transaction status
   - Implement idempotency
   - Handle edge cases

4. **Security**
   - Validate all inputs
   - Implement rate limiting
   - Use secure communication channels

## Complete Documentation

For comprehensive documentation including deployment guides, async examples, and advanced usage patterns, please refer to:

📖 **[Complete Export Guide](/docs/export_guide.md)** - Detailed documentation covering:
- Installation and deployment methods
- Synchronous and asynchronous API usage
- Complete code examples
- Best practices and troubleshooting
- Agent creation and management
- Balance queries and payment processing

## API Reference

### Synchronous API
- `tpay_initialize()` - Initialize the SDK
- `create_agent()` - Create new agents
- `get_agent_asset_balance()` - Query asset balances
- `TPayAgent` class - Full agent management

### Asynchronous API
- `async_create_agent()` - Create agents asynchronously
- `async_get_agent_asset_balance()` - Query balances asynchronously  
- `AsyncTPayAgent` class - Full async agent management
- `async_make_request()` - Core async HTTP requests

For detailed API documentation and examples, see the [Export Guide](/docs/export_guide.md).

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.
