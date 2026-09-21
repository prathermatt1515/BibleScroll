#!/usr/bin/env python3
"""Rebuild data/study_Ephesians.json from Calvin and F. B. Meyer.

Ephesians is the one book of 66 that kjvstudy.org left as an unfilled
template ("[Verse 2:8 text would be quoted here]"), so its commentary has
to come from elsewhere. Both sources are public domain, via
thefrenchpressed/pillar-commentary-data:

  explain  John Calvin, Commentary on Ephesians  (verse by verse)
  deeper   F. B. Meyer, Through the Bible Day by Day  (passage by passage)

The Greek interlinear and cross-references already in the file are genuine
and are carried over untouched.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_book_data import smart_trim, EXPLAIN_MAX, DEEPER_MAX, TAKEAWAY_MAX

PILLAR = '/home/user/pillar/c'
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
CHAPTERS = {1: 23, 2: 22, 3: 21, 4: 32, 5: 33, 6: 24}


def entries(commentator, chapter):
    """Return {verse number: text} for one chapter."""
    path = os.path.join(PILLAR, commentator, 'EPH', '%d.json' % chapter)
    with io.open(path, encoding='utf-8') as fh:
        doc = json.load(fh)
    out = {}
    for item in doc['chapter']['content']:
        if item.get('type') != 'verse':
            continue
        text = ' '.join(c.get('text', '') for c in item['content']
                        if isinstance(c, dict))
        text = text.replace('\r\n', '\n').strip()
        if text:
            out.setdefault(item['number'], text)
    return out


def lead_bold(text, kjv):
    """Bold Calvin's opening quotation of the verse, as the other books do.

    Calvin opens each note by quoting the verse's first words ("8. For by
    grace are ye saved. This is an inference..."). Bold that opener only
    when it really is a quotation — short, and sharing wording with the
    verse — so ordinary prose is never mistaken for one.
    """
    text = re.sub(r'^\s*\d+\s*[.:]\s*', '', text)
    m = re.match(r'(.{0,90}?[.!?])(\s+)(.*)', text, re.S)
    if not m:
        return text
    head, gap, rest = m.group(1), m.group(2), m.group(3)
    verse_words = set(re.findall(r'[a-z]+', kjv.lower()))
    head_words = [w for w in re.findall(r'[a-z]+', head.lower()) if len(w) > 2]
    if len(head_words) >= 3 and sum(w in verse_words for w in head_words) >= 3:
        return '<strong>%s</strong>%s%s' % (head, gap, rest)
    return text


def meyer_note(text):
    """Meyer's notes open with a passage title; keep it, so the reader can
    see the note covers a passage rather than this verse alone."""
    parts = text.split('\n\n', 1)
    if len(parts) == 2 and len(parts[0]) < 120:
        title = re.sub(r'\s*--\s*', ' — ', parts[0].strip())
        return '<em>%s</em><br><br>%s' % (title, parts[1].strip())
    return text


def main():
    path = os.path.join(DATA, 'study_Ephesians.json')
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)

    verses_path = os.path.join(DATA, 'verses_Ephesians.json')
    with io.open(verses_path, encoding='utf-8') as fh:
        kjv = {'%d:%d' % (v['c'], v['v']): v['kjv'] for v in json.load(fh)}

    filled_explain = filled_deeper = 0
    for chapter, last in CHAPTERS.items():
        calvin = entries('calvin', chapter)
        meyer = entries('fbmeyer', chapter)
        # Meyer comments on passages, keyed by the verse each one opens with.
        starts = sorted(meyer)

        for verse in range(1, last + 1):
            key = '%d:%d' % (chapter, verse)
            entry = study.get(key)
            if entry is None:
                continue

            if verse in calvin:
                explain = smart_trim(lead_bold(calvin[verse], kjv.get(key, '')),
                                     EXPLAIN_MAX)
                filled_explain += 1
            else:
                explain = ''

            opening = [s for s in starts if s <= verse]
            if opening:
                deeper = smart_trim(meyer_note(meyer[opening[-1]]), DEEPER_MAX)
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
    missing = [k for k, v in study.items() if not v['explain']]
    print('verses without Calvin:', ', '.join(sorted(missing, key=lambda s: tuple(map(int, s.split(':'))))) or 'none')


if __name__ == '__main__':
    main()
