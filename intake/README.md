# Optimal — Medical Intake (intake only)

The patient-facing presentation for a **Longevity Membership (Core) medical
intake** at Optimal Health Clinic (Barrie, ON), for a patient who has **already
had their Introductory Meeting, was cleared by the NP, and joined**. 16 screens:
a personalised welcome, then 15 slides.

New on Oct 22, 2026. It is a fork of [`../intro-intake/`](../intro-intake/)
and runs on the same engine, cover screens and PDF export. Open it from the
launcher (`../`), or go straight to `intake/`.

## Why these slides

A patient arriving for intake-only has already sat through the intro deck. At
that meeting they were sold the membership, cleared by the NP, paid at the front
desk and booked this visit. So this deck drops everything that persuades, keeps
what a new member needs to start using their care, and frames the NP's intake.

| # | Slide | Source | Why |
|---|---|---|---|
| 1 | Welcome back. Let's get you *started*. | Title, **adapted** | Today's visit is the full medical intake. Outcome: onboarding complete. |
| 2 | This is Optimal | verbatim | A pause slide while the patient settles in. |
| 3 | Agenda for your *intake* | Agenda, **adapted** | Three parts: recap (admin), intake (NP), how care works (care team). No branch points, because the decisions are already made. |
| 4 | Here's where you *are* | **new**, built from the intro deck's onboarding checklist | Same five steps, same wording. Pay, schedule intake and clinic forms are **Done**; questions and complete intake are **Today**. |
| 5 | Part 1: A quick recap of your *membership* | divider, **adapted** | |
| 6 | Membership highlights | verbatim | |
| 7 | Meet the team | verbatim | They will be assigned a primary NP. |
| 8 | Annual Longevity Exam | verbatim | What membership starts with. |
| 9 | Wait-time promise | verbatim | How fast they can get care, now that they're a member. |
| 10 | Patient portal | verbatim | How they will book. |
| 11 | Rights & responsibilities | verbatim | How results and follow-ups work from here. |
| 12 | Part 2: Your full medical *intake* | divider, **adapted** | Hand-off to the NP. |
| 13 | "…will now complete your full medical *intake*." | Goals of care, **adapted** | The NP-led conversation. |
| 14 | Part 3: How care works from *here* | divider, **adapted** | |
| 15 | How care works from *here* + Questions | Next steps, **adapted** | Book, urgent, results, follow-ups, messages. Each line comes from the wait-time, portal or rights slide. Contact details and PDF export are kept. |

**Dropped from the intro + intake deck**, because the patient has heard it and
already decided:
- Mission and How we practice
- What happens next (the four paths)
- Substitute or supplement, and both patient-story slides
- Membership plans, Cancellation policy and Missed payment
- The goal-alignment and intake-now-or-later branch points

### New wording (needs Peter's sign-off)

The other decks' copy is client-approved. These phrases are new, written for
this deck:
- **Title:** "Welcome back. Let's get you started." / "Member onboarding · 2026" / "Today's visit: Full medical intake" / "Outcome: Onboarding complete"
- **Agenda:** "Agenda for your intake." / "In person · 3 parts" / the three part names / "Questions are welcome at any point — that's what today is for."
- **Where you are:** "Here's where you are." / "3 of 5 done" / the Done and Today markers
- **Dividers:** "A quick recap of your membership." / "Your full medical intake." / "How care works from here."
- **Intake slide:** "You and your nurse practitioner will now complete your full medical intake."
- **Close:** "Your membership" / "How care works from here." and these five rows:
  - Book appointments — Online, or call / text
  - Urgent concern — Same or next-day
  - Test results — We'll notify you if needed
  - Follow-ups — Book when your NP asks
  - Anything else — Send a secure message
  - plus "We're happy to talk anything through — today, or any time as a member."
- **Prep screen:** "Medical Intake · Preparation" / "Let's set up this visit." / "Date of visit"

**Assumptions to confirm:**
- The patient paid at their intro. The intro-only deck has them pay at the front desk before booking intake.
- Clinic forms are done before the visit. If they aren't, sort that out before Part 2.
- No visit length is stated, because no deck gives one for the intake alone.

## How it's built

`index.html` is **generated** from `../intro-intake/index.html` by
[`tools/build_from_intro_intake.py`](tools/build_from_intro_intake.py):

```bash
python3 intake/tools/build_from_intro_intake.py   # run from the repo root
```

The script copies the shared slides verbatim and rewrites only the slides
listed above. It also renumbers every footer (`NN / 16`) and renames the deck
in the `<title>`, the prep screen and the PDF filename.
- **To change a shared slide** (care team, wait times, portal, rights), edit it in `intro-intake/` and re-run the script. Then this deck stays in sync.
- **To change intake-only copy**, edit the script, not `index.html`, or the next run will overwrite your edit.

Everything else (navigation, fullscreen, the PDF export path, motion,
`deck-stage.js`) works exactly as described in
[`../intro-intake/README.md`](../intro-intake/README.md).
