#!/usr/bin/env python3
"""Snapshot one source into studies/<lang>/sources/ and register it in the manifest.

Example:
    scripts/add_source.py --lang rust --kind paper --url https://... --title "Region types"
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    Parser,
    EXIT_OK,
    EXIT_PRECONDITION,
    EXIT_USAGE,
    KIND_LABELS,
    KINDS,
    fail,
    load_json,
    ok,
    save_json,
    sha256_bytes,
    slugify,
    studies_root,
    study_dir,
)

USER_AGENT = "pl-dialectics/1.0 (+source snapshot)"
TIMEOUT = 30


class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer"}
    BLOCK = {"p", "div", "section", "article", "li", "tr", "h1", "h2", "h3", "h4", "br"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self.SKIP:
            self._skip_depth += 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]
        return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def html_to_text(markup: str) -> str:
    parser = _TextExtractor()
    parser.feed(markup)
    return parser.text()


def guess_extension(url: str, content_type: str) -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower() if url else ""
    if suffix in {".html", ".htm", ".xhtml"}:
        return ".html"
    if suffix == ".pdf":
        return ".pdf"
    if suffix in {".md", ".markdown"}:
        return ".md"
    if suffix == ".txt":
        return ".txt"
    if "pdf" in content_type:
        return ".pdf"
    if "html" in content_type:
        return ".html"
    if "markdown" in content_type:
        return ".md"
    return ".txt"


def fetch(url: str, script: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.read(), response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        fail(
            script,
            EXIT_PRECONDITION,
            f"HTTP {exc.code} while fetching {url}",
            "the source is gone, paywalled, or blocks automated downloads",
            "download it manually and pass --file <path> instead",
        )
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        fail(
            script,
            EXIT_PRECONDITION,
            f"cannot reach {url}: {exc}",
            "no network, DNS failure, or a TLS restriction in this environment",
            "retry, or download manually and pass --file <path>",
        )
    return b"", ""


def read_file(path: Path, script: str) -> tuple[bytes, str]:
    try:
        return path.read_bytes(), path.suffix.lower()
    except OSError as exc:
        fail(
            script,
            EXIT_PRECONDITION,
            f"cannot read {path}: {exc}",
            "the path is wrong or unreadable",
            "check the path and retry",
        )
    return b"", ""


def render_manifest(manifest: dict) -> str:
    lines = [
        f"# Sources — {manifest['language']}",
        "",
        f"Schema version {manifest['schema_version']}. Machine-readable twin: `manifest.json`.",
        "Add sources with `scripts/add_source.py`; do not edit by hand.",
        "",
        "| ID | Kind | Title | Locator | Snapshot | SHA-256 |",
        "|----|------|-------|---------|----------|---------|",
    ]
    for item in manifest["sources"]:
        locator = item.get("url") or item.get("origin", "")
        lines.append(
            "| {id} | {kind} | {title} | {locator} | {snapshot} | {sha} |".format(
                id=item["id"],
                kind=item["kind"],
                title=item["title"].replace("|", "\\|"),
                locator=locator.replace("|", "\\|"),
                snapshot=item["snapshot"],
                sha=item["sha256"][:16],
            )
        )
    if not manifest["sources"]:
        lines.append("| — | — | no sources yet | — | — | — |")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(
        prog="add_source.py",
        description=(
            "Download (or copy) one source, write a text extraction next to it, and append "
            "a stable SRC-nn entry to studies/<lang>/manifest.json."
        ),
        epilog=(
            "examples:\n"
            "  scripts/add_source.py --lang rust --kind spec \\\n"
            "      --url https://doc.rust-lang.org/reference/ --title 'The Rust Reference'\n"
            "  scripts/add_source.py --lang rust --kind paper --file ~/papers/regions.pdf \\\n"
            "      --title 'Region-based memory management'\n"
            "\n"
            "kinds: " + ", ".join(f"{k} ({KIND_LABELS[k]})" for k in KINDS) + "\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--lang", required=True, help="language of the study, e.g. rust")
    parser.add_argument("--kind", required=True, choices=KINDS, help="source class")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="fetch the source over HTTP(S)")
    source.add_argument("--file", help="copy an already-downloaded source")
    parser.add_argument("--title", required=True, help="human title used in citations")
    parser.add_argument(
        "--locator",
        default="",
        help="citation locator hint, e.g. 'ch. 4.2' or 'RFC 2094'; defaults to the URL/path",
    )
    parser.add_argument("--note", default="", help="why this source matters (one line)")
    parser.add_argument("--root", default=None, help="studies directory (default: ./studies)")
    parser.add_argument(
        "--dry-run", action="store_true", help="print what would be written, change nothing"
    )
    return parser


def main(argv: list[str]) -> int:
    script = "add_source"
    parser = build_parser()
    if not argv:
        parser.print_usage(sys.stderr)
        print(
            "  hint: --lang, --kind, --title and one of --url/--file are required\n"
            "  run --help for all options and the list of kinds",
            file=sys.stderr,
        )
        return EXIT_USAGE
    args = parser.parse_args(argv)

    slug = slugify(args.lang)
    directory = study_dir(studies_root(args.root), slug)
    manifest_path = directory / "manifest.json"
    manifest = load_json(manifest_path, script)

    if args.url:
        payload, content_type = fetch(args.url, script)
        extension = guess_extension(args.url, content_type)
        origin = args.url
    else:
        file_path = Path(args.file).expanduser()
        payload, suffix = read_file(file_path, script)
        extension = suffix if suffix in {".html", ".htm", ".pdf", ".md", ".markdown", ".txt"} else ".txt"
        content_type = "application/pdf" if extension == ".pdf" else ""
        origin = str(file_path)

    digest = sha256_bytes(payload)
    for existing in manifest["sources"]:
        if existing["sha256"] == digest:
            fail(
                script,
                EXIT_USAGE,
                f"duplicate source: same bytes as {existing['id']} ({existing['title']})",
                "the same document must keep one ID so citations stay stable",
                "reuse the existing ID, or pick a different document",
            )
        if args.url and existing.get("url") == args.url:
            fail(
                script,
                EXIT_USAGE,
                f"duplicate URL already registered as {existing['id']}",
                "one URL maps to one SRC id",
                f"cite {existing['id']}, or remove it first",
            )

    next_number = len(manifest["sources"]) + 1
    while any(item["id"] == f"SRC-{next_number:02d}" for item in manifest["sources"]):
        next_number += 1
    source_id = f"SRC-{next_number:02d}"
    snapshot_name = f"{source_id}{extension if extension != '.htm' else '.html'}"
    text_name = f"{source_id}.txt"

    if args.dry_run:
        ok(f"dry-run: would write {directory / 'sources' / snapshot_name}")
        ok(f"dry-run: would register {source_id} ({args.kind}) {args.title}")
        return EXIT_OK

    sources_dir = directory / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    (sources_dir / snapshot_name).write_bytes(payload)

    text = ""
    if extension in {".html", ".htm"}:
        text = html_to_text(payload.decode("utf-8", errors="replace"))
    elif extension in {".md", ".markdown", ".txt"}:
        text = payload.decode("utf-8", errors="replace")
    elif extension == ".pdf":
        text = "[binary PDF snapshot; no text extraction available without external tools]"
    (sources_dir / text_name).write_text(text, encoding="utf-8")

    entry = {
        "id": source_id,
        "kind": args.kind,
        "title": args.title.strip(),
        "url": args.url or "",
        "origin": origin,
        "locator": args.locator.strip() or origin,
        "note": args.note.strip(),
        "snapshot": f"sources/{snapshot_name}",
        "text": f"sources/{text_name}",
        "sha256": digest,
        "bytes": len(payload),
        "added": date.today().isoformat(),
        "extracted_chars": len(text),
    }
    manifest["sources"].append(entry)
    save_json(manifest_path, manifest)
    (directory / "MANIFEST.md").write_text(render_manifest(manifest), encoding="utf-8")

    ok(f"added {source_id} ({args.kind}) {entry['title']}")
    ok(f"  snapshot: {entry['snapshot']} ({len(payload)} bytes, sha256 {digest[:16]})")
    ok(f"  text:     {entry['text']} ({len(text)} chars extracted)")
    if extension == ".pdf":
        ok("  note: PDF text is not extracted; cite the PDF locator directly")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
