#!/usr/bin/env python3
"""Swap Calvin out of Deeper study in favour of F. B. Meyer.

Calvin is accurate but reads as 16th-century prose, which is heavy going in a
one-verse-at-a-time feed. Meyer's Through the Bible Day by Day covers all 26
New Testament books and reads far more naturally, so it becomes the supplement
everywhere Calvin had been used.

  srcDeeper 'kc'  kjvstudy background + Calvin  ->  background + Meyer ('km')
  srcDeeper 'c'   Calvin alone                  ->  Meyer alone ('m')

Verses Meyer's passage notes do not reach keep what they have. Entries already
on Meyer, and Explain text, are untouched.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commentary_sources as cs
from build_book_data import smart_trim, DEEPER_MAX, load_commentary, stems
from deepen_deeper import BOOKS, DATA


def swap(stem, display):
    path = os.path.join(DATA, 'study_%s.json' % stem)
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)

    targets = [k for k, e in study.items() if e.get('srcDeeper') in ('c', 'kc')]
    if not targets:
        return 0, 0

    usfm = cs.USFM[stem]
    chapters = sorted({int(k.split(':')[0]) for k in targets})
    meyer = {c: cs.entries('fbmeyer', usfm, c) for c in chapters}
    try:
        kjvstudy = load_commentary(stems(display)[2])
    except (IOError, OSError):
        kjvstudy = {}

    swapped = kept = 0
    for key in targets:
        c, v = (int(x) for x in key.split(':'))
        entry = study[key]
        passage = cs.passage_for(meyer.get(c, {}), v)
        if not passage:
            kept += 1
            continue
        note = cs.meyer_note(passage)
        # 'kc' paired a kjvstudy background with Calvin; rebuild that background
        # from source rather than trying to unpick it from the combined text.
        background = ''
        if entry['srcDeeper'] == 'kc':
            hit = kjvstudy.get((c, v))
            background = (hit.get('historical') or '').strip() if hit else ''
        if background:
            entry['deeper'] = smart_trim('%s<br><br>%s' % (background, note), DEEPER_MAX)
            entry['srcDeeper'] = 'km'
        else:
            entry['deeper'] = smart_trim(note, DEEPER_MAX)
            entry['srcDeeper'] = 'm'
        swapped += 1

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    return swapped, kept


def main():
    total_s = total_k = 0
    for stem, display in BOOKS.items():
        swapped, kept = swap(stem, display)
        if swapped or kept:
            print('%-16s swapped %5d   kept (no Meyer passage) %d' % (stem, swapped, kept))
        total_s += swapped
        total_k += kept
    print('%-16s swapped %5d   kept %d' % ('TOTAL', total_s, total_k))


if __name__ == '__main__':
    main()
