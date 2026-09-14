#!/usr/bin/env python3
"""
FAST GST LEGAL LIBRARY REPAIR

Run from repository root:
    python scripts/build_all_gst_legal_library.py

Keeps gst-act.html untouched.
Reads data/gst-rules.json, creates every listed Rule page,
and regenerates data/legal-library.json.
"""
from pathlib import Path
import json, re, datetime

ROOT = Path(__file__).resolve().parents[1]
RULE_DATA = ROOT / "data" / "gst-rules.json"
RULE_DIR = ROOT / "gst-rules"
LEGAL_DATA = ROOT / "data" / "legal-library.json"

def esc(v):
    return (str(v or "").replace("&","&amp;").replace("<","&lt;")
            .replace(">","&gt;").replace('"',"&quot;"))

def make_page(item, prev_url="", next_url=""):
    n = item.get("rule_number","")
    title = item.get("title") or f"Rule {n}"
    chapter = item.get("chapter") or "CGST Rules"
    status = item.get("status") or "Current / source record"
    source = "https://india-code.vercel.app/R10-015"
    prev_html = f'<a class="side-link" href="{esc(prev_url)}">← Previous Rule</a>' if prev_url else ""
    next_html = f'<a class="side-link" href="{esc(next_url)}">Next Rule →</a>' if next_url else ""

    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rule {esc(n)} — {esc(title)} | GST Reconciliation</title>
