#!/bin/sh
# Render sign HTML files to PDF (for printing) and PNG (for previews).
#   tools/render.sh signs/kitchen-door/*.html
# Output goes next to each source file. Needs Google Chrome; fonts load from Google Fonts.
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
# How long to let webfonts and layout settle, in ms. CI raises this.
BUDGET="${BUDGET:-5000}"
for f in "$@"; do
  abs="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
  base="${abs%.html}"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget="$BUDGET" \
    --print-to-pdf="$base.pdf" "file://$abs" 2>/dev/null
  # Letter at 96px/in. Landscape signs ("landscape" in the sign's class list) get 11x8.5.
  size=816,1056
  grep -Eq 'class="sign( [a-z]+)* landscape|class="sign landscape' "$abs" && size=1056,816
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget="$BUDGET" \
    --window-size="$size" --default-background-color=00000000 \
    --screenshot="$base.png" "file://$abs" 2>/dev/null
  echo "rendered $base.pdf $base.png"
done
