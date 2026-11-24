# PDX Hackerspace (CTRL-H) Signs

Signs, labels and posters for PDX Hackerspace, plus the design system they share.

## ➜ Start here: [DESIGN.md](DESIGN.md)

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
| [`tools/`](tools) | `build_brand.py` regenerates brand SVGs; `render.sh` makes PDF/PNG |

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

## Signs

| Sign | Family | Files |
|---|---|---|
| Kitchen door, inside: PUSH | house | [`signs/kitchen-door/inside-push.pdf`](signs/kitchen-door/inside-push.pdf) |
| Kitchen door, outside: PULL | house | [`signs/kitchen-door/outside-pull.pdf`](signs/kitchen-door/outside-pull.pdf) |
| All door signs, one per page | house | [`signs/kitchen-door/all-door-signs.pdf`](signs/kitchen-door/all-door-signs.pdf) (rebuild with `pdfunite signs/kitchen-door/inside-push.pdf signs/kitchen-door/outside-pull.pdf signs/kitchen-door/all-door-signs.pdf`) |
| Table IDs (1-1 Ninja … 2-3-3 Alien), all in one PDF | wayfinding | [`signs/tables/all-tables.pdf`](signs/tables/all-tables.pdf) (one page per table; single files `table-<coord>.pdf`) |