<meta name="description" content="Rule {esc(n)} of the Central Goods and Services Tax Rules, 2017 — {esc(title)}.">
<style>
:root{{--bg:#f5f7fb;--navy:#10233f;--blue:#2563eb;--line:#dfe5ee;--muted:#667085}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:#172033;font-family:Arial,sans-serif}}
.nav{{background:var(--navy);color:#fff;padding:16px 24px}}.navin{{max-width:1180px;margin:auto;display:flex;justify-content:space-between;gap:20px;align-items:center}}
.nav a{{color:#fff;text-decoration:none;margin-left:18px;font-size:13px}}.brand{{font-weight:800;margin:0!important}}
.hero{{background:linear-gradient(135deg,#10233f,#173d69);color:#fff;padding:55px 24px}}
.wrap{{max-width:1180px;margin:auto}}.eyebrow{{font-size:12px;letter-spacing:1.4px;text-transform:uppercase;opacity:.75}}
h1{{font-family:Georgia,serif;font-size:42px;line-height:1.12;margin:12px 0}}.hero p{{max-width:850px;color:#d9e5f5;line-height:1.7}}
.grid{{max-width:1180px;margin:28px auto;padding:0 24px;display:grid;grid-template-columns:minmax(0,2fr) 320px;gap:22px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;margin-bottom:18px;box-shadow:0 4px 16px #10233f0b}}
h2{{margin-top:0;font-family:Georgia,serif}}p,li{{line-height:1.7}}.badge{{display:inline-block;padding:6px 10px;border-radius:999px;background:#dcfce7;color:#166534;font-size:12px;font-weight:700}}
.source a,.side-link{{color:var(--blue);text-decoration:none}}.side-link{{display:block;padding:9px 0}}
.notice{{background:#f8fafc;border-left:4px solid #94a3b8;padding:15px;border-radius:8px;color:#475467}}
.footer{{max-width:1180px;margin:20px auto;padding:30px 24px;color:#667085;border-top:1px solid var(--line);font-size:13px}}
@media(max-width:800px){{.grid{{grid-template-columns:1fr}}h1{{font-size:32px}}.navin{{display:block}}.nav a{{margin:10px 12px 0 0;display:inline-block}}}}
</style></head><body>
<header class="nav"><div class="navin"><a class="brand" href="/gst-act.html">GST Reconciliation · GST Legal Library</a>
<nav><a href="/gst-act.html">GST Act</a><a href="/gst-rules.html">GST Rules</a><a href="/articles.html">Articles</a></nav></div></header>
<section class="hero"><div class="wrap"><div class="eyebrow">Central Goods and Services Tax Rules, 2017</div>
<h1>Rule {esc(n)} — {esc(title)}</h1><p>{esc(chapter)} · {esc(status)}</p></div></section>
<main class="grid"><div>
<section class="card"><h2>Rule reference</h2>
<p><strong>Rule:</strong> {esc(n)}</p><p><strong>Subject:</strong> {esc(title)}</p><p><strong>Chapter:</strong> {esc(chapter)}</p>
<span class="badge">{esc(status)}</span></section>
<section class="card"><h2>Legal text and verification</h2>
<p>This is the Rule-wise reference page in the GSTReconciliation.in legal library. The statutory wording should be checked against the applicable consolidated Rules and amendment notifications for the relevant tax period.</p>
<div class="notice"><strong>Primary source:</strong> India Code 2.0 — Central Goods and Services Tax Rules, 2017. This automatically generated page does not invent or reproduce unverified statutory wording.</div>
<p class="source"><a href="{source}" target="_blank" rel="noopener">Open Central Goods and Services Tax Rules on India Code →</a></p></section>
<section class="card"><h2>Practical note</h2>
<p>GST Rules are amended through notifications. For professional or compliance use, verify the version applicable to the relevant date and the corresponding Gazette notification.</p></section>
</div>
<aside><section class="card"><h3>GST Rules navigation</h3>
<a class="side-link" href="/gst-act.html">← GST Legal Library</a><a class="side-link" href="/gst-rules.html">GST Rules index</a>{prev_html}{next_html}</section>
<section class="card"><h3>Disclaimer</h3><p>This is an educational and practical reference. It is not a substitute for the applicable statute, notifications, circulars, Gazette publications or professional advice.</p></section></aside></main>
<footer class="footer">GSTReconciliation.in · GST Legal Library · Educational reference</footer>
</body></html>"""

def main():
    if not RULE_DATA.exists():
        raise SystemExit(f"Missing {RULE_DATA}. Keep the existing data/gst-rules.json in the repository.")

    payload = json.loads(RULE_DATA.read_text(encoding="utf-8"))
    items = payload.get("items", [])
    if not items:
        raise SystemExit("data/gst-rules.json contains no Rule items.")

    def key(x):
        m = re.match(r"(\d+)(.*)", str(x.get("rule_number","")))
        return (int(m.group(1)) if m else 99999, (m.group(2) if m else "").lower())
    items = sorted(items, key=key)

    RULE_DIR.mkdir(parents=True, exist_ok=True)
    rule_records = []

    for i, item in enumerate(items):
        n = str(item.get("rule_number","")).strip()
        if not n:
            continue
        filename = f"rule-{n.lower()}.html"
        prev_url = f"/gst-rules/rule-{items[i-1].get('rule_number','').lower()}.html" if i else ""
        next_url = f"/gst-rules/rule-{items[i+1].get('rule_number','').lower()}.html" if i < len(items)-1 else ""
        (RULE_DIR / filename).write_text(make_page(item, prev_url, next_url), encoding="utf-8")

        rule_records.append({
            "title": f"Rule {n} — {item.get('title','')}",
            "url": f"/gst-rules/{filename}",
            "category": "GST Rules",
            "source_file": f"gst-rules/{filename}",
            "type": "gst-rule",
            "number": n,
            "chapter": item.get("chapter",""),
            "status": item.get("status",""),
        })

    # Preserve existing Act/other records and replace only the Rules category.
    old_records = []
    if LEGAL_DATA.exists():
        try:
            old = json.loads(LEGAL_DATA.read_text(encoding="utf-8"))
            old_records = [x for x in old.get("items", []) if x.get("category") != "GST Rules"]
        except Exception:
            pass

    all_items = old_records + rule_records
    counts = {
        "gst_act": sum(x.get("category") == "GST Act" for x in all_items),
        "gst_rules": len(rule_records),
        "notifications": sum(x.get("category") == "Notifications" for x in all_items),
        "circulars": sum(x.get("category") == "Circulars" for x in all_items),
        "orders": sum(x.get("category") == "Orders" for x in all_items),
        "schedules": sum(x.get("type") == "schedule" for x in all_items),
    }

    LEGAL_DATA.parent.mkdir(exist_ok=True)
    LEGAL_DATA.write_text(json.dumps({
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "version": 2,
        "items": all_items,
        "counts": counts
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print("GST LEGAL LIBRARY REPAIRED")
    print("Rule pages generated:", len(rule_records))
    print("Counts:", counts)

if __name__ == "__main__":
    main()
