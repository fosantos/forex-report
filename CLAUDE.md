# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Summary

Forex Report is a static, dependency-free Single Page Application delivering daily fundamental/technical Forex analysis for six currency pairs (EUR/USD, USD/JPY, AUD/USD, GBP/USD, EUR/JPY, GBP/JPY). It's hosted for free on GitHub Pages from the `/docs` directory. There is no build step, no bundler, and no package dependencies — `package.json` is intentionally empty (`{}`).

## Local Development

```bash
npx browser-sync start --server 'docs' --files 'docs/*.html, docs/*.css'
```

There is no build, lint, or test tooling in this repo — it's plain HTML5/CSS3/vanilla JS served as-is. Verify changes by opening the page in a browser (or via browser-sync above) and checking both language toggles and both the dashboard and the individual pair page.

## Architecture

### Dual representation of the same data (critical to understand)

Every pair's analysis exists in **two places that must be kept in sync**:

1. **`docs/index.html`** — contains the `forexData` JS object (~line 460), a static JSON-like database keyed by pair (`"EUR/USD"`, `"USD/JPY"`, ...). Each pair has `quote`, `bias`, `biasType`, and parallel `pt`/`en` blocks with fields like `fundamental`, `trend`, `support`, `resistance`, `priceAction`, `recommendation`, `trigger`, `stop`, `target`, `rr`, `rrValue`, `justification`. This object drives the dashboard's dynamic pair-selector view (`renderForexReport()`).
2. **`docs/[pair-name].html`** (e.g. `docs/eur-usd.html`) — a static, pre-rendered detail page for that pair. Content is duplicated inline as pairs of elements: `class="lang-en"` and `class="lang-pt" style="display:none;"`, toggled via CSS/JS rather than re-rendered from JSON.

**When updating an analysis, both the `forexData` entry in `index.html` and the corresponding static page must be edited together, in both languages.** They are not generated from one source — keeping them symmetric is a manual discipline enforced by convention, not code.

### Client-side i18n engine (docs/index.html)

- `initLanguageDetection()` inspects `navigator.languages`/`navigator.language`; auto-selects Portuguese only for `pt-br`/`pt-pt`, otherwise defaults to English.
- URL param `?lang=pt` or `?lang=en` overrides detection (used for CRO/marketing links) — internal links should propagate the active `?lang` param.
- `translateUI()` pushes an `i18n` dictionary into DOM nodes by ID; `renderForexReport()` re-renders the selected pair's data from `forexData` into the report panel.
- The static pair pages (`docs/[pair].html`) use a simpler mechanism: both languages are always in the DOM, and the inactive one is hidden via inline `style="display:none"` toggled by a language switch script.

### Dashboard rendering mechanics (docs/index.html)

`renderForexReport()` consumes `forexData[selectedPair]` and derives several visuals **automatically** — keep the JSON fields consistent with what renders:

- **Range gauge is auto-computed** from the leading number parsed out of `quote`, `support`, and `resistance` (the parser tolerates PT comma decimals). Don't hand-set a gauge on the dashboard; it follows the data.
- **Verdict card/badge class is chosen by keyword** in `recommendation`: contains `AGUARDAR`/`WAIT` → `verdict-wait`; `VENDA`/`SELL` → `verdict-sell`; otherwise `verdict-buy`. Recommendation strings must contain one of those keywords or the coloring breaks.
- **`biasType`** (`bull`/`bear`/`neutral`) drives both the `report-container bias-*` class and the badge color.
- **`rrValue` must equal `round(R × 25)`** where `R` is the reward multiple in `rr` (e.g. `1:2.40` → `60`, `1:2.13` → `53`, `1:3.10` → `78`). It sets the R/R progress-bar width, so changing `rr` without recomputing `rrValue` desyncs the bar. `N/A` (no-trade) pairs use `rrValue: 0`.

On the **static pair pages** these same visuals are **hardcoded** (range-gauge `left:%`, `.ratio-bar-fill` `width:%`, the `bias-*`/`verdict-*` classes) — they are not derived from JSON, so when editing a static page you must keep all of them consistent with the analysis by hand.

### Required pair order

Wherever pairs are iterated, listed, or updated (ticker tape, `forexData` keys, individual HTML pages), maintain this exact order: **EUR/USD → USD/JPY → AUD/USD → GBP/USD → EUR/JPY → GBP/JPY**.

### Bias color classes

- Bullish → `bias-bull` (emerald green)
- Bearish → `bias-bear` (rose red)
- Neutral → `bias-neutral` (gray)

### Design system

- Slate gray dark: `#0f172a`; off-white background: `#f8fafc`; action/accent blue: `#2563eb`.
- Ad slots use `.ad-placeholder` / `ins.adsbygoogle` with CSS `:empty` selectors so they self-hide when no ad script loads (needed for AdSense approval without external requests).
- Modals (Privacy Policy, Disclaimer) are lightweight and glassmorphic, with no external resource dependencies.
- Shared stylesheet: `docs/style.css`.

### Other static pages

`docs/about.html`, `docs/contact.html`, `docs/privacy.html`, `docs/terms.html`, `docs/disclaimer.html` are institutional/compliance pages, independent of the pair-analysis data flow. `docs/guides/` holds six evergreen educational pages (forex-basics, fundamental-analysis, our-methodology, risk-management, technical-analysis, trading-glossary), also independent of the data flow.

## Analysis Methodology (when generating/updating a forex analysis)

This repo doubles as a quant-analyst prompt target — the **`forex-report` agent** (`.claude/agents/forex-report.md`) runs the full daily pipeline (fetch data → compute indicators → set biases → update all files) and embodies the analyst persona/process. The rules below are the premises it — and any manual edit — must preserve:

1. **Data integrity**: If live market data/quotes aren't available, don't invent them. Prepend the analysis with an explicit warning (e.g. "Quote and macro context based on training knowledge — confirm values before trading.") and set `data-warning="true"` on that pair's HTML element. (Note: `data-warning` has no CSS/JS consumer — it is a semantic flag only; the visible warning must also be written as text in the analysis.)
2. **Technical definitions**: Use SMA 50 and SMA 200 on the D1 chart; Fibonacci retracements at 38.2%/50%/61.8% on D1/W1 moves; price-action signals (Pin Bar, Bullish/Bearish Engulfing, Inside Bar, Doji) at liquidity zones. Trend structure on W1, entry triggers on D1. Where possible, **compute** SMA/Fibonacci from a fetched historical daily-close series (e.g. ECB/Frankfurter reference rates) rather than estimating the levels, and state the data basis in the analysis.
3. **Risk/Reward gate**: A trade recommendation requires (a) a structurally-protected stop loss, (b) minimum 1:2 risk/reward on the take-profit target, and (c) no significant intermediate support/resistance blocking the path to target. If any condition fails, the verdict must be **"AGUARDAR OUTRO GATILHO"** / **"WAIT FOR ANOTHER TRIGGER"** — never force a directional call.
4. **Timestamp format**: `DD/MM/YYYY HH:MM UTC`. In `index.html` update all three spots — the `#generationTime` badge and the `generatedAt` string in both the EN and PT `i18n` blocks. The static pair pages have no separate timestamp element; the date lives inline in the fundamental paragraph (update both `lang-en` and `lang-pt`).
5. Preserve the existing HTML/CSS structure — only the analysis data and quotes change per update, not layout or design.
