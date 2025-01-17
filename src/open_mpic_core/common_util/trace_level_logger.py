import logging
import time
from contextlib import asynccontextmanager

TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with trace capability added (if it doesn't exist).
    Use this instead of logging.getLogger() directly.
    :param name: logger name
    """
    if not hasattr(logging.Logger, 'trace'):
        def trace(self, message, *args, **kwargs):
            """
            Logs the provided message at TRACE_LEVEL.
            """
            if self.isEnabledFor(TRACE_LEVEL):
                self._log(TRACE_LEVEL, message, args, **kwargs)  # logger takes its '*args' as 'args'
        logging.Logger.trace = trace

    if not hasattr(logging.Logger, 'trace_timing'):
        @asynccontextmanager
        async def trace_timing(self, operation_name, *args, **kwargs):
            """
            Used to log the time taken for an async operation to complete. Use 'with', when timing an 'await'.
            """
            if self.isEnabledFor(TRACE_LEVEL):
                start = time.perf_counter()
                try:
                    yield
                finally:
                    elapsed = time.perf_counter() - start
                    self._log(TRACE_LEVEL, f"{operation_name} took {elapsed:.4f} seconds", args, **kwargs)
            else:
                yield
        logging.Logger.trace_timing = trace_timing

    logger = logging.getLogger(name)
    # TODO set logger level here based on environment configuration

    return logger
