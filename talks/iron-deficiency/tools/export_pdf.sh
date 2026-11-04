#!/bin/bash
# Regenerate the downloadable PDF through the deck's own print path. From anywhere:
#   talks/iron-deficiency/tools/export_pdf.sh
# Run it after any slide change. ?static leaves the date off the welcome page.
set -e
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TMP="$(mktemp -d)"
python3 -m http.server 3047 --bind 127.0.0.1 --directory "$ROOT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null; rm -rf "$TMP"' EXIT
sleep 1
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --no-pdf-header-footer \
  --user-data-dir="$TMP/profile" --virtual-time-budget=9000 --run-all-compositor-stages-before-draw \
  --print-to-pdf="$ROOT/talks/iron-deficiency/iron-deficiency-in-women.pdf" \
  "http://127.0.0.1:3047/talks/iron-deficiency/?static" >/dev/null 2>&1
ls -la "$ROOT/talks/iron-deficiency/iron-deficiency-in-women.pdf"
