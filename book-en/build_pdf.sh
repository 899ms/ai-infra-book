#!/usr/bin/env bash
# Build the English edition as a single PDF. See build_pdf.py for options.
# Usage: bash book-en/build_pdf.sh [--output-dir DIR] [--source-ref SHA]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/build_pdf.py" "$@"
