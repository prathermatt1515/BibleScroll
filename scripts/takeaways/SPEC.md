# Writing takeaways

A "key takeaway" is ONE sentence (occasionally two short ones) stating **what
that specific verse turns on**. It appears in the app under the verse's
commentary.

It is NOT a summary of the commentary, NOT a paraphrase of the verse, and NOT
a devotional exhortation. It tells the reader something they might have walked
past.

Target 50–125 characters, averaging ~90. **Plain text only — no HTML.**

## Voice

From the finished Matthew (narrative):

- `1:6` — "\"Her that had been the wife of Urias\" — David's worst hour is left in the record rather than edited out."
- `20:15` — "\"Is thine eye evil, because I am good?\" Generosity to another is resented as though it were theft."
- `25:25` — "\"I was afraid.\" Fear of the master produced a life with nothing to show."
- `26:50` — "\"Friend, wherefore art thou come?\" He calls Judas friend at the moment of the arrest."
- `27:42` — "\"He saved others; himself he cannot save.\" A taunt that states the gospel exactly."

From the finished Ephesians (epistle — closer to what most of these books are):

- `2:9` — "Works are excluded because boasting must be, and that silence is where peace starts."
- `4:3` — "The Spirit made the unity. We are told to keep it, never to create it."
- `5:25` — "The husband's command is not to rule but to die."
- `6:12` — "The person opposite you is not the opponent."
- `6:24` — "Grace is not the introduction to this letter's subject. It is the subject."

Often a short quoted phrase from the verse, then the observation. Concrete.
Unsentimental. Willing to name what is uncomfortable. **No exclamation marks**
(except inside a KJV quotation that has one), no "Wow", no second-person
exhortation ("You should…"). It observes; it does not instruct.

## Theological register

A Lutheran reading, held lightly — law and gospel distinguished, righteousness
received rather than achieved, assurance located in Christ rather than in the
believer's own state, ordinary work treated as calling. Most lines are simply
careful observation of the text; do not make this heavy-handed, and do not
force it onto verses where it does not belong.

## Coverage

Leave OUT verses carrying no standalone point: bare connectives, travel notes,
greeting and name lists, the lead-in half of a quotation formula, and any verse
where you would end up repeating a neighbouring line.

- **Epistles** are dense argument — expect 85–95%.
- **Narrative** (Acts) and **apocalyptic** (Revelation) run lower — expect 75–88%.

Never pad to raise the number. An omitted verse is better than a filler line,
and a filler line is the exact thing this whole feature replaced.

## Hard requirements

- Every line unique **within the book**. No two verses share a takeaway.
- Keys are valid `"chapter:verse"` strings that exist in that book.
- No HTML (`<em>`, `<strong>`, `<br>`).
- Double-quoted Python strings; escape inner double quotes as `\"`.

## File format

One file per book at `scripts/takeaways/<module>.py`:

```python
#!/usr/bin/env python3
"""Written one-line takeaways for <Book>."""

TAKEAWAYS = {
    # ---- Chapter 1 ----
    '1:1': "...",
}
```

Append later chapters with `TAKEAWAYS.update({...})` blocks so you can work in
batches. Group with `# ---- Chapter N ----` comments.
