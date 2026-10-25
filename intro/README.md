# Optimal — Introductory Meeting

The patient-facing orientation presentation shown during the in-clinic
**Introductory Meeting** at Optimal Health Clinic (Barrie, ON).
25 screens: a personalised welcome, then 24 slides covering the membership,
the care team, plans, policies, and next steps.

It is a **static website** — no build step, no dependencies. Open `index.html`
and it runs.

> Forked from [`intro-meeting-intake-presentation`](https://github.com/Optimal-Research-Team/intro-meeting-intake-presentation),
> the **Introductory Meeting & Possible Intake** deck. This version is the
> intro-only meeting: no intake on the day; if approved, the patient pays and
> books the intake for a later date.

---

## The flow

1. **Preparation** — before the patient walks in, the front desk types their
   name, confirms the date, and can put the display into fullscreen. Nothing is
   stored or sent anywhere; the values live in the page for the length of the
   meeting.
2. **Welcome** — the animated leaves-canopy wallpaper with the Optimal wordmark,
   and *"Welcome, [Name]"* beneath it. This is screen 01 of the printed 25.
3. **The deck** — 24 slides at a fixed 1920×1080 artboard, letterboxed to fit
   whatever screen it runs on.

## Navigating

| Action | How |
|---|---|
| Next / previous | `→` `←`, `PgDn` `PgUp`, `Space`, or tap the right/left half on touch |
| Jump to a slide | `Home` / `End`, number keys, or the overlay at the bottom |
| Restart | `R` |
| Fullscreen | `F`, the floating control, or **Fullscreen** on the preparation screen (`Esc` exits) |
| Deep link a slide | `#12` in the URL — `#1` is the Title slide (printed "02 / 25") |
| Export a PDF | **Export as PDF** on the closing slide, the floating control, or the preparation screen |

### Exporting for the chart

The export runs the browser's print path (**Save as PDF**), laying out one
slide per page with the patient's name and date stamped into the filename. The
welcome screen becomes page 1; live affordances (buttons, keyboard hints, the
floating controls) are dropped from the printed record.

Use **Landscape** and enable **Background graphics**.

## Run it locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` over `file://` mostly
works, but a local server is more reliable for fonts and images.

---

## What's in here

| File | Purpose |
|---|---|
| `index.html` | The whole presentation — cover screens, all 24 slides, and the runtime. |
| `deck-stage.js` | Slide engine (`<deck-stage>`): scaling/letterboxing, keyboard nav, print pagination. Shared with the menopause deck. |
| `colors_and_type.css` | Optimal brand tokens (colors, type) as CSS custom properties. |
| `assets/` | Clinic photography, team headshots, brand marks, the canopy wallpaper. |

## Working on it

- **Slide content is intentional, hand-tuned HTML.** Each slide is a `<section>`
  directly inside `<deck-stage>`, fully inline-styled at 1920×1080 — the artboard
  is the source of truth. To change a slide, edit that section's markup.
- **The copy is client-approved.** Change markup, not words.
- **Don't rewrite `deck-stage.js`.** It is a general-purpose engine and the
  slides depend on its contract: every direct-child `<section>` is a slide. It
  also owns the URL hash.
- **Reuse the tokens** in `colors_and_type.css` rather than hardcoding hex values.
- Each slide keeps its `data-speaker-notes` attribute from the design handoff.
  Nothing renders it — it is inert documentation of what the slide is for.

### How the animations work

Motion is deliberately conservative — no bounce, no spring, no parallax. One
easing curve (`cubic-bezier(.2,.7,.2,1)`) is used throughout.

Slides crossfade over 300ms. Within a slide, content blocks rise 24px into place
with a 60ms stagger, replayed on every visit. Reveal targets are chosen
*structurally* at load — the script walks into each slide, skips the layers that
animate on their own clock, and staggers the natural content blocks — so new
slides animate correctly without hand-tagging.

The layers with their own timing are tagged in the markup:

| Class | Behaviour |
|---|---|
| `dk-bg` / `dk-panel` | Photography: fades in, settling out of a 6s 1.03→1 zoom |
| `dk-scrim` | Gradient wash over a photo |
| `dk-ring` | Hand-drawn ring accent, draws in after the headline lands (`--rot` preserves its tilt) |
| `dk-rule` | Timeline rail, draws left to right |
| `dk-footer` | Slide footer, arrives last |

All of it collapses under `prefers-reduced-motion` and is disabled for print.

## Deployment

Served from GitHub Pages on `main` / root. A `.nojekyll` file keeps Pages from
running Jekyll over the assets. Push to `main` and it redeploys.

---

**Optimal Clinic** — 630 Huronia Road, Unit 5, Barrie ON · (437) 370-0291 ·
care@beoptimal.ca · [beoptimal.ca](https://beoptimal.ca)
