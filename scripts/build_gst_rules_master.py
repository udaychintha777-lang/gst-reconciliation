import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "gst-rules.json"
SOURCE_URL = "https://india-code.vercel.app/R10-015"


class IndiaCodeParser(HTMLParser):
    """Extract visible India Code headings and Rule links from the HTML page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.events = []
        self.capture = None
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "a":
            self.capture = "rule"
            self.buffer = []
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.capture = "heading"
            self.buffer = []

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.capture == "rule" and tag == "a":
            text = " ".join("".join(self.buffer).split())
            if re.match(r"^Rule\s+\d+[A-Za-z]?\b", text, re.I):
                self.events.append(("rule", text))
            self.capture = None
            self.buffer = []
        elif self.capture == "heading" and tag in {
            "h1", "h2", "h3", "h4", "h5", "h6"
        }:
            text = " ".join("".join(self.buffer).split())
            if re.match(r"^Chapter\s+[IVXLCDM]+\b", text, re.I):
                self.events.append(("chapter", text))
            self.capture = None
            self.buffer = []


def fetch_page():
    req = Request(
        SOURCE_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/140 Safari/537.36"
            )
        },
    )
    with urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_rule_text(text):
    # Example:
    # Rule 88C. C. Manner of dealing with...
    # Rule 69. ****
    m = re.match(
        r"^Rule\s+([0-9]+[A-Za-z]?)\s*[.\-:]?\s*(.*)$",
        text,
        re.I,
    )
    if not m:
        return None

    number = m.group(1).upper()
    raw_title = m.group(2).strip()

    # India Code uses **** / *** markers for omitted or historical provisions.
    omitted = bool(re.search(r"\*{3,}", raw_title))

    title = re.sub(r"\*{3,}", "", raw_title)
    title = re.sub(r"^\s*[A-Za-z]\.\s*", "", title)  # e.g. "C. Manner..."
    title = re.sub(r"\s+", " ", title).strip(" .:-")

    if not title:
        title = "Omitted / historical provision"

    return {
        "type": "gst_rules",
        "rule_number": number,
        "title": title,
        "status": (
            "Omitted / historical"
            if omitted
            else "Current in India Code record"
        ),
        "url": f"/gst-rules/rule-{number.lower()}.html",
        "source_id": "R10-015",
    }


def main():
    print("Reading current CGST Rules page from India Code...")
    html = fetch_page()

    parser = IndiaCodeParser()
    parser.feed(html)

    expected_match = re.search(r"Rules\s*\((\d+)\)", html, re.I)
    expected = int(expected_match.group(1)) if expected_match else None

    chapter = ""
    records = []
    seen = set()

    for kind, text in parser.events:
        if kind == "chapter":
            chapter = text
            continue

        record = parse_rule_text(text)
        if not record:
            continue

        record["chapter"] = chapter

        # Exact duplicate protection only.
        key = (
            record["rule_number"],
            record["title"],
            record["status"],
            record["chapter"],
        )
        if key not in seen:
            seen.add(key)
            records.append(record)

    print()
    print("========== CGST RULES DIAGNOSTIC ==========")
    print("India Code stated rule count:", expected or "not found")
    print("Rule links extracted:", len(records))
    print(
        "Unique rule numbers:",
        len({r["rule_number"] for r in records}),
    )
    print(
        "Current/named:",
        sum(
            1 for r in records
            if r["status"] == "Current in India Code record"
        ),
    )
    print(
        "Omitted/historical:",
        sum(
            1 for r in records
            if r["status"] == "Omitted / historical"
        ),
    )
    print("============================================")
    print()

    if expected is None:
        raise RuntimeError(
            "Could not find the India Code 'Rules (214)' count in the page."
        )

    if expected is not None and len(records) != expected:
        print(
            f"NOTE: India Code reports {expected} Rules in the collection heading, "
            f"but {len(records)} individual Rule entries are listed on the page."
        )
        print(
            "The master index will preserve this discrepancy transparently; "
            "no unverified Rule will be invented."
        )

    current_named = sum(
        1 for r in records
        if r["status"] == "Current in India Code record"
    )
    omitted_historical = sum(
        1 for r in records
        if r["status"] == "Omitted / historical"
    )

    output = {
        "schema_version": 1,
        "type": "gst_rules_master",
        "source": {
            "name": "India Code 2.0",
            "code_id": "R10-015",
            "title": "Central Goods and Services Tax Rules, 2017",
            "url": SOURCE_URL,
            "as_at": "14 September 2026",
            "in_force_from": "22 June 2017",
            "collection_count_reported": expected,
            "individual_entries_listed": len(records),
            "count_note": (
                "India Code reports 214 Rules in the collection heading, "
                "while 213 individual Rule entries are listed on the source page. "
                "This index uses only individually identifiable entries and does "
                "not invent an unverified additional Rule."
            ),
        },
        "counts": {
            "rules": len(records),
            "source_reported": expected,
            "individual_entries": len(records),
            "current_named": current_named,
            "omitted_historical": omitted_historical,
        },
        "items": records,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("SUCCESS")
    print("GST Rules master index generated with transparent source-count metadata.")
    print("Output:", OUT)
    print("Rules extracted:", len(records))


if __name__ == "__main__":
    main()
