# app/core/errors.py
from typing import Optional, Any

class TojikaiException(Exception):
    """Base exception for all Tojikai platform errors"""
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        details: Optional[dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(TojikaiException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, "VALIDATION_ERROR", 400, details)


class AuthenticationError(TojikaiException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR", 401)


class AuthorizationError(TojikaiException):
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, "AUTHORIZATION_ERROR", 403)


class NotFoundError(TojikaiException):
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with id {identifier} not found"
        super().__init__(message, "NOT_FOUND", 404)


class ConflictError(TojikaiException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, "CONFLICT", 409, details)


class QuotaExceededError(TojikaiException):
    def __init__(self, message: str = "Quota exceeded", details: Optional[dict] = None):
        super().__init__(message, "QUOTA_EXCEEDED", 429, details)


class PaymentError(TojikaiException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, "PAYMENT_ERROR", 402, details)


class ExternalServiceError(TojikaiException):
    def __init__(self, service: str, message: str):
        msg = f"External service {service} error: {message}"
        super().__init__(msg, "EXTERNAL_SERVICE_ERROR", 502)


class AIGenerationError(TojikaiException):
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, "AI_GENERATION_ERROR", 500, details)
