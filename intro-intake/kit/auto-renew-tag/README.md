# Optimal — Auto-renew tag kit

A drop-in addition for the **payment / pricing slide** of any Optimal patient
deck: a small animated tag reading **"Membership payment auto-renews"**, as
built on the Introductory Meeting & Possible Intake deck (slide 17).

It adds one element. It changes nothing else — no copy, no layout, no
colours anywhere on the deck. That is the whole contract of this kit.

See `reference/slide-17-membership-plans.png` for the intended result, and
open `preview.html` in a browser to watch the motion before integrating.

---

## What's in the kit

| File | What it is | Where it goes |
|---|---|---|
| `tag.html` | The tag markup — two variants, dark surface and cream surface | Into the payment slide, one place |
| `tag.css` | Entrance + pulse styles, print and reduced-motion rules | End of the deck's `<style>` block |
| `tag.js` | Replays the entrance each time the slide becomes active | Just before `</body>` |
| `preview.html` | Standalone demo of the tag on both surfaces | Open it; don't ship it |
| `reference/` | The finished slide as rendered, plus its full section markup for context | Look; don't paste |

The three pieces to integrate are ~10 lines of HTML, ~40 of CSS, ~15 of JS.

---

## Apply it — four steps, in order

Work only in the deck's `index.html`.

### 1 · Styles
Open `tag.css`. Copy the **entire file**. Paste it at the **end** of the deck's
main `<style>` block (immediately before `</style>`).

It only targets `.dk-tag` and `.dk-tag-dot`, so it cannot restyle anything else.

### 2 · Markup
Open `tag.html`. It has two variants. Copy **one**:

- **Variant A** if the price sits on the dark forest-green panel.
- **Variant B** if the price sits on the cream canvas or a white/outlined card.

Find the payment slide (`<section data-label="Membership plans"` or whatever
that deck calls it). Paste the variant **directly beneath the line that states
the renewal cadence** — in the intro deck that is the paragraph reading
"Renews once a year." inside the annual price block. The tag sits under it as
its own row.

Do not put it beside the "ANNUAL BILLING" label — the row is too narrow, and
the tag would have to shrink below the deck's 24px minimum text size.

### 3 · Script
Open `tag.js`. Copy the **entire file** (it is a complete `<script>` block).
Paste it **just before `</body>`**, after the `<deck-stage>…</deck-stage>` markup.

It hooks the `slidechange` event that every Optimal deck's `deck-stage.js`
dispatches. No edits to `deck-stage.js` are needed or wanted.

### 4 · Verify
Open the deck and navigate to the payment slide. You should see:

- The tag fades and rises in about **0.8s after** the slide appears (so the
  price lands first).
- The small dot carries a **slow pulse** on a ~2.6s loop.
- Navigate away and back: the entrance **replays**.
- `Cmd/Ctrl + P`: in the print preview the tag is **static and fully visible**.
- With Reduce Motion on (System Settings → Accessibility): **no pulse**, and
  the tag simply appears.

If all five hold, you're done. Commit with a message like
*"Add auto-renew tag to the pricing slide"* and push.

---

## Rules

- **Copy is exact:** `Membership payment auto-renews`. Don't rephrase, don't
  add punctuation, don't title-case it (the CSS uppercases it).
- **One tag, one slide.** It belongs on the payment slide only.
- **Change nothing else.** No reflowing the card, no resizing the price, no
  "while I'm in here" fixes. If the slide needs other work, that's a separate
  change with its own review.
- **Don't edit `deck-stage.js`.**
- Keep the tag's inline styles as shipped; they're the deck's own capsule
  language (48px radius, sage fill, hairline border, 24px caps at .12em).

---

## Troubleshooting

| Symptom | Cause |
|---|---|
| Tag shows but never animates | `tag.js` wasn't pasted, or was pasted above the `<deck-stage>` markup. Move it to just before `</body>`. |
| Tag looks wrong on the surface (low contrast) | Wrong variant. Dark panel → Variant A; cream/white → Variant B. |
| Tag appears on the wrong slide | The markup was pasted into a different `<section>`. Each `<section>` is one slide. |
| Two tags | Pasted both variants. Keep one. |
| `.dk-tag` already exists in the file | That deck already has the tag. Nothing to do. |
| Pulse never stops | Correct — it's a live indicator. It stops under Reduce Motion and in print. |

---

## Handing this to Claude Code

Drop the kit folder next to the deck and paste this:

> Apply the auto-renew tag kit in `./optimal-auto-renew-tag-kit/` to this
> deck's `index.html`, following its README exactly: paste `tag.css` at the
> end of the main style block, paste the correct variant from `tag.html`
> directly beneath the renewal-cadence line on the payment slide, paste
> `tag.js` just before `</body>`. Make **no other changes** to any file. Then
> open the deck, go to the payment slide, and confirm with a screenshot that
> the tag is present and animating.

---

Optimal Clinic · 630 Huronia Road, Unit 5, Barrie ON · care@beoptimal.ca
