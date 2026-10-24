# Optimal — Hyperbaric Oxygen Therapy (HBOT) briefing

The patient presentation for hyperbaric oxygen therapy, Optimal's
investigational longevity & wellness service. Sessions are delivered at the
partner hyperbaric facility; its physician screens, sets the protocol,
supervises and holds clinical responsibility. 16 screens: a personalised
welcome, then 15 slides.

**v2.0.0 (Oct 24, 2026).** The copy mirrors the beoptimal.ca HBOT page after
Chantelle's edits (`BeOptimal/beoptimal-landing` commits `70590e0` and
`28a7386`):
- no Israel, Shamir or Sagol references;
- no "honest" framing;
- the partner physician holds clinical responsibility;
- the "who it may suit" list is removed;
- "What the research shows" replaces "Read it yourself".

v2 also adds motion: moving micrographs, animated diagrams and a session
schematic.

## How it's built

`index.html` is **generated**. Edit the script, then rebuild:

```bash
python3 hbot/tools/build_deck.py   # from the repo root
```

The script does three things:
- It copies the chrome (cover screens, reveal engine, PDF export, fullscreen) from `../intro/index.html`.
- It writes the 15 slides plus the HBOT-only motion CSS and JS.
- It refuses to build if any of these words reappear: Sagol, Shamir, Israel, honest, yourself.

**When the landing page changes, mirror the change in the script.**

## Slides

| # | Slide | From the page | Motion |
|---|---|---|---|
| 1 | Hyperbaric *oxygen* therapy, with the chamber room and three facts | hero + trust bar | photo settles slowly |
| 2 | What we'll *cover* | new (agenda) | rows rise in |
| 3 | *Oxygen*, under pressure: chamber / elevated oxygen / repeated sessions | How it works | three animated diagrams: pressure rings close in, O₂ flows into the vessel, sessions fill in |
| 4 | Inside the *protocol* | The protocol we follow | session schematic builds left to right; "~90 min" counts up |
| 5 | Potential *longevity*-related benefits 1/2: cellular aging, tissue & regeneration | What the research explores | **micrograph video loops** |
| 6 | … 2/2: brain & neuroplasticity, mitochondria & oxidative signalling | What the research explores | **micrograph video loops** |
| 7 | The bottom line | research note | neuron loop on the right |
| 8 | Where this fits, *plainly*, plus four commitments | In plain terms + trust bar | |
| 9 | Who runs your *sessions*: partner physician vs Optimal | The clinic behind it | duty lists tick in |
| 10 | What a session is *like* | What to expect | |
| 11 | Who should not — or should *wait* | eligibility | |
| 12 | Where HBOT *is* an established treatment | For context | |
| 13 | What the research *shows*, plus QR code to every source | The evidence | |
| 14 | Your *questions*, answered | FAQ | |
| 15 | Curious whether HBOT is right for *you*? | closing CTA + disclaimer | |

### Motion rules

All motion uses the house vocabulary (one easing curve, no bounce) and is gated on
the slide being in view, so it replays on every visit.

**Video loops** (`assets/video/`, sources in `assets/video/SOURCES.md`):
- They are Kling 3.0 clips generated from the page's own stills. The start frame and end frame are the same still, so each loop is seamless and opens on the exact still.
- Only the slide on screen plays its loops; leaving a slide pauses them, and each visit restarts from frame 0.
- Each loop sits over its still. In print, PDF export and reduced motion, only the still shows.

**Print / PDF:**
- Diagrams render fully drawn.
- The duty lists render visible.
- Slow photo drift is off.

## Deck wording that differs from the page

Approved by Peter on Oct 24, 2026 (the v1 list), and carried into v2 with the
page's new copy.

**Page references now point at the deck:**
- "linked further down" became "cited at the end".
- "Every claim on this page links to its source" became "Every claim in this presentation cites its source".
- "described below" was dropped.

**New labels:**
- **Agenda:** titles and right-hand labels.
- **Title facts:** Physician (MD) / A series of sessions / HSA-eligible.
- **Session moments:** Before / In the chamber / Good to know / After.
- **Close:** the next-steps rows.
- **QR card:** its copy.

**Shortened:**
- **Evidence slide:** two key citations per domain, each with a short descriptor. The QR code opens the full list.
- **FAQ:** four of the seven questions, with answers verbatim.
- **Closing disclaimer:** trimmed.

**New in v2 (please check):**
- **Session schematic:** "One session, schematic", "Exact parameters are decided with the physician" (from the protocol FAQ answer), and the labels PRESSURE UP / OXYGEN / AIR BREAK / PRESSURE DOWN. It shows the *shape* of a session only, with no counts or durations.
- **Role split on slide 9:**
  - Partner physician (MD): Screens you / Sets your protocol / Supervises every session / Holds clinical responsibility.
  - Optimal: The introduction / No HBOT screening / No protocol management / No results review.
  - Every line restates the page's two paragraphs, which sit on the same slide.
- **FAQ:** "What protocol do you follow?" (new page wording) replaces "Who administers the treatment, and where?". The page's answer to that one still says *"Optimal coordinates your screening, program, and follow-up"*, which contradicts the new "Who runs your sessions" section. Fix the page, then decide whether the deck should carry it.

## Editing

Edit `tools/build_deck.py`, rebuild, check the slides, and keep footers numbered
`NN / 16`; the welcome screen is 01. When the title slide changes, regenerate
`../assets/thumbs/hbot.webp` for the launcher.
