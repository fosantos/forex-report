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

- Bullish → `bias-bull` (moss green)
- Bearish → `bias-bear` (rust red)
- Neutral → `bias-neutral` (slate gray)

### Design system

- **Identity: "Research Desk" (light theme).** Cool bond-paper field (`--bg-body #eceef1`), deep petrol-navy ink (`--text-primary #13242c`), a single petrol-teal brand signal (`--color-primary #0e5963`) stamped with a sparing ochre "seal" accent (`--color-accent #b07a1b`), and muted market polarity (moss `--color-success` / rust `--color-danger` / ochre `--color-warning`). Type: **Archivo** (display) / **Hanken Grotesk** (body) / **IBM Plex Mono** (data), loaded via the Google Fonts `<link>` in each page's `<head>`. The signature element is the **stamped trade-ticket** (`verdict-card` / `trade-ticket`) — a serialled order slip with a tilted rubber-stamp verdict, an ochre R:R seal, and a dashed perforation.
- **Token NAMES are an immutable cross-page contract.** Every page (index, 6 pair pages, guides, compliance) references `var(--*)` inline, and the 6 guides carry their own embedded `<style>` blocks that are also fully token-driven. So re-themes happen by changing VALUES in `:root` of `docs/style.css` only — never rename a token, and never hardcode hex/rgba in page markup (the inline `rgba(14,89,99,…)` petrol borders in `contact.html` are the one deliberate exception).
- Ad slots use `.ad-placeholder` / `ins.adsbygoogle` with CSS `:empty` selectors so they self-hide when no ad script loads (needed for AdSense approval without external requests).
- Modals (Privacy Policy, Disclaimer) are lightweight and glassmorphic, with no external resource dependencies.
- Shared stylesheet: `docs/style.css`.

### Other static pages

`docs/about.html`, `docs/contact.html`, `docs/privacy.html`, `docs/terms.html`, `docs/disclaimer.html` are institutional/compliance pages, independent of the pair-analysis data flow. `docs/guides/` holds six evergreen educational pages (forex-basics, fundamental-analysis, our-methodology, risk-management, technical-analysis, trading-glossary), also independent of the data flow.

## Analysis Methodology (when generating/updating a forex analysis)

This repo doubles as a quant-analyst prompt target — the **`forex-report` agent** (`.claude/agents/forex-report.md`) runs the full daily pipeline (fetch data → compute indicators → set biases → update all files) and embodies the analyst persona/process. The rules below are the premises it — and any manual edit — must preserve:

1. **Data integrity**: If live market data/quotes aren't available, don't invent them. Prepend the analysis with an explicit warning (e.g. "Quote and macro context based on training knowledge — confirm values before trading.") and set `data-warning="true"` on that pair's HTML element. (Note: `data-warning` has no CSS/JS consumer — it is a semantic flag only; the visible warning must also be written as text in the analysis.)
2. **Technical definitions**: Use SMA 50 and SMA 200, σ20 (standard deviation of the last 20 daily % changes, also in pips), and Donchian 10/20-day extremes on the D1 chart, plus Fibonacci retracements at 38.2%/50%/61.8% on D1/W1 moves as **confluence only**. **Bias by alignment:** bullish only when close > SMA200 *and* SMA50 > SMA200; bearish only when close < SMA200 *and* SMA50 < SMA200; otherwise neutral (default verdict WAIT unless a confirmed breakout resolves the mix). **Anchor hierarchy** for stops/targets: (1) SMA 50/200; (2) real swing extremes and Donchian 10/20 levels; (3) round numbers (00/50 pips); (4) Fibonacci — never the sole justification. **Triggers are mechanical and close-based** (the ECB/Frankfurter series has no OHLC): pullback = daily close in the trend direction off the anchor zone; breakout = daily close beyond the **10-day** Donchian extreme (second confirming close for major levels; the 10-day channel is the backtest-validated standard, 20-day levels remain anchors). Candlestick patterns (Pin Bar, Engulfing, Inside Bar, Doji) are narrative color only — **never the entry condition**. Where possible, **compute** all of these from a fetched historical daily-close series (e.g. ECB/Frankfurter reference rates) rather than estimating the levels, and state the data basis in the analysis.
3. **Risk/Reward gate + volatility floor**: A trade recommendation requires (a) a structurally-protected stop loss, (b) stop distance from entry ≥ 1.5×σ20 (2.5×σ20 on JPY pairs while intervention risk is active — intervention or jawboning within 30 days), (c) minimum 1:2 risk/reward on the take-profit target, and (d) no significant intermediate support/resistance blocking the path to target. Every directional `stop` field ends with the fixed suffix — PT `· risco sugerido ≤ 1% por operação`, EN `· suggested risk ≤ 1% per trade`. If any condition fails, the verdict must be **"AGUARDAR OUTRO GATILHO"** / **"WAIT FOR ANOTHER TRIGGER"** — never force a directional call.
4. **Event filter**: No new directional entry within 24h before a top-tier event for the pair's currencies (FOMC/CPI/NFP for USD; ECB for EUR; BoE for GBP; BoJ/MoF for JPY; RBA and China data for AUD). Inside the window: WAIT with a "reassess after the event" note, or a trigger valid only after the event.
5. **Track-record ledger**: Every daily run updates `docs/track-record.json` — resolve existing `watching`/`open` tickets against the new closes per the conventions in its `meta` block (close-based resolution), then append the report's directional setups as new `watching` entries.
6. **Strategy re-validation**: The rules have a backtest baseline — `.claude/backtest_strategy.py` re-runs the 2000-present test on the same ECB/Frankfurter series (canonical config: Donchian 10 breakout, 10-session expiry, 1.5σ20 floor, R/R ≥ 1:2; baseline: `.claude/backtest_results_2026-08-17.txt`). Re-run and compare before adopting any rule change.
7. **Timestamp format**: `DD/MM/YYYY HH:MM UTC`. In `index.html` update all three spots — the `#generationTime` badge and the `generatedAt` string in both the EN and PT `i18n` blocks. The static pair pages have no separate timestamp element; the date lives inline in the fundamental paragraph (update both `lang-en` and `lang-pt`).
8. Preserve the existing HTML/CSS structure — only the analysis data and quotes change per update, not layout or design.
