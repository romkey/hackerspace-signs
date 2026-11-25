#!/usr/bin/env python3
"""Lint this repo's own prose against the house style.

DESIGN.md 8.1 asks the dash, emoji and word rules of the repo's writing as well
as of the signs, because this is where the next sign gets its wording. Checked:
the Markdown at the top level and under .claude/skills, and the docstrings of
the build scripts. Code blocks, inline code, link targets and URLs are skipped,
since a shell command or a CSS token is not prose.

A doc that has to quote what it bans (DESIGN.md 8.1 itself, for one) wraps that
part in a marker:

    <!-- house-style: ignore start -->
    ... text that may break the rules ...
    <!-- house-style: ignore end -->

or ends a single line with a <!-- house-style: ignore --> comment.

    python3 tools/lint_docs.py            # every doc
    python3 tools/lint_docs.py README.md

Exits non-zero and prints "<file>:<line>: <problem>" for each failure.
"""
import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import house_style as hs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FENCE = re.compile(r"^(?P<fence>```|~~~).*?^(?P=fence)[^\n]*$", re.S | re.M)
CODE_SPAN = re.compile(r"``[^`]*``|`[^`\n]*`")
LINK_TARGET = re.compile(r"\]\([^)\n]*\)")
URL = re.compile(r"<?https?://[^\s>)]+>?")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
# Markdown tables of punctuation rules are prose; HTML tags in a doc are not.
HTML_TAG = re.compile(r"</?[a-zA-Z][^>\n]*>")


def docs():
    """Every doc this lint covers, in a stable order."""
    found = [os.path.join(ROOT, n) for n in sorted(os.listdir(ROOT))
             if n.endswith(".md")]
    skills = os.path.join(ROOT, ".claude", "skills")
    for dirpath, _dirs, names in os.walk(skills):
        found += [os.path.join(dirpath, n) for n in sorted(names) if n.endswith(".md")]
    found += [os.path.join(ROOT, "tools", n) for n in sorted(os.listdir(
        os.path.join(ROOT, "tools"))) if n.endswith(".py")]
    for dirpath, _dirs, names in os.walk(os.path.join(ROOT, "signs")):
        found += [os.path.join(dirpath, n) for n in sorted(names)
                  if n.startswith("build_") and n.endswith(".py")]
    return found


def prose_of_markdown(text):
    """The doc with its code, links and ignored parts blanked out."""
    for pattern in (hs.IGNORE, hs.IGNORE_LINE, FENCE, CODE_SPAN, LINK_TARGET,
                    URL, HTML_COMMENT, HTML_TAG):
        text = pattern.sub(hs.blank, text)
    return text


def prose_of_python(path, text):
    """Just the docstrings, blank everywhere else, so line numbers still point home."""
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return None, "will not parse (%s)" % exc
    keep = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
            continue
        body = getattr(node, "body", None)
        if not body or not isinstance(body[0], ast.Expr):
            continue
        value = body[0].value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            keep[value.lineno] = (value.end_lineno, value.value)
    lines = [""] * len(text.split("\n"))
    for start, (end, doc) in keep.items():
        piece = doc.split("\n")
        for i, line in enumerate(piece):
            if start - 1 + i < len(lines):
                lines[start - 1 + i] = line
        del end
    return "\n".join(lines), None


def main(argv):
    targets = [os.path.abspath(a) for a in argv] or docs()
    problems = []
    for path in targets:
        rel = os.path.relpath(path, ROOT)
        if rel.startswith(".."):
            rel = path
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        if path.endswith(".py"):
            prose, err = prose_of_python(path, raw)
            if err:
                problems.append("%s: %s" % (rel, err))
                continue
        else:
            prose = prose_of_markdown(raw)
        for lineno, complaint in hs.findings(prose, hs.DOC_RULES):
            problems.append("%s:%d: %s" % (rel, lineno, complaint))
    for p in problems:
        print(p)
    print("lint_docs: %s checked, %s found"
          % (hs.plural(len(targets), "doc"), hs.plural(len(problems), "problem")))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
