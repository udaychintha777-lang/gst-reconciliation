from pathlib import Path
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

GA4 = """<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NBKTXWJ20G"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){dataLayer.push(arguments);}
gtag('js',new Date());
gtag('config','G-NBKTXWJ20G');
</script>
"""

ADSENSE = """<!-- Google AdSense -->
<script async
  src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8493595246856929"
  crossorigin="anonymous"></script>
"""

WIDTH_CSS = """
/* GST Reconciliation site-wide width standard — matches homepage exactly. */
.wrap,
.legal-wrap,
.rule-wrap,
.section-wrap,
.section-page-wrap,
.legal-container,
.legal-page-wrap,
.site-container,
main.container,
header .container,
.hero .container,
footer .container {
  width: min(1400px, calc(100% - 64px));
  max-width: none;
  margin-left: auto;
  margin-right: auto;
  box-sizing: border-box;
}
"""

def add_tracking(html):
    if "G-NBKTXWJ20G" not in html:
        html = html.replace("</head>", GA4 + "\n</head>", 1)
    if "ca-pub-8493595246856929" not in html:
        html = html.replace("</head>", ADSENSE + "\n</head>", 1)
    return html

def add_width_standard(html):
    if "GST Reconciliation site-wide width standard" not in html:
        html = html.replace("</head>", "<style>" + WIDTH_CSS + "</style>\n</head>", 1)

    # Replace the known arbitrary outer widths used by the legal pages.
    replacements = [
        (r"\.rule-wrap\s*\{\s*max-width\s*:\s*1120px\s*;", ".rule-wrap{width:min(1400px,calc(100% - 64px));max-width:none;"),
        (r"\.container\s*\{\s*max-width\s*:\s*1120px\s*;", ".container{width:min(1400px,calc(100% - 64px));max-width:none;"),
        (r"\.container\s*\{\s*max-width\s*:\s*1180px\s*;", ".container{width:min(1400px,calc(100% - 64px));max-width:none;"),
        (r"\.container\s*\{\s*width\s*:\s*min\(1180px,\s*calc\(100% - 40px\)\s*\);", ".container{width:min(1400px,calc(100% - 64px));"),
    ]
    for pattern, repl in replacements:
        html = re.sub(pattern, repl, html, flags=re.I)

    return html

def numeric_rule_sort_patch(html):
    # Ensure rule index renders numerically, so Rule 9 comes before Rule 10,
    # Rule 10A after Rule 10, etc.
    if "gst-rules-numeric-sort-v1" in html:
        return html

    marker = "/* gst-rules-numeric-sort-v1 */"
    patch = f"""
<style>
{marker}
</style>
<script>
(function(){{
  function gstRuleSortValue(v){{
    const s=String(v ?? "").replace(/^rule[-_ ]?/i,"").trim().toUpperCase();
    const m=s.match(/^(\\d+)([A-Z]*)/);
    if(!m) return [999999,s];
    const n=parseInt(m[1],10);
    const suffix=m[2]||"";
    return [n,suffix];
  }}
  window.gstSortRulesNumerically=function(arr){{
    return [...arr].sort((a,b)=>{{
      const av=gstRuleSortValue(a.number ?? a.rule_number ?? a.id);
      const bv=gstRuleSortValue(b.number ?? b.rule_number ?? b.id);
      if(av[0]!==bv[0]) return av[0]-bv[0];
      return av[1].localeCompare(bv[1],undefined,{{numeric:true}});
    }});
  }};
}})();
</script>
"""
    html = html.replace("</head>", patch + "\n</head>", 1)

    # Patch the common rule-index assignment patterns.
    html = html.replace(
        "rules=raw.map(normalise);",
        "rules=gstSortRulesNumerically(raw.map(normalise));"
    )
    html = html.replace(
        "rules=Array.isArray(data.items)?data.items:[];",
        "rules=gstSortRulesNumerically(Array.isArray(data.items)?data.items:[]);"
    )
    return html

def process_file(path):
    html = path.read_text(encoding="utf-8")
    original = html

    html = add_tracking(html)
    html = add_width_standard(html)

    # Rule index sorting only applies to the root GST Rules page.
    if path.name.lower() == "gst-rules.html":
        html = numeric_rule_sort_patch(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False

targets = []

for folder in ("gst-act", "gst-rules"):
    base = ROOT / folder
    if base.exists():
        targets.extend(base.rglob("*.html"))

for root_name in ("gst-act.html", "gst-rules.html"):
    p = ROOT / root_name
    if p.exists():
        targets.append(p)

changed = 0
for p in sorted(set(targets)):
    if process_file(p):
        changed += 1

print(f"GST homepage-width standard applied.")
print(f"Files checked: {len(set(targets))}")
print(f"Files changed: {changed}")
print("Width standard: width:min(1400px,calc(100% - 64px));")
print("GA4: G-NBKTXWJ20G")
print("AdSense: ca-pub-8493595246856929")
