"""Build talks/iron-deficiency/index.html and sources.html.

    python3 talks/iron-deficiency/tools/build_deck.py      # from the repo root

The chrome (cover screens, reveal engine, PDF export, fullscreen) is copied from
../../intro/index.html so every Optimal deck behaves the same. ../../tools/talk_chrome.py then
applies what all talks share: no foliage on the cover screens, and the motion layer. The slides
are below.

Copy source: the clinical team's draft talk (Nov 4 2026). Citations were checked against
PubMed and the CMAJ full text. Any change to a fact needs a citation and clinical review.
"""
import math
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'talks' / 'tools'))
import talk_chrome  # noqa: E402

DECK = ROOT / 'talks' / 'iron-deficiency'
SRC = (ROOT / 'intro' / 'index.html').read_text()
NAME = 'Iron Deficiency in Women'
VERSION = 'iron-deficiency-talk v1.2.0'
NB = '  ·  '

# ── Tokens: the same set as the HBOT deck, at the 1920 artboard's ~2x scale ──
CREAM, INK, INK2, MUTED = '#FFFCF7', '#040504', '#474747', '#76736D'
GREEN, GREEN_DEEP, SAGE, LINE, SAGE50 = '#2C4E25', '#1A500F', '#87A482', '#DFD7CA', '#F0F4EE'
SAGE100, SAGE200, SAGE300 = '#DDE7D2', '#C3D2BE', '#A5BBA0'
EYEBROW = f"font-size:24px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:{GREEN_DEEP}"
EYEBROW_D = "font-size:24px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,252,247,.66)"
H2 = f"margin:22px 0 0;font-family:Castoro,serif;font-weight:400;font-size:76px;line-height:1.05;letter-spacing:-.03em;color:{INK}"
BODY = f"font-size:30px;line-height:1.46;letter-spacing:-.012em;color:{INK2}"
CAPS = f"font-size:22px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:{MUTED}"
SERIF = "font-family:Castoro,serif;font-weight:400"
SVGTXT = "font-family=\"Public Sans, system-ui, sans-serif\""
SVGSER = "font-family=\"Castoro, serif\""
SECTION = ("position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;"
           "font-family:'Public Sans',system-ui,sans-serif;")
LIGHT = SECTION + f"background:{CREAM};color:{INK};"
DARK = SECTION + f"background:linear-gradient(135deg,{GREEN} 0%,#1C3118 100%);color:{CREAM};"
PAD = "padding:88px 120px 172px;display:flex;flex-direction:column"

# ── Sources: numbered once, cited by key on the slides, listed on the last slide
#    and on sources.html (the QR code opens that page) ───────────────────────────
SOURCES = [
    ('cmaj', 'Sholzberg et al., CMAJ 2025', 'Sholzberg M, Hillis C, Crowther M, Selby R.', 'Diagnosis and management of iron deficiency in females.', 'CMAJ 2025;197(24):E680–E687.', 'https://doi.org/10.1503/cmaj.240570'),
    ('naseem', 'Al-Naseem et al., Clin Med 2021', 'Al-Naseem A, Sallam A, Choudhury S, Thachil J.', 'Iron deficiency without anaemia: a diagnosis that matters.', 'Clin Med (Lond) 2021;21(2):107–113.', 'https://doi.org/10.7861/clinmed.2020-0582'),
    ('abdelhay', 'Abdelhay et al., Am J Hematol 2026', 'Abdelhay A, Reghis M, Salhab T, Jadhav N, Sholzberg M, Kouides P.', 'Impact of optimizing the lower limit of normal for ferritin on iron deficiency diagnosis and treatment patterns: a pre and post-intervention study using EHR data.', 'Am J Hematol 2026;101(3):439–446.', 'https://doi.org/10.1002/ajh.70198'),
    ('cycle', 'Balakirishnan et al., Front Biosci 2026', 'Balakirishnan D, Dukovski F, Bytheway H, Dugan C.', 'Cyclical iron homeostasis: the role of sex hormones in female iron regulation.', 'Front Biosci (Landmark Ed) 2026;31(9):54404.', 'https://doi.org/10.31083/FBL54404'),
    ('ahanchi', 'Ahanchi et al., Clin Nutr 2024', 'Ahanchi NS, Khatami F, Llanaj E, et al.', 'The complementary roles of iron and estrogen in menopausal differences in cardiometabolic outcomes.', 'Clin Nutr 2024;43(5):1136–1150.', 'https://doi.org/10.1016/j.clnu.2024.03.026'),
    ('fiani', 'Fiani et al., Neurosci Biobehav Rev 2025', 'Fiani D, Chahine S, Zaboube M, Solmi M, Powers JM, Calarge C.', 'Psychiatric and cognitive outcomes of iron supplementation in non-anemic children, adolescents, and menstruating adults: a meta-analysis and systematic review.', 'Neurosci Biobehav Rev 2025;178:106372.', 'https://doi.org/10.1016/j.neubiorev.2025.106372'),
    ('beatrix', 'Beatrix et al., Eur J Clin Nutr 2022', 'Beatrix J, Piales C, Berland P, Marchiset E, Gerbaud L, Ruivard M.', 'Non-anemic iron deficiency: correlations between symptoms and iron status parameters.', 'Eur J Clin Nutr 2022;76(6):835–840.', 'https://doi.org/10.1038/s41430-021-01047-5'),
    ('dziem', 'Dziembowska et al., Physiol Behav 2019', 'Dziembowska I, Kwapisz J, Izdebski P, Żekanowska E.', 'Mild iron deficiency may affect female endurance and behavior.', 'Physiol Behav 2019;205:44–50.', 'https://doi.org/10.1016/j.physbeh.2018.09.012'),
    ('scott', 'Scott &amp; Murray-Kolb, J Nutr 2016', 'Scott SP, Murray-Kolb LE.', 'Iron status is associated with performance on executive functioning tasks in nonanemic young women.', 'J Nutr 2016;146(1):30–37.', 'https://doi.org/10.3945/jn.115.223586'),
    ('murray', 'Murray-Kolb, J Nutr 2011', 'Murray-Kolb LE.', 'Iron status and neuropsychological consequences in women of reproductive age: what do we know and where are we headed?', 'J Nutr 2011;141(4):747S–755S.', 'https://doi.org/10.3945/jn.110.130658'),
    ('easl', 'EASL guidelines 2022', 'European Association for the Study of the Liver.', 'EASL clinical practice guidelines on haemochromatosis.', 'J Hepatol 2022;77(2):479–502.', 'https://doi.org/10.1016/j.jhep.2022.03.033'),
    ('chang', 'Chang et al., BMC Cancer 2019', 'Chang VC, Cotterchio M, Khoo E.', 'Iron intake, body iron status, and risk of breast cancer: a systematic review and meta-analysis.', 'BMC Cancer 2019;19:543.', 'https://doi.org/10.1186/s12885-019-5642-0'),
    ('correnti', 'Correnti et al., Biomedicines 2026', 'Correnti M, Gammella E, Cairo G, Recalcati S.', 'The interplay between bone biology and iron metabolism: molecular mechanisms and clinical implications.', 'Biomedicines 2026;14(2):301.', 'https://doi.org/10.3390/biomedicines14020301'),
    ('fischer', 'Fischer et al., Nutr Rev 2023', 'Fischer JAJ, Cherian AM, Bone JN, Karakochuk CD.', 'The effects of oral ferrous bisglycinate supplementation on hemoglobin and ferritin concentrations in adults and children: a systematic review and meta-analysis of randomized controlled trials.', 'Nutr Rev 2023;81(8):904–920.', 'https://doi.org/10.1093/nutrit/nuac106'),
    ('li', 'Li et al., JAMA Netw Open 2020', 'Li N, Zhao G, Wu W, et al.', 'The efficacy and safety of vitamin C for iron supplementation in adult patients with iron deficiency anemia: a randomized clinical trial.', 'JAMA Netw Open 2020;3(11):e2023644.', 'https://doi.org/10.1001/jamanetworkopen.2020.23644'),
    ('ods', 'NIH Office of Dietary Supplements', 'NIH Office of Dietary Supplements.', 'Iron: fact sheet for health professionals.', '', 'https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/'),
    ('maltol', 'Health Canada approval notice, 2024', 'KYE Pharmaceuticals.', 'Health Canada approval of ferric maltol for iron deficiency anemia in adults (press release).', 'August 27, 2024.', 'https://www.newswire.ca/fr/news-releases/kye-pharmaceuticals-annonce-l-approbation-au-canada-d-accrufer-r-maltol-ferrique-pour-le-traitement-de-l-anemie-ferriprive-chez-les-patients-adultes-826210146.html'),
]
SHORT = {s[0]: s[1] for s in SOURCES}


def cite(*keys, note=''):
    """One quiet line above the footer: who said this, so it can be looked up."""
    txt = '; '.join(SHORT[k] for k in keys)
    tail = f' {note}' if note else ''
    return (f'<div class="ir-cite" style="position:absolute;left:120px;right:120px;bottom:100px;font-size:21px;line-height:1.35;color:{MUTED}">'
            f'Source: {txt}.{tail}</div>')


def paper(key, kind):
    """The study slides lead with the paper itself, as the draft did."""
    s = next(x for x in SOURCES if x[0] == key)
    return (f'<div class="ir-cite" style="position:absolute;left:120px;right:120px;bottom:100px;font-size:21px;line-height:1.35;color:{MUTED}">'
            f'{kind}. {s[2]} {s[3]} {s[4]}</div>')


def ring(word, inset='-8px -24px', rot=-2.5, delay='.95s', margin='0'):
    """The design system's hand-drawn ring. One per slide at most, and few in the deck."""
    return (f'<span style="position:relative;display:inline-block;margin:{margin}"><em>{word}</em>'
            f'<span class="dk-ring" style="position:absolute;inset:{inset};border:3px solid rgba(26,80,18,.5);'
            f'border-radius:50%;transform:rotate({rot}deg);pointer-events:none;--rot:{rot}deg;--ring-d:{delay}"></span></span>')


def footer(dark=False):
    if dark:
        return ('<div class="dk-footer" style="position:absolute;left:120px;right:120px;bottom:50px;display:flex;justify-content:space-between;align-items:center">'
                '<div style="font-size:24px;letter-spacing:-.01em;color:rgba(255,252,247,.5)"><span style="color:#FFFCF7;font-weight:600">{N}</span>  '
                f'{NAME} — Optimal Clinic, Barrie</div><img src="assets/logos/symbol-white.png" alt="" style="height:30px;opacity:.7" loading="eager" decoding="async"></div>')
    return ('<div class="dk-footer" style="position:absolute;left:120px;right:120px;bottom:50px;display:flex;justify-content:space-between;align-items:center">'
            '<div style="font-size:24px;letter-spacing:-.01em;color:#8A867D"><span style="color:#1A500F;font-weight:600">{N}</span>  '
            f'{NAME} — Optimal Clinic, Barrie</div><img src="assets/logos/symbol-green-nobg.png" alt="" style="height:30px;opacity:.85" loading="eager" decoding="async"></div>')


def head(eyebrow, title, size=84):
    return f'<div><div style="{EYEBROW}">{eyebrow}</div><h2 style="{H2};font-size:{size}px">{title}</h2></div>'


def row(title, body, top=True, size=38):
    edge = f'border-top:2px solid {LINE};' if top else ''
    return (f'<div style="{edge}padding:21px 0 23px">'
            f'<div style="{SERIF};font-size:{size}px;line-height:1.12;letter-spacing:-.02em;color:{INK}">{title}</div>'
            f'<div style="margin-top:9px;font-size:29px;line-height:1.36;letter-spacing:-.012em;color:{INK2}">{body}</div></div>')


slides = []


def add(label, notes, style, body, cls='sl'):
    slides.append(f'<section data-label="{label}" data-speaker-notes="{notes}" style="{style}" class="{cls}">\n{body}\n</section>')


def part_ticks(n):
    """Where this part sits in the talk: earlier parts full, this one drawing in."""
    cells = ''
    for i in range(1, 5):
        inner = ''
        if i < n:
            inner = f'<span style="display:block;height:100%;background:{CREAM}"></span>'
        elif i == n:
            inner = f'<span class="ir-bar" style="--d:.55s;display:block;height:100%;background:{CREAM}"></span>'
        cells += f'<span style="display:block;width:64px;height:3px;background:rgba(255,252,247,.22)">{inner}</span>'
    return f'<div style="display:flex;gap:8px">{cells}</div>'


