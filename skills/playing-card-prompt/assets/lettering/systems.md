# Court-Card Lettering Systems

The visible index **letter** on court cards depends on the deck's language/region.
The descriptive RANK_NAME stays English (King / Queen / Jack) so the image model
understands it; only RANK_LETTER (the printed index) changes.

| System                      | King letter | Queen letter | Jack letter |
|-----------------------------|-------------|--------------|-------------|
| Anglo-American (default)    | K           | Q            | J           |
| French                      | R (Roi)     | D (Dame)     | V (Valet)   |
| German / Austrian           | K (König)   | D (Dame)     | B (Bube)    |
| Russian / Soviet            | К           | Д            | В           |
| Dutch                       | H (Heer)    | V (Vrouw)    | B (Boer)    |
| Scandinavian (SE/DK)        | K           | D            | Kn (Knekt)  |

## How RANK_LETTER is set
- Court cards (King/Queen/Jack): use the letter from the chosen system above.
- Ace: defaults to `A` (some systems print `1` — ask only if the user cares).
- Number cards 2–10: the numeral itself; lettering system does not apply.

Present the systems to the user as tappable options. Default to Anglo-American.
