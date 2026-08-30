# GST Reconciliation V12 — GitHub Pages Deployment

## 1. Upload to GitHub
Upload the contents of this `gstreconciliation-v12` folder to the repository currently serving `gstreconciliation.in`.

The package keeps the existing Purchase Register vs GSTR-2B reconciliation page as `reconciliation.html`. The reconciliation engine and browser-side workflow are preserved; only the public home-page design/navigation has been redesigned.

Important public files/folders:
- `index.html`
- `reconciliation.html`
- `articles.html`
- `questions.html`
- `gst-act.html`
- `articles/`
- `gst-act/`
- `tools/`
- `data/`
- `styles.css`, `app.js`, `tools.js`
- `assets/`
- `robots.txt`, `sitemap.xml`
- `CNAME`
- `favicon.svg`

## 2. GitHub Pages
Keep the existing custom domain `gstreconciliation.in` and the current HTTPS configuration. GitHub Pages supports custom domains; configure/confirm the domain in the repository Pages settings.

## 3. Google Analytics
The GA4 tag has been added using Measurement ID:
`G-NBKTXWJ20G`

After publishing, open Google Analytics > Realtime and visit `https://gstreconciliation.in/` in another tab. Events are also sent for internal search and reconciliation-tool clicks.

## 4. Google Search Console
Submit:
`https://gstreconciliation.in/sitemap.xml`

Inspect the homepage and important article/tool URLs and request indexing where appropriate.

No HTML change can guarantee a #1 Google ranking. The package is structured to make the site easier for search engines to crawl: canonical URLs, descriptive titles/descriptions, structured data, robots.txt and an XML sitemap are included.

## 5. AdSense
Advertisement spaces are included in the design, but actual Google ads cannot be activated until the site is added to your AdSense account, connected/verified and approved. Do not invent a publisher ID.

When AdSense provides your publisher code, place the exact code supplied by Google in the required location and replace the placeholder guidance in `ads.txt` with the exact line from your AdSense account.

See `ADSENSE-SETUP.md`.

## 6. Reconciliation tool
The existing tool remains at:
`https://gstreconciliation.in/reconciliation.html`

It continues to support Purchase Register and GSTR-2B upload, validation, invoice-level reconciliation and Excel report output.

## 7. Important
Do not upload any private GST source-book/backend package to a public GitHub Pages repository.