def divider(n, title, img, notes):
    add(f'Part {n} divider', notes, DARK + 'padding:88px 120px 96px;display:flex;flex-direction:column', f'''
  <div class="dk-panel ir-breathe" style="position:absolute;top:140px;right:120px;width:800px;height:800px;display:flex;align-items:center;justify-content:center">
    <img class="ir-ink" style="--d:.2s;--dur:1700ms;max-width:100%;max-height:100%;display:block" src="assets/images/{img}.webp" alt="" loading="eager" decoding="async">
  </div>
  <div style="display:flex;align-items:center;gap:32px"><div style="{EYEBROW_D}">Part {n} of 4</div>{part_ticks(n)}</div>
  <div style="flex:1;display:flex;align-items:center">
    <h1 style="margin:0;max-width:860px;{SERIF};font-size:118px;line-height:1.02;letter-spacing:-.035em;color:{CREAM}">{title}</h1>
  </div>
  {footer(dark=True)}''', 'sl sl-dark')


# 1 ── Title ───────────────────────────────────────────────────────────────────
add('Title', 'Welcome the group. This is a talk about iron in women: how we measure it, what happens when it runs high or low, and what the treatment options are. Educational only.', LIGHT + 'padding:88px 120px 96px', f'''
  <div class="dk-panel ir-breathe" style="position:absolute;top:96px;right:92px;width:800px;height:800px">
    <img class="ir-iris" src="assets/images/blood-field.webp" alt="Illustrative blood smear seen through a microscope" style="width:100%;height:100%;object-fit:contain;display:block" loading="eager" decoding="async">
    <div style="margin-top:14px;text-align:center;font-size:20px;font-style:italic;color:{MUTED}">Blood smear, illustrative</div>
  </div>
  <div style="width:900px;height:100%;display:flex;flex-direction:column">
    <div>
      <img src="assets/logos/OptimalLogo-Green.png" alt="Optimal" style="height:44px" loading="eager" decoding="async">
      <div style="margin-top:26px;padding-bottom:26px;border-bottom:2px solid {LINE};{CAPS};letter-spacing:.22em">Educational talk{NB}2026{NB}Barrie, ON</div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
      <div style="{EYEBROW}">A women&rsquo;s health talk from Optimal</div>
      <h1 style="margin:28px 0 0;{SERIF};font-size:128px;line-height:1;letter-spacing:-.04em;color:{GREEN}">Iron deficiency<br>in <em>women</em>.</h1>
      <p style="margin:40px 0 0;max-width:860px;font-size:32px;line-height:1.45;letter-spacing:-.015em;color:{INK2}">How we measure it, what it does, and how it&rsquo;s treated.</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:36px;border-top:2px solid {LINE};padding-top:30px">
      <div><div style="{CAPS};font-size:20px">Format</div><div style="margin-top:12px;{SERIF};font-size:30px;letter-spacing:-.015em;color:{GREEN}">Group talk</div></div>
      <div><div style="{CAPS};font-size:20px">Covers</div><div style="margin-top:12px;{SERIF};font-size:30px;letter-spacing:-.015em;color:{GREEN}">Testing to treatment</div></div>
      <div><div style="{CAPS};font-size:20px">Evidence</div><div style="margin-top:12px;{SERIF};font-size:30px;letter-spacing:-.015em;color:{GREEN}">{len(SOURCES)} sources cited</div></div>
    </div>
  </div>''')


# 2 ── The pyramid ─────────────────────────────────────────────────────────────
def pyramid():
    tiers = [
        (GREEN, f'<span><em style="color:{GREEN}">Nutraceuticals</em> and additional supplements</span>'),
        (SAGE, 'Protein, carb and fat intake; goal-specific activity'),
        (SAGE300, 'Quantity of activity'),
        (SAGE200, 'Mental well-being'),
        (SAGE100, 'Adequate rest, caloric intake, hydration and safety'),
    ]
    rh, gap, half = 150, 8, 320
    total = 5 * rh - gap
    polys, labels = [], []
    for i, (fill, text) in enumerate(tiers):
        y0, y1 = i * rh, i * rh + rh - gap
        h0, h1 = half * y0 / total, half * y1 / total
        d = f'{(4 - i) * 0.16 + 0.35:.2f}s'
        polys.append(f'<polygon class="ir-tier" style="--d:{d}" points="{half - h0:.1f},{y0} {half + h0:.1f},{y0} {half + h1:.1f},{y1} {half - h1:.1f},{y1}" fill="{fill}"/>')
        edge = f'border-top:2px solid {LINE};' if i else ''
        labels.append(f'<div class="ir-build" style="--d:{d};height:{rh}px;box-sizing:border-box;{edge}display:flex;align-items:center;{SERIF};font-size:36px;line-height:1.14;letter-spacing:-.02em;color:{INK}">{text}</div>')
    return (f'<div style="display:grid;grid-template-columns:640px 1fr;gap:48px;width:1160px">'
            f'<svg viewBox="0 0 640 {total}" style="width:640px;height:{total}px;display:block;overflow:visible" role="img" aria-label="A five-level pyramid, with supplements at the top">{"".join(polys)}</svg>'
            f'<div>{"".join(labels)}</div></div>')


add('Foundations', 'Everything underneath matters before supplements do. Rest, enough food, hydration and safety first, then mental well-being, activity, then the fine-tuning. Nutraceuticals are the small tip of the pyramid.', LIGHT + 'padding:88px 120px 110px;display:grid;grid-template-columns:1fr 1160px;gap:60px;align-items:center', f'''
  <div>
    <div style="{EYEBROW}">Start at the base</div>
    <h2 style="{H2}">Supplements sit at the <em>top</em>.</h2>
    <p style="margin:34px 0 0;{BODY};font-size:32px">Get the base right first. They&rsquo;re the last layer, not the first.</p>
  </div>
  {pyramid()}
  {footer()}''')


# 3 ── Six dietary building blocks ─────────────────────────────────────────────
def hexagon():
    cx, cy, rn, rh = 450, 400, 296, 120
    names = ['Protein', 'Water', 'Nutraceuticals', 'Fatty acids', 'Vitamins', 'Minerals']
    parts = []
    hexpts = ' '.join(f'{cx + rh * math.cos(math.radians(a)):.1f},{cy + rh * math.sin(math.radians(a)):.1f}' for a in range(-90, 270, 60))
    for i, n in enumerate(names):
        a = math.radians(-90 + i * 60)
        x, y = cx + rn * math.cos(a), cy + rn * math.sin(a)
        ix, iy = cx + rh * math.cos(a), cy + rh * math.sin(a)
        d = 0.5 + i * 0.1
        on = n == 'Minerals'
        fill = GREEN if on else CREAM
        tcol = CREAM if on else INK
        style = 'italic' if on else 'normal'
        dim = '' if on else ' class="ir-dim"'
        ex, ey = cx + (rn - 104) * math.cos(a), cy + (rn - 104) * math.sin(a)  # stops at the circle's edge
        parts.append(f'<g{dim}><line class="ir-draw" pathLength="1" style="--d:{d - .16:.2f}s;--dur:460ms" x1="{ix:.1f}" y1="{iy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{SAGE}" stroke-width="2.5"/>'
                     f'<g class="ir-pop" style="--d:{d:.2f}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="104" fill="{fill}" stroke="{GREEN}" stroke-width="2.5"/>'
                     f'<text x="{x:.1f}" y="{y + 11:.1f}" text-anchor="middle" {SVGSER} font-size="{27 if n == "Nutraceuticals" else 32}" font-style="{style}" fill="{tcol}">{n}</text></g></g>')
    a = math.radians(210)
    mx, my = cx + rn * math.cos(a), cy + rn * math.sin(a)
    return (f'<svg viewBox="0 0 900 800" style="width:880px;height:782px;display:block;overflow:visible" role="img" aria-label="Six dietary building blocks around a hexagon, with minerals highlighted">'
            f'<g class="ir-pop" style="--d:.2s"><polygon points="{hexpts}" fill="{SAGE50}" stroke="{GREEN}" stroke-width="2.5"/>'
            f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" {SVGSER} font-style="italic" font-size="42" fill="{GREEN}">Dietary</text></g>'
            f'{"".join(parts)}'
            f'<g transform="rotate(-6 {mx:.1f} {my:.1f})"><ellipse class="ir-draw" pathLength="1" style="--d:1.3s;--dur:1000ms" cx="{mx:.1f}" cy="{my:.1f}" rx="128" ry="118" fill="none" stroke="rgba(26,80,18,.55)" stroke-width="3" stroke-linecap="round"/></g></svg>')


add('Dietary building blocks', 'Diet has six building blocks: protein, water, nutraceuticals, fatty acids, vitamins and minerals. Iron is a mineral, and it is the one we will zoom in on today.', LIGHT + 'padding:88px 120px 110px;display:grid;grid-template-columns:1fr 880px;gap:40px;align-items:center', f'''
  <div>
    <div style="{EYEBROW}">Zooming in</div>
    <h2 style="{H2};font-size:96px">Today, one <em>mineral</em>.</h2>
    <p style="margin:34px 0 0;{BODY};font-size:32px">Diet has six building blocks. This talk is about one mineral within them: iron.</p>
  </div>
  {hexagon()}
  {footer()}''')


# 4 ── Agenda ──────────────────────────────────────────────────────────────────
def agenda_part(n, img, name, label, d):
    """Each part previews the engraving on its divider, in green ink on cream."""
    return (f'<div style="display:flex;flex-direction:column">'
            f'<div style="height:340px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:26px;box-sizing:border-box"><img class="ir-ink" src="assets/images/{img}.webp" alt="" style="--d:{d:.2f}s;--dur:1300ms;max-width:86%;max-height:100%;display:block" loading="eager" decoding="async"></div>'
            f'<div style="border-top:2px solid {LINE};padding-top:22px;{SERIF};font-size:44px;line-height:1;color:{GREEN_DEEP}">{n}</div>'
            f'<div style="margin-top:16px;min-height:150px;{SERIF};font-size:46px;line-height:1.08;letter-spacing:-.022em">{name}</div>'
            f'<div style="margin-top:14px;{CAPS}">{label}</div></div>')


add('Agenda', 'Four parts: how we evaluate iron stores, what iron levels mean, what happens when iron is too high or too low, and how it is treated.', LIGHT + 'padding:88px 120px 130px;display:flex;flex-direction:column', f'''
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    {head('Today', 'What we&rsquo;ll <em>cover</em>.')}
    <div style="{CAPS};padding-bottom:14px">4 parts</div>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:repeat(4,1fr);column-gap:44px;align-content:center">
    {agenda_part('01', 'test-tubes', 'How we evaluate iron stores', 'Ferritin', .3)}
    {agenda_part('02', 'vein-red-cells', 'Iron levels', 'What iron does', .45)}
    {agenda_part('03', 'woman-tired-armchair', 'Consequences of high and low iron', 'The evidence', .6)}
    {agenda_part('04', 'iron-tablets', 'Treatment options', 'Pill, IV, diet', .75)}
  </div>
  {footer()}''')

divider(1, 'How we evaluate iron <em>stores</em>.', 'test-tubes-cream', 'Part 1: how we evaluate iron stores.')


# 6 ── Ferritin: the magnifier finds it ────────────────────────────────────────
def lab_card():
    labels = ['Hemoglobin', 'Ferritin', 'Transferrin saturation']
    rows = []
    for i, name in enumerate(labels):
        y = 190 + i * 196
        rows.append(f'<text x="56" y="{y + 12}" {SVGTXT} font-size="30" fill="{INK2}">{name}</text>'
                    f'<rect class="ir-grow" style="--d:{.25 + i * .12:.2f}s" x="520" y="{y - 14}" width="{230 - i * 28}" height="28" rx="4" fill="{SAGE100}"/>'
                    + (f'<line x1="56" y1="{y + 98}" x2="804" y2="{y + 98}" stroke="{LINE}" stroke-width="2"/>' if i < 2 else ''))
    return f'''<svg viewBox="0 0 860 730" style="width:860px;height:730px;display:block;overflow:visible" role="img" aria-label="A magnifying glass moves over a lab report and stops on ferritin">
  <rect x="1" y="1" width="858" height="700" rx="8" fill="#fff" stroke="{LINE}" stroke-width="2"/>
  <text x="56" y="84" {SVGTXT} font-size="24" font-weight="600" letter-spacing="4" fill="{MUTED}">TEST RESULTS</text>
  <line x1="56" y1="112" x2="804" y2="112" stroke="{GREEN}" stroke-width="2"/>
  {''.join(rows)}
  <g class="ir-lens">
    <line x1="328" y1="502" x2="410" y2="584" stroke="{GREEN}" stroke-width="28" stroke-linecap="round"/>
    <circle cx="212" cy="386" r="158" fill="{CREAM}" stroke="{GREEN}" stroke-width="14"/>
    <circle cx="212" cy="386" r="146" fill="none" stroke="{SAGE100}" stroke-width="2"/>
    <path d="M112 322 A122 122 0 0 1 176 270" fill="none" stroke="{SAGE200}" stroke-width="5" stroke-linecap="round"/>
    <text class="ir-lens-word" x="212" y="411" text-anchor="middle" {SVGSER} font-style="italic" font-size="78" fill="{GREEN}">Ferritin</text>
  </g>
</svg>'''


