#!/usr/bin/env python3
"""The mechanical house style rules from DESIGN.md 8.1, "No AI tells".

Shared by tools/lint_signs.py (sign copy, where every rule applies) and
tools/lint_docs.py (this repo's own prose, where DESIGN.md asks only for the
dash, emoji and word rules). The read-aloud test is still a human job.

Two things are deliberately not checked. "just" as a softener needs a human to
tell it from "just the one", and the rule that arrows belong in a diagram and
not in a sentence cannot be told apart from a legitimate sequence like
"header -> trail -> footer".
"""
import re

# U+2713 and U+2717, the plain check and cross, are icons DESIGN.md 3 asks for.
# The emoji check mark U+2705 and the dingbats 8.1 names are not.
EMOJI = (r"[\U0001F300-\U0001FAFF"      # pictographs, faces, transport
         r"☀-⛿"               # misc symbols
         r"✀-✒✔-✖✘-➿"   # dingbats, keeping check and cross
         r"⬀-⯿️]")       # arrows-as-symbols, variation selector

#: (name, pattern, what the writer should do instead)
RULES = {
    "em-dash": (re.compile(r"—|&mdash;|(?<= )--(?= )"),
                "an em dash (use a full stop, comma or colon)"),
    "en-dash": (re.compile(r"(?<!\d)\s?–\s?(?!\d)"),
                "an en dash used as a dash (it is only for number spans)"),
    "emoji": (re.compile(EMOJI),
              "an emoji or dingbat (we have critters, LEDs and hexagons)"),
    "semicolon": (re.compile(r";"), "a semicolon (split the sentence)"),
    "plural-s": (re.compile(r"\w\(s\)"), "an (s) plural"),
    "ellipsis": (re.compile(r"\.\.\.|…\s*$"), "a trailing ellipsis"),
    "colon-label": (re.compile(r"\b(?:Note|Remember|Pro tip|Important|Warning|Tip"
                               r"|Reminder|Disclaimer)\s*:", re.I),
                    "a colon-dash label (the note box and LEDs already do that job)"),
}

#: Sign copy gets the lot.
SIGN_RULES = list(RULES)
#: Repo prose gets the dash, emoji and word rules (DESIGN.md 8.1).
DOC_RULES = ["em-dash", "en-dash", "emoji"]

WORDS = [
    "simply", "seamless", "seamlessly", "effortless", "effortlessly", "robust",
    "leverage", "utilize", "delve", "foster", "elevate", "unlock", "streamline",
    "crucial", "vital", "essential", "best practices", "journey", "game-changer",
    "at the end of the day", "kindly", "ensure", "ensures", "ensuring",
]
WORD_RE = {w: re.compile(r"\b%s\b" % re.escape(w).replace(r"\ ", r"\s+"), re.I)
           for w in WORDS}

# A doc that has to quote what it bans says so, between these markers.
IGNORE = re.compile(r"<!--\s*house-style:\s*ignore start\s*-->.*?"
                    r"<!--\s*house-style:\s*ignore end\s*-->", re.S | re.I)
IGNORE_LINE = re.compile(r"^.*<!--\s*house-style:\s*ignore\s*-->.*$", re.M | re.I)


def blank(match):
    """Replace a match with spaces, keeping the line numbering intact."""
    return re.sub(r"[^\n]", " ", match.group(0))


def plural(n, word):
    return "%d %s" % (n, word if n == 1 else word + "s")


def findings(text, rules, words=True):
    """Yield (line number, complaint) for each rule the text breaks."""
    for lineno, line in enumerate(text.split("\n"), start=1):
        for name in rules:
            pattern, complaint = RULES[name]
            if pattern.search(line):
                yield lineno, complaint
        if words:
            for word in WORDS:
                if WORD_RE[word].search(line):
                    yield lineno, ("the word %r, which we do not print" % word)
