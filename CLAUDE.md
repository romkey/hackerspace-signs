# CLAUDE.md

This repo holds signs for PDX Hackerspace (CTRL-H) and their design system.

**Always follow [DESIGN.md](DESIGN.md)** when creating or editing any sign, label, poster or
brand asset. For a new sign, use the `make-sign` skill (`.claude/skills/make-sign/SKILL.md`).

- Signs are HTML in `signs/<topic>/`, built on `brand/tokens.css` + `templates/sign.css`.
  Copy `templates/sign-template.html`; don't invent new layouts or colours.
- Render with `tools/render.sh <file.html>` and **look at the PNG** before calling a sign done.
  Check for overflow, overlap (the critter must never cover text) and text running off the page.
  Then run `python3 tools/lint_signs.py` and `python3 tools/check_pdfs.py` (what CI runs).
- After editing `DESIGN.md`, `README.md`, a skill or a build script's docstring, run
  `python3 tools/lint_docs.py`. DESIGN.md §8.1 applies to this repo's prose, not just signs.
- Never hand-edit generated SVGs in `brand/logo`, `brand/illustrations` or `brand/patterns`.
  Edit `tools/build_brand.py` and run `python3 tools/build_brand.py`.
- Nyan Cat is ours to use (we have permission). Treat it as a critter, by DESIGN.md §7.
- Add every new sign to the table in README.md.