add('Ferritin', 'Two tests to start: a complete blood count picks up anemia, and ferritin tells us about stores. Ferritin is the best screening test because it most accurately reflects stores and is not sensitive to recent dietary intake. Caveat: it is an acute-phase reactant, so inflammation pushes it up even when iron is low. In that case we add full iron studies, fasting.', LIGHT + 'padding:88px 120px 150px;display:grid;grid-template-columns:1fr 860px;gap:70px;align-items:center', f'''
  <div>
    <div style="{EYEBROW}">How we evaluate</div>
    <h2 style="{H2}">One test does the <em>most</em>.</h2>
    <p style="margin:26px 0 30px;{BODY}">A blood count picks up anemia. Ferritin tells us about your stores.</p>
    {row('Reflects your stores', 'The best screening test for iron deficiency.')}
    {row('Not swayed by your last meal', 'Recent eating doesn&rsquo;t change it.')}
    {row('Reads high with inflammation', 'It can look normal even when iron is low.')}
  </div>
  {lab_card()}
  {cite('cmaj')}
  {footer()}''')


# 7 ── Venn ────────────────────────────────────────────────────────────────────
def venn():
    return f'''<svg viewBox="0 0 980 620" style="width:980px;height:620px;display:block;overflow:visible" role="img" aria-label="Two overlapping circles: iron deficiency without anemia, anemia from other causes, and iron deficiency anemia where they overlap">
  <defs><clipPath id="ir-venn-clip"><circle cx="350" cy="310" r="300"/></clipPath></defs>
  <circle class="ir-venn-l" cx="350" cy="310" r="300" fill="{SAGE100}"/>
  <circle class="ir-venn-r" cx="630" cy="310" r="300" fill="{SAGE50}" stroke="{SAGE100}" stroke-width="2"/>
  <g class="ir-fade" style="--d:.8s"><circle cx="630" cy="310" r="300" fill="{GREEN}" clip-path="url(#ir-venn-clip)"/></g>
  <g {SVGSER} font-size="36" text-anchor="middle">
    <g class="ir-build" style="--d:.8s"><text x="190" y="296" fill="{INK}">Iron deficiency,</text><text x="190" y="340" fill="{INK}">no anemia</text></g>
    <g class="ir-build" style="--d:1.1s"><text x="490" y="274" fill="{CREAM}" font-style="italic">Iron</text><text x="490" y="318" fill="{CREAM}" font-style="italic">deficiency</text><text x="490" y="362" fill="{CREAM}" font-style="italic">anemia</text></g>
    <g class="ir-build" style="--d:.95s"><text x="790" y="296" fill="{INK}">Anemia from</text><text x="790" y="340" fill="{INK}">other causes</text></g>
  </g>
</svg>'''


def stat_big(num, body):
    return (f'<div style="border-top:2px solid {LINE};padding:20px 0 26px">'
            f'<div class="ir-num" style="{SERIF};font-size:96px;line-height:1;letter-spacing:-.03em;color:{GREEN}">{num}</div>'
            f'<div style="margin-top:12px;font-size:29px;line-height:1.36;letter-spacing:-.012em;color:{INK2}">{body}</div></div>')


add('Not always anemia', 'Iron deficiency and anemia overlap but they are not the same thing. In a 2022 Ontario study of screening samples, 38 percent of nonpregnant females screened had iron deficiency without anemia and 13 percent had iron deficiency anemia. The blood count is typically normal in that first group, so without a ferritin it can be missed.', LIGHT + PAD, f'''
  {head('How we evaluate', 'Low iron isn&rsquo;t always <em>anemia</em>.')}
  <div style="flex:1;display:grid;grid-template-columns:980px 1fr;gap:70px;align-items:center">
    {venn()}
    <div>
      {stat_big('38%', 'of nonpregnant females screened in Ontario had iron deficiency without anemia.')}
      {stat_big('13%', 'had iron deficiency anemia.')}
      <p style="margin:0;padding-top:20px;border-top:2px solid {LINE};{SERIF};font-size:30px;line-height:1.25;letter-spacing:-.015em;color:{GREEN}">Without anemia, a blood count is typically normal.</p>
    </div>
  </div>
  {cite('cmaj')}
  {footer()}''')


# 8 ── The ferritin line ───────────────────────────────────────────────────────
def scale():
    k = 21  # px per µg/L, on an 80 µg/L ruler
    segs = [(0, 15, '#1C3118'), (15, 30, GREEN), (30, 50, SAGE), (50, 80, SAGE100)]
    rects = ''.join(f'<rect class="ir-seg" style="--d:{.12 + i * .2:.2f}s" x="{a * k + (2 if i else 0)}" y="64" width="{(b - a) * k - (2 if i else 0)}" height="128" fill="{c}"/>' for i, (a, b, c) in enumerate(segs))
    return f'''<svg viewBox="0 0 1680 264" style="width:1680px;height:264px;display:block;overflow:visible" role="img" aria-label="A ferritin scale. The lower limit of normal moved from 12 to 15 up to 30 micrograms per litre.">
  <defs><clipPath id="ir-scale-clip"><rect x="0" y="64" width="1680" height="128" rx="6"/></clipPath></defs>
  <g clip-path="url(#ir-scale-clip)">{rects}</g>
  <g class="ir-fade" style="--d:.5s"><line x1="{15 * k}" y1="44" x2="{15 * k}" y2="212" stroke="{INK2}" stroke-width="3" stroke-dasharray="7 7"/>
    <text x="{15 * k + 8}" y="28" text-anchor="end" {SVGTXT} font-size="24" font-weight="600" fill="{MUTED}">Old lower limit, 12–15</text></g>
  <g class="ir-marker"><line x1="{30 * k}" y1="44" x2="{30 * k}" y2="212" stroke="{INK}" stroke-width="5"/>
    <text x="{30 * k}" y="28" text-anchor="middle" {SVGTXT} font-size="24" font-weight="700" fill="{INK}">Lower limit since 2024, 30</text></g>
  <g {SVGSER} font-size="34" fill="{INK}" text-anchor="middle">
    <text x="{15 * k}" y="254">15</text><text x="{30 * k}" y="254">30</text><text x="{50 * k}" y="254">50</text>
  </g>
  <text x="1680" y="250" text-anchor="end" {SVGTXT} font-size="23" fill="{MUTED}">Ferritin, µg/L (the same number as ng/mL)</text>
</svg>'''


def zone(width, title, body):
    return (f'<div style="width:{width}px;box-sizing:border-box;padding-right:26px">'
            f'<div style="{SERIF};font-size:38px;line-height:1.1;letter-spacing:-.018em;color:{GREEN_DEEP}">{title}</div>'
            f'<div style="margin-top:8px;font-size:27px;line-height:1.32;letter-spacing:-.01em;color:{INK2}">{body}</div></div>')


def treat(num, who):
    return (f'<div style="display:flex;align-items:baseline;gap:18px">'
            f'<span style="{SERIF};font-size:68px;line-height:1;letter-spacing:-.03em;color:{GREEN}">&lt;{num}</span>'
            f'<span style="font-size:27px;color:{INK2}">{who}</span></div>')


add('Where the line moved', 'In 2024 the lower limit of normal for ferritin was raised in the largest Canadian community labs and some hospitals, from 12 to 15 up to 30 for adults and 20 for children. A value under 50 already goes with abnormal iron markers and increased gut absorption. Treatment is indicated below 50 in pregnancy, below 30 in other adults and below 20 in children. On oral iron, the target is 50 or higher. With inflammation and a ferritin of 30 or more, transferrin saturation under 20 percent fits iron deficiency.', LIGHT + PAD, f'''
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:60px">
    {head('How we evaluate', 'Where the line <em>moved</em>.')}
    <p style="margin:0 0 8px;max-width:760px;{BODY}">In 2024, Canada&rsquo;s largest community labs raised the lower limit of normal for ferritin.</p>
  </div>
  <div style="margin-top:44px">{scale()}</div>
  <div style="margin-top:22px;display:flex">
    {zone(315, 'Under 15', 'Flagged low by the old range.')}
    {zone(315, '15 to 30', 'Iron deficiency. Often missed before.')}
    {zone(420, '30 to 50', 'Possible deficiency. With inflammation, check transferrin saturation.')}
    {zone(630, '50 and up', 'The treatment target on oral iron.')}
  </div>
  <div style="margin-top:auto;padding-top:22px;border-top:2px solid {LINE};display:grid;grid-template-columns:340px 1fr 1fr 1fr;align-items:center;gap:20px">
    <div style="{CAPS};line-height:1.35">Treatment<br>is indicated</div>
    {treat(50, 'in pregnancy')}
    {treat(30, 'in other adults')}
    {treat(20, 'in children')}
  </div>
  {cite('cmaj')}
  {footer()}''')


# 9 ── "Normal" is a statistic ─────────────────────────────────────────────────
def bell():
    cx, s, base, peak = 500, 150, 520, 40
    y = lambda x: base - (base - peak) * math.exp(-0.5 * ((x - cx) / s) ** 2)

    def area(a, b):
        pts = ' '.join(f'L{x} {y(x):.1f}' for x in range(a, b + 1, 4))
        return f'M{a} {base} {pts} L{b} {base} Z'
    bands = [(cx - s, cx + s, SAGE200), (cx - 2 * s, cx - s, SAGE100), (cx + s, cx + 2 * s, SAGE100)]
    fills = ''.join(f'<path d="{area(a, b)}" fill="{c}"/>' for a, b, c in bands)
    curve = 'M20 ' + f'{y(20):.1f} ' + ' '.join(f'L{x} {y(x):.1f}' for x in range(24, 984, 4))
    ticks = ''.join(f'<line x1="{cx + i * s}" y1="{y(cx + i * s):.1f}" x2="{cx + i * s}" y2="{base}" stroke="{GREEN}" stroke-width="1.5" stroke-dasharray="6 6"/>' for i in (-2, -1, 1, 2))
    lo = cx - 2 * s
    hi = cx + 2 * s
    return f'''<svg viewBox="0 0 1000 650" style="width:1000px;height:650px;display:block;overflow:visible" role="img" aria-label="A bell curve. The reference range is the middle 95 percent of the people tested, and that group can include people with low iron.">
  <g class="ir-wipe">{fills}</g>
  <g class="ir-fade" style="--d:1.25s">{ticks}</g>
  <path class="ir-draw" pathLength="1" d="{curve}" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round"/>
  <circle class="ir-ride" r="9" fill="{GREEN}" style="offset-path:path('{curve}')"/>
  <line x1="0" y1="{base}" x2="1000" y2="{base}" stroke="{INK2}" stroke-width="2"/>
  <path class="ir-spread" style="--d:1.15s" d="M{lo} {base + 34} H{hi} M{lo} {base + 24} V{base + 44} M{hi} {base + 24} V{base + 44}" stroke="{INK}" stroke-width="2.5" fill="none"/>
  <text class="ir-build" style="--d:1.4s" x="{cx}" y="{base + 86}" text-anchor="middle" {SVGSER} font-size="38" fill="{INK}">The &ldquo;normal&rdquo; range: the middle 95%</text>
  <g class="ir-build" style="--d:1.55s">
    <text x="10" y="176" {SVGSER} font-style="italic" font-size="32" fill="{GREEN}">People with low iron</text>
    <text x="10" y="216" {SVGSER} font-style="italic" font-size="32" fill="{GREEN}">were counted in here</text>
  </g>
  <path class="ir-draw" pathLength="1" style="--d:1.75s;--dur:620ms" d="M190 232 Q210 310 {cx - 1.5 * s:.0f} 440" stroke="{GREEN}" stroke-width="2.5" fill="none"/>
  <circle class="ir-pop" style="--d:2.2s" cx="{cx - 1.5 * s:.0f}" cy="440" r="7" fill="{GREEN}"/>
</svg>'''


