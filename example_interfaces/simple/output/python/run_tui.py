#!/usr/bin/env python3
"""Launch the SimpleIPC TUI."""

import logging
from simpleipc.tui.app import SimpleIPCApp


def main():
    """Run the TUI application."""
    # Remove all existing handlers and configure logging to file
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set up file handler
    file_handler = logging.FileHandler("/tmp/jacob.log", mode="a")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)

    logging.debug("Starting SimpleIPC TUI application.")

    app = SimpleIPCApp()
    app.run()


if __name__ == "__main__":
    main()
