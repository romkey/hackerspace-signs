# PDX Hackerspace (CTRL-H) Signs

[![CI](https://img.shields.io/github/actions/workflow/status/romkey/hackerspace-signs/ci.yml?branch=main&label=CI&style=flat-square)](https://github.com/romkey/hackerspace-signs/actions/workflows/ci.yml)
[![Printables](https://img.shields.io/badge/printables-latest%20CI%20build-6DB33F?style=flat-square)](https://github.com/romkey/hackerspace-signs/actions/workflows/ci.yml?query=branch%3Amain)
[![Design language](https://img.shields.io/badge/design%20language-DESIGN.md-7468C2?style=flat-square)](DESIGN.md)
[![License](https://img.shields.io/badge/license-MIT-119FD6?style=flat-square)](LICENSE)

Signs, labels and posters for PDX Hackerspace, plus the design system they share.

## Start here: [DESIGN.md](DESIGN.md)

**[DESIGN.md](DESIGN.md) is the design language.** Read it before making or changing a sign.
In short: ink header with the `^H` mark → rainbow trail → one big plain message on warm
paper → one pixel critter in its own corner → footer with the sign id.

## Layout

| Path | What |
|---|---|
| [`DESIGN.md`](DESIGN.md) | The rules: colour, type, layout, whimsy, voice, materials |
| [`brand/tokens.css`](brand/tokens.css) | Colours, fonts and spacing as CSS variables |
| [`brand/logo/`](brand/logo) | Mark and badge SVGs (generated), original line art |
| [`brand/illustrations/`](brand/illustrations) | Sasquatch, alien, saucer, sparkles, LEDs, resistors |
| [`brand/patterns/`](brand/patterns) | Rainbow trail, honeycomb |
| [`brand/mural/`](brand/mural) | Photo of the Nyan mural |
| [`brand/reference/`](brand/reference) | The badge as built: LED, metal, patch, plywood |
| [`templates/`](templates) | `sign.css` layout and `sign-template.html` starter |
| [`signs/`](signs) | Finished signs, one folder per topic (HTML source + PDF + PNG) |
| [`tools/`](tools) | `build_brand.py` regenerates brand SVGs, `render.sh` makes PDF/PNG, `lint_signs.py`, `lint_docs.py` and `check_pdfs.py` are the checks CI runs |

## Make a sign

```bash
mkdir -p signs/my-topic && cp templates/sign-template.html signs/my-topic/my-sign.html
# edit it, then:
tools/render.sh signs/my-topic/my-sign.html
```

Print the PDF at 100% (no "fit to page") on US Letter. Rendering needs Google Chrome
and an internet connection for the fonts.

If you use Claude Code here, it follows `DESIGN.md` automatically. Ask for
"a sign for X" (the `make-sign` skill).

## Checks

[CI](.github/workflows/ci.yml) runs on every push and pull request. It cannot tell you
whether a sign *looks* right, so always open the PNG for that. It does catch the mistakes
that are easy to miss.

| Check | What it catches |
|---|---|
| `python3 tools/lint_signs.py` | A sign that skips `tokens.css`/`sign.css`, has no family or an invented one, hard-codes a hex colour, points at art that isn't there, still carries template placeholder text, has no rendered PDF/PNG beside it, or is missing from the table below |
| the same lint, on the copy | The mechanical [no-AI-tells](DESIGN.md) rules on sign copy: em dashes, semicolons, emoji, `(s)` plurals, `Note:` labels, and the words we don't print |
| `python3 tools/lint_docs.py` | The dash, emoji and word rules on the repo's own writing (Markdown here and under `.claude/skills`, plus build-script docstrings), which is where the next sign gets its wording |
| `python3 tools/build_brand.py` + `git diff` | A hand-edited SVG in `brand/`. Those are generated, so edit `build_brand.py` instead |
| `build_bins.py` / `build_tables.py` + `git diff` | Sign HTML edited by hand when a build script owns it |
| `python3 tools/check_pdfs.py` | A sign that spills onto a second page (overflow), wrong paper size, wrong orientation. Needs `pypdf` |

CI also re-renders every sign from scratch in headless Chrome and attaches the whole set of
PDFs and PNGs to the run, so the current printables can be downloaded without a local Chrome
(the **printables** badge above goes there).

Run the lot locally:

```bash
python3 tools/lint_signs.py && python3 tools/lint_docs.py && python3 tools/check_pdfs.py
```

Both lints share their rule tables ([`tools/house_style.py`](tools/house_style.py)). A doc
that has to quote what it bans, the way DESIGN.md §8.1 does, wraps that part in a marker:

```markdown
<!-- house-style: ignore start -->
... text that may break the rules ...
<!-- house-style: ignore end -->
```

A single line can end with `<!-- house-style: ignore -->` instead. Code blocks, inline code,
link targets and URLs are skipped already, so a shell command or a `--hs-*` token is safe.

## License

[MIT](LICENSE). Take these signs and remix them for your own space.

Two things in here are **not** ours to relicense: the Nyan Cat artwork, which CTRL-H uses
with permission from its creator, and the photographs in [`brand/reference/`](brand/reference)
and [`brand/mural/`](brand/mural) of the space's own badge and mural. Replace the critters
with your own before you print someone else's cat.

## Signs

| Sign | Family | Files |
|---|---|---|
| Kitchen door, inside: PUSH | house | [`signs/kitchen-door/inside-push.pdf`](signs/kitchen-door/inside-push.pdf) |
| Kitchen door, outside: PULL | house | [`signs/kitchen-door/outside-pull.pdf`](signs/kitchen-door/outside-pull.pdf) |
| All door signs, one per page | house | [`signs/kitchen-door/all-door-signs.pdf`](signs/kitchen-door/all-door-signs.pdf) (rebuild with `pdfunite signs/kitchen-door/inside-push.pdf signs/kitchen-door/outside-pull.pdf signs/kitchen-door/all-door-signs.pdf`) |
| Server room door, inside: PUSH | house | [`signs/server-room/inside-push.pdf`](signs/server-room/inside-push.pdf) |
| Server room door, outside: PULL | house | [`signs/server-room/outside-pull.pdf`](signs/server-room/outside-pull.pdf) |
| Server room door, both sides, one per page | house | [`signs/server-room/all-door-signs.pdf`](signs/server-room/all-door-signs.pdf) (rebuild with `pdfunite signs/server-room/inside-push.pdf signs/server-room/outside-pull.pdf signs/server-room/all-door-signs.pdf`) |
| Table IDs (1-1 Ninja … 2-3-3 Alien), all in one PDF | wayfinding | [`signs/tables/all-tables.pdf`](signs/tables/all-tables.pdf) (one page per table; single files `table-<coord>.pdf`) |
| Bin label: garbage (gray bin) | green | [`signs/bins/garbage.pdf`](signs/bins/garbage.pdf) |
| Bin label: mixed recycling (blue bin) | green | [`signs/bins/recycling.pdf`](signs/bins/recycling.pdf) |
| Bin label: compost (green bin) | green | [`signs/bins/compost.pdf`](signs/bins/compost.pdf) |
| Bin label: glass (yellow bin) | green | [`signs/bins/glass.pdf`](signs/bins/glass.pdf) |
| Bin label: yard debris (green bin) | green | [`signs/bins/yard-debris.pdf`](signs/bins/yard-debris.pdf) |
| All five bin labels, one per page | green | [`signs/bins/all-bins.pdf`](signs/bins/all-bins.pdf) (rebuild with `python3 signs/bins/build_bins.py`) |
| 3D printer build plates: edges only, how to clean (Prusa MK4S satin, Bambu P2S textured PEI) | tools | [`signs/printers/build-plates.pdf`](signs/printers/build-plates.pdf) |
| Filament bunker storage (right / wrong) | tools | [`signs/printers/bunker-storage.pdf`](signs/printers/bunker-storage.pdf) |

### Bin labels

Letter **landscape**, meant to be laminated and taped to the bin. Edit the copy in
[`signs/bins/build_bins.py`](signs/bins/build_bins.py) (not the HTML), then rerun it and
`tools/render.sh signs/bins/*.html`.

The sorting rules are the City of Portland **commercial** requirements, which differ from
residential service. Most importantly, business compost is food only. Check these before
reprinting:

- [Business recycling requirement](https://www.portland.gov/bps/garbage-recycling/business-garbage-policies/recycling-requirement): all businesses must separate paper/metal/plastic, with glass in its own container
- [What goes in each bin](https://www.portland.gov/bps/garbage-recycling/recycling): accepted and rejected materials
- [Business compost / food scraps](https://www.portland.gov/bps/garbage-recycling/compost): food only, BPI-certified liners only
- [Containers in the right-of-way](https://www.portland.gov/bps/garbage-recycling/business-garbage-policies/containers-right-way): set-out and retrieval times
- [ENN-2.06 commercial collection rules](https://www.portland.gov/policies/environment-natural/solid-waste-recycling/enn-206-commercial-collection-customers-solid) (amended effective 1 Jan 2026): the binding rule. "a business must not have any recyclables in their garbage"
- Questions: `wasteinfo@portlandoregon.gov`, 503-823-7202

Yard debris has no business service of its own in these rules. Business compost is food
only, so the yard debris bin is ours to empty: members take it to a yard debris recycler
([Metro's Find a Recycler](https://www.oregonmetro.gov/tools-living/garbage-and-recycling/find-a-recycler)
lists them). Its yes/no lists borrow the city's limits for home yard debris (branches
under 4 in thick and 36 in long, no dirt, rocks, sod, stumps, lumber or plastic bags).
Our yard debris bin is green, the same as the compost bin, so the two labels tell them
apart by the kicker (COMPOST, YARD DEBRIS) and point to each other by name, not colour.

Two things the signs deliberately do **not** say:

- **Garbage is not billed by weight.** The City does not set commercial rates; businesses
  negotiate with a permitted private hauler on container size and pickup frequency
  (ENN-2.06 mentions weight only as a waste-*prevention* measure). Sorting saves money by
  letting you downsize the garbage container, not by the pound.
- **Not all garbage has to be bagged.** The city lists specific items that must be bagged
  (broken glass and ceramics, shredded paper, ashes, sawdust, packaging peanuts, pet waste,
  and sealed cooking oil/grease); ENN-2.06 contains no blanket rule. If our hauler's contract
  requires everything bagged, set `BAG_EVERYTHING = True` in `build_bins.py` and rebuild.

### Filament bunkers

Letter **portrait**, taped to each MARS cereal-box bunker. The sign is a right / wrong pair
(`.compare` in [`templates/sign.css`](templates/sign.css)) over the written checklist, drawn in the
**storage configuration**: both ends of the PTFE tube in the lid fittings, so the filament end sits
back inside the sealed box. The two drawings come from [`tools/build_brand.py`](tools/build_brand.py)
(`bunker-latched.svg`, `bunker-open.svg`), so change the script, not the SVGs.
