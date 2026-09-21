#!/usr/bin/env python3
"""Replace repeated book-level "Deeper study" text with per-verse commentary.

For some verses kjvstudy.org has no verse-specific historical background and
falls back to a paragraph about the book as a whole. The text is accurate but
identical across many verses — Revelation repeats one paragraph on 325 of its
404 verses — so scrolling the Deeper study tab shows the same note again and
again.

This swaps only those repeated entries for Calvin's note on that verse, or
Meyer's note on the passage containing it where Calvin did not write on the
book (Revelation). Entries that are already verse-specific are left alone.
"""
import io
import json
import os
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commentary_sources as cs
from build_book_data import smart_trim, DEEPER_MAX

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# A background paragraph shared by this many verses is book-level filler
# rather than commentary on any one verse.
REPEAT_THRESHOLD = 3


def load(name):
    with io.open(os.path.join(DATA, name), encoding='utf-8') as fh:
        return json.load(fh)


def fill(book):
    usfm = cs.USFM[book]
    study = load('study_%s.json' % book)
    kjv = {'%d:%d' % (v['c'], v['v']): v['kjv']
           for v in load('verses_%s.json' % book)}

    counts = collections.Counter(e.get('deeper', '') for e in study.values())
    boilerplate = {t for t, n in counts.items() if t and n >= REPEAT_THRESHOLD}
    targets = [k for k, e in study.items() if e.get('deeper', '') in boilerplate]
    if not targets:
        return book, 0, 0, 0, 0

    chapters = sorted({int(k.split(':')[0]) for k in targets})
    calvin = {c: cs.entries('calvin', usfm, c) for c in chapters}
    meyer = {c: cs.entries('fbmeyer', usfm, c) for c in chapters}

    from_calvin = from_meyer = unchanged = 0
    for key in targets:
        c, v = (int(x) for x in key.split(':'))
        text = src = None
        if v in calvin.get(c, {}):
            text = cs.lead_bold(calvin[c][v], kjv.get(key, ''), book, c, v)
            src = 'c'
            from_calvin += 1
        else:
            note = cs.passage_for(meyer.get(c, {}), v)
            if note:
                text = cs.meyer_note(note)
                src = 'm'
                from_meyer += 1
        if text is None:
            unchanged += 1          # keep the book-level note over nothing
            continue
        study[key]['deeper'] = smart_trim(text, DEEPER_MAX)
        study[key]['srcDeeper'] = src

    with io.open(os.path.join(DATA, 'study_%s.json' % book), 'w',
                 encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    return book, len(targets), from_calvin, from_meyer, unchanged


def main(argv):
    books = argv or ['Matthew', 'Mark', '2Corinthians', 'Philippians',
                     '2Peter', 'Revelation']
    print('%-16s %8s %8s %8s %10s' % ('book', 'repeated', 'calvin', 'meyer', 'kept'))
    for book in books:
        name, n, cal, mey, kept = fill(book)
        print('%-16s %8d %8d %8d %10d' % (name, n, cal, mey, kept))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
