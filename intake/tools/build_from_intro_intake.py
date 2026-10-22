"""Rebuild intake/index.html from intro-intake/index.html.

The Intake-only deck is a fork of the Introductory Meeting & Possible Intake
deck: same engine, cover screens and slide markup. This script keeps the
approved slides that matter to a patient who already had their intro and was
cleared, drops the ones that sell the membership, and writes the few new or
adapted slides. Re-run it after editing intro-intake so shared slides (care
team, wait times, portal, policies) stay in sync:

    python3 intake/tools/build_from_intro_intake.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "intro-intake" / "index.html"
OUT = ROOT / "intake" / "index.html"
DECK_NAME = "Medical Intake"

src = SRC.read_text()
open_tag = re.search(r"<deck-stage[^>]*>", src)
start = open_tag.end()
end = src.index("</deck-stage>")
body = src[start:end]

# Split the deck into its <section> slides, keyed by data-label.
sections = {}
for m in re.finditer(r"<section data-label=\"([^\"]+)\".*?</section>", body, re.S):
    sections[m.group(1)] = m.group(0)


def sub1(s, old, new):
    assert old in s, f"missing: {old[:80]}"
    return s.replace(old, new, 1)


def notes(s, text):
    return re.sub(r'data-speaker-notes="[^"]*"', f'data-speaker-notes="{text}"', s, count=1)


# ── 1. Title ────────────────────────────────────────────────────────────────
title = sections["Title"]
title = notes(title, "Welcome the patient back. They had their introductory meeting, were cleared by the NP, and joined. Today is the full medical intake, which completes onboarding.")
NB = "\u00a0\u00a0·\u00a0\u00a0"  # the decks space their eyebrow dots with non-breaking spaces
title = sub1(title, f"Patient orientation{NB}Spring 2026{NB}Barrie, ON", f"Member onboarding{NB}2026{NB}Barrie, ON")
title = sub1(title, ">Introductory meeting</div>", ">Medical intake</div>")
title = sub1(title, "Introductory meeting<br>&amp; possible <em>intake</em>.", "Welcome back.<br>Let's get you <em>started</em>.")
title = sub1(title, ">Today's meeting<", ">Today's visit<")
title = sub1(title, ">Up to ~60 minutes<", ">Full medical intake<")
title = sub1(title, ">Membership &amp; intake decision<", ">Onboarding complete<")

# ── 3. Agenda: three parts, no branch points ───────────────────────────────
agenda = sections["Agenda"]
agenda = notes(agenda, "Walk the three parts. Part 1 is a short recap they have heard before; the NP leads the intake.")
agenda = sub1(agenda, "Agenda for the introductory <em>meeting</em>.", "Agenda for your <em>intake</em>.")
agenda = sub1(agenda, "~60 minutes · 4 parts", "In person · 3 parts")
ROW = ('<div style="display:grid;grid-template-columns:140px 1fr 460px;align-items:center;border-top:1px solid rgba(44,78,37,.28);{extra}padding:44px 0">\n'
       '      <div style="font-family:Castoro,serif;font-size:44px;color:#1A500F">{n}</div>\n'
       '      <div style="font-family:Castoro,serif;font-size:40px;letter-spacing:-.02em">{name}</div>\n'
       '      <div style="text-align:right;font-size:24px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#75726B">{who}</div>\n'
       '    </div>')
rows = "\n    ".join([
    ROW.format(n="01", name="A quick recap of your membership", who="Admin team", extra=""),
    ROW.format(n="02", name="Your full medical intake", who="Nurse Practitioner", extra=""),
    ROW.format(n="03", name="How care works from here", who="Care team", extra="border-bottom:1px solid rgba(44,78,37,.28);"),
])
agenda = re.sub(r'<div style="flex:1;display:flex;flex-direction:column;justify-content:center">.*?<p style="margin:36px 0 0;font-size:27px;color:#5B5F55;letter-spacing:-.02em">If you decide to join — payment is handled at the front desk.</p>',
                lambda _: '<div style="flex:1;display:flex;flex-direction:column;justify-content:center">\n    ' + rows +
                '\n    <p style="margin:36px 0 0;font-size:27px;color:#5B5F55;letter-spacing:-.02em">Questions are welcome at any point — that\'s what today is for.</p>',
                agenda, count=1, flags=re.S)
assert "Branch point" not in agenda

# ── 4. Where you are: the onboarding checklist from the intro deck, with state ─
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="width:26px;height:26px;vertical-align:-4px;margin-right:12px"><path d="M4 12.5l5 5L20 6.5"/></svg>'
def step(n, name, detail, today, last=False):
    border = "border-bottom:1px solid rgba(44,78,37,.28);" if last else ""
    if today:
        state = '<span style="display:inline-block;padding:10px 22px;border-radius:8px;background:rgba(135,164,130,.25);color:#1A500F;font-size:24px;font-weight:600;letter-spacing:.12em;text-transform:uppercase">Today</span>'
        tone, num = "#040504", "#1A500F"
    else:
        state = f'<span style="font-size:24px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#1A500F">{CHECK}Done</span>'
        tone, num = "rgba(4,5,4,.42)", "rgba(26,80,18,.42)"
    return (f'<div style="display:grid;grid-template-columns:140px 1fr 420px 240px;align-items:center;border-top:1px solid rgba(44,78,37,.28);{border}padding:30px 0">'
            f'<div style="font-family:Castoro,serif;font-size:44px;color:{num}">{n}</div>'
            f'<div style="font-family:Castoro,serif;font-size:40px;letter-spacing:-.02em;color:{tone}">{name}</div>'
            f'<div style="font-size:24px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#75726B">{detail}</div>'
            f'<div style="text-align:right">{state}</div></div>')
steps = "\n    ".join([
    step("01", "Pay", "At the front desk", False),
    step("02", "Schedule intake", "For a later date", False),
    step("03", "Clinic forms", "Read and review", False),
    step("04", "Questions?", "Discuss at intake", True),
    step("05", "Complete intake", "In-person", True, last=True),
])
where = f'''<section data-label="Where you are" data-speaker-notes="The five onboarding steps from the intro meeting. Three are behind them; today finishes the last two. If clinic forms aren't done yet, sort that out before Part 2." style="position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;background:#FFFCF7;color:#040504;font-family:'Public Sans',system-ui,sans-serif;padding:88px 120px 130px;display:flex;flex-direction:column" class="sl">
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div>
      <div style="font-size:24px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:#1A500F">Patient onboarding</div>
      <h2 style="margin:24px 0 0;font-family:Castoro,serif;font-weight:400;font-size:76px;line-height:1.05;letter-spacing:-.03em">Here's where you <em>are</em>.</h2>
    </div>
    <div style="font-size:24px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:#75726B;padding-bottom:14px">3 of 5 done</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    {steps}
  </div>
  <div style="position:absolute;left:120px;right:120px;bottom:50px;display:flex;justify-content:space-between;align-items:center" class="dk-footer"><div style="font-size:24px;letter-spacing:-.01em;color:#8A867D"><span style="color:#1A500F;font-weight:600">00 / 00</span>  Introductory Meeting &amp; Possible Intake — Optimal Clinic, Barrie</div><img src="assets/logos/symbol-green-nobg.png" alt="" style="height:30px;opacity:.85" loading="eager" decoding="async"></div>
</section>'''

# ── Dividers ────────────────────────────────────────────────────────────────
def divider(base, n, h2_old, h2_new, part, note):
    s = notes(sections[base], note)
    s = re.sub(r">0\d</div>", f">{n}</div>", s, count=1)
    s = sub1(s, h2_old, h2_new)
    s = re.sub(r"Part \d of 4", f"Part {int(n)} of 3", s, count=1)
    return s

part1 = divider("Part 1 divider", "01", "Overview of Optimal <em>Membership</em>.", "A quick recap of your <em>membership</em>.", 1,
                "Part 1: a short recap of what the membership includes. They heard this at the intro, so keep it brisk and skip anything they are clear on.")
part2 = divider("Part 2 divider", "02", "Meet with your nurse <em>practitioner</em>.", "Your full medical <em>intake</em>.", 2,
                "Hand off from the admin team to the NP for the full medical intake.")
# Part 3 reuses the Part 1 divider layout (photo panel, no branch-point pill).
part3 = sections["Part 1 divider"]
part3 = notes(part3, "Part 3: how care works now that onboarding is complete.")
part3 = sub1(part3, 'data-label="Part 1 divider"', 'data-label="Part 3 divider"')
part3 = sub1(part3, "assets/photos/waiting_room_portrait_4x5.jpg", "assets/photos/reception_hallway_portrait_4x5.jpg")
part3 = re.sub(r">01</div>", ">03</div>", part3, count=1)
part3 = sub1(part3, "Overview of Optimal <em>Membership</em>.", "How care works from <em>here</em>.")
part3 = sub1(part3, "Part 1 of 4", "Part 3 of 3")

# ── 13. The intake itself ──────────────────────────────────────────────────
intake = sections["Goals of care"]
intake = sub1(intake, 'data-label="Goals of care"', 'data-label="Medical intake"')
intake = notes(intake, "The NP takes over for the full medical intake, one-on-one. Invite questions throughout.")
intake = sub1(intake, "You and your nurse practitioner will now discuss your goals of <em>care</em>.",
              "You and your nurse practitioner will now complete your full medical <em>intake</em>.")

# ── 15. Close: how care works from here ────────────────────────────────────
close = sections["Next steps"]
close = sub1(close, 'data-label="Next steps"', 'data-label="Care from here"')
close = notes(close, "Close: how to use the membership from today, drawn from the wait-time promise, the portal and rights &amp; responsibilities. Invite questions. Contact details on screen.")
close = sub1(close, ">Patient onboarding<", ">Your membership<")
close = sub1(close, "Next steps — let's get you <span", "How care works from <span")
close = sub1(close, "<em>started</em><span", "<em>here</em><span")
close = sub1(close, "inset:-10px -30px;", "inset:-10px -26px;")
CROW = ('<div style="display:grid;grid-template-columns:110px 1fr 470px;align-items:center;border-top:1px solid rgba(44,78,37,.28);{extra}padding:29px 0">'
        '<div style="font-family:Castoro,serif;font-size:38px;color:#1A500F">{n}</div>'
        '<div style="font-family:Castoro,serif;font-size:36px;letter-spacing:-.02em">{name}</div>'
        '<div style="text-align:right;font-size:24px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#75726B">{detail}</div></div>')
crows = "\n        ".join([
    CROW.format(n="01", name="Book appointments", detail="Online, or call / text", extra=""),
    CROW.format(n="02", name="Urgent concern", detail="Same or next-day", extra=""),
    CROW.format(n="03", name="Test results", detail="We'll notify you if needed", extra=""),
    CROW.format(n="04", name="Follow-ups", detail="Book when your NP asks", extra=""),
    CROW.format(n="05", name="Anything else", detail="Send a secure message", extra="border-bottom:1px solid rgba(44,78,37,.28);"),
])
close = re.sub(r'<div style="margin-top:52px">.*?</div>\n    </div>\n    <div style="background:linear-gradient',
               lambda _: '<div style="margin-top:52px">\n        ' + crows + '\n      </div>\n    </div>\n    <div style="background:linear-gradient',
               close, count=1, flags=re.S)
close = sub1(close, "We're happy to talk anything through — today or after you've thought it over.",
             "We're happy to talk anything through — today, or any time as a member.")

order = [
    title,
    sections["This is Optimal"],
    agenda,
    where,
    part1,
    sections["Membership highlights"],
    sections["Care team"],
    sections["Longevity Exam"],
    sections["Wait-time promise"],
    sections["Patient portal"],
    sections["Rights &amp; responsibilities"],
    part2,
    intake,
    part3,
    close,
]
total = len(order) + 1  # + the welcome screen, printed as 01

out = []
for i, s in enumerate(order, start=1):
    printed = i + 1
    s = re.sub(r'<span style="color:#1A500F;font-weight:600">\d\d / \d\d</span>',
               f'<span style="color:#1A500F;font-weight:600">{printed:02d} / {total}</span>', s)
    s = s.replace("Introductory Meeting &amp; Possible Intake — Optimal Clinic, Barrie", f"{DECK_NAME} — Optimal Clinic, Barrie")
    s = s.replace("Introductory Meeting &amp; Possible Intake</div>", f"{DECK_NAME}</div>")
    out.append(s)

deck = src[:start] + "\n\n" + "\n\n".join(out) + "\n\n" + src[end:]

# ── Chrome around the deck ─────────────────────────────────────────────────
deck = sub1(deck, "<title>Introductory Meeting &amp; Possible Intake — Optimal Clinic, Barrie</title>", f"<title>{DECK_NAME} — Optimal Clinic, Barrie</title>")
deck = sub1(deck, 'content="Patient orientation presentation for Optimal Clinic, Barrie — membership overview, care team, wait-time promise, plans, and next steps."',
            'content="Medical intake presentation for Optimal Clinic, Barrie — for members who had their introductory meeting and were cleared: where they are in onboarding, a membership recap, the intake, and how care works from here."')
deck = sub1(deck, "Introductory Meeting & Possible Intake — Optimal Clinic, Barrie\n", f"{DECK_NAME} (intake only) — Optimal Clinic, Barrie\n     Generated from ../intro-intake by tools/build_from_intro_intake.py.\n")
deck = sub1(deck, "The 24 slides below", f"The {len(order)} slides below")
deck = sub1(deck, '<div class="prep-eyebrow">Introductory Meeting · Preparation</div>', '<div class="prep-eyebrow">Medical Intake · Preparation</div>')
deck = sub1(deck, "Let's set up <em>this meeting</em>.", "Let's set up <em>this visit</em>.")
deck = sub1(deck, '<span class="field-label">Date of meeting</span>', '<span class="field-label">Date of visit</span>')
deck = sub1(deck, "the welcome screen is 01 of the printed 25 but", f"the welcome screen is 01 of the printed {total} but")
deck = sub1(deck, 'printed "02 / 25"', f'printed "02 / {total}"')
deck = sub1(deck, "'Optimal — Introductory Meeting — '", f"'Optimal — {DECK_NAME} — '")

assert "Possible Intake" not in deck.split("<deck-stage")[1], "stale deck name inside the deck"
OUT.write_text(deck)
print(f"wrote {OUT.relative_to(ROOT)}: {len(order)} slides, printed /{total}")