add('Normal is a statistic', 'A reference range describes the people who were tested. It does not tell us what a body needs. The older ferritin ranges came from samples that did not exclude people with iron deficiency, so the bottom of normal was set too low. Iron deficiency anemia affects about 1.2 billion people, and iron deficiency without anemia is at least twice as common. Schematic only: ferritin itself is not a neat bell curve.', LIGHT + PAD, f'''
  {head('How we evaluate', '&ldquo;Normal&rdquo; is a <em>statistic</em>.')}
  <div style="flex:1;display:grid;grid-template-columns:1000px 1fr;gap:80px;align-items:center">
    {bell()}
    <div>
      {row('It describes the people tested', 'Not what your body needs.', size=38)}
      {row('The old sample wasn&rsquo;t clean', 'It didn&rsquo;t exclude people with iron deficiency.', size=38)}
      {row('Twice as common', 'Iron deficiency without anemia, compared with the 1.2 billion people who have iron deficiency anemia.', size=38)}
    </div>
  </div>
  {cite('cmaj', 'naseem', note='Curve is schematic.')}
  {footer()}''')


# 10 ── Raising the lower limit (2026) ─────────────────────────────────────────
def dumbbell():
    x = lambda v: 170 + (v - 45) * 42
    rows = [('Women', 49.4, 58.0, 120), ('Men', 57.0, 60.2, 250)]
    grid = ''.join(f'<line x1="{x(v)}" y1="48" x2="{x(v)}" y2="300" stroke="{LINE}" stroke-width="2"/><text x="{x(v)}" y="338" text-anchor="middle" {SVGTXT} font-size="23" fill="{MUTED}">{v}%</text>' for v in (45, 50, 55, 60, 65))
    out = []
    for i, (name, a, b, yy) in enumerate(rows):
        strong = name == 'Women'
        lag = i * .18
        out.append(f'<text x="0" y="{yy + 13}" {SVGSER} font-size="40" fill="{GREEN if strong else INK}">{name}</text>'
                   f'<line class="ir-grow" style="--d:{.65 + lag:.2f}s" x1="{x(a)}" y1="{yy}" x2="{x(b)}" y2="{yy}" stroke="{GREEN if strong else SAGE}" stroke-width="{8 if strong else 6}"/>'
                   f'<circle class="ir-pop" style="--d:{.4 + lag:.2f}s" cx="{x(a)}" cy="{yy}" r="15" fill="{CREAM}" stroke="{GREEN if strong else SAGE}" stroke-width="4"/>'
                   f'<circle class="ir-pop" style="--d:{1.2 + lag:.2f}s" cx="{x(b)}" cy="{yy}" r="19" fill="{GREEN if strong else SAGE}"/>'
                   f'<text class="ir-fade" style="--d:{.4 + lag:.2f}s" x="{x(a) - 26}" y="{yy + 11}" text-anchor="end" {SVGSER} font-size="34" fill="{INK2}">{a:.1f}</text>'
                   f'<text class="ir-fade" style="--d:{1.2 + lag:.2f}s" x="{x(b) + 32}" y="{yy + 12}" {SVGSER} font-size="40" fill="{GREEN if strong else INK2}"><tspan class="ir-num" data-from="{a}" data-delay="{650 + lag * 1000:.0f}">{b:.1f}</tspan></text>')
    return f'''<svg viewBox="0 0 1040 350" style="width:1040px;height:350px;display:block;overflow:visible" role="img" aria-label="Diagnosis rate among patients with ferritin under 30. Women rose from 49.4 to 58.0 percent; men rose from 57.0 to 60.2 percent.">
  <g class="ir-fade" style="--d:.2s">{grid}</g>{''.join(out)}
</svg>'''


def mini(num, body):
    return (f'<div style="border-top:2px solid {LINE};padding-top:16px"><div class="ir-num" data-delay="1250" style="{SERIF};font-size:58px;line-height:1;letter-spacing:-.025em;color:{GREEN}">{num}</div>'
            f'<div style="margin-top:10px;font-size:25px;line-height:1.3;letter-spacing:-.008em;color:{INK2}">{body}</div></div>')


add('Raising the lower limit', 'Rochester Regional Health moved the ferritin lower limit in September 2023, from 10 in women and 22 in men to 30 for everyone. Among patients with a ferritin under 30, about 50,000 across two 18-month periods, diagnoses rose most in women. Diagnoses of iron deficiency without anemia went up 47 percent. It is a retrospective study from one US health system. Iron deficiency is globally underdiagnosed, particularly in women.', LIGHT + PAD, f'''
  {head('Study · 2026', 'Move the line, find more <em>women</em>.', 76)}
  <div style="flex:1;display:grid;grid-template-columns:480px 1040px;gap:80px;align-items:center">
    <div>
      <div style="{CAPS}">Ferritin lower limit, women</div>
      <div style="margin-top:14px;{SERIF};font-size:120px;line-height:1;letter-spacing:-.04em;color:{GREEN}">10 → <span class="ir-num" data-from="10" data-delay="500">30</span></div>
      <p style="margin:26px 0 0;{BODY}">One US health system changed one number on the lab report. About 50,000 patients later, this is what changed.</p>
    </div>
    <div>
      <div style="{CAPS};margin-bottom:6px">Diagnosed with iron deficiency, ferritin under 30</div>
      <div style="display:flex;gap:32px;font-size:23px;color:{MUTED};margin-bottom:6px"><span>○ Before</span><span>● After</span></div>
      {dumbbell()}
      <div style="margin-top:22px;display:grid;grid-template-columns:repeat(3,1fr);gap:36px">
        {mini('+47%', 'diagnoses of iron deficiency without anemia')}
        {mini('+15%', 'oral iron prescriptions')}
        {mini('+8.2', 'ng/mL ferritin at 3–6 months in women, vs +4.0 in men')}
      </div>
    </div>
  </div>
  {paper('abdelhay', 'Retrospective pre and post study')}
  {footer()}''')

divider(2, 'Iron <em>levels</em>.', 'vein-red-cells-cream', 'Part 2: what iron and ferritin actually do, and what moves them.')


# 12 ── Jobs of iron and ferritin ──────────────────────────────────────────────
def job(text, dark=False):
    edge = 'rgba(255,252,247,.24)' if dark else LINE
    col = CREAM if dark else INK
    return (f'<div style="border-top:2px solid {edge};padding:21px 0 23px;{SERIF};font-size:33px;line-height:1.14;letter-spacing:-.018em;color:{col}">{text}</div>')


iron_jobs = ['Oxygen transport and storage', 'Making blood cells (hematopoiesis)', 'Mitochondrial energy production', 'Energy metabolism',
             'DNA synthesis', 'Myelination', 'Neurotransmitter synthesis', 'Cell growth, including bone-building osteoblasts']
ferritin_jobs = ['The main iron-storage protein', 'A buffer for how much iron is available', 'Keeps iron usable and non-toxic', 'A marker of inflammation, which raises it']
add('Jobs of iron and ferritin', 'Iron does a long list of jobs, well beyond carrying oxygen: DNA synthesis, myelination, energy metabolism, neurotransmitter synthesis, blood cell production, mitochondrial energy, and cell growth including osteoblasts. Ferritin is the protein that stores it, buffers its availability and detoxifies it, which is what makes iron both usable and non-toxic. Inflammation increases ferritin production, which is why it can mislead.', LIGHT + 'padding:88px 120px 110px;display:grid;grid-template-columns:1fr 620px;gap:70px;align-items:stretch', f'''
  <div style="display:flex;flex-direction:column;justify-content:center">
    {head('The jobs', 'Iron does the work. Ferritin <em>holds</em> it.')}
    <div style="margin-top:36px;display:grid;grid-template-columns:1fr 1fr;gap:0 48px">
      <div>{''.join(job(j) for j in iron_jobs[:4])}</div>
      <div>{''.join(job(j) for j in iron_jobs[4:])}</div>
    </div>
  </div>
  <div style="background:linear-gradient(160deg,{GREEN} 0%,#1C3118 100%);color:{CREAM};border-radius:8px;padding:56px 50px;display:flex;flex-direction:column;justify-content:center;margin-bottom:30px">
    <div style="{EYEBROW_D}">Ferritin</div>
    <div style="margin:18px 0 30px;{SERIF};font-size:66px;line-height:1;letter-spacing:-.03em"><em>The store</em></div>
    {''.join(job(j, dark=True) for j in ferritin_jobs)}
  </div>
  {footer()}''')


# 13 ── The cycle ──────────────────────────────────────────────────────────────
def cycle():
    x = lambda d: 30 + d * (980 / 28)
    base, top = 380, 60
    e2 = lambda d: .16 + .78 * math.exp(-((d - 13) / 2.6) ** 2) + .32 * math.exp(-((d - 21) / 4) ** 2)
    p4 = lambda d: .05 + .8 * math.exp(-((d - 21) / 4) ** 2)
    path = lambda f: 'M' + ' L'.join(f'{x(d / 4):.1f} {base - f(d / 4) * (base - top):.1f}' for d in range(0, 113))
    area = lambda f: path(f) + f' L{x(28):.1f} {base} L{x(0):.1f} {base} Z'
    return f'''<svg viewBox="0 0 1040 440" style="width:1040px;height:440px;display:block;overflow:visible" role="img" aria-label="Schematic of estrogen and progesterone across a 28-day cycle">
  <defs>
    <linearGradient id="ir-cy-e2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".2"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
    <linearGradient id="ir-cy-p4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SAGE}" stop-opacity=".3"/><stop offset="1" stop-color="{SAGE}" stop-opacity="0"/></linearGradient>
  </defs>
  <g class="ir-wipe"><path d="{area(p4)}" fill="url(#ir-cy-p4)"/><path d="{area(e2)}" fill="url(#ir-cy-e2)"/></g>
  <g class="ir-fade" style="--d:.15s"><line x1="{x(14)}" y1="24" x2="{x(14)}" y2="{base}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 7"/>
  <text x="{x(14)}" y="14" text-anchor="middle" {SVGTXT} font-size="21" font-weight="600" letter-spacing="2" fill="{MUTED}">OVULATION</text></g>
  <line x1="30" y1="{base}" x2="1010" y2="{base}" stroke="{INK2}" stroke-width="2"/>
  <path class="ir-draw" pathLength="1" d="{path(p4)}" fill="none" stroke="{SAGE}" stroke-width="6" stroke-linecap="round"/>
  <path class="ir-draw" pathLength="1" d="{path(e2)}" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linecap="round"/>
  <circle class="ir-ride" r="10" fill="{SAGE}" style="offset-path:path('{path(p4)}')"/>
  <circle class="ir-ride" r="10" fill="{GREEN}" style="offset-path:path('{path(e2)}')"/>
  <g class="ir-build" style="--d:1.5s" {SVGSER} font-size="36">
    <text x="{x(13) - 28}" y="{base - e2(13) * (base - top) + 8}" text-anchor="end" fill="{GREEN}">Estrogen</text>
    <text x="{x(21) + 16}" y="{base - p4(21) * (base - top) - 18}" text-anchor="middle" fill="#5F7C5A">Progesterone</text>
  </g>
  <g {SVGSER} font-size="34" text-anchor="middle" fill="{INK}">
    <text x="{x(7)}" y="{base + 50}">Follicular phase</text><text x="{x(21)}" y="{base + 50}">Luteal phase</text>
  </g>
</svg>'''


