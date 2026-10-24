# Optimal — Hyperbaric Oxygen Therapy (HBOT) briefing

The patient presentation for hyperbaric oxygen therapy, Optimal's
investigational longevity & wellness service. Sessions are delivered at the
partner hyperbaric facility under its physician. 16 screens: a personalised
welcome, then 15 slides.

New on Oct 24, 2026. The August HBOT sales presentation couldn't be found:
- not on this Mac, in GitHub, in Claude artifacts or in Claude sessions;
- not in Slack, Notion or Google Drive.

So this deck was built fresh from the **beoptimal.ca HBOT page**: its MD-reviewed copy and the visual pass made on Oct 24
(`BeOptimal/beoptimal-landing` commits `5219bb0` and `fa104e7`). If the August
deck turns up, port anything it has that this one lacks (pricing, for one).

## Slides

| # | Slide | Built from |
|---|---|---|
| 1 | Hyperbaric oxygen *therapy*. Chamber photo, plus administered by / protocol / coverage | hero + trust strip |
| 2 | What we'll *cover*: five parts | new (agenda) |
| 3 | Oxygen, under *pressure*: chamber / elevated oxygen / repeated sessions | How it works |
| 4 | The Sagol *protocol*: ~90 min / Series / Cycled O₂ / MD-led, beside the Sigma 36 control panel | The protocol we follow |
| 5 | Potential longevity-related *benefits* 1/2: cellular aging markers, tissue & regeneration | What the research explores |
| 6 | … 2/2: brain & neuroplasticity, mitochondria & oxidative signalling | What the research explores |
| 7 | The honest bottom line, on forest, with the neuron micrograph | research note |
| 8 | Where this fits, *plainly*, plus the four commitments | The honest version + trust strip |
| 9 | Longevity care, with a clinician's *hand*: who plans, who oversees, who reviews | The clinic behind it |
| 10 | What a session is *like*: before / in the chamber / good to know / after | What to expect |
| 11 | Who it may *suit* / who should not, or should *wait* | Eligibility |
| 12 | Where HBOT is an established *treatment*: six UHMS indications | For context |
| 13 | Read it *yourself*: five evidence domains, key citations, and a QR code to every source | The evidence |
| 14 | Your *questions*, answered: four of the page's seven FAQs | FAQ |
| 15 | Curious whether HBOT is right for *you*? Info call → screening → program; contact panel and PDF export | closing CTA + disclaimer |

## Look

The deck matches the landing page's Oct 24 pass:
- **Tokens:** the Optimal `--op-*` set. That means cream canvas, forest headings, `#474747` body copy and `#DFD7CA` hairlines, with no heavy green rules and no navy.
- **Micrographs:** the four from the design system's v1.3 layer (telomeres, angiogenesis, neurons, mitochondria). They sit on their night-950 ground as card bands.
- **Real photography:** the partner facility's chamber room and the Sigma 36 control panel. The chamber room replaces the leaf canopy on the preparation and welcome screens; the wordmark sits over it as its own layer.
- **Ring accent:** the hand-drawn one, used on three headings only: *plainly*, *yourself* and *questions*.

The engine, cover screens, PDF export, fullscreen and motion all come from
`../intro/`, unchanged. The QR code (`assets/images/qr-evidence.svg`) opens
`beoptimal.ca/services/hyperbaric-oxygen-therapy#evidence`.

## Wording that differs from the page (approved by Peter, Oct 24, 2026)

Body copy is the page's, verbatim, except for these changes. All of them are approved; treat them as client-approved copy, like the rest of the deck.

**Page references now point at the deck:**
- "linked further down" became "cited at the end".
- "Everything on this page… linked in full" became "Everything in this presentation… cited in full".
- "described below" was dropped.

**Restructured, same words:**
- The research note's lead-in "The honest bottom line:" is now the slide's eyebrow.
- Its two sentences became a headline and a subline.

**New labels:**
- The agenda (titles and the right-hand labels).
- The title-slide facts: Physician (MD) / Modelled on Sagol / HSA-eligible.
- On the clinic slide, the role labels Optimal / Physician (MD) / You.
- The session moments: Before / In the chamber / Good to know / After.
- The eligibility eyebrows.
- The close: "Info call — No obligation", "Medical screening — With the physician" and "Your program — A series over weeks".
- The QR card copy.

**Shortened:**
- **Evidence slide:** two key citations per domain, each with a short descriptor that paraphrases the paper's title. The QR code opens the full list.
- **FAQ:** four of the seven questions, with answers verbatim.
- **Closing disclaimer:** trimmed to the opening "Offered as…".

## Editing

Slides are hand-tuned, inline-styled `<section>`s inside `<deck-stage>`, the
same as every other deck here. Edit `index.html` directly. Keep footers
numbered `NN / 16`; the welcome screen is 01.
