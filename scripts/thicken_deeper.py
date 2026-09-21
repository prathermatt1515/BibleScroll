#!/usr/bin/env python3
"""Add Calvin's exposition where the background note alone is thin.

After re-trimming at the longer cap, about a third of verses still had a
Deeper study shorter than their Explain, because kjvstudy.org's historical
note for those verses is genuinely brief — there was no more text to draw on.

Where that happens, Calvin's exposition of the verse is appended to the
background note, so Deeper study gives history and then exposition rather
than a single short paragraph. Where Calvin is unavailable — he did not write
on Revelation, and this collection lacks his Acts — Meyer's note on the
containing passage is used instead. Combined entries are tagged 'kc' or 'km'
so the drawer credits both. Entries already sourced wholly from Calvin or
Meyer are left alone.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commentary_sources as cs
from build_book_data import smart_trim, DEEPER_MAX
from deepen_deeper import BOOKS, DATA

# Below this many visible characters a Deeper note reads as a stub rather
# than a study; Explain averages a little over 400.
THIN = 600


def visible(html):
    return len(re.sub(r'<[^>]+>', '', html or ''))


def thicken(stem, display):
    path = os.path.join(DATA, 'study_%s.json' % stem)
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)
    with io.open(os.path.join(DATA, 'verses_%s.json' % stem), encoding='utf-8') as fh:
        kjv = {'%d:%d' % (v['c'], v['v']): v['kjv'] for v in json.load(fh)}

    usfm = cs.USFM[stem]
    has_calvin = cs.has_book('calvin', usfm)
    has_meyer = cs.has_book('fbmeyer', usfm)
    if not (has_calvin or has_meyer):
        return len(study), 0, 0

    chapters = sorted({int(k.split(':')[0]) for k in study})
    calvin = {c: cs.entries('calvin', usfm, c) for c in chapters} if has_calvin else {}
    meyer = {c: cs.entries('fbmeyer', usfm, c) for c in chapters} if has_meyer else {}

    added = skipped = 0
    for key, entry in study.items():
        if entry.get('srcDeeper'):        # already Calvin or Meyer throughout
            continue
        if visible(entry.get('deeper')) >= THIN:
            continue
        c, v = (int(x) for x in key.split(':'))
        raw = calvin.get(c, {}).get(v)
        if raw:
            note, tag = cs.lead_bold(raw, kjv.get(key, ''), display, c, v), 'c'
        else:
            passage = cs.passage_for(meyer.get(c, {}), v)
            if not passage:
                skipped += 1
                continue
            note, tag = cs.meyer_note(passage), 'm'
        background = (entry.get('deeper') or '').rstrip()
        combined = '%s<br><br>%s' % (background, note) if background else note
        entry['deeper'] = smart_trim(combined, DEEPER_MAX)
        entry['srcDeeper'] = ('k' + tag) if background else tag
        added += 1

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    return len(study), added, skipped


def main():
    print('%-16s %7s %9s %9s' % ('book', 'verses', 'deepened', 'no_calvin'))
    totals = [0, 0, 0]
    for stem, display in BOOKS.items():
        n, added, skipped = thicken(stem, display)
        totals = [totals[0] + n, totals[1] + added, totals[2] + skipped]
        if added or skipped:
            print('%-16s %7d %9d %9d' % (stem, n, added, skipped))
    print('%-16s %7d %9d %9d' % ('TOTAL', *totals))


if __name__ == '__main__':
    main()