add('Iron and the cycle', 'Estrogen and progesterone directly affect how much iron is available, through hepcidin, the hormone that acts as the gatekeeper for iron. Estrogen suppresses hepcidin and progesterone raises it. That predicts more iron taken up in the follicular phase and less in the luteal phase. The authors are careful here: the predicted late-luteal hepcidin peak has not shown up in cohorts sampled across the cycle, so the cycle-level effect is still an open question. What does hold is that markers shift with phase, so one result can mislead. Our reading: states like perimenopause can substantially change iron status.', LIGHT + PAD, f'''
  {head('Study · 2026', 'Iron moves with your <em>cycle</em>.')}
  <div style="flex:1;display:grid;grid-template-columns:1040px 1fr;gap:70px;align-items:center">
    <div>
      {cycle()}
      <div style="margin-top:18px;display:grid;grid-template-columns:1fr 1fr;gap:40px;font-size:28px;line-height:1.34;letter-spacing:-.01em;color:{INK2}">
        <div>Estrogen lowers hepcidin, the body&rsquo;s iron gatekeeper. <strong style="font-weight:600;color:{INK}">More iron let in.</strong></div>
        <div>Progesterone raises it. <strong style="font-weight:600;color:{INK}">Less iron let in.</strong></div>
      </div>
    </div>
    <div>
      {row('One result can mislead', 'Iron markers shift with cycle phase.')}
      {row('A prediction, not yet proof', 'Sampling across the cycle hasn&rsquo;t confirmed the expected hepcidin peak.')}
      {row('Why perimenopause matters', 'When these hormones change, iron status can too.')}
    </div>
  </div>
  {paper('cycle', 'Review. Curves are schematic')}
  {footer()}''')

divider(3, 'Too much, too <em>little</em>.', 'woman-tired-armchair-cream', 'Part 3: the consequences of high and low iron, then what the studies do and do not show.')


# 15 ── High iron ──────────────────────────────────────────────────────────────
def plate(img, alt, name, body, col, d):
    return (f'<div style="grid-column:{col};display:flex;flex-direction:column">'
            f'<div style="height:310px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:20px;box-sizing:border-box"><img class="ir-ink" src="assets/images/{img}.webp" alt="{alt}" style="--d:{d:.2f}s;--dur:1300ms;max-width:92%;max-height:100%;display:block" loading="eager" decoding="async"></div>'
            f'<div style="border-top:2px solid {LINE};padding-top:18px;{SERIF};font-size:48px;line-height:1.05;letter-spacing:-.022em;color:{INK}">{name}</div>'
            f'<div style="margin-top:10px;font-size:27px;line-height:1.32;letter-spacing:-.012em;color:{INK2}">{body}</div></div>')


def evidence_head(label, col, strong):
    edge = f'3px solid {GREEN}' if strong else f'3px solid {SAGE200}'
    tone = GREEN_DEEP if strong else MUTED
    return f'<div style="grid-column:{col};border-top:{edge};padding-top:16px;{CAPS};color:{tone}">{label}</div>'


add('High iron', 'Too much iron is not better. In iron-overload disease, iron collects in the liver and can scar it over time, and severe overload can weaken the heart muscle. Beyond that, the evidence is softer. The link with cardiovascular disease is still debated. Excess iron favours bone loss, particularly with aging and after menopause. For breast cancer, a 2019 meta-analysis found a modest link with serum iron and heme iron intake, but not with ferritin. Remember ferritin can also run high from inflammation, so a high result needs a closer look.', LIGHT + PAD, f'''
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:60px">
    {head('High iron', 'More isn&rsquo;t <em>better</em>.')}
    <p style="margin:0 0 8px;max-width:760px;{BODY}">Inflammation can also raise ferritin, so a high result needs a closer look.</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 28px 1fr 1fr 1fr;column-gap:32px;align-content:center">
    {evidence_head('Clear in iron overload', '1 / 3', True)}
    {evidence_head('Still being studied', '4 / 7', False)}
    {plate('liver', 'Engraving of a liver', 'Liver', 'The main store. Overload can scar it over time.', 1, .35)}
    {plate('heart', 'Engraving of a heart', 'Heart', 'Severe overload can weaken the muscle.', 2, .5)}
    {plate('apob-plaque', 'Engraving of an artery in cross-section', 'Arteries', 'The link with cardiovascular disease is still debated.', 4, .65)}
    {plate('femur', 'Engraving of a femur in section', 'Bone', 'Excess iron favours bone loss, especially after menopause.', 5, .8)}
    {plate('breast', 'Engraving of breast tissue in cross-section', 'Breast', 'A modest link with serum iron. Not shown for ferritin.', 6, .95)}
  </div>
  {cite('easl', 'ahanchi', 'correnti', 'chang')}
  {footer()}''')


# 16 ── Low iron ───────────────────────────────────────────────────────────────
def pct(p):
    return f'<strong style="font-weight:600;color:{GREEN_DEEP}">{p}</strong>'


SYM_COLS = 'display:grid;grid-template-columns:230px 1fr 1fr;column-gap:56px'


def group(name, without, anemia):
    cell = 'font-size:27px;line-height:1.36;letter-spacing:-.008em'
    return (f'<div style="{SYM_COLS};border-top:2px solid {LINE};padding:20px 0 22px">'
            f'<div style="{SERIF};font-size:34px;line-height:1.1;letter-spacing:-.015em;color:{GREEN}">{name}</div>'
            f'<div style="{cell};color:{INK2}">{without}</div>'
            f'<div style="{cell};color:{INK2}">{anemia}</div></div>')


add('Low iron', 'This is the symptom map from the 2025 CMAJ review, retyped. Percentages are the reported estimated point prevalence in the literature. On the left, iron deficiency without anemia: fatigue is by far the most reported, and it also includes brain fog, mood change, poor exercise tolerance, hair loss, restless legs and pica. On the right, once anemia is present: pallor, headaches, a racing heart and shortness of breath come in. Some of these are subtle, and people may accept them as normal.', LIGHT + PAD, f'''
  {head('Low iron', 'It can show up <em>before</em> anemia.')}
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div style="{SYM_COLS};padding-bottom:14px"><div></div><div style="{CAPS};color:{INK}">Iron deficiency without anemia</div><div style="{CAPS};color:{INK}">Iron deficiency anemia</div></div>
    {group('General', f'Physical fatigue {pct("83%")}, exhaustion, muscle weakness or pain, slower run times, poor sleep', f'Pallor {pct("45–50%")}, fatigue {pct("44%")}, muscular weakness')}
    {group('Neurological', 'Brain fog, low mood or irritability, poor memory and concentration, anxiety, depression, headaches, dizziness', f'Headaches {pct("63%")}, lightheadedness, insomnia, vertigo, fainting {pct("0.3%")}')}
    {group('Hair, skin, nails', 'Hair loss, brittle nails, dry skin', f'Hair loss {pct("30%")}, sore smooth tongue {pct("27%")}, spoon-shaped or brittle nails, cold hands and feet')}
    {group('Heart, lungs', 'Palpitations, chest pain, shortness of breath', f'Murmur {pct("10%")}, rapid heart rate {pct("9%")}, palpitations, chest pain, shortness of breath')}
    {group('Also', f'Cold intolerance {pct("13%")}, restless legs {pct("13%")}, pica {pct("8%")}', f'Restless legs {pct("24%")}')}
  </div>
  {cite('cmaj', note='Adapted from Figure 1. Percentages are reported estimated prevalence.')}
  {footer()}''')


# 17 ── After menopause ────────────────────────────────────────────────────────
def lifeline():
    x = lambda t: 50 + t * 950
    base, top = 400, 40
    men = lambda t: .1 + .76 * (1 - math.exp(-t / .1))
    women = lambda t: .1 + .2 * (1 - math.exp(-t / .1)) + .4 / (1 + math.exp(-(t - .63) / .035))
    path = lambda f: 'M' + ' L'.join(f'{x(i / 100):.1f} {base - f(i / 100) * (base - top):.1f}' for i in range(0, 101))
    area = path(women) + f' L{x(1):.1f} {base} L{x(0):.1f} {base} Z'
    return f'''<svg viewBox="0 0 1040 470" style="width:1040px;height:470px;display:block;overflow:visible" role="img" aria-label="Schematic of body iron stores across life. Women stay lower than men before menopause, and rise during and after it.">
  <defs><linearGradient id="ir-life" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity=".2"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient></defs>
  <rect class="ir-fade" style="--d:.2s" x="{x(.56)}" y="{top - 20}" width="{x(.72) - x(.56)}" height="{base - top + 20}" fill="{SAGE50}"/>
  <path class="ir-wipe" d="{area}" fill="url(#ir-life)"/>
  <line x1="50" y1="{base}" x2="1010" y2="{base}" stroke="{INK2}" stroke-width="2"/>
  <line x1="50" y1="{top - 20}" x2="50" y2="{base}" stroke="{INK2}" stroke-width="2"/>
  <text transform="translate(26 {base}) rotate(-90)" {SVGTXT} font-size="22" font-weight="600" letter-spacing="2" fill="{MUTED}">IRON STORES</text>
  <path class="ir-draw" pathLength="1" d="{path(men)}" fill="none" stroke="{SAGE}" stroke-width="6" stroke-linecap="round"/>
  <path class="ir-draw" pathLength="1" d="{path(women)}" fill="none" stroke="{GREEN}" stroke-width="7" stroke-linecap="round"/>
  <circle class="ir-ride" r="10" fill="{SAGE}" style="offset-path:path('{path(men)}')"/>
  <circle class="ir-ride" r="11" fill="{GREEN}" style="offset-path:path('{path(women)}')"/>
  <g class="ir-build" style="--d:1.5s" {SVGSER} font-size="38">
    <text x="{x(.3)}" y="{base - men(.3) * (base - top) - 20}" fill="#5F7C5A">Men</text>
    <text x="{x(.3)}" y="{base - women(.3) * (base - top) + 54}" fill="{GREEN}" font-style="italic">Women</text>
  </g>
  <g {SVGSER} font-size="32" text-anchor="middle" fill="{INK}">
    <text x="{x(.28)}" y="{base + 50}">Reproductive years</text><text x="{x(.64)}" y="{base + 50}">Menopause</text><text x="{x(.87)}" y="{base + 50}">After</text>
  </g>
</svg>'''


add('After menopause', 'Iron metabolism changes with the hormonal changes of menopause. Before menopause, body iron stores are lower in women than in men. They rise during and after menopause, in step with cardiometabolic risk. The link with type 2 diabetes is more consistent than the link with cardiovascular disease, which is still controversial, and this is mostly observational evidence, so it does not establish cause.', LIGHT + PAD, f'''
  {head('Study · 2024', 'After menopause, stores <em>climb</em>.')}
  <div style="flex:1;display:grid;grid-template-columns:1040px 1fr;gap:70px;align-items:center">
    {lifeline()}
    <div>
      {row('Lower, then rising', 'Stores are lower than men&rsquo;s before menopause, then rise during and after it.')}
      {row('Risk may climb too', 'Excess iron may add to cardiometabolic risk: more consistently type 2 diabetes than heart disease.')}
      {row('A link, not a cause', 'Most of this evidence is observational.')}
    </div>
  </div>
  {paper('ahanchi', 'Review. Curves are schematic')}
  {footer()}''')


# 18 ── The evidence is mixed ──────────────────────────────────────────────────
def mixed(n, text, last=False):
    bottom = 'border-bottom:1px solid rgba(255,252,247,.28);' if last else ''
    return (f'<div style="display:grid;grid-template-columns:120px 1fr;align-items:baseline;border-top:1px solid rgba(255,252,247,.28);{bottom}padding:32px 0">'
            f'<div style="{SERIF};font-size:44px;color:rgba(255,252,247,.6)">{n}</div>'
            f'<div style="{SERIF};font-size:50px;line-height:1.14;letter-spacing:-.022em;color:{CREAM}">{text}</div></div>')


add('The evidence is mixed', 'Before the studies, set expectations. Some studies indicate that low or suboptimal iron has effects beyond anemia, and earlier than current cut-offs. But the evidence is mixed, samples are small and the time frames are limited. There is not enough to make strong recommendations for everyone, and there is enough to keep exploring it as part of a multimodal approach to a variety of concerns.', DARK + 'padding:88px 120px 130px;display:flex;flex-direction:column', f'''
  <div><div style="{EYEBROW_D}">Iron&rsquo;s impact on women</div>
  <h2 style="margin:22px 0 0;{SERIF};font-size:112px;line-height:1.02;letter-spacing:-.035em;color:{CREAM}">The evidence is <em>mixed</em>.</h2></div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    {mixed('01', 'Low iron may matter beyond anemia, and earlier than current cut-offs.')}
    {mixed('02', 'Studies are small and cover limited periods of time.')}
    {mixed('03', 'Not enough to make strong recommendations for everyone.')}
    {mixed('04', 'Enough to explore further, as part of a multimodal approach.', last=True)}
  </div>
  {footer(dark=True)}''', 'sl sl-dark')


