# Cycle & Hormone Care — Patient Briefing Deck

Optimal Clinic patient orientation presentation for the **Cycle & Hormone Care Program**. Duplicated from the Menopause & Perimenopause Foundation Program deck and rebranded; content otherwise identical at the time of duplication.

**Live:** https://optimal-research-team.github.io/cycle-hormone-care-presentation/

## Features

- 16 slides at a fixed 1920×1080 design size, auto-scaled and letterboxed (`deck-stage.js` web component)
- Preparation screen (patient name + session date), personalized welcome cover, full-screen toggle
- Deck-wide entrance animations that replay per slide visit; two choreographed SVG infographics (incidental-findings routing diagram, bloodwork time track)
- One-click PDF export via the browser print dialog — one page per slide plus a stamped welcome/record page for the CRM
- Keyboard navigation: ←/→, number keys, Home/End, R to reset

## Structure

- `index.html` — the entire deck (styles, slides, scripts)
- `deck-stage.js` — reusable slide-stage web component (scaling, nav, print layout)
- `colors_and_type.css` — Optimal design tokens (Castoro / Public Sans, cream + forest palette)
- `assets/` — logos, team headshots, clinic photography, canopy cover art

## Deployment

GitHub Pages from `main` (root). Push to `main` and Pages redeploys automatically.
