#!/usr/bin/env python3
"""
Build the table ID signs. Edit TABLES, then:

    python3 signs/tables/build_tables.py
    tools/render.sh signs/tables/*.html

Writes one HTML per table, all-tables.html (every table, one per page, for
printing in one go) and a resistor SVG per coordinate. Symbols are pixel sprites
from brand/illustrations (add new ones in tools/build_brand.py).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build_brand import RESISTOR_BANDS, resistor_svg  # noqa: E402

# coordinate, name, symbol sprite (brand/illustrations/<symbol>.svg)
TABLES = [
    ("1-1", "Ninja", "ninja"),
    ("1-3", "Kitty", "kitty"),
    ("2-1-1", "Doggie", "doggie"),
    ("2-2-1", "Pirate", "pirate"),
    ("2-3-1", "Robot", "robot"),
    ("2-3-2", "Llama", "llama"),
    ("2-3-3", "Alien", "alien"),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="../../brand/tokens.css">
<link rel="stylesheet" href="../../templates/sign.css">
<style>.trail {{ background-image: url("../../brand/patterns/rainbow-trail.svg"); }}</style>
</head>
<body>
"""

SIGN = """<main class="sign" data-family="wayfinding">
  <header class="sign-header">
    <img class="mark" src="../../brand/logo/ctrlh-mark-rainbow.svg" alt="CTRL-H">
    <div class="kicker">Table<small>PDX Hackerspace</small></div>
    <div class="accent-hex"></div>
  </header>
  <div class="trail"></div>

  <section class="sign-body table-id">
    <h1 class="table-coord">{coord}</h1>
    <img class="table-symbol" src="../../brand/illustrations/{symbol}.svg" alt="">
    <p class="table-name">{name}</p>
    <div class="resistor-code">
      <img src="resistor-{coord}.svg" alt="">
      <span>{coord} in resistor colours</span>
    </div>
  </section>

  <footer class="sign-footer">
    <img class="mark" src="../../brand/logo/ctrlh-mark.svg" alt="">
    <span>PDX Hackerspace &middot; CTRL-H</span>
    <span class="right">wayfinding / table-{coord}</span>
  </footer>
</main>
"""
FOOT = "</body>\n</html>\n"


def main():
    pages = []
    for coord, name, symbol in TABLES:
        assert os.path.exists(os.path.join(ROOT, "brand/illustrations", f"{symbol}.svg")), symbol
        bands = [RESISTOR_BANDS[int(d)] for d in coord.split("-")]
        with open(os.path.join(HERE, f"resistor-{coord}.svg"), "w") as f:
            f.write(resistor_svg(bands).strip() + "\n")
        sign = SIGN.format(coord=coord, name=name, symbol=symbol)
        pages.append(sign)
        with open(os.path.join(HERE, f"table-{coord}.html"), "w") as f:
            f.write(HEAD.format(title=f"Table {coord}: {name}") + sign + FOOT)
        print(f"wrote table-{coord}.html")
    with open(os.path.join(HERE, "all-tables.html"), "w") as f:
        f.write(HEAD.format(title="All tables") + "\n".join(pages) + FOOT)
    print("wrote all-tables.html")


if __name__ == "__main__":
    main()
