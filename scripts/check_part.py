#!/usr/bin/env python3
"""Check one takeaway part file before it is merged.

Usage: check_part.py scripts/takeaways/parts/genesis_01_25.py Genesis [1 25]

Verifies the keys exist in that book, that nothing is written twice, that no
line carries HTML, and reports coverage over the chapter range so you can see
it against the bands in SPEC.md.
"""
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    path, stem = argv[0], argv[1]
    lo = int(argv[2]) if len(argv) > 2 else 1
    hi = int(argv[3]) if len(argv) > 3 else 10 ** 6

    spec = importlib.util.spec_from_file_location('part', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    written = mod.TAKEAWAYS

    with io.open(os.path.join(DATA, 'study_%s.json' % stem),
                 encoding='utf-8') as fh:
        keys = set(json.load(fh))
    in_range = {k for k in keys if lo <= int(k.split(':')[0]) <= hi}

    bad = []
    stray = sorted(set(written) - keys)
    if stray:
        bad.append('keys not in %s: %s' % (stem, ', '.join(stray[:8])))
    outside = sorted(set(written) - in_range - set(stray))
    if outside:
        bad.append('keys outside chapters %d-%d: %s'
                   % (lo, hi, ', '.join(outside[:8])))
    seen = {}
    for k, line in written.items():
        if line in seen:
            bad.append('same line at %s and %s' % (seen[line], k))
        seen[line] = k
        if '<' in line:
            bad.append('%s: HTML' % k)
        if not (30 <= len(line) <= 160):
            bad.append('%s: %d chars' % (k, len(line)))

    pct = 100.0 * len(written) / len(in_range) if in_range else 0
    print('%s: %d of %d verses in chapters %d-%d (%.1f%%)'
          % (os.path.basename(path), len(written), len(in_range), lo, hi, pct))
    for b in bad[:20]:
        print('  PROBLEM %s' % b)
    if len(bad) > 20:
        print('  ... and %d more' % (len(bad) - 20))
    if not bad:
        print('  OK')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
