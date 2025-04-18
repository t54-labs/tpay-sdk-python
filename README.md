# tPay SDK for Python

## Product Introduction

Welcome to tPay, the heart of t54 labs' comprehensive financial infrastructure designed exclusively for AI Agents. Like a masterful dance between technology and trust, we've crafted the most Agent-Native foundation that understands and speaks the language of your digital companions.

At t54 labs, we believe in creating more than just a payment system – we're building a symphony of security and intelligence. Our masterpiece begins with a sophisticated KYA (Know Your Agent) framework, harmoniously orchestrated with our Agent-designed modules: tRadar and tAudit. Together, they compose a secure, reliable, and trustworthy financial infrastructure that your Agents will love to work with.

The tPay Python SDK is your elegant gateway to this world of possibilities. Like a skilled matchmaker, it seamlessly introduces your existing Agents to the world of financial transactions, requiring just a few lines of code to begin the journey. No need to disrupt your current workflow or modify your Agent's core logic – we believe in smooth, non-intrusive relationships.

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

1. **Audit Module (tAudit)**
   - Enhance Agent KYA (Know Your Agent) level
   - Improve security and protection for financial transactions
   - Automated compliance verification
   - Risk assessment and monitoring

2. **Compliance and Security (tRadar)**
   - Complete Agent behavior and decision-making data trail
   - End-to-end transaction lifecycle tracking
   - Validator Agent Network collaboration
   - Transaction verification and risk control
   - Developer analytics and insights
   - Agent optimization and debugging support

3. **Error Handling**
   - Comprehensive error management
   - Detailed error messages
   - Error recovery mechanisms

## Installation

```bash
pip install tpay
```

## Requirements

### Environment
- Python 3.8 or higher
- Operating System: Windows, macOS, or Linux

### Dependencies
The SDK has the following main dependencies:
- `requests>=2.31.0`: For HTTP requests
- `pydantic>=2.5.0`: For data validation and settings management
- `python-dotenv>=1.0.0`: For environment variable management
- `openai>=1.0.0`: For OpenAI API integration (optional, only if using OpenAI features)

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
from tpay import create_payment_tool, create_balance_tool

# Create payment tool
payment_tool = create_payment_tool()

# Create balance tool
balance_tool = create_balance_tool()

# Define tools for your agent
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_payment",
            "description": "Create a payment transaction between agents",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"},
                    "amount": {"type": "number"},
                    "recipient_agent_id": {"type": "string"},
                    "currency": {"type": "string", "default": "USDT"},
                    "settlement_network": {"type": "string", "default": "solana"}
                },
                "required": ["agent_id", "amount", "recipient_agent_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_agent_balance",
            "description": "Query agent's account balance",
            "parameters": {
                "type": "object",
                "properties": {
                    "agent_id": {"type": "string"}
                },
                "required": ["agent_id"]
            }
        }
    }
]
```

2. **Add Tools to Your Agent**

Simply add the tools to your existing agent's tool list:

```python
# Example with OpenAI's client
from openai import OpenAI

client = OpenAI(
    api_key="your_openai_api_key",
    model="gpt-4-turbo-preview",
    tools=tools,  # Add our tools to your existing tools
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

## Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 