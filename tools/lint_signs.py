#!/usr/bin/env python3
"""Lint the signs against DESIGN.md's structural rules.

Checks every signs/<topic>/*.html for the house layout: the shared stylesheets,
a <main class="sign"> with a real family, a title, a footer, assets that exist
on disk, colours that come from tokens (no raw hex), no leftover template
placeholders, a committed PDF + PNG, and a mention in the README table.

    python3 tools/lint_signs.py            # lint every sign
    python3 tools/lint_signs.py signs/bins/garbage.html

Exits non-zero and prints "<file>: <problem>" for each failure. Stdlib only.
"""
import html as html_mod
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = {"safety", "tools", "house", "green", "wayfinding", "community"}
# Phrases that ship in templates/sign-template.html and must be replaced.
PLACEHOLDERS = [
    "SIGN TITLE", "Verb-first title.", "Sub-kicker", "Where / what",
    "family / sign-name", "One line on why it matters.",
    "First thing to do", "The key confirming action.",
]
HEX = re.compile(r"#[0-9A-Fa-f]{3}(?:[0-9A-Fa-f]{3})?\b")
# DESIGN.md 8.1, "No AI tells". Only the mechanical rules are checked here: the
# read-aloud test is still a human job.
TELLS = [
    (re.compile(r"\u2014|&mdash;|(?<= )--(?= )"), "an em dash (use a full stop, comma or colon)"),
    (re.compile(r"(?<!\d)\s?\u2013\s?(?!\d)"), "an en dash used as a dash (it is only for number spans)"),
    (re.compile(r";"), "a semicolon (split the sentence)"),
    (re.compile(r"\w\(s\)"), "an (s) plural"),
    (re.compile(r"\.\.\.|\u2026\s*$"), "a trailing ellipsis"),
    (re.compile(r"[\U0001F300-\U0001FAFF\u2700-\u27BF\u2B00-\u2BFF\u2190-\u21FF\u2600-\u26FF]"),
     "an emoji or dingbat (we have critters, LEDs and hexagons)"),
    (re.compile(r"\b(?:Note|Remember|Pro tip|Important|Warning|Tip|Reminder|Disclaimer)\s*:",
                re.I), "a colon-dash label (the note box and LEDs already do that job)"),
]
BANNED_WORDS = [
    "simply", "seamless", "seamlessly", "effortless", "effortlessly", "robust",
    "leverage", "utilize", "ensure", "ensuring", "delve", "foster", "elevate",
    "unlock", "streamline", "crucial", "vital", "essential", "best practices",
    "journey", "game-changer", "at the end of the day", "kindly",
]
WORD_RE = {w: re.compile(r"\b%s\b" % re.escape(w), re.I) for w in BANNED_WORDS}
TAGS = re.compile(r"(?:<!--.*?-->|<(?:script|style)\b.*?</(?:script|style)>|<[^>]+>)", re.S | re.I)

REF = re.compile(r'(?:src|href)="([^"]+)"')
MAIN = re.compile(r'<main[^>]*class="sign(?:\s+landscape)?"[^>]*>')
FAMILY = re.compile(r'<main[^>]*\bdata-family="([^"]*)"')
TITLE = re.compile(r"<title>(.*?)</title>", re.S)

problems = []


def plural(n, word):
    return "%d %s" % (n, word if n == 1 else word + "s")


def fail(path, msg):
    problems.append("%s: %s" % (os.path.relpath(path, ROOT), msg))


def sign_files():
    out = []
    for dirpath, _dirs, names in os.walk(os.path.join(ROOT, "signs")):
        for n in sorted(names):
            if n.endswith(".html"):
                out.append(os.path.join(dirpath, n))
    return sorted(out)


def visible_text(html):
    """The words a reader actually sees, with markup and comments removed."""
    text = html_mod.unescape(TAGS.sub(" ", html))
    return re.sub(r"[^\S\n]+", " ", text)


def lint(path, readme):
    with open(path, encoding="utf-8") as fh:
        html = fh.read()
    here = os.path.dirname(path)

    # Shared stylesheets, by resolved path rather than by spelling.
    sheets = {os.path.normpath(os.path.join(here, m)) for m in REF.findall(html)
              if m.endswith(".css")}
    for want in ("brand/tokens.css", "templates/sign.css"):
        if os.path.join(ROOT, want) not in sheets:
            fail(path, "does not link %s" % want)

    # House layout.
    mains = MAIN.findall(html)
    if not mains:
        fail(path, 'no <main class="sign"> (copy templates/sign-template.html)')
    fams = FAMILY.findall(html)
    if len(fams) != len(mains):
        fail(path, "%s but %s" % (plural(len(mains), "sign"),
                                  plural(len(fams), "data-family attribute")))
    for fam in sorted(set(fams)):
        if fam not in FAMILIES:
            fail(path, 'data-family="%s" is not one of %s (DESIGN.md §4)'
                 % (fam, ", ".join(sorted(FAMILIES))))
    if "sign-footer" not in html:
        fail(path, "no sign-footer (every sign carries the footer and sign id)")
    title = TITLE.search(html)
    if not title or not title.group(1).strip():
        fail(path, "empty or missing <title>")

    # Leftover template text.
    for ph in PLACEHOLDERS:
        if ph in html:
            fail(path, "leftover template placeholder %r" % ph)

    # Colour comes from tokens, never a raw hex in a sign.
    for hexcode in sorted(set(HEX.findall(html))):
        fail(path, "raw hex colour %s, use a var(--hs-*) token (DESIGN.md §3)" % hexcode)

    # Sign copy has to read like a member wrote it (DESIGN.md 8.1).
    text = visible_text(html)
    for pattern, what in TELLS:
        if pattern.search(text):
            fail(path, "copy contains %s" % what)
    for word, pattern in WORD_RE.items():
        if pattern.search(text):
            fail(path, "copy uses %r, a word we do not print (DESIGN.md 8.1)" % word)

    # Every local asset resolves.
    for ref in sorted(set(REF.findall(html))):
        if re.match(r"^(?:https?:)?//|^#|^data:|^mailto:", ref):
            continue
        target = os.path.normpath(os.path.join(here, ref.split("#")[0].split("?")[0]))
        if not os.path.exists(target):
            fail(path, "broken reference %s" % ref)

    # Printables are committed next to the source.
    base = path[: -len(".html")]
    for ext in (".pdf", ".png"):
        if not os.path.exists(base + ext):
            fail(path, "no %s rendered, run tools/render.sh %s"
                 % (ext, os.path.relpath(path, ROOT)))

    # The README table is the index, so a sign nobody can find is a missing sign.
    topic = os.path.relpath(here, ROOT).replace(os.sep, "/")
    if topic not in readme:
        fail(path, "%s is not mentioned in README.md" % topic)


def main(argv):
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
        readme = fh.read()
    targets = [os.path.abspath(a) for a in argv] or sign_files()
    if not targets:
        print("no signs found under signs/", file=sys.stderr)
        return 1
    for path in targets:
        lint(path, readme)
    for p in problems:
        print(p)
    print("lint: %s checked, %s found"
          % (plural(len(targets), "sign file"), plural(len(problems), "problem")))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
