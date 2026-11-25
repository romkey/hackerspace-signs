---
name: make-sign
description: Make a printable sign, label, table tent or poster for PDX Hackerspace (CTRL-H) following the house design language. Use for any request like "make a sign for the laser cutter", "door reminder", "table numbers", "recycling sign", "volunteer list".
---

# Make a CTRL-H sign

1. **Read `DESIGN.md`** (at least §4 families, §6 layout, §7 whimsy, §8 voice and §8.1 AI tells) if it isn't already in context.
2. **Pin down the content.** What is the one thing the reader must do? Who reads it, and where (door, machine, bin, table)? Size and orientation (default: US Letter portrait). If the user didn't say, pick sensible defaults and say so.
3. **Pick the family** (`safety`, `tools`, `house`, `green`, `wayfinding`, `community`). It sets the accent colour and whimsy level.
4. **Write the copy first** (DESIGN.md §8): title of 1–5 words, verb first, at most 5 bullets, one "why" line, numbers in mono. Cut until it's terse.
   Then check it against **§8.1 (No AI tells)**: no em dashes, no `&mdash;`, no semicolons, no emoji or dingbats, no "not just X but Y", no rule-of-three padding, no "simply / ensure / seamless / crucial", no sign-off pleasantries. Read it aloud. If it sounds like an assistant being helpful, rewrite it shorter. <!-- house-style: ignore -->
5. **Pick at most one critter** that fits the message (sasquatch = house/strength, alien = newcomers/outside, goggled sasquatch = safety only, LED/resistor = tools and wayfinding). Optional 1–2 word Silkscreen bubble.
6. **Build it:** `mkdir -p signs/<topic>`, copy `templates/sign-template.html`, fix the relative paths (`../../brand/...`), set `data-family`, fill in the content. Use only the classes in `templates/sign.css`. If a genuinely new component is needed, add it to `sign.css` (tokens only, no raw hex), and document it in DESIGN.md.
7. **Render:** `tools/render.sh signs/<topic>/*.html`, then **read the PNG**. Fix overflow, overlap, text off the page, or anything that fails the DESIGN.md §10 checklist. Re-render.
8. **Record it:** add a row to the Signs table in README.md.
9. Report the PDF path(s) to the user and note any assumptions (wording, which side of a door, etc.).

Paired signs (two sides of a door, a set of table numbers, a set of bins) share one layout and
differ only in their words. Generate them from one template so they stay in sync.
