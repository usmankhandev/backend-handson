from typing import Any

#  Base


class AppError(Exception):
    
    
    status_code: int = 500
    error_code: str = "INTERNAL_ERROR"
    
    def __init__(self, detail: str = "An Unexpected error occurred", **context: Any):
        self.detail = detail
        self.context = context
        super().__init__(detail)
        


# Resource Errors

class NotFoundError(AppError):
    status_code = 404
    error_code = "NOT_FOUND"
    
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            detail=f"{resource} with identifier '{identifier}' was not found.",
            resource=resource,
            identifier=identifier,
        )
        

class PostNotFoundError(NotFoundError):
    def __init__(self, post_id: int):
        super().__init__(resource="Post", identifier=post_id)
        

class ValidationError(AppError):
    status_code = 422
    error_code = "VALIDATION_ERROR"


class ConflictError(AppError):
    status_code = 409
    error_code = "CONFLICT_ERROR"
    
class UnAuthorizedError(AppError):
    status_code = 401
    error_code = "UNAUTHORIZED_ERROR"
    
    def __init__(self, detail: str = "Authentication Required"):
        super().__init__(detail=detail)
        
        

# OLLAMA Errors


class LLMError(AppError):
    
    status_code = 502
    error_code = "LLM_ERROR"
    
    def __init__(self, detail: str = "Error communicating with LLM service"):
        super().__init__(detail=detail)
        

class OllamaUnavailbleError(LLMError):
    error_code = "LLM_UNAVAILABLE"
    
    def __init__(self, detail: str = "LLM Service is currently unavailable"):
        super().__init__(detail=detail)
        
    

class OllamaTimeoutError(LLMError):
    error_code = "LLM_TIMEOUT"
    status_code = 504
    
    def __init__(self, timeout_seconds: float = 0):
        super().__init__(
            detail = f"LLM Service timed out after {timeout_seconds} seconds"
            timeout_seconds = timeout_seconds
        )

class LLMGenerationError(LLMError):
    error_code = "LLM_GENERATION_ERROR"
    
    def __init__(self, detail: str = "LLM failed to generate a response"):
        super().__init__(detail=detail)


# ─────────────────────────────────────────────
#  Database Errors
# ─────────────────────────────────────────────
 
class DatabaseError(AppError):
    status_code = 503
    error_code = "DATABASE_ERROR"
 
    def __init__(self, detail: str = "A database error occurred. Please try again."):
        super().__init__(detail=detail)
 
 
class DatabaseConnectionError(DatabaseError):
    error_code = "DATABASE_UNAVAILABLE"
 
    def __init__(self):
        super().__init__(detail="Unable to connect to the database. Please try again shortly.")
 
 
class DatabaseIntegrityError(DatabaseError):
    error_code = "DATABASE_INTEGRITY_ERROR"
    status_code = 409
 