#!/usr/bin/env python3
"""Check rendered sign PDFs: page count, paper size and orientation.

A sign that overflows its page spills onto a second page, so "one page per
<main class="sign">" catches the most common rendering fault. Paper must be US
Letter, landscape exactly when the sign asks for it.

    python3 tools/check_pdfs.py             # every sign with a PDF beside it
    python3 tools/check_pdfs.py signs/bins/garbage.html

Needs pypdf (pip install pypdf). Exits non-zero on any problem.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = re.compile(r'<main[^>]*class="sign((?:\s+\w+)*)"[^>]*>')
LETTER = (612.0, 792.0)   # points, portrait
TOL = 2.0                 # Chrome rounds; 2pt is well under a visible error

try:
    from pypdf import PdfReader
except ImportError:
    print("check_pdfs: needs pypdf (pip install pypdf)", file=sys.stderr)
    sys.exit(2)

problems = []


def plural(n, word):
    return "%d %s" % (n, word if n == 1 else word + "s")


def fail(rel, msg):
    problems.append("%s: %s" % (rel, msg))


def html_files():
    out = []
    for dirpath, _dirs, names in os.walk(os.path.join(ROOT, "signs")):
        for n in sorted(names):
            if n.endswith(".html"):
                out.append(os.path.join(dirpath, n))
    return sorted(out)


def check(path):
    rel = os.path.relpath(path, ROOT)
    pdf = path[: -len(".html")] + ".pdf"
    if not os.path.exists(pdf):
        fail(rel, "no PDF rendered")
        return
    with open(path, encoding="utf-8") as fh:
        mains = MAIN.findall(fh.read())
    want_landscape = ["landscape" in m.split() for m in mains]
    if not mains:
        fail(rel, 'no <main class="sign"> to check against')
        return

    pages = PdfReader(pdf).pages
    if len(pages) != len(mains):
        fail(rel, "%s in the PDF but %s in the HTML, so a sign is "
                  "overflowing its page" % (plural(len(pages), "page"),
                                            plural(len(mains), "sign")))
        return

    for i, (page, landscape) in enumerate(zip(pages, want_landscape), start=1):
        box = page.mediabox
        w, h = float(box.width), float(box.height)
        short, long_ = sorted((w, h))
        if abs(short - LETTER[0]) > TOL or abs(long_ - LETTER[1]) > TOL:
            fail(rel, "page %d is %.0fx%.0fpt, not US Letter (612x792pt)" % (i, w, h))
            continue
        if (w > h) != landscape:
            fail(rel, "page %d is %s but the HTML asks for %s"
                 % (i, "landscape" if w > h else "portrait",
                    "landscape" if landscape else "portrait"))


def main(argv):
    targets = [os.path.abspath(a) for a in argv] or html_files()
    for path in targets:
        check(path)
    for p in problems:
        print(p)
    print("check_pdfs: %s checked, %s found"
          % (plural(len(targets), "sign file"), plural(len(problems), "problem")))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
