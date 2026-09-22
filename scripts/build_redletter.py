#!/usr/bin/env python3
"""Build data/redletter.json: which words of each verse are spoken by Jesus.

Red letters are an editorial tradition, not part of the text, so they have to
come from an edition that marks them. Two public-domain sources do:

  KJV  eng-kjv.osis.xml   <q who="Jesus" sID/eID> milestones
  WEB  eng-web.usfx.xml   <wj> ... </wj> containers

Both are parsed into character ranges over the verse's own plain text, then
checked against the text this app actually ships. A range is only kept when
the source's verse text matches ours exactly, or when the marked words can be
located in ours unambiguously; anything else is dropped and reported, because
a red span at the wrong offset would colour the wrong words.

Usage: build_redletter.py <eng-kjv.osis.xml> <eng-web.usfx.xml>
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from commentary_sources import USFM                                # noqa: E402

DATA = os.path.join(HERE, '..', 'data')
TAG = re.compile(r'<[^>]+>')

OSIS_BOOKS = {
    'Matt': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
    'Acts': 'Acts', 'Rom': 'Romans', '1Cor': '1 Corinthians',
    '2Cor': '2 Corinthians', 'Gal': 'Galatians', 'Eph': 'Ephesians',
    'Heb': 'Hebrews', 'Jas': 'James', '1Pet': '1 Peter', '2Pet': '2 Peter',
    '1John': '1 John', 'Rev': 'Revelation', '1Tim': '1 Timothy',
    '2Tim': '2 Timothy', 'Col': 'Colossians', 'Phil': 'Philippians',
    '1Thess': '1 Thessalonians', '2Thess': '2 Thessalonians',
    'Titus': 'Titus', 'Phlm': 'Philemon', 'Jude': 'Jude',
    '1Kgs': '1 Kings', 'Gen': 'Genesis',
}
USFX_BOOKS = {code: name for name, code in
              ((n, USFM[n.replace(' ', '')]) for n in
               [b for b in USFM])}


def collapse(pairs):
    """Squeeze whitespace the way the shipped verse text is squeezed."""
    out = []
    for ch, red in pairs:
        if ch.isspace():
            if out and out[-1][0] != ' ':
                out.append((' ', red))
        else:
            out.append((ch, red))
    while out and out[0][0] == ' ':
        out.pop(0)
    while out and out[-1][0] == ' ':
        out.pop()
    return out


def ranges_of(pairs):
    spans, start = [], None
    for i, (_, red) in enumerate(pairs):
        if red and start is None:
            start = i
        elif not red and start is not None:
            spans.append([start, i])
            start = None
    if start is not None:
        spans.append([start, len(pairs)])
    # Trim trailing space out of a span so the colour stops at the word.
    text = ''.join(c for c, _ in pairs)
    for sp in spans:
        while sp[1] > sp[0] and text[sp[1] - 1] == ' ':
            sp[1] -= 1
    return [sp for sp in spans if sp[1] > sp[0]]


def parse_osis(path):
    with io.open(path, encoding='utf-8') as fh:
        doc = fh.read()
    verses, cur, red, in_note = {}, None, 0, 0
    pos = 0
    for m in TAG.finditer(doc):
        text = doc[pos:m.start()]
        if cur and text and not in_note:
            verses[cur].extend((ch, red > 0) for ch in text)
        pos = m.end()
        tag = m.group(0)
        if tag.startswith('<note'):
            in_note += 0 if tag.endswith('/>') else 1
        elif tag.startswith('</note'):
            in_note = max(0, in_note - 1)
        elif tag.startswith('<verse'):
            sid = re.search(r'osisID="([^"]+)"', tag)
            if sid and 'sID=' in tag:
                cur = sid.group(1)
                verses.setdefault(cur, [])
            elif 'eID=' in tag:
                cur = None
        elif tag.startswith('<q'):
            if 'who="Jesus"' in tag and 'sID=' in tag:
                red += 1
            elif 'eID=' in tag and red:
                red -= 1
    out = {}
    for osis_id, pairs in verses.items():
        parts = osis_id.split('.')
        if len(parts) != 3 or parts[0] not in OSIS_BOOKS:
            continue
        book = OSIS_BOOKS[parts[0]]
        squeezed = collapse(pairs)
        spans = ranges_of(squeezed)
        if spans:
            out.setdefault(book, {})['%s:%s' % (parts[1], parts[2])] = (
                ''.join(c for c, _ in squeezed), spans)
    return out


def parse_usfx(path):
    with io.open(path, encoding='utf-8') as fh:
        doc = fh.read()
    out, book, chapter, verse = {}, None, None, None
    pairs, red, skip = [], 0, 0

    def flush():
        if book and chapter and verse and pairs:
            squeezed = collapse(pairs)
            spans = ranges_of(squeezed)
            if spans:
                out.setdefault(book, {})['%s:%s' % (chapter, verse)] = (
                    ''.join(c for c, _ in squeezed), spans)

    pos = 0
    for m in TAG.finditer(doc):
        text = doc[pos:m.start()]
        if verse and text and not skip:
            pairs.extend((ch, red > 0) for ch in text)
        pos = m.end()
        tag = m.group(0)
        name = re.match(r'</?([a-zA-Z]+)', tag)
        name = name.group(1) if name else ''
        if name in ('f', 'x', 'fe'):                    # footnotes, cross refs
            if tag.startswith('</'):
                skip = max(0, skip - 1)
            elif not tag.endswith('/>'):
                skip += 1
        elif name == 'book':
            code = re.search(r'id="([^"]+)"', tag)
            book = USFX_BOOKS.get(code.group(1)) if code else None
        elif name == 'c':
            c = re.search(r'id="([^"]+)"', tag)
            chapter = c.group(1) if c else chapter
        elif name == 'v':
            flush()
            v = re.search(r'id="([^"]+)"', tag)
            verse, pairs, red = (v.group(1) if v else None), [], 0
        elif name == 've':
            flush()
            verse, pairs, red = None, [], 0
        elif name == 'wj':
            red = 0 if tag.startswith('</') else red + 1
    flush()
    return out


WORD = re.compile(r"[A-Za-z\u2019']+")


def _anchor(words, text, start_at=0, from_end=False):
    """Find a run of words in `text`, returning its character span."""
    if not words:
        return None
    probe = words if not from_end else words
    hits = []
    for m in WORD.finditer(text, start_at):
        if m.group(0).lower() != probe[0].lower():
            continue
        pos, ok, end = m.start(), True, m.end()
        it = WORD.finditer(text, m.start())
        for want in probe:
            try:
                nxt = next(it)
            except StopIteration:
                ok = False
                break
            if nxt.group(0).lower() != want.lower():
                ok = False
                break
            end = nxt.end()
        if ok:
            hits.append((pos, end))
            if len(hits) > 1:
                return None            # ambiguous, refuse to guess
    return hits[0] if len(hits) == 1 else None


def relocate(src_text, spans, mine):
    """Place a span in our text when the two editions are not identical.

    Whole-span matching fails whenever the editions differ *inside* the quote,
    which the WEB revisions do often ("out of the mouth of God" against "out
    of God's mouth"). Only the edges of a span decide where the colour starts
    and stops, so the first and last few words are anchored and whatever lies
    between them is taken as spoken.
    """
    out = []
    cursor = 0
    for lo, hi in spans:
        piece = src_text[lo:hi]
        at = mine.find(piece, cursor)
        if at >= 0 and mine.find(piece, at + 1) < 0:
            out.append([at, at + len(piece)])
            cursor = at + len(piece)
            continue
        words = WORD.findall(piece)
        if len(words) < 6:
            return None                # too short to anchor safely
        head = _anchor(words[:4], mine, cursor)
        if not head:
            return None
        tail = _anchor(words[-4:], mine, head[0])
        if not tail or tail[1] <= head[0]:
            return None
        out.append([head[0], tail[1]])
        cursor = tail[1]
    return out or None


def verify(parsed, field):
    """Keep only spans whose offsets are right for the text we ship."""
    kept, exact, relocated, dropped = {}, 0, 0, 0
    for book, entries in parsed.items():
        path = os.path.join(DATA, 'verses_%s.json' % book.replace(' ', ''))
        if not os.path.exists(path):
            dropped += len(entries)
            continue
        with io.open(path, encoding='utf-8') as fh:
                # A few verses carry no WEB text at all — the ones that edition
            # omits, such as Acts 8:37 — so there is nothing to colour.
            ours = {'%d:%d' % (r['c'], r['v']): r[field]
                    for r in json.load(fh) if field in r}
        for key, (src_text, spans) in entries.items():
            mine = ours.get(key)
            if mine is None:
                dropped += 1
                continue
            if mine == src_text:
                kept.setdefault(book, {})[key] = spans
                exact += 1
                continue
            found = relocate(src_text, spans, mine)
            if found:
                kept.setdefault(book, {})[key] = found
                relocated += 1
            else:
                dropped += 1
    return kept, exact, relocated, dropped


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 1
    result = {}
    for label, parser, field, path in (('kjv', parse_osis, 'kjv', argv[0]),
                                       ('web', parse_usfx, 'web', argv[1])):
        parsed = parser(path)
        kept, exact, relocated, dropped = verify(parsed, field)
        verses = sum(len(v) for v in kept.values())
        spans = sum(len(s) for v in kept.values() for s in v.values())
        print('%-4s %5d verses, %5d spans across %2d books '
              '(%d exact, %d relocated, %d dropped)'
              % (label, verses, spans, len(kept), exact, relocated, dropped))
        result[label] = kept

    out = os.path.join(DATA, 'redletter.json')
    with io.open(out, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    print('wrote %s (%.0f KB)' % (out, os.path.getsize(out) / 1024))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
