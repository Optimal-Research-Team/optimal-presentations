# Iron Deficiency in Women — educational talk

The clinical team's 26-page draft, restyled in the house deck style. **Same slides, same order, same words.** Page N of the draft is slide N here, and only the design differs.

- **Present:** https://optimal-research-team.github.io/optimal-presentations/talks/iron-deficiency/
- **PDF:** [`iron-deficiency-in-women.pdf`](iron-deficiency-in-women.pdf), 26 pages, linked from the selector

## How it's built

`index.html` is **generated**. Edit the script, then rebuild from the repo root:

```bash
python3 talks/iron-deficiency/tools/build_deck.py
```

The script copies the chrome (set-up screen, reveal engine, PDF export, fullscreen) from
`../../intro/index.html`, writes the slides, and applies `../tools/talk_chrome.py`.

**The build refuses to finish if a slide's words differ from that page of the draft.** The draft's
words are in `tools/draft_words.json`, spelling included. A wording change is the clinical lead's
to make: update that file and the slide together, and only once they've asked for it.

**After any slide change, also regenerate the PDF and, if slide 1 changed, the thumbnail:**

```bash
talks/iron-deficiency/tools/export_pdf.sh
```

The thumbnail is `../../assets/thumbs/iron-deficiency.webp`, 960 px wide, from slide 1.

## PDF export

Two in the deck: **Export PDF** on the set-up screen, and the floating control while presenting. The
selector also links the pre-rendered PDF, which works on phones.

## Pictures

- **`assets/draft/`** comes straight from the draft: the paper screenshots and the Low Iron figure as
  they were, and the skeleton, icons and nutrition labels re-inked in the deck's green.
- **`assets/images/`** holds design system engravings standing in for the draft's clip art of the same
  subjects. `breast.webp` was generated in Higgsfield, because the system has no breast plate.
- The other diagrams are hand-built SVG of the draft's own diagrams.

## Motion

The shared tools live in `../tools/talk_chrome.py`; the moves only this talk needs (the magnifier
travelling from slide 5 to slide 6, the two circles on slide 7) are in `IRON_CSS` in the build script.
Print and reduced motion always show the finished state.
