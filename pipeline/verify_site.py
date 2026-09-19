#!/usr/bin/env python3
"""Site-wide structural verification: internal links, AdSense/consent pattern,
guide bilingual parity, orphan pages, and the homepage no-JS fallback freshness.
Run after any structural change:  python pipeline/verify_site.py"""
import os, re, glob, sys

DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")
os.chdir(DOCS)

pages = sorted(p.replace(os.sep, "/") for p in glob.glob("*.html") + glob.glob("guides/*.html"))
errors = []

# 1. internal link check (skip JS template literals, remote and mailto refs)
for page in pages:
    s = open(page, encoding="utf-8").read()
    base = os.path.dirname(page)
    for r in re.findall(r'(?:href|src)="([^"#]+?)(?:[?#][^"]*)?"', s):
        if r.startswith(("http", "mailto:", "data:", "//", "${")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(base, r))):
            errors.append(f"{page}: broken ref -> {r}")

# 2. ad pattern on every page carrying the loader
ad_pages = 0
for page in pages:
    s = open(page, encoding="utf-8").read()
    if "pagead2.googlesyndication.com" not in s:
        continue
    ad_pages += 1
    i_np, i_load = s.find("requestNonPersonalizedAds"), s.find("pagead2.googlesyndication.com")
    if i_np == -1 or not (0 <= i_np < i_load):
        errors.append(f"{page}: NPA pre-block missing or misplaced")
    if "consent.js" not in s:
        errors.append(f"{page}: consent.js missing")
    n_ins, n_push = s.count("<ins"), s.count("|| []).push({});")
    if n_ins != n_push:
        errors.append(f"{page}: {n_ins} <ins> vs {n_push} pushes")

# 3. all 6 guides bilingual with toggle + EN/PT structural parity
guides = [p for p in glob.glob("guides/*.html") if not p.endswith("index.html")]
if len(guides) != 6:
    errors.append(f"expected 6 guides, found {len(guides)}")
for gp in guides:
    s = open(gp, encoding="utf-8").read()
    en = re.search(r'<div class="lang-en">.*?<div class="lang-pt"', s, re.S)
    pt = re.search(r'<div class="lang-pt".*?</div>\s*(?=<!-- Ad Space|</main>|<footer)', s, re.S)
    if not (en and pt and "initLanguage" in s):
        errors.append(f"{gp}: bilingual structure/toggle missing")
        continue
    for tag in ["<section", "<h2", "<h3"]:
        a, b = en.group(0).count(tag), pt.group(0).count(tag)
        if a != b:
            errors.append(f"{gp}: {tag} EN {a} vs PT {b}")

# 4. orphan pages (404.html exempt — served by GitHub Pages for missing URLs)
all_pages = set(pages)
linked = set()
for page in pages:
    s = open(page, encoding="utf-8").read()
    base = os.path.dirname(page)
    for r in re.findall(r'href="([^"#]+?)(?:[?#][^"]*)?"', s):
        if not r.startswith(("http", "mailto:", "${")):
            t = os.path.normpath(os.path.join(base, r)).replace(os.sep, "/")
            if t in all_pages:
                linked.add(t)
for page in sorted(all_pages - linked - {"404.html"}):
    errors.append(f"ORPHAN page (no inbound links): {page}")

# 5. sitemap URLs all exist, and key pages are in the sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
for url in re.findall(r"<loc>([^<]+)</loc>", sm):
    path = url.replace("https://newsforextrading.com/", "").replace("https://newsforextrading.com", "index.html") or "index.html"
    if not os.path.exists(path):
        errors.append(f"sitemap: URL without file -> {url}")
for must in ("track-record.html", "guides/index.html"):
    if f"/{must}" not in sm and must not in sm:
        errors.append(f"sitemap: {must} missing")

# 6. homepage no-JS fallback is present (freshness of values is checked by build_static_pages assertions)
idx = open("index.html", encoding="utf-8").read()
for probe, what in [("<noscript>", "noscript nav"), ("guides/index.html", "education link"),
                    ("track-record.html", "track-record link"), ('id="reportFundamental"', "fallback report")]:
    if probe not in idx:
        errors.append(f"index.html: {what} missing")

if errors:
    print(f"FAILED with {len(errors)} error(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"ALL SITE CHECKS PASSED: {len(pages)} pages, {ad_pages} ad pages, 6 bilingual guides, "
      "no broken refs, no orphans, sitemap consistent, fallback + noscript present.")
