"""Logs viewer screen for debugging."""

import logging
from collections import deque
from typing import Deque
from textual.app import ComposeResult  # typing: ignore
from textual.screen import Screen  # typing: ignore
from textual.widgets import Header, Footer, RichLog  # typing: ignore
from textual.containers import Container  # typing: ignore


class LogCapture(logging.Handler):
    """Custom logging handler that captures log records in memory."""

    def __init__(self, max_records: int = 1000):
        """Initialize the log capture handler.
        
        Args:
            max_records: Maximum number of log records to keep in memory
        """
        super().__init__()
        self.records: Deque[logging.LogRecord] = deque(maxlen=max_records)
        self.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%H:%M:%S"
            )
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Capture a log record."""
        self.records.append(record)


# Global log capture handler
_log_handler = LogCapture()


def get_log_handler() -> LogCapture:
    """Get the global log capture handler."""
    return _log_handler


def install_log_handler() -> None:
    """Install the log capture handler to the root logger."""
    root_logger = logging.getLogger()
    if _log_handler not in root_logger.handlers:
        root_logger.addHandler(_log_handler)


class LogsScreen(Screen):
    """Screen for viewing application logs."""

    CSS = """
    LogsScreen {
        align: center top;
    }
    
    #logs_container {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    
    RichLog {
        width: 100%;
        height: 100%;
        border: solid $primary;
    }
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Close"),
        ("c", "clear_logs", "Clear"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the logs screen widgets."""
        yield Header()
        with Container(id="logs_container"):
            yield RichLog(highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        """Load existing logs when screen mounts."""
        self.title = "Application Logs"
        self._refresh_logs()

    def _refresh_logs(self) -> None:
        """Refresh the log display with all captured logs."""
        rich_log = self.query_one(RichLog)
        rich_log.clear()
        
        log_handler = get_log_handler()
        for record in log_handler.records:
            formatted = log_handler.format(record)
            
            # Color code by level
            if record.levelno >= logging.ERROR:
                rich_log.write(f"[bold red]{formatted}[/]")
            elif record.levelno >= logging.WARNING:
                rich_log.write(f"[bold yellow]{formatted}[/]")
            elif record.levelno >= logging.INFO:
                rich_log.write(f"[bold blue]{formatted}[/]")
            else:
                rich_log.write(formatted)

    def action_clear_logs(self) -> None:
        """Clear all logs."""
        log_handler = get_log_handler()
        log_handler.records.clear()
        self._refresh_logs()
        self.notify("Logs cleared")