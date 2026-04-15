class BaseAPIException(Exception):
    """Base class for API exceptions."""
    status_code: int = 400
    detail: str = "An error occurred."
    
    error_code: str = "INTERNAL_ERROR"
    