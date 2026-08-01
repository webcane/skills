#!/usr/bin/env python3
"""
Scan a Logseq mm-wiki graph and emit a JSON report used by mm-wiki-lint,
mm-wiki-status, and mm-wiki-prune. Stdlib only — no dependencies required,
so it runs the same way under any code agent.

Usage:
  python3 wiki_scan.py <pages_dir> [--access-log <path>]

Output (JSON to stdout): pages, hubs, links, orphans, broken_refs,
index_drift, credential_hits, empty_pages, access_log entries, etc.
Every check here is deterministic (regex/graph traversal) — the calling
skill is responsible for judgment calls (is this orphan actually fine?,
should this really be demoted?).
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

PROP_RE = re.compile(r"^\s*-?\s*([a-zA-Z][a-zA-Z0-9_-]*)::\s*(.*)$")
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
TAG_RE = re.compile(r"(?<!\])#([a-zA-Z][\w-]*)")
INDEX_LINE_RE = re.compile(r"\[\[([^\]]+)\]\]\s*--\s*(.*)$")
SECTION_RE = re.compile(r"^\s*-?\s*###\s+(Index|Archive)\s*$")
HEADING_RE = re.compile(r"^\s*-?\s*#{1,6}\s")

CRED_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+]{8,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"\bsk-[A-Za-z0-9]{20,}\b",
        r"\bghp_[A-Za-z0-9]{20,}\b",
    ]
]


def filename_to_page(path: Path) -> str:
    return path.stem.replace("___", "/")


def page_to_filename(page: str) -> str:
    return page.replace("/", "___") + ".md"


def parse_page(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    props = {}
    i = 0
    while i < len(lines):
        m = PROP_RE.match(lines[i])
        if not m:
            break
        props[m.group(1)] = m.group(2).strip()
        i += 1

    body_lines = lines[i:]
    body_text = "\n".join(body_lines)
    links = LINK_RE.findall(body_text)
    tags = TAG_RE.findall(body_text)

    non_empty_body = [ln for ln in body_lines if ln.strip() not in ("", "-")]
    is_empty = len(non_empty_body) == 0

    cred_hits = []
    for pat in CRED_PATTERNS:
        for m in pat.finditer(text):
            snippet = text[max(0, m.start() - 20):m.end() + 5]
            if snippet not in cred_hits:
                cred_hits.append(snippet)

    # Hub Index/Archive sections
    index_entries, archive_entries = [], []
    section = None
    for ln in lines:
        sm = SECTION_RE.match(ln)
        if sm:
            section = sm.group(1)
            continue
        if HEADING_RE.match(ln) and not sm:
            section = None
            continue
        if section:
            im = INDEX_LINE_RE.search(ln)
            if im:
                entry = {"page": im.group(1), "description": im.group(2).strip()}
                (index_entries if section == "Index" else archive_entries).append(entry)

    return {
        "page": filename_to_page(path),
        "file": path.name,
        "properties": props,
        "links": sorted(set(links)),
        "tags": sorted(set(tags)),
        "is_empty": is_empty,
        "credential_hits": cred_hits,
        "index_entries": index_entries,
        "archive_entries": archive_entries,
    }


def build_report(pages_dir: Path, access_log_path: Optional[Path]) -> dict:
    files = sorted(pages_dir.glob("*.md"))
    pages = {}
    for f in files:
        info = parse_page(f)
        pages[info["page"]] = info

    all_page_names = set(pages.keys())

    # Backlink graph
    incoming = {name: set() for name in all_page_names}
    broken_refs = []
    for name, info in pages.items():
        for target in info["links"]:
            if target in all_page_names:
                incoming[target].add(name)
            elif target not in all_page_names:
                broken_refs.append({"from": name, "to": target})

    orphans = [
        name for name, info in pages.items()
        if info["properties"].get("type") != "hub"
        and not incoming.get(name)
        and not info["properties"].get("access-log")
    ]

    hubs = {name: info for name, info in pages.items() if info["properties"].get("type") == "hub"}

    # Index drift: routing line with no matching page, or archived page still in Index,
    # or active page with no routing line anywhere.
    routed_pages = set()
    orphaned_routing_lines = []
    archived_in_live_index = []
    for hub_name, hub in hubs.items():
        for entry in hub["index_entries"]:
            routed_pages.add(entry["page"])
            if entry["page"] not in all_page_names:
                orphaned_routing_lines.append({"hub": hub_name, "entry": entry})
            elif pages.get(entry["page"], {}).get("properties", {}).get("archived"):
                archived_in_live_index.append({"hub": hub_name, "entry": entry})
        for entry in hub["archive_entries"]:
            routed_pages.add(entry["page"])

    unroutable = [
        name for name, info in pages.items()
        if info["properties"].get("type") not in ("hub",)
        and not info["properties"].get("access-log")
        and name not in routed_pages
    ]

    missing_index_description = [
        {"hub": hub_name, "entry": entry}
        for hub_name, hub in hubs.items()
        for entry in hub["index_entries"]
        if not entry["description"]
    ]

    empty_pages = [name for name, info in pages.items() if info["is_empty"]]
    credential_leaks = [
        {"page": name, "hits": info["credential_hits"]}
        for name, info in pages.items() if info["credential_hits"]
    ]
    no_outgoing_links = [
        name for name, info in pages.items()
        if not info["links"] and info["properties"].get("type") != "hub"
        and not info["properties"].get("access-log")
    ]

    access_log = []
    if access_log_path and access_log_path.exists():
        log_text = access_log_path.read_text(encoding="utf-8", errors="replace")
        for ln in log_text.splitlines():
            parts = [p.strip() for p in ln.split(" -- ")]
            if len(parts) >= 3 and re.match(r"^\d{4}-\d{2}-\d{2}", parts[0].lstrip("- ")):
                date = parts[0].lstrip("- ").strip()
                page_m = LINK_RE.search(parts[1])
                if page_m:
                    access_log.append({"date": date, "page": page_m.group(1), "raw": ln.strip()})

    return {
        "pages_dir": str(pages_dir),
        "page_count": len(pages),
        "pages": pages,
        "hub_count": len(hubs),
        "hubs": list(hubs.keys()),
        "orphans": orphans,
        "broken_refs": broken_refs,
        "orphaned_routing_lines": orphaned_routing_lines,
        "archived_in_live_index": archived_in_live_index,
        "unroutable_active_pages": unroutable,
        "missing_index_description": missing_index_description,
        "empty_pages": empty_pages,
        "credential_leaks": credential_leaks,
        "pages_with_no_outgoing_links": no_outgoing_links,
        "access_log": access_log,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages_dir")
    ap.add_argument("--access-log", default=None, help="Path to Wiki___Reference___Access-Log.md")
    args = ap.parse_args()

    pages_dir = Path(args.pages_dir)
    if not pages_dir.is_dir():
        print(json.dumps({"error": f"pages_dir not found: {pages_dir}"}))
        sys.exit(1)

    access_log_path = Path(args.access_log) if args.access_log else pages_dir / "Wiki___Reference___Access-Log.md"
    report = build_report(pages_dir, access_log_path)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
