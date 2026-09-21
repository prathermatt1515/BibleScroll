#!/usr/bin/env python3
"""Build data/verses_<Book>.json and data/study_<Book>.json for BibleScroll.

Sources (all public domain / open):
  KJV text        aruljohn/Bible-kjv
  WEB text        TehShrike/world-english-bible
  commentary,     kennethreitz/kjvstudy.org
  interlinear,
  cross-refs

Usage: build_book_data.py "Philippians" ["Colossians" ...]
"""
import gzip
import json
import os
import re
import sys

KJV_DIR = '/home/user/kjv-bible'
WEB_DIR = '/home/user/web-bible/json'
STUDY_DIR = '/home/user/kennethreitz/kjvstudy.org/kjvstudy_org/data'
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

EXPLAIN_MAX = 500
DEEPER_MAX = 1200   # Deeper study is the long read; Explain stays short
TAKEAWAY_MAX = 180

# Book name -> (kjv file stem, web file stem, commentary stem, xref stem, interlinear key)
# The interlinear keys one book under an older title than everything else.
INTERLINEAR_ALIASES = {'Song of Solomon': "Solomon's Song"}


def stems(book):
    squashed = book.replace(' ', '')
    return (squashed, squashed.lower(), book.replace(' ', '_').lower(),
            book.replace(' ', '_'), INTERLINEAR_ALIASES.get(book, book))


# ---------- HTML-aware trimming ----------
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)[^>]*>')
VOID_TAGS = {'br', 'hr', 'img', 'wbr'}


def visible_len(html):
    return len(TAG_RE.sub('', html))


def repair_html(html):
    """Drop a dangling partial tag and close any tags left open."""
    # A '<' with no matching '>' after it means we cut mid-tag.
    last_open = html.rfind('<')
    if last_open != -1 and html.find('>', last_open) == -1:
        html = html[:last_open]
    stack = []
    for m in TAG_RE.finditer(html):
        closing, name = m.group(1), m.group(2).lower()
        if name in VOID_TAGS:
            continue
        if closing:
            if stack and stack[-1] == name:
                stack.pop()
        else:
            stack.append(name)
    for name in reversed(stack):
        html += '</%s>' % name
    return html.rstrip()


def smart_trim(html, limit):
    """Trim to `limit` visible characters, preferring a sentence boundary.

    Never cuts inside an HTML tag and always returns balanced markup.
    """
    if not html:
        return ''
    html = html.strip()
    if visible_len(html) <= limit:
        return repair_html(html)

    # Walk the string tracking visible characters so tags don't count against
    # the budget, and remember the last sentence end we passed.
    visible = 0
    cut = None
    sentence_cut = None
    i = 0
    n = len(html)
    while i < n:
        m = TAG_RE.match(html, i)
        if m:
            i = m.end()
            continue
        ch = html[i]
        visible += 1
        i += 1
        if visible > limit:
            cut = i - 1
            break
        if ch in '.!?' and (i >= n or html[i] in ' \n<'):
            sentence_cut = i
    if cut is None:
        cut = n

    # Use the sentence boundary when it keeps at least 60% of the budget,
    # otherwise fall back to the last word boundary before the cut.
    if sentence_cut is not None and visible_len(html[:sentence_cut]) >= limit * 0.6:
        out = html[:sentence_cut]
    else:
        out = html[:cut]
        space = out.rfind(' ')
        if space > 0 and visible_len(out[:space]) >= limit * 0.5:
            out = out[:space]
        out = out.rstrip().rstrip(',;:—-') + '…'
    return repair_html(out)


# ---------- loaders ----------
_interlinear = None


def interlinear():
    global _interlinear
    if _interlinear is None:
        with gzip.open(os.path.join(STUDY_DIR, 'interlinear.json.gz')) as fh:
            _interlinear = json.load(fh)
    return _interlinear


def load_kjv(stem):
    with open(os.path.join(KJV_DIR, stem + '.json')) as fh:
        doc = json.load(fh)
    out = {}
    for ch in doc['chapters']:
        c = int(ch['chapter'])
        for v in ch['verses']:
            out[(c, int(v['verse']))] = ' '.join(v['text'].split())
    return out


