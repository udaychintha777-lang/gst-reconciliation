#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import quote
import re, html, json, datetime

ROOT=Path(__file__).resolve().parents[1]
ARTICLES_DIR=ROOT/"articles"
INDEX_FILE=ROOT/"articles.html"
SITEMAP_FILE=ROOT/"sitemap.xml"
SITE="https://gstreconciliation.in"
EXCLUDE_PATTERNS=("-backup","_backup","backup.",".bak",".old",".tmp")
IGNORE_DIRS={".git",".github","node_modules","venv","__pycache__"}
CATEGORY_RULES=[
("GSTR-2B Reconciliation",["gstr-2b","gstr2b","reconciliation","purchase register","itc reconciliation"]),
("GSTR-1",["gstr-1","gstr1"]),("GSTR-3B",["gstr-3b","gstr3b"]),
("GSTR-9C",["gstr-9c","gstr9c"]),("GSTR-9",["gstr-9","gstr9"]),
("GSTR-7",["gstr-7","gstr7","gst tds"]),("ISD / GSTR-6",["gstr-6","gstr6","isd"]),
("E-Invoice",["e-invoice","einvoice","e invoice"]),("GST TDS / TCS",["gst tds","gst tcs","gstr-8"]),
("GST ITC",["itc","input tax credit"])]

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__();self.title="";self.h1="";self.meta={};self._title=False;self._h1=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=="title":self._title=True
        if tag=="h1":self._h1=True
        if tag=="meta":
            n=(d.get("name") or "").strip().lower()
            if n:self.meta[n]=d.get("content","").strip()
    def handle_endtag(self,tag):
        if tag=="title":self._title=False
        if tag=="h1":self._h1=False
    def handle_data(self,data):
        if self._title:self.title+=data
        if self._h1 and not self.h1:self.h1+=data

def parse_article(path):
    p=MetaParser()
    try:p.feed(path.read_text(encoding="utf-8",errors="ignore"))
    except Exception:pass
    title=" ".join(p.title.split()) or " ".join(p.h1.split()) or path.stem.replace("-"," ").title()
    desc=p.meta.get("description","")
    category=p.meta.get("article-category","") or p.meta.get("category","")
    hay=(path.stem+" "+title+" "+desc).lower()
    if not category:
        for cat,keys in CATEGORY_RULES:
            if any(k in hay for k in keys):category=cat;break
    return {"path":path,"title":title,"description":desc,"category":category or "GST General"}

def esc(v):return html.escape(v,quote=True)

def article_card(a):
    rel="/"+a["path"].relative_to(ROOT).as_posix()
    desc=a["description"] or ("Practical guide covering "+a["title"]+".")
    if len(desc)>170:desc=desc[:167].rsplit(" ",1)[0]+"..."
    return f'''<a class="article-card" href="{esc(rel)}" data-category="{esc(a["category"])}">
  <span class="badge">{esc(a["category"])}</span>
  <h3>{esc(a["title"])}</h3>
  <p>{esc(desc)}</p>
  <span class="read">Read guide →</span>
</a>'''

def update_index(articles):
    text=INDEX_FILE.read_text(encoding="utf-8")
    start="<!-- AUTO_ARTICLES_START -->";end="<!-- AUTO_ARTICLES_END -->"
    if start not in text or end not in text:raise RuntimeError("articles.html is missing AUTO_ARTICLES markers.")
    articles=sorted(articles,key=lambda a:(0 if "reconcil" in a["category"].lower() else 1,a["title"].lower()))
    cards="\n".join(article_card(a) for a in articles)
    s=text.index(start)+len(start);e=text.index(end)
    text=text[:s]+"\n"+cards+"\n "+text[e:]
    itemlist={"@context":"https://schema.org","@type":"ItemList","name":"GST Knowledge Articles",
              "itemListElement":[{"@type":"ListItem","position":i+1,"name":a["title"],
              "url":SITE+"/"+a["path"].relative_to(ROOT).as_posix()} for i,a in enumerate(articles)]}
    schema='<script type="application/ld+json" id="articleListSchema">\n'+json.dumps(itemlist,ensure_ascii=False,indent=2)+'\n</script>'
    pattern=r'<script type="application/ld\+json" id="articleListSchema">.*?</script>'
    text=re.sub(pattern,schema,text,flags=re.S) if re.search(pattern,text,flags=re.S) else text.replace("</head>",schema+"\n</head>")
    INDEX_FILE.write_text(text,encoding="utf-8")
    return len(articles)

def should_include(path):
    if path.suffix.lower()!=".html":return False
    if any(x in path.name.lower() for x in EXCLUDE_PATTERNS):return False
    if {p.lower() for p in path.relative_to(ROOT).parts}&IGNORE_DIRS:return False
    return True

def make_sitemap():
    urls=set()
    for p in ROOT.rglob("*.html"):
        if should_include(p):
            rel=p.relative_to(ROOT).as_posix()
            urls.add(SITE+"/" if rel=="index.html" else SITE+"/"+quote(rel,safe="/-_.~"))
    today=datetime.date.today().isoformat()
    lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in sorted(urls):
        last=f"<lastmod>{today}</lastmod>" if url in {SITE+"/articles.html",SITE+"/reconciliation.html",SITE+"/compliance.html"} else ""
        lines.append(f"  <url><loc>{html.escape(url,quote=True)}</loc>{last}</url>")
    lines.append("</urlset>")
    SITEMAP_FILE.write_text("\n".join(lines)+"\n",encoding="utf-8")
    return len(urls)

def main():
    ARTICLES_DIR.mkdir(exist_ok=True)
    articles=[]
    for p in ARTICLES_DIR.rglob("*.html"):
        if any(x in p.name.lower() for x in EXCLUDE_PATTERNS):continue
        a=parse_article(p)
        if a:articles.append(a)
    print(f"Generated articles.html with {update_index(articles)} article(s).")
    print(f"Generated sitemap.xml with {make_sitemap()} URL(s).")

if __name__=="__main__":main()
