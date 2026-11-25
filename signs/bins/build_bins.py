#!/usr/bin/env python3
"""
Build the four bin labels (garbage, mixed recycling, compost, glass).
Edit BINS below, then:

    python3 signs/bins/build_bins.py
    tools/render.sh signs/bins/*.html

Writes one landscape HTML per bin plus all-bins.html (all four, one per page).
Sorting rules follow the City of Portland commercial requirements. The URLs are
in README.md. Letter landscape, meant to be laminated and taped to the bin.

Note on cost: Portland does NOT bill commercial garbage by weight. Businesses
negotiate rates with a permitted private hauler, priced on container size and
pickup frequency, so the saving from sorting is a smaller or less frequent
garbage pickup. Don't put "by the pound" on these signs.
"""
import os

# The City of Portland requires only SPECIFIC items to be bagged (ENN-2.06 has no
# blanket rule, and neither does portland.gov/bps/garbage-recycling/garbage). Some
# haulers add one in their own contract. Set this True if ours does.
BAG_EVERYTHING = False

HERE = os.path.dirname(os.path.abspath(__file__))

GARBAGE_NOTE = (
    "City rule: <b>no recyclables in the garbage.</b> "
    + ("<b>Bag everything</b> before it goes in. "
       if BAG_EVERYTHING else
       "Bag first: broken glass, ceramics, shredded paper, ashes, "
       "sawdust, packaging peanuts, pet waste. Seal oil and grease. ")
    + "Everything on the right needs a drop-off or another bin."
)

