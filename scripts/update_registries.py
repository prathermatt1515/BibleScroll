"""Rewrite the four book registries in index.html from what is in data/.

CONTENT_AVAILABLE, BOOK_CODES, BOOK_FILE_NAMES and CHAPTER_COUNTS have to
agree with each other and with the files on disk; keeping them in step by
hand is how a book ends up half-registered. This regenerates all four from
data/verses_*.json, in canonical Bible order.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commentary_sources import USFM                      # noqa: E402

ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua",
    "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings",
    "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job",
    "Psalms", "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah",
    "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
    "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai",
    "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts",
    "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
    "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation",
]

# James ships inline in data.js rather than as a data/ file.
INLINE = {"James": [27, 26, 18, 17, 20]}


def counts_for(book):
    if book in INLINE:
        return INLINE[book]
    path = os.path.join(ROOT, 'data', 'verses_%s.json' % book.replace(' ', ''))
    if not os.path.exists(path):
        return None
    with io.open(path, encoding='utf-8') as fh:
        verses = json.load(fh)
    per = {}
    for row in verses:
        c = int(row['c'])
        per[c] = max(per.get(c, 0), int(row['v']))
    return [per[c] for c in sorted(per)]


def js_key(book):
    return book if re.match(r'^[A-Za-z]+$', book) else "'%s'" % book


def main():
    books, counts = [], {}
    for book in ORDER:
        cs = counts_for(book)
        if cs:
            books.append(book)
            counts[book] = cs

    avail = '  const CONTENT_AVAILABLE = [%s];' % ', '.join(
        "'%s'" % b for b in books)
    codes = '  const BOOK_CODES = { %s };' % ', '.join(
        '%s: %r' % (js_key(b), USFM[b.replace(' ', '')]) for b in books)
    files = '  const BOOK_FILE_NAMES = { %s };' % ', '.join(
        "'%s': '%s'" % (b, b.replace(' ', '')) for b in books)
    chapters = '  const CHAPTER_COUNTS = {\n%s\n  };' % ',\n'.join(
        '    %s: [%s]' % (js_key(b), ','.join(str(n) for n in counts[b]))
        for b in books)

    path = os.path.join(ROOT, 'index.html')
    with io.open(path, encoding='utf-8') as fh:
        html = fh.read()

    subs = [
        (r'^  const CONTENT_AVAILABLE = \[.*?\];$', avail),
        (r'^  const BOOK_CODES = \{.*?\};$', codes),
        (r'^  const BOOK_FILE_NAMES = \{.*?\};$', files),
        (r'^  const CHAPTER_COUNTS = \{.*?^  \};$', chapters),
    ]
    for pattern, replacement in subs:
        html, n = re.subn(pattern, lambda _m: replacement, html,
                          count=1, flags=re.S | re.M)
        if n != 1:
            raise SystemExit('registry not found: %s' % pattern)

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('registered %d books (%d chapters)'
          % (len(books), sum(len(counts[b]) for b in books)))


if __name__ == '__main__':
    main()
