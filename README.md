# Optimal — Presentations

Every patient presentation Optimal Clinic (Barrie, ON) uses, in one project and
on one website. The home page is a launcher for the care coordinator: pick
today's visit and that presentation opens on its own preparation screen
(patient name, date, Begin).

**Live:** https://optimal-research-team.github.io/optimal-presentations/

| # | Visit | Path | Presented by |
|---|---|---|---|
| 1 | Menopause Foundation | [`menopause-foundation/`](menopause-foundation/) | Nurse practitioner |
| 2 | Ongoing Care (menopause graduation) | [`menopause-foundation/graduation-ongoing-care/`](menopause-foundation/graduation-ongoing-care/) | Nurse practitioner |
| 3 | Cycle & Hormone Care | [`cycle-hormone-care/`](cycle-hormone-care/) | Nurse practitioner |
| 4 | Longevity Membership — tour only (walk-in) | [`tour/`](tour/) | Care coordinator |
| 5 | Longevity Membership — intro only | [`intro/`](intro/) | Admin team + NP |
| 6 | Longevity Membership — intro + possible intake | [`intro-intake/`](intro-intake/) | Admin team + NP |
| 7 | Longevity Membership — intake only | [`intake/`](intake/) | Admin team + NP |

## Using it

- Open the live link and click a visit. Or hover or use the arrow keys to preview one, press Enter to open it, or press its number key (`1`–`7`).
- Every preparation screen has an **All presentations** link back to the launcher;
  the browser Back button also returns to it from anywhere in a deck (the decks
  rewrite the slide number with `replaceState`, so Back never steps through slides).
- Each deck keeps its own controls: arrow keys, `F` fullscreen, PDF export for the chart.

## How it's built

A static site with no build step. Every presentation is a **self-contained
folder** — its own `index.html`, `deck-stage.js` slide engine,
`colors_and_type.css` brand tokens and `assets/` — so a change to one deck can
never break another. Each folder has its own README with that deck's details
(the Ongoing Care deck also has `HYPO3D.md` and the `tools/build-hypo3d.sh`
build for its 3-D hypothalamus).

The launcher (`index.html` at the root) is plain HTML + CSS with a small
script. It's built like the decks' own slides:
- a cream canvas with Castoro display type and hairline rows on the left, one per visit, grouped by program;
- a forest preview panel on the right that shows the selected deck's title slide and the three facts its title slide states (who leads, length, outcome), the same list-plus-panel pairing as the decks' closing slide.

Hover or arrow keys choose a deck, and Enter or a click opens it. The number keys `1`–`7` jump straight to a deck. The last deck opened is remembered per device (localStorage). Below 960px the panel is dropped and each row carries its own thumbnail. Thumbnails in `assets/thumbs/` are
screenshots of each deck's title slide — regenerate them when a title slide
changes.

Run it locally:

```bash
python3 -m http.server 8000
```

then open http://localhost:8000.

## Where this came from

On Oct 22, 2026 the five separate presentation repos were folded in here (copied
from each repo's `HEAD`; their full history stays in the original repos):

| Folder | Source repo | Commit |
|---|---|---|
| `menopause-foundation/` (incl. `graduation-ongoing-care/`) | `menopause-foundation-presentation` | `acb984b` |
| `cycle-hormone-care/` | `cycle-hormone-care-presentation` | `0c1e5a7` |
| `tour/` | `walk-in-presentation` | `a1b0f44` |
| `intro/` | `intro-meeting-presentation` | `a8b39b7` |
| `intro-intake/` | `intro-meeting-intake-presentation` | `0988633` |

`intake/` is new — forked from `intro-intake/` (see its README).

**This repo is now the source of truth.** Make deck edits here, not in the old
repos. The old repos are due to go private, which takes their GitHub Pages
links offline.

The only changes made to the copied decks: an **All presentations** link on each
preparation screen.

## Deployment

GitHub Pages from `main` / root (`.nojekyll` keeps Jekyll off the assets). Push
to `main` and it redeploys in about a minute. The repo must stay **public** for
Pages to serve it on this account. Nothing in it is patient data: names typed
on a preparation screen stay in that browser tab and are never stored or sent.

---

**Optimal Clinic** — 630 Huronia Road, Unit 5, Barrie ON · (437) 370-0291 ·
care@beoptimal.ca · [beoptimal.ca](https://beoptimal.ca)
