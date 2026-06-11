# Index options (NOT a wizard step)

The index is the rank+suit marker in the card corners. This is an **advanced setting**:
the wizard does NOT ask about it. The assembly always applies the DEFAULTS below to build
`[INDEX_LINE]`. Only if the user explicitly requests a different index ("make it jumbo",
"no indices", "side-by-side") do you swap in the alternative text from the menus here.

## Defaults (applied silently)
- Size: **Standard**
- Count: **4-Index** (all four corners)
- Layout: **Rank stacked above suit**

## Composed default `[INDEX_LINE]`
```
four corner indices, each with rank [RANK_LETTER] stacked above suit symbol [SUIT_SYMBOL], standard small index size, upper indices upright, lower indices rotated 180 degrees,
```

---

## Menu A — Size
| Option            | Text fragment                                             |
|-------------------|-----------------------------------------------------------|
| Standard (default)| `standard small index size`                               |
| Jumbo             | `jumbo oversized indices`                                 |
| Magnum            | `magnum extra-large indices spanning much of the card width`|

## Menu B — Count / placement
| Option            | Text fragment                                                                 |
|-------------------|-------------------------------------------------------------------------------|
| Regular 2-Index   | `indices in two opposite corners (top-left and bottom-right)`                  |
| 4-Index (default) | `four corner indices` + `upper indices upright, lower indices rotated 180 degrees`|

## Menu C — Layout
| Option                  | Text fragment                                                        |
|-------------------------|----------------------------------------------------------------------|
| Stacked (default)       | `rank [RANK_LETTER] stacked above suit symbol [SUIT_SYMBOL]`          |
| Side-by-side            | `rank [RANK_LETTER] and suit symbol [SUIT_SYMBOL] side by side`       |
| Peek / Dual-Squeeze     | (add to any of the above) `plus tiny peek mini-indices at the corner tips`|
| Traditional (no index)  | `no corner indices; rank is readable only from the count of pip symbols`|

To build a non-default `[INDEX_LINE]`, combine one fragment from each of B, C, and A
(in that reading order) and keep the trailing comma.
