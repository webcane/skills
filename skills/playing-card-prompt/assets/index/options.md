# Index options (NOT a wizard step)

The index is the corner marker on each card. This is an **advanced setting**: the wizard
does NOT ask about it. The assembly always applies the DEFAULTS for the card's index
type (standard or joker). Only if the user explicitly requests a change ("make it
jumbo", "no indices", "side-by-side") do you swap in the alternative text from the
menus here.

There are two INDEX_LINE construction paths, selected by `index.type`:
- **`standard`** (default) — rank letter + suit symbol, assembled from Menus A/B/C.
- **`joker`** — symbol-only (no rank letter, no suit symbol), assembled from Menus A/D2.
  The assembler automatically uses `joker` when the card group is `joker`.

---

## Standard INDEX_LINE (index.type = "standard")

### Defaults (applied silently)
- Size: **Standard**
- Count: **4-Index** (all four corners)
- Layout: **Rank stacked above suit**

### Composed default `[INDEX_LINE]`
```
four corner indices, each with rank [RANK_LETTER] stacked above suit symbol [SUIT_SYMBOL], standard small index size, upper indices upright, lower indices rotated 180 degrees,
```

### Menu A — Size
| Option             | Text fragment                                              |
|--------------------|------------------------------------------------------------|
| Standard (default) | `standard small index size`                                |
| Jumbo              | `jumbo oversized indices`                                  |
| Magnum             | `magnum extra-large indices spanning much of the card width` |

### Menu B — Count / placement
| Option            | Text fragment                                                                  |
|-------------------|--------------------------------------------------------------------------------|
| 4-Index (default) | `four corner indices` + `upper indices upright, lower indices rotated 180 degrees` |
| 2-Index           | `indices in two opposite corners (top-left and bottom-right)`                  |

### Menu C — Layout
| Option                 | Text fragment                                                        |
|------------------------|----------------------------------------------------------------------|
| Stacked (default)      | `rank [RANK_LETTER] stacked above suit symbol [SUIT_SYMBOL]`         |
| Side-by-side           | `rank [RANK_LETTER] and suit symbol [SUIT_SYMBOL] side by side`      |
| Peek / Dual-Squeeze    | (add to any of the above) `plus tiny peek mini-indices at the corner tips` |
| Traditional (no index) | `no corner indices; rank is readable only from the count of pip symbols` |

To build a non-default standard `[INDEX_LINE]`, combine one fragment from each of B, C,
and A (in that reading order) and keep the trailing comma.

---

## Joker INDEX_LINE (index.type = "joker")

Used automatically when the card group is `joker`. No rank letter, no suit symbol —
only the glyph from `index.symbol` appears in each corner index.

### Defaults (applied silently for Joker)
- Size: **Standard** (`index.size`)
- Count / placement: **4-corner** (`index.count = "4-index"`)
- Symbol: **star-in-circle** (`index.symbol = "star-in-circle"`)

### Composed default Joker `[INDEX_LINE]`
```
four corner indices, each showing a star enclosed in a circle glyph,
no rank letter, no suit symbol, standard small index size,
upper indices upright, lower indices rotated 180 degrees,
```

### Menu D2 — Placement (Joker)
| Option               | `index.count`  | Text fragment                                       |
|----------------------|----------------|-----------------------------------------------------|
| 4-corner (default)   | `"4-index"`    | `four corner indices` + rotation fragment           |
| 2-corner             | `"2-index"`    | `two corner indices (top-left and bottom-right)`    |
| Top-only             | `"top-only"`   | `single top-left index only`                        |
| None / Full-bleed    | `"none"`       | _(replaces entire INDEX_LINE — see below)_          |

When `index.count = "none"` for a Joker, drop the full composed INDEX_LINE and emit
only:
```
no corner indices, full-bleed illustration,
```

### Symbol descriptions (for `index.symbol`)
| Config value     | Phrase used in INDEX_LINE                    |
|------------------|----------------------------------------------|
| `star-in-circle` | `a star enclosed in a circle glyph`          |
| `star`           | `a five-pointed star`                        |
| `Jkr`            | `the text "Jkr"`                             |
| `J`              | `the letter "J"`                             |
| `crown`          | `a small crown glyph`                        |
| `jester-face`    | `a stylized jester face glyph`               |
| `none`           | _(same as `index.count = "none"` — full-bleed)_ |
| custom text      | used verbatim                                |

To build a non-default Joker `[INDEX_LINE]`, choose one row from D2 and one from the
Symbol table, combine with the size fragment from Menu A, and keep the trailing comma.
