"""Custom exceptions for the health diagnosis application."""


class HealthSenseError(Exception):
    """Base exception for HealthSense application."""
    pass


class GeminiAPIError(HealthSenseError):
    """Exception raised when Gemini API call fails."""
    pass


class ConfigurationError(HealthSenseError):
    """Exception raised when configuration is invalid."""
    pass


class ValidationError(HealthSenseError):
    """Exception raised when input validation fails."""
    pass


class RAGError(HealthSenseError):
    """Exception raised when RAG engine fails."""
    pass