# 19 ── Meta-analysis (2025) ───────────────────────────────────────────────────
def effect(label, d, i):
    return (f'<div style="display:grid;grid-template-columns:340px 1fr 90px;align-items:center;gap:20px;border-top:2px solid {LINE};padding:14px 0">'
            f'<div style="{SERIF};font-size:34px;letter-spacing:-.018em">{label}</div>'
            f'<div style="height:30px;background:{SAGE50}"><div class="ir-bar" style="--d:{.4 + i * .1:.2f}s;height:100%;width:{d / 0.8 * 100:.1f}%;background:{GREEN}"></div></div>'
            f'<div class="ir-num" data-delay="{400 + i * 100}" style="{SERIF};font-size:38px;color:{GREEN};text-align:right">{d:.2f}</div></div>')


def effect_scale():
    """The rule of thumb, as a ruler hung under the bars it explains."""
    mark = lambda p, t: (f'<span style="position:absolute;left:{p}%;top:-14px;width:2px;height:12px;background:{SAGE}"></span>'
                         f'<span style="position:absolute;left:{p}%;top:2px;transform:translateX(-50%);white-space:nowrap;font-size:23px;color:{MUTED}">{t}</span>')
    labels = f'{mark(25, "0.2 small")}{mark(62.5, "0.5 medium")}{mark(100, "0.8 large")}'
    return (f'<div style="display:grid;grid-template-columns:340px 1fr 90px;align-items:center;gap:20px;border-top:2px solid {LINE};padding:12px 0 12px">'
            f'<div style="font-size:23px;color:{MUTED}">As a rule of thumb, d of</div>'
            f'<div style="position:relative;height:32px">{labels}</div><div></div></div>')


def noeffect(label, note):
    return (f'<div style="display:grid;grid-template-columns:340px 1fr;align-items:center;gap:20px;border-top:2px solid {LINE};padding:14px 0">'
            f'<div style="{SERIF};font-size:34px;letter-spacing:-.018em;color:{MUTED}">{label}</div>'
            f'<div style="font-size:27px;letter-spacing:-.01em;color:{MUTED}">{note}</div></div>')


add('Meta-analysis', 'Despite iron being critical in energy metabolism and neurotransmitter synthesis, iron deficiency is the most common nutritional deficiency worldwide. This meta-analysis pooled 18 studies of iron supplementation in non-anemic children, adolescents and menstruating adults. In randomized trials it improved anxiety, fatigue, physical well-being, cognitive intelligence and short-term memory, but not attention or depression. Depression did improve in the pre-post studies. Key point: the effect was absent once iron-deficient participants were excluded, so this supports treating deficiency, not taking iron without one.', LIGHT + PAD, f'''
  {head('Meta-analysis · 2025', 'Where iron was low, iron <em>helped</em>.', 76)}
  <div style="flex:1;display:grid;grid-template-columns:1040px 1fr;gap:70px;align-items:center">
    <div>
      <div style="{CAPS};margin-bottom:12px">Randomized trials, no anemia. Effect size d</div>
      {effect('Short-term memory', .53, 0)}
      {effect('Cognitive intelligence', .46, 1)}
      {effect('Physical well-being', .42, 2)}
      {effect('Anxiety', .34, 3)}
      {effect('Fatigue', .34, 4)}
      {effect_scale()}
      {noeffect('Attention', 'No improvement')}
      {noeffect('Depression', 'No improvement in randomized trials')}
    </div>
    <div>
      {stat_big('18', 'studies, 12 of them randomized. 1,408 children, adolescents and menstruating adults.')}
      <p style="margin:0;padding-top:24px;border-top:2px solid {LINE};{SERIF};font-size:42px;line-height:1.14;letter-spacing:-.02em;color:{GREEN}">No effect once iron-deficient participants were excluded.</p>
    </div>
  </div>
  {paper('fiani', 'Meta-analysis')}
  {footer()}''')


# 20 ── Symptoms above the old cut-off (2021) ──────────────────────────────────
def level(cut, n, pctv, sym, sub, i):
    return (f'<div style="display:grid;grid-template-columns:230px 560px 1fr;align-items:center;gap:40px;border-top:2px solid {LINE};padding:30px 0">'
            f'<div><div style="{CAPS};font-size:20px">Ferritin</div><div style="margin-top:6px;{SERIF};font-size:64px;line-height:1;letter-spacing:-.03em;color:{GREEN}">≤{cut}</div></div>'
            f'<div><div style="height:44px;background:{SAGE50}"><div class="ir-bar" style="--d:{.45 + i * .16:.2f}s;height:100%;width:{pctv}%;background:{GREEN}"></div></div>'
            f'<div style="margin-top:10px;font-size:27px;letter-spacing:-.01em;color:{INK2}">{n} women, {pctv}%</div></div>'
            f'<div><div style="{SERIF};font-size:48px;line-height:1.08;letter-spacing:-.024em">{sym}</div><div style="margin-top:8px;font-size:28px;line-height:1.3;letter-spacing:-.012em;color:{INK2}">{sub}</div></div></div>')


add('Symptoms and ferritin', 'A cross-sectional study of 554 non-anemic menstruating women in France, aged 18 to 50. Over half had a ferritin below 50. Restless legs were significantly more common at 50 or below, and recent hair loss at 20 or below. These are correlations, not causes, and only those two symptoms held up. But both sit well above the old lab cut-off of 12 to 15.', LIGHT + PAD, f'''
  {head('Study · 2021', 'Symptoms appear <em>above</em> the old cut-off.')}
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    {level(50, 304, 54.9, 'Restless legs', '2.8 times the odds', 0)}
    {level(20, 103, 18.6, 'Recent hair loss', '2.3 times the odds. Also more limits from emotional problems.', 1)}
    {level(15, 60, 10.8, 'Recent hair loss', '2.2 times the odds', 2)}
    <div style="border-top:2px solid {LINE};padding-top:18px;font-size:27px;letter-spacing:-.01em;color:{MUTED}">554 non-anemic menstruating women, aged 18–50. A correlation, measured at one point in time.</div>
  </div>
  {paper('beatrix', 'Cross-sectional study')}
  {footer()}''')


# 21 ── Endurance (2019) ───────────────────────────────────────────────────────
add('Endurance', 'The central nervous system needs iron to function. This small study compared iron status with perceived energy and EEG findings in 23 non-anemic women aged 20 to 32, in the follicular phase. Those with a ferritin below 12 reported lower activity and endurance. The groups did not differ in intelligence or anxiety, but the deficient group took a median of 3 minutes longer to finish the assessment. Very small sample, so treat it as a signal.', LIGHT + 'padding:88px 120px 172px;display:grid;grid-template-columns:800px 1fr;grid-template-rows:minmax(0,1fr);gap:80px', f'''
  <div style="display:flex;flex-direction:column">
    {head('Study · 2019', 'Same score.<br><em>Three more minutes.</em>', 84)}
    <div style="margin-top:auto">
      <div class="ir-num" data-delay="700" style="{SERIF};font-size:210px;line-height:.9;letter-spacing:-.05em;color:{GREEN}">+3<span style="font-size:96px;letter-spacing:-.02em"> min</span></div>
      <p style="margin:26px 0 0;max-width:640px;{BODY}">Median extra time to finish the same intelligence test, with ferritin below 12.</p>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:space-between">
    <img class="ir-ink" src="assets/images/neuron.webp" alt="Engraving of a neuron" style="--dur:1800ms;width:620px;height:auto;display:block;align-self:flex-end" loading="eager" decoding="auto">
    <div>
      {row('Intelligence and anxiety scores', 'No difference between the groups.')}
      {row('Activity and endurance', 'Reported lower with low ferritin.')}
      {row('Brain activity', 'An EEG pattern linked with withdrawal tendencies.')}
      <div style="border-top:2px solid {LINE};padding-top:16px;font-size:27px;letter-spacing:-.01em;color:{MUTED}">23 non-anemic women, aged 20–32, in the follicular phase.</div>
    </div>
  </div>
  {paper('dziem', 'Small comparison study')}
  {footer()}''')


# 22 ── Executive function (2016) ──────────────────────────────────────────────
def verdict(label, items, muted=False):
    col = MUTED if muted else GREEN
    edge = f'2px solid {LINE}' if muted else f'4px solid {GREEN}'
    return (f'<div style="border-top:{edge};padding-top:26px"><div style="{CAPS};color:{col}">{label}</div>'
            f'<div style="margin-top:28px;display:flex;flex-direction:column;gap:34px;min-height:440px">{items}</div></div>')


def vitem(name, sub=''):
    extra = f'<div style="margin-top:8px;font-size:30px;line-height:1.32;letter-spacing:-.012em;color:{INK2}">{sub}</div>' if sub else ''
    return f'<div><div style="{SERIF};font-size:58px;line-height:1.05;letter-spacing:-.026em">{name}</div>{extra}</div>'


add('Executive function', '127 non-anemic females aged 18 to 35. Better iron status went with better attention, meaning faster reaction time, better inhibitory control, and better planning, with less planning time. Several other executive functions showed no link, possibly because of performance ceilings. Working memory actually appeared worse with better iron status, which the authors call paradoxical. It is a limited, observational study.', LIGHT + PAD, f'''
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:60px">
    {head('Study · 2016', 'Better iron, better <em>focus</em>. Mostly.', 76)}
    <p style="margin:0 0 8px;{BODY};text-align:right;white-space:nowrap;flex-shrink:0">127 non-anemic females, aged 18–35.<br>A limited study.</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:64px;align-items:center;align-content:center">
    {verdict('Better with better iron', vitem('Attention', 'Faster reaction time') + vitem('Inhibitory control', 'Steadier reaction time') + vitem('Planning', 'Less time needed'))}
    {verdict('No link', vitem('Several other executive functions', 'Possibly a performance ceiling'), muted=True)}
    {verdict('Unexpectedly worse', vitem('Working memory', 'Appeared to worsen with better iron status'), muted=True)}
  </div>
  {paper('scott', 'Observational study')}
  {footer()}''')


# 23 ── The open question (2011) ───────────────────────────────────────────────
add('The open question', 'Iron deficiency disproportionately affects infants, children and women of reproductive age. This older review pointed to the need to explore how iron status interacts with cognition, emotions and behaviour. And it leaves the question we are still asking.', LIGHT + 'padding:88px 120px 172px;display:flex;flex-direction:column', f'''
  <div style="{EYEBROW}">Review · 2011</div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div data-words style="{SERIF};font-size:112px;line-height:1.08;letter-spacing:-.035em;color:{GREEN};max-width:1560px;text-wrap:balance">How low does iron have to go before it {ring('matters', inset='-2px -20px -8px', rot=-2, delay='1.05s', margin='0 20px 0 14px')}?</div>
    <div style="margin-top:56px;display:grid;grid-template-columns:1fr 1fr;gap:70px;max-width:1500px">
      {row('Who it affects most', 'Infants, children and women of reproductive age.')}
      {row('What to keep exploring', 'How iron interacts with cognition, emotions and behaviour.')}
    </div>
  </div>
  {paper('murray', 'Review')}
  {footer()}''')

divider(4, 'Treatment <em>options</em>.', 'iron-tablets-cream', 'Part 4: pill or IV, what diet can and cannot do, which iron to choose, and how to take it.')


# 25 ── Pill or IV ─────────────────────────────────────────────────────────────
def route(img, alt, imgw, title, sub, items, foot):
    rows = ''.join(f'<li style="border-top:2px solid {LINE};padding:17px 0 19px;font-size:30px;line-height:1.26;letter-spacing:-.014em;color:{INK2};list-style:none">{i}</li>' for i in items)
    return (f'<div style="display:grid;grid-template-columns:230px 1fr;gap:36px;align-items:start">'
            f'<div style="display:flex;align-items:center;justify-content:center;align-self:center"><img class="ir-ink" src="assets/images/{img}.webp" alt="{alt}" style="--ang:180deg;width:{imgw}px;height:auto;display:block" loading="eager" decoding="async"></div>'
            f'<div><div style="{SERIF};font-size:72px;line-height:1;letter-spacing:-.03em;color:{GREEN}">{title}</div>'
            f'<div style="margin:14px 0 26px;min-height:78px;{SERIF};font-size:34px;line-height:1.14;letter-spacing:-.018em;color:{INK}">{sub}</div>'
            f'<ul style="margin:0;padding:0">{rows}</ul>'
            f'<div style="border-top:2px solid {LINE};padding-top:18px;font-size:27px;line-height:1.32;letter-spacing:-.01em;color:{MUTED}">{foot}</div></div></div>')


