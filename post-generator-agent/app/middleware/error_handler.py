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
    OllamaUnavailableError,
)

from app.utils.logging import get_logger

logger = get_logger(__name__)

# Response Helpers

# _ highlights that this is an internal helper function and should not be used outside of this module

def _error_response(
    status_code: int,
    error_code: str,
    message: str,
    request_id: str = None,
    details: dict = None,
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

def _ms(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 2)



# Middleware

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    
    def __init__(self, app: ASGIApp, debug: bool = False):
        super().__init__(app)
        self.debug = debug # when true, returns detailed error messages in the response for easier debugging during development
        
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        
        request_id = str(uuid.uuid4())
        start = time.time()
        
        request.state.request_id = request_id
        
        try:
            response = await call_next(request)
            return response
        
        except AppError as exc:
            duration_ms = _ms(start)
            logger.error(
                exc.error_code,
                extra = {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": exc.status_code,
                    "error_code": exc.error_code,
                    "detail": exc.detail,
                    "exc_type": type(exc).__name__,
                    "duration_ms": duration_ms,
                    **exc.context,
                }
            )
            return _error_response(exc.status_code, exc.error_code, exc.detail, request_id)
        
        except RequestValidationError as exc:
            duration_ms = _ms(start)
            logger.error(
                "validation_error",
                extra = {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 422,
                    "error_code": "validation_error",
                    "detail": exc.errors(),
                    "exc_type": type(exc).__name__,
                    "duration_ms": duration_ms,
                }
            )
            return JSONResponse(
                status_code=422,
                content={
                    "success": False,
                    "error": {
                        "code": "validation_error",
                        "message": "Request validation failed",
                        "details": exc.errors()
                    },
                    "request_id": request_id
                }
            )
            
        except IntegrityError as exc:
            duration_ms = _ms(start)
            mapped = DatabaseIntegrityError()
            logger.error(
                "Database_Integrity_Error",
                extra = {
                    "request_id": request_id,
                    "path": request.url.path,
                    "status_code": mapped.status_code,
                    "error_code": mapped.error_code,
                    "pg_detail": str(exc.orig),
                    "duration_ms": duration_ms
                },
                exc_info = self.debug
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)
        
        except OperationalError as exc:
            duration_ms = _ms(start)
            mapped = DatabaseConnectionError()
            logger.critical(
                "DATABASE_UNAVAILABLE",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "status_code": mapped.status_code,
                    "error_code": mapped.error_code,
                    "pg_detail": str(exc.orig),
                    "duration_ms": duration_ms,
                },
                exc_info=self.debug,
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)
        
        except SQLAlchemyError as exc:
            duration_ms = _ms(start)
            mapped = DatabaseError()
            logger.error(
                "DATABASE_ERROR",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "status_code": mapped.status_code,
                    "error_code": mapped.error_code,
                    "duration_ms": duration_ms,
                },
                exc_info=self.debug,
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)

        except httpx.ConnectError:
            duration_ms = _ms(start)
            mapped = OllamaUnavailableError()
            logger.error(
                "LLM_UNAVAILABLE",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "status_code": mapped.status_code,
                    "error_code": mapped.error_code,
                    "duration_ms": duration_ms,
                },
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)

        except httpx.TimeoutException as exc:
            duration_ms = _ms(start)
            mapped = OllamaTimeoutError(timeout_seconds=duration_ms / 1000)
            logger.error(
                "LLM_TIMEOUT",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "status_code": mapped.status_code,
                    "error_code": mapped.error_code,
                    "duration_ms": duration_ms,
                },
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)
        
        except httpx.HTTPStatusError as exc:
            duration_ms = _ms(start)
            mapped = OllamaUnavailableError(
                detail=f"AI model service returned an unexpected status: {exc.response.status_code}."
            )
            logger.error(
                "LLM_HTTP_ERROR",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "ollama_status": exc.response.status_code,
                    "status_code": mapped.status_code,
                    "duration_ms": duration_ms,
                },
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)

        except AsyncTimeoutError:
            duration_ms = _ms(start)
            mapped = OllamaTimeoutError(timeout_seconds=duration_ms / 1000)
            logger.error(
                "LLM_TIMEOUT",
                extra={
                    "request_id": request_id,
                    "path": request.url.path,
                    "status_code": mapped.status_code,
                    "duration_ms": duration_ms,
                },
            )
            return _error_response(mapped.status_code, mapped.error_code, mapped.detail, request_id)
        
        except Exception as exc:
            duration_ms = _ms(start)
            tb = traceback.format_exc()
            logger.critical(
                "UNHANDLED_EXCEPTION",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "error_code": "INTERNAL_ERROR",
                    "exc_type": type(exc).__name__,
                    "duration_ms": duration_ms,
                    "traceback": tb,
                },
            )
            # In production: generic message. In debug: include detail.
            message = str(exc) if self.debug else "An internal server error occurred. Please try again."
            return _error_response(500, "INTERNAL_ERROR", message, request_id)
 