def load_web(stem):
    path = os.path.join(WEB_DIR, stem + '.json')
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        doc = json.load(fh)
    parts = {}
    for item in doc:
        if 'chapterNumber' not in item or 'verseNumber' not in item:
            continue
        value = item.get('value')
        if not value:
            continue
        key = (int(item['chapterNumber']), int(item['verseNumber']))
        parts.setdefault(key, []).append(value)
    return {k: ' '.join(' '.join(v).split()) for k, v in parts.items()}


def load_commentary(stem):
    with open(os.path.join(STUDY_DIR, 'verse_commentary', stem + '.json')) as fh:
        doc = json.load(fh)
    out = {}
    for c, verses in doc.get('commentary', {}).items():
        for v, entry in verses.items():
            out[(int(c), int(v))] = entry
    return out


def load_xrefs(stem, book):
    path = os.path.join(STUDY_DIR, 'cross_references', stem + '.json')
    if not os.path.exists(path):
        return {}
    with open(path) as fh:
        doc = json.load(fh)
    out = {}
    for key, refs in doc.items():
        _, c, v = key.rsplit(':', 2)
        out[(int(c), int(v))] = [r['ref'] for r in refs if r.get('ref')]
    return out


def greek_for(book, c, v):
    entry = interlinear().get('%s:%d:%d' % (book, c, v))
    if not entry:
        return []
    # Only word, english and the definition are ever rendered; transliteration
    # is empty for every word in the source, and parsing/position are unused.
    # The definition itself is not stored per word: the same few thousand
    # Strong's entries repeat across 445,000 words, which is 32.5 MB of
    # duplication against 0.7 MB for data/strongs.json, which the app loads
    # once and looks up.
    return [{
        'word': w.get('original', ''),
        'strongs': w.get('strongs', ''),
        'english': w.get('english', ''),
    } for w in entry]


# ---------- build ----------
def build(book):
    kjv_stem, web_stem, comm_stem, xref_stem, il_key = stems(book)
    kjv = load_kjv(kjv_stem)
    web = load_web(web_stem)
    comm = load_commentary(comm_stem)
    xrefs = load_xrefs(xref_stem, book)

    keys = sorted(kjv)
    verses = [{'c': c, 'v': v, 'kjv': kjv[(c, v)], 'web': web.get((c, v), kjv[(c, v)])}
              for c, v in keys]

    study = {}
    for c, v in keys:
        entry = comm.get((c, v))
        explain = smart_trim(entry['analysis'], EXPLAIN_MAX) if entry else ''
        deeper = smart_trim(entry['historical'], DEEPER_MAX) if entry else ''
        questions = list(entry.get('questions') or []) if entry else []
        study['%d:%d' % (c, v)] = {
            'explain': explain,
            'deeper': deeper,
            'greek': greek_for(il_key, c, v),
            'related': xrefs.get((c, v), []),
            'takeaway': smart_trim(explain, TAKEAWAY_MAX),
            'apply': questions[0] if questions else '',
        }

    chapters = {}
    for c, v in keys:
        chapters[c] = max(chapters.get(c, 0), v)
    counts = [chapters[c] for c in sorted(chapters)]
    return verses, study, counts


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    for book in argv:
        verses, study, counts = build(book)
        stem = book.replace(' ', '')
        for name, payload in (('verses', verses), ('study', study)):
            path = os.path.join(OUT_DIR, '%s_%s.json' % (name, stem))
            with open(path, 'w') as fh:
                json.dump(payload, fh, ensure_ascii=False, separators=(', ', ': '))
        missing_web = sum(1 for x in verses if x['web'] == x['kjv'])
        no_comm = sum(1 for e in study.values() if not e['explain'])
        print('%-18s verses=%-5d chapters=%-3d no_commentary=%-4d web_fallback=%-4d'
              % (book, len(verses), len(counts), no_comm, missing_web))
        print('    %s: [%s]' % (book, ','.join(str(x) for x in counts)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
