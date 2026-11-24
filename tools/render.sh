#!/bin/sh
# Render sign HTML files to PDF (for printing) and PNG (for previews).
#   tools/render.sh signs/kitchen-door/*.html
# Output goes next to each source file. Needs Google Chrome; fonts load from Google Fonts.
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
for f in "$@"; do
  abs="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
  base="${abs%.html}"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=5000 \
    --print-to-pdf="$base.pdf" "file://$abs" 2>/dev/null
  # 8.5x11in at 96px/in; landscape signs get cropped, use the PDF for those
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=5000 \
    --window-size=816,1056 --default-background-color=00000000 \
    --screenshot="$base.png" "file://$abs" 2>/dev/null
  echo "rendered $base.pdf $base.png"
done
