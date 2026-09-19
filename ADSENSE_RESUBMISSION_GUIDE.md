# Forex Report — AdSense Resubmission Guide

**Date:** September 19, 2026
**Site:** https://newsforextrading.com
**Violation being addressed:** Low value content (site does not yet meet publisher-network criteria)
**Relevant policies:** AdSense Program Policies (minimum content requirements), Low value content, Webmaster thin-content guidance

---

## What the September 2026 audit found

The July content expansion (~22k words of guides) existed in the repository but was **invisible or unreachable**:

1. The homepage — the URL AdSense reviews — was a JavaScript shell: ~489 visible words; the analysis lived in a JS object rendered on load, and the no-JS static fallback in `#reportContainer` was months stale.
2. `index.html` contained **zero links** to the 6 pair pages (the market map rendered `<button>`s, not `<a>`s) and **zero links to the guides** — the 6 guides were fully orphaned (no page linked to them; the guides' own breadcrumb pointed to a nonexistent `guides/index.html`).
3. The 6 pair pages shared 35–48% lexical overlap: same template, ~600 unique EN words each.
4. `docs/track-record.json` — the site's most differentiated asset, a verifiable ticket ledger — was rendered nowhere.
5. The guides were English-only (dead EN/PT selector), inconsistent with the bilingual rest of the site.
6. The previous version of this guide (July 2026) described a state that no longer existed (author credentials that had been removed, word counts ~2× inflated). This version counts words the way a crawler does (visible DOM text).

## What was fixed (2026-09-19)

### Crawlability & navigation (the core fix)
- **index.html no-JS fallback is now data-fresh and pipeline-maintained**: `pipeline/build_static_pages.py` rewrites the static EUR/USD report inside `#reportContainer` from `forexData` on every daily run (quote, bias, verdict, gauge, all fields). The homepage no longer looks empty without JS.
- **Market-map cards are real `<a href>` links** to the 6 static pair pages (plain click still switches the in-page tab; ctrl/middle-click opens the page). CSS anchor reset added.
- **`<noscript>` block** on the homepage links all 6 pairs, News, Track Record and Education.
- **Header nav on every page** now includes **Education** → `guides/index.html`.
- **Footer on every page** now includes **Track Record** and **Education** links.
- **New page `docs/guides/index.html`** (bilingual education hub; also fixes the previously broken guides breadcrumb).

### New public surface for original content
- **New page `docs/track-record.html`** — the performance ledger rendered: every directional ticket published since 17/08/2026, resolved mechanically on daily closes (targets, stops, expiries, **revoked setups included**), with resolution rules and honest aggregate stats. Generated from `docs/track-record.json` by `pipeline/build_track_record_page.py` (re-run on every ledger update). This is content no competitor site publishes.
- **Pair pages**: each "Understanding [PAIR]" evergreen section gained a pair-specific **"How the desk trades [PAIR]"** subsection (methodology applied to that pair's characteristics — intervention clause on JPY pairs, event sensitivity on Cable, risk-sentiment on AUD) plus "Go deeper" links into the guides and the track record. Unique evergreen text per pair roughly doubled.

### Consistency & freshness
- **All 6 guides are now bilingual** (EN block + PT-BR block with working language toggle, `-pt` anchor suffixes), matching the rest of the site.
- `sitemap.xml`: 24 URLs, `guides/index.html` and `track-record.html` added, all `lastmod` dates refreshed to the real change dates.
- `build_static_pages.py` derives the macro-driver chips from `macroDrivers` in `index.html` (they had drifted a month stale) and builds the data-basis line from the fundamental text itself, so it can no longer go stale.

## Current content inventory (measured as visible DOM text)

| Surface | Pages | Approx. unique text |
|---|---|---|
| Homepage (static fallback + wire + labels) | 1 | full EUR/USD report visible without JS |
| Pair pages (daily article + evergreen profile) | 6 | ~900–1,100 words per language each |
| Education guides | 6 + hub | ~1,300–1,600 words per language each |
| Track record ledger | 1 | full ticket history + rules |
| News wire | 1 | full desk digest |
| About/Contact/Legal | 5 | institutional pages |
| **Total** | **24** | all bilingual (EN + PT) |

## Remaining known risks (be honest in any appeal)

- **Site age & traffic.** The domain is ~4 months old with modest organic traffic. "Low value content" rejections often persist until the site demonstrates a track record of updates and visitors. Do not resubmit more than once every few weeks.
- **Small ledger sample.** The track record is transparent but young (2 resolved, 6 revoked, 1 open, 1 watching as of 19/09). It grows daily; it is credibility-positive precisely because losses and revocations are shown.
- **Shared ad slot id.** All `<ins>` units use manual slot `8549246934`; if the AdSense dashboard shows a different slot, swap all `data-ad-slot` attributes in one pass (see AGENTS.md).

## Resubmission checklist

1. Deploy all changes to GitHub Pages (`/docs` → main branch).
2. Verify the live site: homepage with JS disabled shows the current EUR/USD report + navigation links; every page reachable from the homepage by following links (Dashboard → pair pages → guides → track record).
3. Submit `https://newsforextrading.com/sitemap.xml` in Search Console; confirm indexation of the 24 URLs (`site:newsforextrading.com`).
4. Let the site accumulate 3–4 weeks of daily updates and traffic before requesting re-review from the AdSense Sites page.
5. Review answer typically arrives by email within days; do not resubmit repeatedly in the meantime.

## Points to show a reviewer (if appealing)

- **Navigation is complete**: every content page is reachable from the homepage nav/footer without JS.
- **Original, differentiated content**: a public, mechanically-resolved performance ledger (`track-record.html`) and a documented methodology actually applied in the daily tickets — not scraped or rewritten third-party content.
- **Bilingual depth**: every analysis and guide exists in full English and Portuguese versions.
- **Freshness**: content updates daily via an assertion-checked pipeline (`pipeline/build_static_pages.py`, `pipeline/build_track_record_page.py`, `pipeline/verify_all.py`).
- **Compliance**: privacy policy, terms, disclaimer, bilingual cookie consent with NPA gating (consent.js), `ads.txt` present.
