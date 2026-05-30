# 📊 Forex Report — Professional Trading Insights

A lightweight, high-performance, and conversion-optimized (**CRO**) Single Page Application designed to deliver daily expert fundamental and technical analysis for major currency pairs. 

This project is fully structured for monetization (Google AdSense, premium affiliates, and donations) and is **100% production-ready** to be hosted for free on GitHub Pages.

---

## 🚀 Live Demo & Hosting
The repository is structured to use **GitHub Pages** from the `/docs` directory. 
To deploy this project live in under a minute:
1. Go to your repository settings on GitHub (**Settings**).
2. Navigate to the **Pages** menu on the left sidebar.
3. Under *Build and deployment*, set the branch to `main` and choose the **`/docs`** directory.
4. Click **Save**. 

Your site will be live at `https://<your-username>.github.io/forex-report/`

---

## 💎 Premium Design & CRO Architecture

This page was engineered following high-converting UI/UX principles to deliver maximum value with zero distractions:

*   **Mobile-First Design:** Fully responsive layout using modern CSS Grid and Flexbox, looking stunning on mobile devices, tablets, and wide desktop screens.
*   **Aesthetics WOW:** Curated color palette using smooth slate grays (`#0f172a`), clean off-white backgrounds (`#f8fafc`), royal blue actions (`#2563eb`), and clear indicators for trading biases (emerald green and rose red).
*   **Strategic Strategic Setup Layout:** Re-engineered trading metrics layout utilizing clean visual blocks with color-coded borders to highlight critical technical metrics such as **Entry Trigger**, **Stop Loss**, and **Take Profit** without text overlapping or squishing.
*   **Google AdSense Ready:** Clean, visual placeholders that dynamically adapt to standard ad sizes (**728x90** on desktop and **320x50** on mobile) and cleanly hide themselves via CSS `:empty` selectors if no scripts are loaded.
*   **Integrated Coffee Donations:** An beautifully styled "Buy Me a Coffee" CTA section at the bottom, perfectly matches the official brand parameters to maximize micro-donations.
*   **Compliance-First:** Built-in lightweight, glassmorphic modal windows for **Privacy Policy** and **Legal Disclaimer** to facilitate instant approval in the Google AdSense program without external file requests.

---

## 🌐 Dynamic Client-Side i18n Engine

Equipped with a lightweight, dependency-free internationalization (i18n) engine built entirely in vanilla JavaScript:
*   **Automatic Detection:** Automatically parses browser preferences (`navigator.languages` or `navigator.language`). If the user's browser is set to Portuguese (**pt-BR** or **pt-PT**), the application translates all text and analyses instantly to Portuguese.
*   **English Default:** Defaults seamlessly to English for all other international visitors.
*   **Manual Toggle:** Includes an elegant, discrete dropdown in the header allowing users to manually switch languages on the fly, immediately re-rendering the active analysis.
*   **Query Param Support:** Allows forcing a specific language using `?lang=pt` or `?lang=en` in the URL (perfect for targeted marketing campaigns).

---

## 📂 Project Structure

```bash
forex-report/
├── docs/
│   └── index.html      # Production-ready SPA (HTML5, modern CSS3 & Vanilla JS ununified)
├── .gitignore          # Keeps the repository clean of IDE/agent junk files
└── README.md           # Documentation and setup guide
```

---

## ⚡ How to Add New Pairs
The trading data is decoupled in a single static JSON database inside `index.html`. To add new pairs:
1. Open `docs/index.html`.
2. Locate the `forexData` object inside the `<script>` tag.
3. Copy one of the structures (e.g., `USD/JPY` or `EUR/USD`) and input your technical metrics, fundamental analyses, and translations for `pt` and `en` blocks.
4. Save and commit. The page will dynamically add the option to the combobox and render the content automatically.

---

## 📄 Disclaimer & Risk Disclosure
Trading foreign exchange (Forex) on margin carries a high level of risk and may not be suitable for all investors. The educational analyses presented on this platform do not constitute financial advice.
