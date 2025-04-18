"""
TPay SDK Exceptions Module
"""

class TPayError(Exception):
    """Base exception for TPay SDK"""
    pass

class TPayAPIError(TPayError):
    """Exception raised for API errors"""
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class TPayConfigError(TPayError):
    """Exception raised for configuration errors"""
    pass

class TPayTimeoutError(TPayError):
    """Exception raised for timeout errors"""
    pass
