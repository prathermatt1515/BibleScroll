#!/usr/bin/env python3
"""Apply written takeaways from scripts/takeaways/<book>.py to the study data.

Only verses with a written line get one. Verses left out — genealogy links,
bare connectives, the lead-in half of a quotation — keep no takeaway at all,
and the drawer hides the card rather than showing filler.

Usage: apply_takeaways.py matthew mark ...
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'takeaways'))
DATA = os.path.join(HERE, '..', 'data')

# module name -> study file stem
STEMS = {
    'matthew': 'Matthew', 'mark': 'Mark', 'luke': 'Luke', 'john': 'John',
}


def apply(module_name):
    stem = STEMS[module_name]
    written = importlib.import_module(module_name).TAKEAWAYS
    path = os.path.join(DATA, 'study_%s.json' % stem)
    with io.open(path, encoding='utf-8') as fh:
        study = json.load(fh)

    stray = sorted(set(written) - set(study))
    if stray:
        raise SystemExit('%s: takeaway for verses that do not exist: %s'
                         % (stem, ', '.join(stray)))
    dupes = len(written) - len(set(written.values()))
    if dupes:
        raise SystemExit('%s: %d duplicate takeaways' % (stem, dupes))

    for key, entry in study.items():
        line = written.get(key)
        if line:
            entry['takeaway'] = line
        else:
            entry.pop('takeaway', None)

    with io.open(path, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(study, ensure_ascii=False, separators=(', ', ': ')))
    return len(study), len(written)


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    for name in argv:
        verses, written = apply(name)
        print('%-10s %5d of %5d verses have a written takeaway (%d%%)'
              % (STEMS[name], written, verses, 100 * written // verses))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
