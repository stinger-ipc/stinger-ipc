#!/usr/bin/env python3
"""Launch the WeatherIPC TUI."""

import argparse
import logging
from weatheripc.tui.app import WeatherIPCApp


def main():
    """Run the TUI application."""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="WeatherIPC TUI Application")
    parser.add_argument(
        "--cafile",
        help="Path to CA certificate file for TLS certificate validation",
    )
    parser.add_argument(
        "--capath",
        help="Path to directory containing CA certificates for TLS",
    )
    parser.add_argument(
        "--cert",
        help="Path to client certificate file for TLS client authentication",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification (not recommended for production)",
    )
    args = parser.parse_args()

    # Remove all existing handlers and configure logging to file
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set up file handler
    file_handler = logging.FileHandler("/tmp/jacob.log", mode="a")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.ERROR)

    logging.debug("Starting WeatherIPC TUI application.")

    app = WeatherIPCApp()
    # Store TLS configuration in the app
    app.tls_config = {
        "cafile": args.cafile,
        "capath": args.capath,
        "cert": args.cert,
        "insecure": args.insecure,
    }
    app.run()


if __name__ == "__main__":
    main()
