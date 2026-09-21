#!/usr/bin/env python3
"""Shared readers for the public-domain commentaries in
thefrenchpressed/pillar-commentary-data.

  calvin    John Calvin's commentaries        verse by verse
  fbmeyer   F. B. Meyer, Through the Bible    passage by passage

Calvin never wrote on Revelation, 2 John or 3 John, so those books have no
calvin/ directory; callers must fall back to Meyer.
"""
import io
import json
import os
import re

PILLAR = '/home/user/pillar/c'

USFM = {
    'Matthew': 'MAT', 'Mark': 'MRK', 'Luke': 'LUK', 'John': 'JHN',
    'Acts': 'ACT', 'Romans': 'ROM', '1Corinthians': '1CO',
    '2Corinthians': '2CO', 'Galatians': 'GAL', 'Ephesians': 'EPH',
    'Philippians': 'PHP', 'Colossians': 'COL', '1Thessalonians': '1TH',
    '2Thessalonians': '2TH', '1Timothy': '1TI', '2Timothy': '2TI',
    'Titus': 'TIT', 'Philemon': 'PHM', 'Hebrews': 'HEB', 'James': 'JAS',
    '1Peter': '1PE', '2Peter': '2PE', '1John': '1JN', '2John': '2JN',
    '3John': '3JN', 'Jude': 'JUD', 'Revelation': 'REV',
}


def has_book(commentator, usfm):
    return os.path.isdir(os.path.join(PILLAR, commentator, usfm))


def entries(commentator, usfm, chapter):
    """Return {verse number: text} for one chapter, or {} if absent."""
    path = os.path.join(PILLAR, commentator, usfm, '%d.json' % chapter)
    if not os.path.exists(path):
        return {}
    with io.open(path, encoding='utf-8') as fh:
        doc = json.load(fh)
    out = {}
    for item in doc['chapter']['content']:
        if item.get('type') != 'verse':
            continue
        text = ' '.join(c.get('text', '') for c in item['content']
                        if isinstance(c, dict)).replace('\r\n', '\n').strip()
        if text:
            out.setdefault(item['number'], text)
    return out


def strip_verse_number(text, book=None, chapter=None, verse=None):
    """Drop Calvin's leading reference to the verse being commented on.

    That is either a bare number ("8. For by grace...") or the full reference
    ("Matthew 15:10. And having called..."), both redundant beside the
    reference the drawer already shows. A leading reference to a DIFFERENT
    passage ("Genesis 11:31-12:1 records Abraham's call...") is the note's own
    content and is left alone, so the book and verse must match to be removed.
    """
    text = re.sub(r'^\s*\d+\s*[.:]\s*', '', text)
    if not book:
        return text
    spaced = re.sub(r'^([123])(?=[A-Z])', r'\1 ', book)
    pattern = r'^\s*%s\s+%d:%d\s*[.:]\s*' % (re.escape(spaced), chapter, verse)
    return re.sub(pattern, '', text)


def lead_bold(text, kjv, book=None, chapter=None, verse=None):
    """Bold Calvin's opening quotation of the verse, as the other books do.

    Only when it really is a quotation — short, and sharing wording with the
    verse — so ordinary prose is never mistaken for one.
    """
    text = strip_verse_number(text, book, chapter, verse)
    m = re.match(r'(.{0,90}?[.!?])(\s+)(.*)', text, re.S)
    if not m:
        return text
    head, gap, rest = m.groups()
    verse_words = set(re.findall(r'[a-z]+', kjv.lower()))
    head_words = [w for w in re.findall(r'[a-z]+', head.lower()) if len(w) > 2]
    if len(head_words) >= 3 and sum(w in verse_words for w in head_words) >= 3:
        return '<strong>%s</strong>%s%s' % (head, gap, rest)
    return text


def meyer_note(text):
    """Meyer's notes open with a passage title; keep it, so the reader can see
    the note covers a passage rather than this verse alone."""
    parts = text.split('\n\n', 1)
    if len(parts) == 2 and len(parts[0]) < 120:
        title = re.sub(r'\s*--\s*', ' — ', parts[0].strip())
        return '<em>%s</em><br><br>%s' % (title, parts[1].strip())
    return text


def passage_for(notes, verse):
    """Meyer keys each note by the verse its passage opens with."""
    starts = [n for n in sorted(notes) if n <= verse]
    return notes[starts[-1]] if starts else None
