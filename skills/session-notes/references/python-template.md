# Python Template

**Extends `language-reference.md`.**
Read that file first for the full section structure, then apply the Python-specific additions below.

---

## Python-specific additions

### Синтаксис → code blocks

Use ` ```python ` (not ` ```<lang> `).

### Эквивалент — Python patterns

Common cases where the short form should always be shown alongside the explicit equivalent:

- List / dict / set comprehensions vs `for` loop + `.append()`
- Generator expressions vs explicit generator function
- `@decorator` vs `func = decorator(func)`
- `with` statement vs `try/finally`
- Walrus operator `:=` vs pre-assignment

### Как работает — Python-specific mechanics to cover when relevant

- **Замыкания (closures):** inner function captures a reference to the variable, not its value at definition time
- **`*args / **kwargs`:** always use in wrapper functions so the decorator works with any signature
- **`functools.wraps`:** preserves `__name__`, `__doc__`, and signature — omitting it silently breaks introspection and tools like `help()`
- **GIL:** relevant for threading topics — CPU-bound threads don't run in parallel, I/O-bound do
- **Mutable default arguments:** `def f(x=[])` — the list is created once at function definition, not per call
- **Late binding in closures:** variables in closures are looked up at call time, not at definition

### Подводные камни — recurring Python gotchas

Flag these when they are relevant to the topic:

- Mutable default argument (`def f(x=[])`)
- Late binding in closures (`lambda i=i` workaround)
- `is` vs `==` for identity vs equality
- Modifying a list while iterating over it
- `__name__` lost without `functools.wraps`
- Shallow vs deep copy (`copy` vs `copy.deepcopy`)
