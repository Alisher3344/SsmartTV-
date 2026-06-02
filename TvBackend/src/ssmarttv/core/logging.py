"""Structured JSON logging with a per-request correlation id.

The request id is stored in a ContextVar set by the RequestIdMiddleware
(see ssmarttv.main) so every log line emitted while handling a request carries
the same ``request_id``.
"""
import json
import logging
from contextvars import ContextVar

request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)

_RESERVED = frozenset(
    logging.makeLogRecord({}).__dict__.keys() | {"message", "asctime", "taskName"}
)


class JsonFormatter(logging.Formatter):
    """Render log records as single-line JSON for log aggregators."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
        }
        request_id = request_id_ctx.get()
        if request_id:
            payload["request_id"] = request_id
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        # Surface any structured extras passed via logger.*(..., extra={...}).
        for key, value in record.__dict__.items():
            if key not in _RESERVED and not key.startswith("_"):
                payload[key] = value
        return json.dumps(payload, default=str, ensure_ascii=False)


def configure_logging(level: str = "INFO", json_output: bool = True) -> None:
    handler = logging.StreamHandler()
    if json_output:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")
        )
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level.upper())
    # uvicorn keeps its own handlers; route everything through ours.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).handlers[:] = []
        logging.getLogger(name).propagate = True
