# TPay Python SDK

TPay 是一个简单易用的支付处理 SDK，用于与 TLedger 支付系统进行集成。

## 安装

```bash
pip install tpay
```

## 快速开始

```python
from tpay import TLedgerAPI

# 初始化 API 客户端
api = TLedgerAPI(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# 创建支付
payment = api.create_payment(
    amount=100,
    currency="USD",
    description="Test payment"
)

# 获取支付状态
status = api.get_payment_status(payment.id)

# 等待支付完成
success = api.wait_for_payment_success(payment.id)
```

## 配置

在使用 SDK 之前，您需要设置以下环境变量：

- `TLEDGER_API_KEY`: 您的 API 密钥
- `TLEDGER_API_SECRET`: 您的 API 密钥
- `TLEDGER_API_URL`: API 端点 URL（可选，默认为生产环境 URL）

## 功能特性

- 创建支付
- 查询支付状态
- 等待支付完成
- 自动重试机制
- 完整的错误处理

## 文档

详细的文档请访问 [https://docs.tledger.com/tpay-python](https://docs.tledger.com/tpay-python)

## 许可证

MIT License 