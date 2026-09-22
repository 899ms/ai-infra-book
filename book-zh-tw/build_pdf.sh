#!/usr/bin/env bash
# 建置繁體中文版 PDF。完整說明見 README.md。
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/build_pdf.py" "$@"
