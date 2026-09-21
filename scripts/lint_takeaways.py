#!/usr/bin/env python3
"""Check written takeaways against scripts/takeaways/SPEC.md.

Reports, per book: coverage, length outliers, duplicates, HTML, keys that do
not exist in the book, and the style tics the spec rules out (exclamation
marks outside a quotation, second-person exhortation, filler openings).

Usage: lint_takeaways.py [module ...]   (default: every module present)
"""
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'takeaways'))
sys.path.insert(0, HERE)
from apply_takeaways import STEMS                          # noqa: E402

DATA = os.path.join(HERE, '..', 'data')
MIN_LEN, MAX_LEN = 30, 160
# Second-person instruction, which the spec rules out. "remember to" only
# counts as an imperative when it opens the line: the KJV's own "he did not
# remember to shew mercy" is a report, not an exhortation.
EXHORT = re.compile(r'\b(you should|you must|we should|we must|let us|ask '
                    r'yourself)\b|^remember to\b', re.I)
FILLER = re.compile(r'^(this verse (?:shows|tells|teaches|reminds|says)'
                    r'|here we see|in this passage)', re.I)


def verse_text(stem):
    path = os.path.join(DATA, 'verses_%s.json' % stem)
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding='utf-8') as fh:
        return {'%d:%d' % (r['c'], r['v']): r['kjv'] for r in json.load(fh)}


def echo_ratio(line, verse):
    """How much of a takeaway is just the verse's own words read back.

    A quoted phrase followed by an observation scores well under 1.0; a line
    that is only the verse quoted scores 1.0, and the spec rules that out —
    the card would then repeat the text directly above it.
    """
    own = re.findall(r"[a-z']+", line.lower())
    if not own:
        return 0.0
    theirs = set(re.findall(r"[a-z']+", verse.lower()))
    return sum(1 for w in own if w in theirs) / len(own)


def verse_keys(stem):
    path = os.path.join(DATA, 'study_%s.json' % stem)
    if not os.path.exists(path):
        return None
    with io.open(path, encoding='utf-8') as fh:
        return set(json.load(fh))


def lint(module):
    stem = STEMS[module]
    keys = verse_keys(stem)
    if keys is None:
        print('%-14s no study data' % module)
        return 0
    written = importlib.import_module(module).TAKEAWAYS
    verses = verse_text(stem)
    problems = []

    stray = sorted(set(written) - keys)
    if stray:
        problems.append('keys not in book: %s' % ', '.join(stray[:6]))

    seen = {}
    for key, line in written.items():
        if line in seen:
            problems.append('duplicate line at %s and %s' % (seen[line], key))
        seen[line] = key
        if '<' in line:
            problems.append('%s: HTML' % key)
        n = len(line)
        if n < MIN_LEN or n > MAX_LEN:
            problems.append('%s: %d chars — %s' % (key, n, line[:70]))
        if '!' in line.replace('!"', '').replace("!'", ''):
            quoted = re.findall(r'"[^"]*"', line)
            if not any('!' in q for q in quoted):
                problems.append('%s: exclamation — %s' % (key, line[:70]))
        # "let us go" inside a KJV quotation is the verse talking, not the
        # takeaway exhorting, so style checks look only at our own words.
        ours = re.sub(r'"[^"]*"', '', line)
        if EXHORT.search(ours):
            problems.append('%s: exhortation — %s' % (key, line[:70]))
        if FILLER.match(ours.strip()):
            problems.append('%s: filler opening — %s' % (key, line[:70]))
        if key in verses and echo_ratio(line, verses[key]) >= 0.95:
            problems.append('%s: only the verse read back — %s' % (key, line[:70]))

    pct = 100.0 * len(written) / len(keys)
    lengths = sorted(len(v) for v in written.values())
    median = lengths[len(lengths) // 2] if lengths else 0
    print('%-14s %5d/%-5d (%4.1f%%)  median %d chars  %s'
          % (module, len(written), len(keys), pct, median,
             'OK' if not problems else '%d PROBLEM(S)' % len(problems)))
    for p in problems[:25]:
        print('    %s' % p)
    if len(problems) > 25:
        print('    ... and %d more' % (len(problems) - 25))
    return len(problems)


def main(argv):
    modules = argv or sorted(
        m for m in STEMS
        if os.path.exists(os.path.join(HERE, 'takeaways', '%s.py' % m)))
    total = sum(lint(m) for m in modules)
    print('\n%d problem(s) across %d book(s)' % (total, len(modules)))
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
