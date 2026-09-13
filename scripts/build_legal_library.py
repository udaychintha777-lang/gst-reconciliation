#!/usr/bin/env python3
"""
Build the GST Legal Library index from HTML files in the repository.

This is a SAFE first-stage script:
- It does NOT modify your existing gst-act.html, app.js, sections.json or articles.
- It only scans legal-content folders and creates data/legal-library.json.
- Existing gst-act/section-1.html ... section-174.html files remain untouched.
"""

from pathlib import Path
from html.parser import HTMLParser
import json
import re
import datetime

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "legal-library.json"

# These are the folders the new library will support.
FOLDERS = {
    "gst-act": "GST Act",
    "gst-rules": "GST Rules",
    "notifications": "Notifications",
    "circulars": "Circulars",
    "orders": "Orders",
}

EXCLUDE = ("-backup", "_backup", "backup.", ".bak", ".old", ".tmp")
IGNORE_DIRS = {".git", ".github", "node_modules", "venv", "__pycache__"}


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1 = ""
        self.meta = {}
        self._title = False
        self._h1 = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "title":
            self._title = True
        elif tag == "h1":
            self._h1 = True
        elif tag == "meta":
            name = (d.get("name") or "").strip().lower()
            if name:
                self.meta[name] = d.get("content", "").strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False
        elif tag == "h1":
            self._h1 = False

    def handle_data(self, data):
        if self._title:
            self.title += data
        elif self._h1 and not self.h1:
            self.h1 += data


def parse_html(path):
    parser = MetaParser()
    try:
        parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        pass

    title = " ".join(parser.title.split())
    h1 = " ".join(parser.h1.split())
    title = title or h1 or path.stem.replace("-", " ").title()

    return parser.meta, title


def included(path):
    if path.suffix.lower() != ".html":
        return False
    if any(x in path.name.lower() for x in EXCLUDE):
        return False
    parts = {p.lower() for p in path.relative_to(ROOT).parts}
    if parts & IGNORE_DIRS:
        return False
    return True


def relative_url(path):
    return "/" + path.relative_to(ROOT).as_posix()


def detect_item(root_folder, path, meta, title):
    rel = path.relative_to(root_folder).as_posix()
    stem = path.stem

    item = {
        "title": meta.get("legal-title") or meta.get("title") or title,
        "url": relative_url(path),
        "category": FOLDERS[root_folder.name],
        "source_file": path.relative_to(ROOT).as_posix(),
    }

    # Existing structure: gst-act/section-1.html
    m = re.fullmatch(r"section-(\d+[A-Za-z]?)", stem, re.I)
    if root_folder.name == "gst-act" and m:
        item["type"] = "cgst-section"
        item["number"] = m.group(1)
        item["chapter"] = meta.get("chapter", "")
        item["status"] = meta.get("status", "active")
        return item

    # Future schedule support: gst-act/schedules/schedule-1.html
    m = re.fullmatch(r"schedule-(.+)", stem, re.I)
    if root_folder.name == "gst-act" and "schedule" in Path(rel).parts:
        item["type"] = "schedule"
        item["number"] = m.group(1) if m else ""
        item["chapter"] = meta.get("chapter", "")
        return item

    # Future rules: gst-rules/rule-1.html
    m = re.fullmatch(r"rule-(.+)", stem, re.I)
    if root_folder.name == "gst-rules" and m:
        item["type"] = "gst-rule"
        item["number"] = m.group(1)
        return item

    # Everything else can use explicit metadata, or a sensible folder type.
    defaults = {
        "notifications": "notification",
        "circulars": "circular",
        "orders": "order",
    }
    item["type"] = meta.get("content-type", defaults.get(root_folder.name, root_folder.name))
    item["number"] = meta.get("number", "")
    item["date"] = meta.get("date", "")
    item["subject"] = meta.get("subject", "")
    return item


def main():
    DATA_DIR.mkdir(exist_ok=True)

    items = []

    for folder_name in FOLDERS:
        folder = ROOT / folder_name
        if not folder.exists():
            continue

        for path in folder.rglob("*.html"):
            if not included(path):
                continue

            meta, title = parse_html(path)
            items.append(detect_item(folder, path, meta, title))

    def sort_key(x):
        category_order = {
            "GST Act": 1,
            "GST Rules": 2,
            "Notifications": 3,
            "Circulars": 4,
            "Orders": 5,
        }
        number = x.get("number", "")
        try:
            number_key = (0, int(re.match(r"\d+", number).group()))
        except Exception:
            number_key = (1, number)
        return (category_order.get(x["category"], 99), number_key, x["title"].lower())

    items.sort(key=sort_key)

    output = {
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "version": 1,
        "items": items,
        "counts": {
            "gst_act": sum(i["category"] == "GST Act" for i in items),
            "gst_rules": sum(i["category"] == "GST Rules" for i in items),
            "notifications": sum(i["category"] == "Notifications" for i in items),
            "circulars": sum(i["category"] == "Circulars" for i in items),
            "orders": sum(i["category"] == "Orders" for i in items),
            "schedules": sum(i["type"] == "schedule" for i in items),
        },
    }

    OUTPUT.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("GST Legal Library index generated.")
    print(f"Output: {OUTPUT}")
    print(f"Total HTML legal pages found: {len(items)}")
    print("Counts:", output["counts"])


if __name__ == "__main__":
    main()
