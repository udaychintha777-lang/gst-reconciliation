# AdSense Readiness Audit — Initial Register

Repository: udaychintha777-lang/gst-reconciliation
Audit branch: adsense-audit-2026-11
Audit baseline: 22 November 2026
Production branch: main (not modified)

## Sitemap inventory
- Total URLs: 535
- Article pages: 127
- CGST Act section pages: 174
- GST Rule pages: 213
- Other pages, indexes and tools: 21

## Confirmed source-level issues from sampled pages
1. About page is brief and generic; strengthen publisher identity, editorial accountability and contact information without inventing qualifications.
2. Privacy policy needs tool-specific disclosure based on actual implementation, especially file processing, storage, retention, analytics, advertising and third-party dependencies.
3. questions.html is a small JavaScript-driven page; inspect its underlying dataset and verify usefulness and crawlability.
4. Sampled statutory pages gst-act/section-1.html, gst-rules/rule-1.html and gst-rules/rule-37.html were missing canonical tags. Self-referencing canonical tags have now been added on the audit branch. Rule 37 sample has about 219 visible words and needs substantive legal/practical treatment.
5. Sampled articles.html and reconciliation.html already contain canonical tags. They are not canonical defects. However, articles.html has a confirmed taxonomy problem: 49 of its 127 article cards were labelled GSTR-2B Reconciliation, including unrelated sector guides, notices and general GST topics. The 127-card index has now been reclassified on the audit branch; category filter behavior still needs browser QA.
6. Sampled E-Way Bill expired article already contains canonical, description and Article schema.
7. Confirmed overlapping topic clusters: employee recoveries; insurance claims/salvage; grants/subsidies/CSR; liquidated damages/penalties; advances/deposits; guarantees. Do not delete, redirect or merge until a full content comparison and explicit approval.
8. Article sample shows inconsistent metadata/schema coverage. The Blocked ITC guide is a strong existing design/content reference and must be preserved.
9. The 127-card article index originally had 8 category labels and overused GSTR-2B Reconciliation on 49 cards. Category labels and visible badges have been reclassified on the audit branch without changing the card design. Current distribution: Sector-specific GST 18; GST Notices & Litigation 2; GSTR-2B Reconciliation 10; GST ITC 42; GST General 31; ISD / GSTR-6 3; GSTR-7 3; GSTR-1 12; GSTR-3B 5; E-Invoice 1. The dynamic filter needs browser QA.

## Important audit qualification
This register contains every URL from the current sitemap. Only rows marked Source sample reviewed have a confirmed page-specific finding from source inspection. Rows marked Pending individual page review are audit work items, not asserted defects. The source audit corrected false positives caused by attribute-order-sensitive HTML parsing; the article listing, reconciliation tool and E-Way Bill article have canonical tags. A complete live audit additionally requires browser/mobile interaction testing, Google Search Console coverage/indexing data, Core Web Vitals, AdSense policy-center details and real-file tool QA.

## Non-destructive policy
No production files have been modified. Three canonical tags were added only on the audit branch to gst-act/section-1.html, gst-rules/rule-1.html and gst-rules/rule-37.html. The 127-card article index taxonomy was also corrected on the audit branch. The privacy policy was rewritten on the audit branch. Any content consolidation, URL retirement, redirects, page deletion, author claims, legal interpretations, or changes affecting data processing require review and approval before implementation.