import logging
import json
from typing import Any, Dict
from datetime import datetime, timezone

# Base setup for structured logging
logging.basicConfig(level=logging.INFO)

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def _log(self, level: int, event_type: str, message: str, context: Dict[str, Any]) -> None:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "message": message,
            "context": context
        }
        self.logger.log(level, json.dumps(log_entry))

    def info(self, event_type: str, message: str, context: Dict[str, Any] = None) -> None:
        self._log(logging.INFO, event_type, message, context or {})

    def error(self, event_type: str, message: str, context: Dict[str, Any] = None) -> None:
        self._log(logging.ERROR, event_type, message, context or {})

    def warning(self, event_type: str, message: str, context: Dict[str, Any] = None) -> None:
        self._log(logging.WARNING, event_type, message, context or {})

def get_workflow_logger() -> StructuredLogger:
    return StructuredLogger("syntra.workflow")

def get_agent_logger() -> StructuredLogger:
    return StructuredLogger("syntra.agent")

def get_tool_logger() -> StructuredLogger:
    return StructuredLogger("syntra.tool")
