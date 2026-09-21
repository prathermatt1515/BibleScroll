#!/usr/bin/env python3
"""Rebuild data/study_Ephesians.json from Calvin and F. B. Meyer.

Ephesians is the one book of 66 that kjvstudy.org left as an unfilled
template ("[Verse 2:8 text would be quoted here]"), so its commentary has to
come from elsewhere. Both sources are public domain, via
thefrenchpressed/pillar-commentary-data:

  explain  John Calvin, Commentary on Ephesians  (verse by verse, 147 of 155)
  deeper   F. B. Meyer, Through the Bible Day by Day  (passage by passage)

The Greek interlinear and cross-references already in the file are genuine
and are carried over untouched.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commentary_sources as cs
from build_book_data import smart_trim, EXPLAIN_MAX, DEEPER_MAX, TAKEAWAY_MAX

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
CHAPTERS = {1: 23, 2: 22, 3: 21, 4: 32, 5: 33, 6: 24}


def main():
    path = os.path.join(DATA, 'study_Ephesians.json')
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)
    with io.open(os.path.join(DATA, 'verses_Ephesians.json'), encoding='utf-8') as fh:
        kjv = {'%d:%d' % (v['c'], v['v']): v['kjv'] for v in json.load(fh)}

    filled_explain = filled_deeper = 0
    for chapter, last in CHAPTERS.items():
        calvin = cs.entries('calvin', 'EPH', chapter)
        meyer = cs.entries('fbmeyer', 'EPH', chapter)

        for verse in range(1, last + 1):
            key = '%d:%d' % (chapter, verse)
            entry = study.get(key)
            if entry is None:
                continue

            if verse in calvin:
                explain = smart_trim(
                    cs.lead_bold(calvin[verse], kjv.get(key, ''),
                                 'Ephesians', chapter, verse), EXPLAIN_MAX)
                filled_explain += 1
            else:
                explain = ''

            note = cs.passage_for(meyer, verse)
            if note:
                deeper = smart_trim(cs.meyer_note(note), DEEPER_MAX)
                filled_deeper += 1
            else:
                deeper = ''

            entry['explain'] = explain
            entry['deeper'] = deeper
            entry['takeaway'] = smart_trim(explain, TAKEAWAY_MAX)
            # Neither source carries reflection questions; the drawer hides
            # the card rather than showing an empty one.
            entry['apply'] = ''
            entry.pop('questions', None)

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))

    total = sum(CHAPTERS.values())
    print('Ephesians rebuilt: explain %d/%d, deeper %d/%d'
          % (filled_explain, total, filled_deeper, total))


if __name__ == '__main__':
    main()
