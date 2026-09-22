#!/usr/bin/env python3
"""Drop APPLY IT cards whose text is reused across verses.

The card asks the reader a question about the verse in front of them. Most of
them are genuinely particular — "Which category describes your response to
correction: understanding, simple, or scorner?" — but 218 lines are templates
stamped across thousands of verses, one of them 586 times. A question that
fits 586 different verses is not about any of them, and it sits directly
under the takeaways, which exist precisely because a filler line is worse
than no line.

Same rule as a takeaway: if it is reusable it is not specific, so it goes.
"""
import io
import json
import collections
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
DATA_JS = os.path.join(HERE, '..', 'data.js')


def main():
    files = sorted(glob.glob(os.path.join(DATA, 'study_*.json')))
    counts = collections.Counter()
    for path in files:
        with io.open(path, encoding='utf-8') as fh:
            for entry in json.load(fh).values():
                text = (entry.get('apply') or '').strip()
                if text:
                    counts[text] += 1

    # James is inline in data.js and shares the same source, so it is counted
    # with the rest rather than judged on its own.
    js = io.open(DATA_JS, encoding='utf-8').read()
    for text in re.findall(r'"apply":\s*"((?:[^"\\]|\\.)*)"', js):
        if text.strip():
            counts[text.strip()] += 1

    reused = {t for t, n in counts.items() if n > 1}
    print('%d distinct lines reused, covering %d cards'
          % (len(reused), sum(counts[t] for t in reused)))

    kept = dropped = 0
    for path in files:
        with io.open(path, encoding='utf-8') as fh:
            study = json.load(fh)
        changed = False
        for entry in study.values():
            text = (entry.get('apply') or '').strip()
            if not text:
                continue
            if text in reused:
                entry.pop('apply', None)
                dropped += 1
                changed = True
            else:
                kept += 1
        if changed:
            with io.open(path, 'w', encoding='utf-8') as fh:
                fh.write(json.dumps(study, ensure_ascii=False,
                                    separators=(', ', ': ')))

    js_dropped = 0
    def strip_one(m):
        nonlocal js_dropped
        if m.group(1).strip() in reused:
            js_dropped += 1
            return '"apply": ""'
        return m.group(0)
    new_js = re.sub(r'"apply":\s*"((?:[^"\\]|\\.)*)"', strip_one, js)
    if js_dropped:
        io.open(DATA_JS, 'w', encoding='utf-8').write(new_js)

    total = kept + dropped + js_dropped
    print('kept %d, dropped %d (%d in data.js) — coverage %d%% of %d verses'
          % (kept, dropped + js_dropped, js_dropped,
             round(100.0 * kept / total), total))


if __name__ == '__main__':
    main()
