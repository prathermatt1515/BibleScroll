#!/usr/bin/env python3
"""Build data/searchindex.json — one searchable blob per book.

Search only ever looked inside the book already open, which was tolerable
when the app held one book and is not now that it holds sixty-six: looking
for "shepherd" from Jude found nothing.

Loading every book to search them would mean holding 9 MB of parsed objects
in memory. Instead each book becomes a single string, one line per verse,
tab separated:

    3:16\\tFor God so loved the world...\\tFor God so loved the world...

A regular expression runs over that string in one pass, so nothing has to be
parsed or lower-cased per keystroke, and the match offset maps straight back
to its line.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
ROOT = os.path.join(HERE, '..')


def main():
    html = io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    books = json.loads(re.search(r'const BOOKS_66 = (\[.*?\]);', html).group(1))

    index, verses = {}, 0
    for book in books:
        path = os.path.join(DATA, 'verses_%s.json' % book.replace(' ', ''))
        if not os.path.exists(path):
            continue                      # James is inline in data.js
        with io.open(path, encoding='utf-8') as fh:
            rows = json.load(fh)
        lines = []
        for r in rows:
            kjv = (r.get('kjv') or '').replace('\t', ' ').replace('\n', ' ')
            web = (r.get('web') or '').replace('\t', ' ').replace('\n', ' ')
            # The WEB copy is dropped where it matches the KJV, which happens
            # wherever that edition had nothing of its own.
            lines.append('%d:%d\t%s\t%s' % (r['c'], r['v'], kjv,
                                            '' if web == kjv else web))
            verses += 1
        index[book] = '\n'.join(lines)

    out = os.path.join(DATA, 'searchindex.json')
    with io.open(out, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(index, ensure_ascii=False, separators=(',', ':')))
    print('%d books, %d verses -> %s (%.2f MB)'
          % (len(index), verses, out, os.path.getsize(out) / 1e6))


if __name__ == '__main__':
    sys.exit(main())