add('Pill or IV', 'Oral iron is first-line for iron deficiency without anemia, and for anemia when hemoglobin is above 100. Hemoglobin starts improving within days to weeks, and ferritin typically takes 3 to 6 months. IV iron can be used when someone cannot tolerate oral iron, when a trial of oral iron has not worked, with malabsorption, or in severe anemia to avoid a transfusion. Adverse effects with IV iron are rare, about 1 in 200, usually self-limited flushing or chest or back tightness. Anaphylaxis is under 1 in 200,000. Also address the cause, such as heavy periods.', LIGHT + PAD, f'''
  {head('Treatment', 'Pill <em>or</em> IV?', 96)}
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start;align-content:center">
    {route('iron-tablets', 'Engraving of iron tablets', 230, 'Oral iron', 'First line, including anemia with hemoglobin above 100', ['Hemoglobin improves in days to weeks', 'Ferritin improves in about 3–6 months', 'Treatment target: ferritin 50 or higher'], 'Gut side effects are what make people stop.')}
    {route('iv-bag', 'Engraving of an IV bag', 190, 'IV iron', 'When oral iron can&rsquo;t do the job', ['You can&rsquo;t tolerate oral iron', 'A trial of oral iron hasn&rsquo;t worked', 'Malabsorption, or severe anemia'], 'Reactions are uncommon, about 1 in 200, and usually mild. Target: ferritin 100 or higher.')}
  </div>
  {cite('cmaj')}
  {footer()}''')


# 26 ── Dietary iron ───────────────────────────────────────────────────────────
add('Dietary iron', 'Making red blood cells takes about 20 milligrams of iron a day. Dietary changes alone do not provide enough elemental iron to treat a deficiency, especially with ongoing losses from periods or pregnancy. An iron-rich diet is still reasonable alongside treatment. Animal sources carry heme iron, which is better absorbed and barely affected by what you eat with it. Non-heme iron absorption is greatly affected by foods eaten at the same time.', LIGHT + 'padding:88px 120px 150px;display:grid;grid-template-columns:1fr 520px;gap:80px;align-items:center', f'''
  <div>
    <div style="{EYEBROW}">Dietary iron</div>
    <h2 style="{H2};font-size:92px">Food alone won&rsquo;t <em>fix</em> it.</h2>
    <p style="margin:26px 0 34px;{BODY};font-size:32px">An iron-rich diet helps alongside treatment. It won&rsquo;t correct a deficiency by itself.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:56px">
      <div style="border-top:2px solid {GREEN};padding-top:20px"><div style="{SERIF};font-size:50px;letter-spacing:-.025em;color:{GREEN}"><em>Heme</em> iron</div><div style="margin-top:12px;font-size:27px;line-height:1.4;color:{INK2}">From animal sources. Better absorbed, and barely affected by what you eat with it.</div></div>
      <div style="border-top:2px solid {LINE};padding-top:20px"><div style="{SERIF};font-size:50px;letter-spacing:-.025em;color:{INK}">Non-heme iron</div><div style="margin-top:12px;font-size:27px;line-height:1.4;color:{INK2}">From plants and fortified foods. Absorption depends heavily on what you eat with it.</div></div>
    </div>
    <div style="margin-top:36px;padding-top:20px;border-top:2px solid {LINE};display:flex;align-items:baseline;gap:26px"><span class="ir-num" data-delay="900" style="{SERIF};font-size:84px;line-height:1;letter-spacing:-.03em;color:{GREEN}">20 mg</span><span style="font-size:27px;line-height:1.4;color:{INK2}">of iron a day goes into making red blood cells.</span></div>
  </div>
  <div class="dk-panel"><img class="ir-ink" src="assets/images/gut-wall.webp" alt="Engraving of the gut wall, where iron is absorbed" style="--dur:1700ms;width:520px;height:auto;display:block" loading="eager" decoding="auto"></div>
  {cite('cmaj', 'ods')}
  {footer()}''')


# 27 ── Which iron ─────────────────────────────────────────────────────────────
IRON_ROW_N = [0]


def iron_row(name, mg, note, cost, extra=''):
    i = IRON_ROW_N[0]
    IRON_ROW_N[0] += 1
    return (f'<div style="display:grid;grid-template-columns:360px 400px 120px 1fr;align-items:center;gap:26px;border-top:2px solid {LINE};padding:15px 0">'
            f'<div style="{SERIF};font-size:32px;letter-spacing:-.018em">{name}</div>'
            f'<div style="display:flex;align-items:center;gap:14px"><div style="width:280px;height:22px;background:{SAGE50}"><div class="ir-bar" style="--d:{.4 + i * .09:.2f}s;height:100%;width:{mg / 150 * 100:.1f}%;background:{GREEN}"></div></div>'
            f'<div style="{SERIF};font-size:30px;color:{GREEN};white-space:nowrap">{mg} mg{extra}</div></div>'
            f'<div class="ir-tnum" style="font-size:26px;color:{INK2}">{cost}</div>'
            f'<div style="font-size:26px;line-height:1.26;letter-spacing:-.012em;color:{INK2}">{note}</div></div>')


def iron_group(label):
    return f'<div style="{CAPS};color:{GREEN_DEEP};margin:20px 0 10px">{label}</div>'


add('Which iron', 'Elemental iron per tablet and estimated daily cost come from Table 2 of the CMAJ review. The three iron salts are first-line: low cost, and no robust evidence that pricier forms work better. Gluconate and sulfate may be better tolerated than fumarate because they carry less elemental iron. Bisglycinate had fewer GI side effects in pregnancy trials, with less data elsewhere. Ferric maltol is a prescription option in Canada, approved in 2024 for adults with iron deficiency anemia who do not respond to or cannot tolerate other oral iron. The best one is the one you tolerate and take consistently.', LIGHT + 'padding:88px 120px 150px;display:flex;flex-direction:column', f'''
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:60px">
    {head('Treatment', 'Which <em>iron</em>?')}
    <p style="margin:0 0 6px;max-width:800px;{SERIF};font-size:40px;line-height:1.14;letter-spacing:-.02em;color:{GREEN}">The best one is the one you tolerate and take consistently.</p>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    <div style="display:grid;grid-template-columns:360px 400px 120px 1fr;gap:26px;{CAPS};font-size:19px"><div>Form</div><div>Elemental iron, per tablet</div><div>Per day</div><div>In short</div></div>
    {iron_group('First line: iron salts')}
    {iron_row('Ferrous gluconate', 35, 'May be better tolerated: less iron per tablet.', '$0.10')}
    {iron_row('Ferrous sulfate', 60, 'May be better tolerated than fumarate.', '$0.20')}
    {iron_row('Ferrous fumarate', 100, 'The most iron of the three, and may be harder on the gut.', '$0.25')}
    {iron_group('Costlier, or more selective')}
    {iron_row('Ferrous bisglycinate', 25, 'Fewer gut effects in pregnancy trials. Less data elsewhere.', '$0.30')}
    {iron_row('Polysaccharide complex', 150, 'No robust evidence it works better than salts.', '$0.75')}
    {iron_row('Ferric maltol', 30, 'Prescription, if other oral iron fails or isn&rsquo;t tolerated.', '—', ' × 2')}
  </div>
  {cite('cmaj', 'fischer', 'maltol', note='Costs are CMAJ&rsquo;s estimates. Ferric maltol isn&rsquo;t in its table.')}
  {footer()}''')


# 28 ── How to take it ─────────────────────────────────────────────────────────
def rec(n, title, body):
    return (f'<div style="display:grid;grid-template-columns:90px 1fr;align-items:baseline;border-top:2px solid {LINE};padding:20px 0 22px">'
            f'<div style="{SERIF};font-size:40px;color:{GREEN_DEEP}">{n}</div>'
            f'<div><div style="{SERIF};font-size:44px;line-height:1.08;letter-spacing:-.022em">{title}</div>'
            f'<div style="margin-top:8px;font-size:28px;line-height:1.3;letter-spacing:-.012em;color:{INK2}">{body}</div></div></div>')


add('How to take it', 'Start by finding the elemental iron dose on the label: 300 milligrams of ferrous sulfate is only 60 of elemental iron. Aim for 60 to 110 milligrams of elemental iron daily, as your clinician advises. Take it on an empty stomach, and apart from calcium and magnesium, which interfere with absorption. Take it with vitamin C: this is common advice, although a 2020 randomized trial found vitamin C added no benefit to oral iron in anemia. The common side effects are nausea, constipation, diarrhea, indigestion and a metallic taste. Every-other-day dosing may be better tolerated, though it can make adherence harder.', LIGHT + 'padding:88px 120px 150px;display:grid;grid-template-columns:600px 1fr;gap:90px;align-items:center', f'''
  <div>
    <div style="{EYEBROW}">Recommendations</div>
    <h2 style="{H2};font-size:92px">How to <em>take</em> it.</h2>
    <div style="margin-top:44px;border:3px solid {INK};border-radius:8px;padding:30px 34px 34px;background:#fff">
      <div style="{SERIF};font-size:38px;letter-spacing:-.02em;padding-bottom:16px;border-bottom:8px solid {INK}">Each tablet contains</div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;padding:18px 0;border-bottom:2px solid {INK};font-size:27px"><span>Ferrous sulfate</span><span>300 mg</span></div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;padding:22px 0 8px;font-size:27px;font-weight:600"><span>Elemental iron</span><span style="position:relative;display:inline-block;{SERIF};font-size:44px;font-weight:400;color:{GREEN}">60 mg<span class="dk-ring" style="position:absolute;inset:-12px -26px;border:3px solid rgba(26,80,18,.5);border-radius:50%;transform:rotate(-4deg);pointer-events:none;--rot:-4deg"></span></span></div>
    </div>
  </div>
  <div>
    {rec('01', 'Find the elemental iron dose', 'That&rsquo;s the number that counts, not the size of the salt.')}
    {rec('02', 'Aim for 60–110 mg elemental iron a day', 'As your clinician advises. Every other day may be gentler.')}
    {rec('03', 'Take it on an empty stomach', 'Apart from calcium and magnesium, which interfere with absorption.')}
    {rec('04', 'Take it with vitamin C', 'Common advice, though one trial found no added benefit.')}
    <div style="border-top:2px solid {LINE};border-bottom:2px solid {LINE}">{rec('05', 'Know the common side effects', 'Nausea, constipation, diarrhea, indigestion, metallic taste.').replace(f'border-top:2px solid {LINE};', '', 1)}</div>
  </div>
  {cite('cmaj', 'li', note='Example label for illustration.')}
  {footer()}''')


# 29 ── Close ──────────────────────────────────────────────────────────────────
def close_row(n, title, label, last=False):
    bottom = f'border-bottom:2px solid {LINE};' if last else ''
    return (f'<div style="display:grid;grid-template-columns:110px 1fr;align-items:baseline;border-top:2px solid {LINE};{bottom}padding:30px 0">'
            f'<div style="{SERIF};font-size:44px;color:{GREEN_DEEP}">{n}</div>'
            f'<div><div style="{SERIF};font-size:48px;line-height:1.08;letter-spacing:-.022em">{title}</div>'
            f'<div style="margin-top:10px;font-size:29px;line-height:1.32;letter-spacing:-.012em;color:{INK2}">{label}</div></div></div>')


