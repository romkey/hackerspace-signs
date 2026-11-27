#!/usr/bin/env python3
"""Write a QR code for a sign as an SVG, in sign ink on a clear background.

    python3 tools/make_qr.py <url> <out.svg>

Needs segno (pip install segno). Uses error correction level M and the standard
4-module quiet zone, so print it no smaller than about 0.8 in across. The SVG is
generated: to change it, run this again with the new URL rather than editing it.
"""
import sys

import segno

INK = "#16181D"  # --hs-ink in brand/tokens.css


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    url, out = sys.argv[1], sys.argv[2]
    qr = segno.make(url, error="m", micro=False)
    qr.save(out, kind="svg", dark=INK, light=None, border=4, scale=1,
            xmldecl=False, svgns=True, title=url, nl=True, omitsize=True)
    print(f"wrote {out} ({qr.version}, {qr.symbol_size()[0]} modules with quiet zone)")


if __name__ == "__main__":
    main()
