#!/usr/bin/env python3
"""Apply written takeaways from scripts/takeaways/<book>.py to the study data.

Only verses with a written line get one. Verses left out — genealogy links,
bare connectives, the lead-in half of a quotation — keep no takeaway at all,
and the drawer hides the card rather than showing filler.

James is stored differently from every other book: its verses and study data
are inlined in data.js as JAMES_VERSES and STUDY_DATA rather than living in
data/. It is patched in place there.

Usage: apply_takeaways.py matthew mark ...   (or `all` for every module present)
"""
import glob
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'takeaways'))
DATA = os.path.join(HERE, '..', 'data')
DATA_JS = os.path.join(HERE, '..', 'data.js')

# module name -> study file stem in data/
STEMS = {
    'genesis': 'Genesis', 'exodus': 'Exodus', 'leviticus': 'Leviticus',
    'numbers': 'Numbers', 'deuteronomy': 'Deuteronomy', 'joshua': 'Joshua',
    'judges': 'Judges', 'ruth': 'Ruth',
    'samuel1': '1Samuel', 'samuel2': '2Samuel',
    'kings1': '1Kings', 'kings2': '2Kings',
    'chronicles1': '1Chronicles', 'chronicles2': '2Chronicles',
    'ezra': 'Ezra', 'nehemiah': 'Nehemiah', 'esther': 'Esther', 'job': 'Job',
    'psalms': 'Psalms', 'proverbs': 'Proverbs',
    'ecclesiastes': 'Ecclesiastes', 'song': 'SongofSolomon',
    'isaiah': 'Isaiah', 'jeremiah': 'Jeremiah',
    'lamentations': 'Lamentations', 'ezekiel': 'Ezekiel', 'daniel': 'Daniel',
    'hosea': 'Hosea', 'joel': 'Joel', 'amos': 'Amos', 'obadiah': 'Obadiah',
    'jonah': 'Jonah', 'micah': 'Micah', 'nahum': 'Nahum',
    'habakkuk': 'Habakkuk', 'zephaniah': 'Zephaniah', 'haggai': 'Haggai',
    'zechariah': 'Zechariah', 'malachi': 'Malachi',
    'matthew': 'Matthew', 'mark': 'Mark', 'luke': 'Luke', 'john': 'John',
    'acts': 'Acts', 'romans': 'Romans',
    'corinthians1': '1Corinthians', 'corinthians2': '2Corinthians',
    'galatians': 'Galatians', 'ephesians': 'Ephesians',
    'philippians': 'Philippians', 'colossians': 'Colossians',
    'thessalonians1': '1Thessalonians', 'thessalonians2': '2Thessalonians',
    'timothy1': '1Timothy', 'timothy2': '2Timothy',
    'titus': 'Titus', 'philemon': 'Philemon', 'hebrews': 'Hebrews',
    'peter1': '1Peter', 'peter2': '2Peter',
    'john1': '1John', 'john2': '2John', 'john3': '3John',
    'jude': 'Jude', 'revelation': 'Revelation',
}
JAMES = 'james'


def check(name, written, verse_keys):
    stray = sorted(set(written) - set(verse_keys))
    if stray:
        raise SystemExit('%s: takeaway for verses that do not exist: %s'
                         % (name, ', '.join(stray[:10])))
    dupes = len(written) - len(set(written.values()))
    if dupes:
        raise SystemExit('%s: %d duplicate takeaways' % (name, dupes))
    html = [k for k, v in written.items() if '<' in v]
    if html:
        raise SystemExit('%s: HTML in %s' % (name, ', '.join(html[:5])))


def apply_book(module_name):
    stem = STEMS[module_name]
    written = importlib.import_module(module_name).TAKEAWAYS
    path = os.path.join(DATA, 'study_%s.json' % stem)
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)
    check(stem, written, study)
    for key, entry in study.items():
        line = written.get(key)
        if line:
            entry['takeaway'] = line
        else:
            entry.pop('takeaway', None)
    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    return stem, len(study), len(written)


def apply_james():
    written = importlib.import_module(JAMES).TAKEAWAYS
    with io.open(DATA_JS, encoding='utf-8') as fh:
        src = fh.read()
    m = re.search(r'(const STUDY_DATA = )(\{.*\})(;\s*)$', src, re.S)
    if not m:
        raise SystemExit('data.js: could not find STUDY_DATA')
    study = json.loads(m.group(2))
    check('James', written, study)
    for key, entry in study.items():
        line = written.get(key)
        if line:
            entry['takeaway'] = line
        else:
            entry.pop('takeaway', None)
    rebuilt = src[:m.start(2)] + json.dumps(study, ensure_ascii=False) + m.group(3)
    with io.open(DATA_JS, 'w', encoding='utf-8') as fh:
        fh.write(rebuilt)
    return 'James', len(study), len(written)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    if argv == ['all']:
        here = os.path.join(HERE, 'takeaways')
        argv = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(here, '*.py'))
                      if os.path.basename(f) != '__init__.py')
    for name in argv:
        if name == JAMES:
            stem, verses, written = apply_james()
        elif name in STEMS:
            stem, verses, written = apply_book(name)
        else:
            raise SystemExit('unknown book module: %s' % name)
        print('%-16s %5d of %5d verses have a written takeaway (%d%%)'
              % (stem, written, verses, 100 * written // verses))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
