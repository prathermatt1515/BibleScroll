#!/usr/bin/env python3
"""Rebuild the Deeper study text at a longer cap, from each entry's own source.

Deeper study was capped at the same ~500 characters as Explain, so the two
read at the same length and Deeper often said less than its source had. The
kjvstudy.org background notes average 537 characters and run to 1,620, and
Calvin and Meyer run far longer, so nearly half of them were being cut.

This re-trims each entry from its original source at DEEPER_MAX, honouring
the srcDeeper tag so Calvin stays Calvin and Meyer stays Meyer. Explain is
left alone: it is meant to be the short one.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commentary_sources as cs
from build_book_data import smart_trim, DEEPER_MAX, load_commentary, stems

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

# file stem -> display name (the form the source readers expect)
BOOKS = {
    'Matthew': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
    'Acts': 'Acts', 'Romans': 'Romans', '1Corinthians': '1 Corinthians',
    '2Corinthians': '2 Corinthians', 'Galatians': 'Galatians',
    'Ephesians': 'Ephesians', 'Philippians': 'Philippians',
    'Colossians': 'Colossians', '1Thessalonians': '1 Thessalonians',
    '2Thessalonians': '2 Thessalonians', '1Timothy': '1 Timothy',
    '2Timothy': '2 Timothy', 'Titus': 'Titus', 'Philemon': 'Philemon',
    'Hebrews': 'Hebrews', '1Peter': '1 Peter', '2Peter': '2 Peter',
    '1John': '1 John', '2John': '2 John', '3John': '3 John',
    'Jude': 'Jude', 'Revelation': 'Revelation',
}


def rebuild(stem, display):
    path = os.path.join(DATA, 'study_%s.json' % stem)
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)
    with io.open(os.path.join(DATA, 'verses_%s.json' % stem), encoding='utf-8') as fh:
        kjv = {'%d:%d' % (v['c'], v['v']): v['kjv'] for v in json.load(fh)}

    usfm = cs.USFM[stem]
    chapters = sorted({int(k.split(':')[0]) for k in study})
    calvin = {c: cs.entries('calvin', usfm, c) for c in chapters}
    meyer = {c: cs.entries('fbmeyer', usfm, c) for c in chapters}
    # kjvstudy keys its commentary by (chapter, verse)
    try:
        kjvstudy = load_commentary(stems(display)[2])
    except (IOError, OSError):
        kjvstudy = {}

    grown = same = 0
    for key, entry in study.items():
        c, v = (int(x) for x in key.split(':'))
        src = entry.get('srcDeeper')
        if src == 'c':
            raw = calvin.get(c, {}).get(v)
            raw = cs.lead_bold(raw, kjv.get(key, ''), display, c, v) if raw else None
        elif src == 'm':
            note = cs.passage_for(meyer.get(c, {}), v)
            raw = cs.meyer_note(note) if note else None
        else:
            hit = kjvstudy.get((c, v))
            raw = hit.get('historical') if hit else None
        if not raw:
            same += 1
            continue
        fresh = smart_trim(raw, DEEPER_MAX)
        if len(fresh) > len(entry.get('deeper') or ''):
            grown += 1
        else:
            same += 1
        entry['deeper'] = fresh

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    return len(study), grown, same


def main():
    print('%-16s %7s %8s %9s' % ('book', 'verses', 'longer', 'unchanged'))
    totals = [0, 0, 0]
    for stem, display in BOOKS.items():
        n, grown, same = rebuild(stem, display)
        totals = [totals[0] + n, totals[1] + grown, totals[2] + same]
        print('%-16s %7d %8d %9d' % (stem, n, grown, same))
    print('%-16s %7d %8d %9d' % ('TOTAL', *totals))


if __name__ == '__main__':
    main()
