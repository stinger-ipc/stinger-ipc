#!/bin/bash

# Clean all generated output directories from example interfaces
# Removes all directories matching: example_interfaces/*/output*/*

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Cleaning all generated output from example_interfaces..."

# Find and delete all output directories
find example_interfaces -maxdepth 2 -type d -name "output*" -exec rm -rfv {} + 2>/dev/null || true

echo "Done. All output directories have been removed."