add('Close', 'Three things to take home, then questions. Educational only: please talk to a clinician about your own results before starting or stopping iron.', LIGHT + 'padding:88px 120px 130px', f'''
  <div style="display:grid;grid-template-columns:1fr 620px;gap:90px;height:100%;box-sizing:border-box;align-items:stretch">
    <div style="display:flex;flex-direction:column;justify-content:center">
      <div style="{EYEBROW}">To take home</div>
      <h2 style="{H2}">Three things to <em>remember</em>.</h2>
      <div style="margin-top:46px">
        {close_row('01', 'Know your ferritin', 'Ask for a blood count and ferritin. &ldquo;Normal&rdquo; has moved.')}
        {close_row('02', 'Look for the cause', 'Menstrual bleeding is the biggest driver in women. Tell your clinician about heavy periods.')}
        {close_row('03', 'Treat low iron, not every tired day', 'Iron helped where it was low, and too much carries its own risks.', last=True)}
      </div>
      <p style="margin:24px 0 0;font-size:23px;line-height:1.4;color:{MUTED}">For education only, not medical advice. Please talk with a clinician about your own results.</p>
    </div>
    <div style="background:linear-gradient(160deg,{GREEN} 0%,#1C3118 100%);color:{CREAM};border-radius:8px;padding:60px 54px;display:flex;flex-direction:column;margin:10px 0 40px;box-sizing:border-box">
      <img src="assets/logos/symbol-white.png" alt="" style="height:42px;align-self:flex-start" loading="eager" decoding="async">
      <div style="margin-top:40px;{SERIF};font-size:66px;letter-spacing:-.03em"><em>Questions?</em></div>
      <p style="margin:18px 0 0;font-size:27px;line-height:1.5;color:rgba(255,252,247,.85)">We&rsquo;re happy to talk anything through, today or after you&rsquo;ve thought it over.</p>
      <div class="closing-export">
        <button type="button" class="export-cta" data-export-pdf>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
          Export as PDF
        </button>
      </div>
      <div style="margin-top:auto;border-top:1px solid rgba(255,252,247,.28);padding-top:34px;display:flex;flex-direction:column;gap:22px;font-size:28px">
        <div><span style="display:block;font-size:22px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,252,247,.6)">Call or text</span><span style="display:block;margin-top:8px">(437) 370-0291</span></div>
        <div><span style="display:block;font-size:22px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,252,247,.6)">Email</span><span style="display:block;margin-top:8px">care@beoptimal.ca</span></div>
        <div><span style="display:block;font-size:22px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,252,247,.6)">Web</span><span style="display:block;margin-top:8px">beoptimal.ca</span></div>
      </div>
    </div>
  </div>
  {footer()}''')


# 30 ── Sources ────────────────────────────────────────────────────────────────
def src_line(i, s):
    title = s[3]
    if len(title) > 96:
        title = title[:title.rfind(' ', 0, 94)] + '…'
    who = s[2].split(',')[0]
    tail = ' et al.' if ',' in s[2] else ''
    return (f'<div style="display:grid;grid-template-columns:44px 1fr;font-size:22px;line-height:1.3;color:{INK2};padding:9px 0;border-top:1px solid {LINE}">'
            f'<span style="color:{GREEN_DEEP};font-weight:600">{i}</span><span>{who}{tail} {title} <span style="color:{MUTED}">{s[4]}</span></span></div>')


half = (len(SOURCES) + 1) // 2
col_a = ''.join(src_line(i + 1, s) for i, s in enumerate(SOURCES[:half]))
col_b = ''.join(src_line(i + 1 + half, s) for i, s in enumerate(SOURCES[half:]))
add('Sources', 'Every claim in this talk has a source. The QR code opens the full list with links.', LIGHT + 'padding:80px 120px 110px;display:flex;flex-direction:column', f'''
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:40px">
    <div>{head('References', 'The <em>sources</em>.')}</div>
    <div style="display:flex;align-items:center;gap:24px">
      <div style="text-align:right;font-size:24px;line-height:1.35;color:{INK2}">Scan for the full list,<br>with links.</div>
      <img src="assets/images/qr-sources.svg" alt="QR code linking to the full list of sources" style="width:130px;height:130px;display:block" loading="eager" decoding="async">
    </div>
  </div>
  <div style="margin-top:26px;display:grid;grid-template-columns:1fr 1fr;gap:0 56px">
    <div>{col_a}</div><div>{col_b}</div>
  </div>
  {footer()}''')

total = len(slides) + 1  # + the welcome screen, printed as 01
numbered = [s.replace('{N}', f'{i + 2:02d} / {total}') for i, s in enumerate(slides)]

# ── Talk-only motion: same vocabulary as the house engine ──────────────────────
IRON_CSS = '''<style>
  /* ==========================================================================
     Iron talk diagrams. The shared tools are in talks/tools/talk_chrome.py;
     these are the moves only this talk needs.
     ========================================================================== */

  /* Ferritin: the magnifier travels over the report and lands on the word */
  .ir-lens { transform: translate(380px, 240px); opacity: 0; }
  deck-stage > section.in-view .ir-lens { animation: ir-lens 1300ms var(--deck-ease) 450ms both; }
  @keyframes ir-lens { from { opacity: 0; transform: translate(380px, 240px); } 25% { opacity: 1; } to { opacity: 1; transform: none; } }
  .ir-lens-word { opacity: 0; }
  deck-stage > section.in-view .ir-lens-word { animation: dk-fade 500ms ease 1500ms both; }

  /* Venn: the two circles close the gap, then the overlap fills */
  deck-stage > section.in-view .ir-venn-l { animation: ir-venn-l 900ms var(--deck-ease) both; }
  deck-stage > section.in-view .ir-venn-r { animation: ir-venn-r 900ms var(--deck-ease) both; }
  @keyframes ir-venn-l { from { transform: translateX(-70px); opacity: 0; } to { transform: none; opacity: 1; } }
  @keyframes ir-venn-r { from { transform: translateX(70px); opacity: 0; } to { transform: none; opacity: 1; } }

  /* The lower limit slides from where it was to where it is */
  .ir-marker { transform: translateX(-315px); opacity: 0; }
  deck-stage > section.in-view .ir-marker { animation: ir-marker 1200ms var(--deck-ease) 1000ms both; }
  @keyframes ir-marker { from { transform: translateX(-315px); opacity: 0; } 15% { opacity: 1; } to { transform: none; opacity: 1; } }

  @media print, (prefers-reduced-motion: reduce) {
    .ir-lens, .ir-lens-word, .ir-marker, .ir-venn-l, .ir-venn-r {
      animation: none !important; opacity: 1 !important; transform: none !important;
    }
  }
</style>
'''

# ── Assemble with the intro deck's chrome ──────────────────────────────────────
start = SRC.index('<deck-stage width="1920" height="1080">') + len('<deck-stage width="1920" height="1080">')
end = SRC.index('</deck-stage>')
html = SRC[:start] + '\n\n' + '\n\n'.join(numbered) + '\n\n' + SRC[end:]

# Drop the auto-renew tag kit (CSS + script): there is no pricing slide here.
html = re.sub(r'/\* =+\s*\n\s*AUTO-RENEW TAG — styles\..*?(?=</style>)', '', html, count=1, flags=re.S)
html = re.sub(r'<!-- =+\s*\n\s*AUTO-RENEW TAG — script\..*?</script>\s*', '', html, count=1, flags=re.S)
assert 'dk-tag' not in html, 'auto-renew kit left behind'


def sub1(old, new):
    global html
    assert old in html, old[:70]
    html = html.replace(old, new, 1)


sub1('<title>Introductory Meeting — Optimal Clinic, Barrie</title>', f'<title>{NAME} — Optimal Clinic, Barrie</title>\n<meta name="version" content="{VERSION}">')
html = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="An educational talk from Optimal Clinic, Barrie: how iron stores are evaluated, what high and low iron do, what the evidence shows, and the treatment options.">', html, count=1)
sub1('     Introductory Meeting — Optimal Clinic, Barrie\n', f'     {NAME} — Optimal Clinic, Barrie\n     Generated by talks/iron-deficiency/tools/build_deck.py. Edit the script, not this file.\n')
html = re.sub(r'The \d+ slides below are the design handoff recreated verbatim',
              f'The {len(slides)} slides below are rebuilt from the clinical team\'s draft', html, count=1)
sub1("Slide copy is client-approved: change markup, not words.", "Slide copy is held to its citations: any change to a fact needs clinical review.")

sub1('<!-- Preparation: the front desk enters the patient\'s name before walking in -->', '<!-- Preparation: the presenter enters the group\'s name before the talk starts -->')
sub1('All presentations</a>', 'All talks</a>')
sub1('<div class="prep-eyebrow">Introductory Meeting · Preparation</div>', f'<div class="prep-eyebrow">{NAME} · Preparation</div>')
sub1("Let's set up <em>this meeting</em>.", "Let's set up <em>this talk</em>.")
html = re.sub(r'<p class="prep-sub">.*?</p>', '<p class="prep-sub">Enter the group or host to personalise the welcome screen, or leave it blank. It stays in this browser tab, and is stamped on any PDF you export.</p>', html, count=1, flags=re.S)
sub1('<span class="field-label">Patient name</span>', '<span class="field-label">Group or host</span>')
sub1('placeholder="e.g. Sarah"', 'placeholder="e.g. Pilates group"')
sub1('<span class="field-label">Date of meeting</span>', '<span class="field-label">Date of talk</span>')
sub1("getName() || 'Patient'", "getName() || 'Group'")
sub1('Export PDF for records', 'Export PDF')
sub1("'Optimal — Introductory Meeting — '", f"'Optimal — {NAME} — '")
html = re.sub(r'the welcome screen is 01 of the printed \d+ but', f'the welcome screen is 01 of the printed {total} but', html)
html = re.sub(r'printed "02 / \d+"', f'printed "02 / {total}"', html)

sub1("dateInput.value = iso(today);", "dateInput.value = new URLSearchParams(location.search).has('static') ? '' : iso(today);  // ?static: the downloadable PDF carries no date")
html = talk_chrome.apply(html)
sub1('</head>', IRON_CSS + '</head>')

assert 'Introductory' not in html
assert 'Sarah' not in html
for typo in ('Mylination', 'Hematopoeisis', 'Mitocondrial', 'Fumurate', 'Bilycinate', 'Polysaccaride', 'Neutraceutical', 'funcitoning', 'substantailly', '18-54', '18–54'):
    assert typo not in html, f'draft typo or error is back: {typo}'
for s in SOURCES:
    assert s[5].startswith('https://'), s[0]
(DECK / 'index.html').write_text(html)

# ── sources.html: what the QR code on the last slide opens ─────────────────────
items = ''.join(
    f'<li><span class="who">{s[2]}</span> {s[3]} <span class="where">{s[4]}</span> <a href="{s[5]}" rel="noopener">{s[5].replace("https://", "") if len(s[5]) < 60 else "Read the notice"}</a></li>'
    for s in SOURCES)
(DECK / 'sources.html').write_text(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<meta name="theme-color" content="{CREAM}">
<title>Sources — {NAME}</title>
<link rel="icon" href="assets/logos/symbol-green-nobg.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Castoro:ital@0;1&amp;family=Public+Sans:wght@400;500;600;700&amp;display=swap">
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ -webkit-text-size-adjust: 100%; background: {CREAM}; }}
  body {{ margin: 0; background: {CREAM}; color: {INK}; font-family: 'Public Sans', system-ui, sans-serif; font-feature-settings: "kern", "liga"; -webkit-font-smoothing: antialiased; }}
  main {{ width: min(780px, 100%); margin: 0 auto; padding: 32px 16px 56px; }}
  .logo {{ display: block; height: 24px; width: auto; }}
  .eyebrow {{ margin-top: 40px; font-size: 12px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: {GREEN_DEEP}; }}
  h1 {{ margin: 12px 0 0; font-family: Castoro, serif; font-weight: 400; font-size: clamp(36px, 9vw, 56px); line-height: 1.04; letter-spacing: -.03em; }}
  h1 em {{ color: {GREEN}; }}
  ol {{ margin: 28px 0 0; padding: 0; list-style: none; counter-reset: s; }}
  li {{ counter-increment: s; position: relative; padding: 16px 0 16px 38px; border-top: 1px solid {LINE}; font-size: 16px; line-height: 1.5; color: {INK2}; overflow-wrap: anywhere; }}
  li::before {{ content: counter(s); position: absolute; left: 0; top: 13px; font-family: Castoro, serif; font-size: 21px; color: {GREEN_DEEP}; }}
  .who {{ color: {INK}; }}
  .where {{ color: {MUTED}; }}
  a {{ display: block; margin-top: 4px; color: {GREEN}; text-underline-offset: 3px; min-height: 24px; }}
  .note {{ margin: 28px 0 0; padding-top: 18px; border-top: 1px solid {LINE}; font-size: 14px; line-height: 1.5; color: {MUTED}; }}
</style>
</head>
<body>
<main>
  <img class="logo" src="assets/logos/OptimalLogo-Green.png" alt="Optimal" width="79" height="24">
  <div class="eyebrow">{NAME}</div>
  <h1>The <em>sources</em>.</h1>
  <ol>{items}</ol>
  <p class="note">For education only, not medical advice. Please talk with a clinician about your own results. Optimal Clinic, 630 Huronia Road, Unit 5, Barrie ON · (437) 370-0291 · care@beoptimal.ca</p>
</main>
</body>
</html>
''')
print(f'wrote talks/iron-deficiency/index.html: {len(slides)} slides, printed /{total}; sources.html: {len(SOURCES)} sources')
