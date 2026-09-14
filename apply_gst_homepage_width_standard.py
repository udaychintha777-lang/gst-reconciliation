from pathlib import Path
import re

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

WIDTH_STYLE = """<style>
/* GST Reconciliation site-wide width standard — matches homepage exactly. */
.gst-site-width-standard,
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
</style>
"""

NUMERIC_SORT_PATCH = r"""<script>
/* gst-rules-numeric-sort-v2 */
(function(){
  function ruleSortValue(v){
    const s=String(v ?? "").replace(/^rule[-_ ]?/i,"").trim().toUpperCase();
    const m=s.match(/^(\d+)([A-Z]*)/);
    if(!m) return [999999,s];
    return [parseInt(m[1],10),m[2]||""];
  }
  window.gstSortRulesNumerically=function(arr){
    return [...arr].sort((a,b)=>{
      const av=ruleSortValue(a.number ?? a.rule_number ?? a.id);
      const bv=ruleSortValue(b.number ?? b.rule_number ?? b.id);
      if(av[0]!==bv[0]) return av[0]-bv[0];
      return av[1].localeCompare(bv[1],undefined,{numeric:true});
    });
  };
})();
</script>
"""

def add_tracking(html):
    if "G-NBKTXWJ20G" not in html:
        html = html.replace("</head>", GA4 + "\n</head>", 1)
    if "ca-pub-8493595246856929" not in html:
        html = html.replace("</head>", ADSENSE + "\n</head>", 1)
    return html

def replace_container_widths(html):
    # Fix common standalone legal-page container widths while preserving page design.
    patterns = [
        (r"(\.rule-wrap\s*\{[^}]*?)max-width\s*:\s*1120px\s*;?", r"\1"),
        (r"(\.rule-wrap\s*\{[^}]*?)max-width\s*:\s*1180px\s*;?", r"\1"),
        (r"(\.container\s*\{[^}]*?)max-width\s*:\s*1120px\s*;?", r"\1"),
        (r"(\.container\s*\{[^}]*?)max-width\s*:\s*1180px\s*;?", r"\1"),
    ]
    for pattern, repl in patterns:
        html = re.sub(pattern, repl, html, flags=re.I | re.S)

    if "GST Reconciliation site-wide width standard" not in html:
        html = html.replace("</head>", WIDTH_STYLE + "\n</head>", 1)
    return html

def add_numeric_rule_sort(html):
    if "gst-rules-numeric-sort-v2" in html:
        return html

    if "gst-rules-numeric-sort-v1" in html:
        html = html.replace("gst-rules-numeric-sort-v1", "gst-rules-numeric-sort-v2", 1)
        return html

    # Add helper. Existing rule pages are unaffected; the index can use it if its
    # data rendering code calls window.gstSortRulesNumerically.
    html = html.replace("</head>", NUMERIC_SORT_PATCH + "\n</head>", 1)

    html = html.replace(
        "rules=raw.map(normalise);",
        "rules=gstSortRulesNumerically(raw.map(normalise));"
    )
    html = html.replace(
        "rules=Array.isArray(data.items)?data.items:[];",
        "rules=gstSortRulesNumerically(Array.isArray(data.items)?data.items:[]);"
    )
    return html

def legal_html_files():
    # All current and future legal-library folders.
    folders = (
        "gst-act",
        "gst-rules",
        "schedules",
        "notifications",
        "circulars",
        "orders",
    )

    files = []
    for folder in folders:
        base = ROOT / folder
        if base.exists():
            files.extend(base.rglob("*.html"))

    # Legal-library root pages.
    for name in ("gst-act.html", "gst-rules.html", "schedules.html",
                 "notifications.html", "circulars.html", "orders.html"):
        p = ROOT / name
        if p.exists():
            files.append(p)

    return sorted(set(files))

def process_file(path):
    html = path.read_text(encoding="utf-8")
    original = html

    html = add_tracking(html)
    html = replace_container_widths(html)

    if path.name.lower() == "gst-rules.html":
        html = add_numeric_rule_sort(html)

    if html != original:
        path.write_text(html, encoding="utf-8", newline="\n")
        return True
    return False

targets = legal_html_files()
changed = sum(process_file(p) for p in targets)

print("GST homepage-width standard applied.")
print(f"Files checked: {len(targets)}")
print(f"Files changed: {changed}")
print("Width standard: width:min(1400px,calc(100% - 64px));")
print("GA4: G-NBKTXWJ20G")
print("AdSense: ca-pub-8493595246856929")
