"""Structured console logging configuration."""

import json
import logging
import sys
import time


class JsonFormatter(logging.Formatter):
    """Render records as one JSON object per line."""

    converter = time.gmtime

    def format(self, record: logging.LogRecord) -> str:
        values = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(values, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=numeric_level, handlers=[handler], force=True)
