# Iron Deficiency in Women — educational talk

A group talk rebuilt from the clinical team's draft (Nov 4, 2026) in the house deck style. 31 printed pages: the welcome screen, then 30 slides.

- **Present:** https://optimal-research-team.github.io/optimal-presentations/talks/iron-deficiency/
- **PDF:** [`iron-deficiency-in-women.pdf`](iron-deficiency-in-women.pdf), linked from the selector
- **Sources page (the QR code on slide 31):** [`sources.html`](sources.html)

## How it's built

`index.html` and `sources.html` are **generated**. Edit the script, then rebuild from the repo root:

```bash
python3 talks/iron-deficiency/tools/build_deck.py
```

The script copies the chrome (cover screens, reveal engine, PDF export, fullscreen) from
`../../intro/index.html`, writes the slides, applies `../tools/talk_chrome.py`, and refuses to
build if one of the draft's typos or factual errors comes back.

**After any slide change, also regenerate the PDF and, if the title slide changed, the thumbnail:**

```bash
talks/iron-deficiency/tools/export_pdf.sh
```

The thumbnail is `../../assets/thumbs/iron-deficiency.webp`, 960 px wide, from the title slide.

## PDF export

Three in the deck, stamped with the group's name and date: **Export PDF** on the set-up screen,
the floating control while presenting, and the button on the closing slide. The selector also
links the pre-rendered, undated PDF, which works on phones.

## Motion

The shared tools live in `../tools/talk_chrome.py`; the moves only this talk needs (the magnifier,
the Venn circles, the lower-limit marker) are in `IRON_CSS` in the build script.

- **Between slides:** the new slide fades in over the old one, with no dip through black.
- **Headlines:** each word comes into focus in turn.
- **Hairlines and rings:** drawn in, not faded.
- **Engravings:** ink in along a diagonal. The blood smear on the title opens like a microscope iris.
- **Diagrams:** build in the order the story is told. Curves draw with a pen tip, and numbers count up.

Print and reduced motion always show the finished state. A count-up's real value stays in the markup.

## Design system

Everything comes from `optimal-design-system` v1.5: tokens, Castoro and Public Sans, italic-noun
headlines, hairlines, the ring accent, the blood-smear field plate (the system's stated image for
iron), and the IV iron and specimen engravings in cream ink on forest and green ink on cream.
Unlike the patient decks, talks don't use the foliage wallpaper: their set-up and welcome screens
sit on the same forest field as the part dividers.

**One new asset:** `assets/images/breast.webp`. The system had no breast plate, so this was
generated in Higgsfield (`gpt_image_2_5`, job f892881e) and exported with the system's own ink
extraction. It's a candidate to add to the system. The charts are hand-built SVG; the curves on
slides 10, 14 and 18 are labelled schematic.

## Clinical review

Citations were checked against PubMed and the CMAJ full text on Nov 4, 2026. The slide-by-slide review list for the clinical lead is kept outside this public repo.
