# Sources — what to collect and how to cite it

A study is only as good as its source base. Gate G0 blocks writing until all five classes are
covered, because a missing class silently converts a gap into an inference.

## Five classes

| Kind | Minimum | What counts | Typical locator |
|------|---------|-------------|-----------------|
| `spec` | 1 | official specification, language reference, standard | section number, e.g. `§4.2` |
| `essay` | 1 | creator essay, design manifesto, rationale post | paragraph or heading |
| `paper` | 2 | peer-reviewed or widely cited academic paper | page or section |
| `release` | 1 | release history, changelog, RFC index, evolution document | version or RFC id |
| `retro` | 1 | critical retrospective, post-mortem, adversarial history | section |

Prefer primary sources. A blog post *about* the reference does not replace the reference. A
conference talk counts as `essay` only if the speaker is a designer of the language and the
transcript or slides exist.

## Collection order

1. `spec` — pin the version. Specifications change; record the version in the title.
2. `release` — this is where thresholds in Task B2 come from. Without it, B2 becomes guesswork.
3. `essay` — declared intent. Keep it separate from mechanism; it is layer (a).
4. `paper` — the external, formal view. Two is the floor, not a target.
5. `retro` — the adversarial view. One hostile source is worth three friendly ones.

## Citation format

```
[Source: SRC-03 The Rust Reference, §10.1]
[Source: SRC-07 RFC 2094 (non-lexical lifetimes), §3]
```

- `SRC-nn` must exist in `manifest.json`; the validator rejects unknown ids.
- The locator must be specific enough that a reader can find the sentence without reading the
  whole document.
- Quote at most two sentences. Long block quotes hide the argument.
- A claim that combines two sources gets two citations, not one averaged citation.

## Markers

| Marker | Use |
|--------|-----|
| `[UNSOURCED]` | your inference, no source supports it |
| `[DISPUTED]` | sources disagree; name both |
| `[NO CLEAR INSTANCE]` | the law or pattern has no instance in this language |

These markers are evidence of rigor, not failure. A study with zero markers is usually a study
that did not look.

## Missing classes

If a class genuinely does not exist for the language (e.g. no peer-reviewed literature for a
young language), record the gap in `quality-gates.md` notes and say so in Task A. Do not
substitute a weaker source silently. `check_sources.py --min-papers 0` is allowed only with a
written justification in `runs/source-exception.md`.

## Snapshots

`add_source.py` stores the raw bytes plus a text extraction:

- `sources/SRC-nn.html|.pdf|.md` — snapshot, hashed
- `sources/SRC-nn.txt` — extracted text used for reading and citation
- `manifest.json` — id, kind, title, locator, sha256, dates

PDFs are not text-extracted by the script; cite the PDF page directly and read it with the
host's PDF support.
