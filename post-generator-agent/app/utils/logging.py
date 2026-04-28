import json
import logging
from os import name
import sys
from datetime import datetime, timezone

class JSONFormatter(logging.Formatter):
    
    LEVEL_MAP = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO",
        logging.WARNING: "WARNING",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRITICAL"
    }
    
    def format(self, record: logging.LogRecord) -> str: 
        
        payload: dict = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": self.LEVEL_MAP.get(record.levelno, "UNKNOWN"),
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        for key, value in record.__dict__.items():
            if key not in {
                "args", "created", "exc_info", "exc_text", "filename",
                "funcName", "levelname", "levelno", "lineno", "message",
                "module", "msecs", "msg", "name", "pathname", "process",
                "processName", "relativeCreated", "stack_info", "thread",
                "threadName",
            }:
                payload[key] = value
        
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(payload)
    
    def setup_logging(self, level=logging.INFO):
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        
        root = logging.getLogger()
        root.setLevel(getattr(logging, level.upper(), logging.INFO))
        root.handlers.clear()
        root.addHandler(handler)
        
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        
    
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)
    