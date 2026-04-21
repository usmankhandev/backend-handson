import time
import traceback
import uuid
import httpx
from typing import Callable
from asyncio import TimeoutError as AsyncTimeoutError
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.utils.exceptions import (
    AppError,
    DatabaseConnectionError,
    DatabaseError,
    DatabaseIntegrityError,
    OllamaTimeoutError,
    OllamaUnavailbleError,
)

from app.utils.logging import JSONFormatter

logger = get_logger(__name__)

# Response Helpers

def _error_response(
    status_code: int,
    error_code: str,
    message: str,
    request_id: str = None,
    details: dict = None
) -> JSONResponse:
    
    payload = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
            "details": details or {}
        },
        "request_id": request_id or str(uuid.uuid4())
    }
    
    return JSONResponse(status_code=status_code, content=payload)


# Middleware