# slug, footer sign id, kicker, bin colour token, bin chip name, title, critter,
# bubble,
# yes-list, no-list
BINS = [
    dict(
        slug="garbage", sign_id="garbage-gray",
        kicker="Garbage",
        bin_token="--hs-steel",
        bin_name="Gray bin",
        title="Sort it first.",
        critter="sasquatch", bubble="HEAVE",
        yes=[
            "Plastic bags, wrap and film",
            "Foam, peanuts, air pillows",
            "Loose lids and bottle caps",
            "Paper towels, napkins, tissues",
            "Take-out boxes, cups, cutlery",
        ],
        no=[
            "Batteries of any kind",
            "Electronics, cords, chargers",
            "CFL tubes and bulbs",
            "Paint, solvents, chemicals",
            "Big piles of food scraps",
        ],
        sort_note=GARBAGE_NOTE,
    ),
    dict(
        slug="recycling", sign_id="recycling-blue",
        kicker="Mixed recycling",
        bin_token="--hs-blue",
        bin_name="Blue bin",
        title="Empty, dry, loose.",
        critter="alien", bubble="HUH?",
        yes=[
            "Flattened cardboard, paper",
            "Metal cans, balled-up foil",
            "Plastic bottles, jugs and tubs",
            "Cartons, clean pizza boxes",
            "Scrap metal under <span class=\"mono\">18 in</span>",
        ],
        no=[
            "Glass (use the yellow bin)",
            "Plastic bags, wrap, rings",
            "Shredded paper",
            "Cups, clamshells, foam",
            "Anything under <span class=\"mono\">2 in</span> square",
        ],
        sort_note="Tip it in loose. One bagged load gets the whole cart pulled as garbage. Caps on only if they screw on. Ball foil up baseball-size. Scrap metal under <span class=\"mono\">10 lb</span>.",
    ),
    dict(
        slug="compost", sign_id="compost-green",
        kicker="Compost",
        bin_token="--hs-green",
        bin_name="Green bin",
        title="Food scraps only.",
        critter="spacecat", bubble="NOM",
        yes=[
            "Any food, plate scrapings",
            "Meat, bones, dairy, bread",
            "Grounds, peels, eggshells",
            "Coffee filters, tea bags",
            "Liners: <b>BPI-certified only</b>",
        ],
        no=[
            "Yard debris, leaves, prunings",
            "Napkins, food-soiled paper",
            "Anything &ldquo;compostable&rdquo;",
            "Cups, bowls, cutlery, trays",
            "Grease, oil, standing liquid",
        ],
        sort_note="Business compost is food only, not the same as your green bin at home. &ldquo;Biodegradable&rdquo; and &ldquo;made from plants&rdquo; are garbage here, and so are napkins.",
    ),
    dict(
        slug="glass", sign_id="glass-yellow",
        kicker="Glass",
        bin_token="--hs-yellow",
        bin_name="Yellow bin",
        title="Bottles and jars only.",
        critter="saucer", bubble="CLINK",
        yes=[
            "Glass bottles, any colour",
            "Glass jars, any colour",
            "Labels can stay on",
            "Rinsed out, <b>lids off</b>",
        ],
        no=[
            "<b>Broken glass of any kind</b>",
            "Lids, caps and corks",
            "Drinking glasses and Pyrex",
            "Dishware, ceramics, vases",
            "Window glass, mirrors, bulbs",
        ],
        sort_note="<b>Broken glass cuts the crew who empty this bin.</b> Bag it and put it in the gray bin. Same for everything else on the right. The city requires this bin to be collected separately from the blue one.",
    ),
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

SIGN = """<main class="sign landscape" data-family="green" style="--bin: var({bin_token});">
  <header class="sign-header">
    <img class="mark" src="../../brand/logo/ctrlh-mark-rainbow.svg" alt="CTRL-H">
    <div class="kicker">{kicker}<small>North Portland &middot; business service</small></div>
    <div class="bin-badge">
      <div class="swatch"></div>
      <p class="bin-name">{bin_name}</p>
    </div>
  </header>
  <div class="trail"></div>

  <section class="sign-body">
    <div class="bin-head">
      <h1 class="title">{title}</h1>
      <div class="accent-rule"></div>
    </div>

    <div class="sort-cols">
      <div class="sort-col yes">
        <div class="sort-head">
          <img src="../../brand/illustrations/led-green.svg" alt="">
          <span>Yes: in here</span>
        </div>
        <ul class="hex-list">
{yes_items}
        </ul>
      </div>
      <div class="sort-col no">
        <div class="sort-head">
          <img src="../../brand/illustrations/led-red.svg" alt="">
          <span>No: keep out</span>
        </div>
        <ul class="hex-list">
{no_items}
        </ul>
      </div>
    </div>

    <p class="sort-note">{sort_note}</p>

    <div class="row-end">
      <div class="note">
        <img src="../../brand/illustrations/led-amber.svg" alt="">
        <span>Bins go out Wednesday night.
          <small>Back inside by Thursday morning. They can&rsquo;t be left in the street.</small>
        </span>
      </div>
      <div class="critter">
        <span class="bubble">{bubble}</span>
        <img src="../../brand/illustrations/{critter}.svg" alt="">
      </div>
    </div>
  </section>

  <footer class="sign-footer">
    <img class="mark" src="../../brand/logo/ctrlh-mark.svg" alt="">
    <span>PDX Hackerspace &middot; CTRL-H</span>
    <span class="right">bins / {sign_id}</span>
  </footer>
</main>
"""

TAIL = "</body>\n</html>\n"


def items(rows):
    return "\n".join("          <li>%s</li>" % r for r in rows)


def render(bin_):
    return SIGN.format(
        yes_items=items(bin_["yes"]),
        no_items=items(bin_["no"]),
        **{k: v for k, v in bin_.items() if k not in ("yes", "no")},
    )


def main():
    everything = []
    for b in BINS:
        title = "%s bin: %s" % (b["bin_name"].split()[0], b["kicker"])
        body = render(b)
        everything.append(body)
        with open(os.path.join(HERE, "%s.html" % b["slug"]), "w") as fh:
            fh.write(HEAD.format(title=title) + body + TAIL)
        print("wrote signs/bins/%s.html" % b["slug"])
    with open(os.path.join(HERE, "all-bins.html"), "w") as fh:
        fh.write(HEAD.format(title="CTRL-H bin labels") + "\n".join(everything) + TAIL)
    print("wrote signs/bins/all-bins.html")


if __name__ == "__main__":
    main()
