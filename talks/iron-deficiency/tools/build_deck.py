"""Build talks/iron-deficiency/index.html.

    python3 talks/iron-deficiency/tools/build_deck.py      # from the repo root

This deck is the clinical team's 26-page draft, restyled, plus the clinical lead's marked-up edits
of Nov 4 2026. The build refuses to finish if a slide's words differ from tools/draft_words.json,
spelling included. Don't reword anything here. Raise it with the clinical lead, and change it only
once they've asked for it. Slides are written in draft-page order; ORDER below sets the talk's order.

The chrome (set-up screen, reveal engine, PDF export, fullscreen) is copied from
../../intro/index.html so every Optimal deck behaves the same. ../../tools/talk_chrome.py then
applies what all talks share: no foliage, no welcome slide, and the motion layer.
"""
import html as entities
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'talks' / 'tools'))
import talk_chrome  # noqa: E402

DECK = ROOT / 'talks' / 'iron-deficiency'
SRC = (ROOT / 'intro' / 'index.html').read_text()
DRAFT = json.loads((DECK / 'tools' / 'draft_words.json').read_text())['pages']
NAME = 'Iron Deficiency in Women'
VERSION = 'iron-deficiency-talk v2.1.0'

# ── Tokens: the same set as the HBOT deck, at the 1920 artboard's ~2x scale ──
CREAM, INK, INK2, MUTED = '#FFFCF7', '#040504', '#474747', '#76736D'
GREEN, GREEN_DEEP, SAGE, LINE, SAGE50 = '#2C4E25', '#1A500F', '#87A482', '#DFD7CA', '#F0F4EE'
SAGE100, SAGE200, SAGE300 = '#DDE7D2', '#C3D2BE', '#A5BBA0'
DEEP = '#1C3118'
SERIF = 'font-family:Castoro,serif;font-weight:400'
SVGTXT = 'font-family="Public Sans, system-ui, sans-serif"'
SVGSER = 'font-family="Castoro, serif"'
SECTION = ("position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;"
           "font-family:'Public Sans',system-ui,sans-serif;")
LIGHT = SECTION + f'background:{CREAM};color:{INK};'
DARK = SECTION + f'background:linear-gradient(135deg,{GREEN} 0%,{DEEP} 100%);color:{CREAM};'
RULE_D = 'rgba(255,252,247,.28)'

# The talk's order, in draft page numbers, from the clinical lead's marked-up PDF. Draft page 10 is
# merged into 21, and 27 is the new closing slide.
ORDER = [1, 2, 3, 4, 5, 6, 12, 13, 7, 8, 9, 11, 14, 16, 15, 17, 18, 19, 20, 21, 23, 22, 24, 25, 26, 27]
slides = {}
page = 0


def words_of(body):
    text = re.sub(r'<(style|defs)\b.*?</\1>', ' ', body, flags=re.S)
    return sorted(re.findall(r'\S+', entities.unescape(re.sub(r'<[^>]+>', ' ', text))))


def footer(dark=False):
    """A page number and the mark. Nothing else."""
    num = '#FFFCF7' if dark else GREEN_DEEP
    mark = 'symbol-white.png' if dark else 'symbol-green-nobg.png'
    return ('<div class="dk-footer" style="position:absolute;left:120px;right:120px;bottom:44px;display:flex;justify-content:space-between;align-items:center">'
            f'<div class="ir-tnum" style="font-size:24px;font-weight:600;letter-spacing:-.01em;color:{num}">{{N}}</div>'
            f'<img src="assets/logos/{mark}" alt="" style="height:30px;opacity:.8" loading="eager" decoding="async"></div>')


def add(body, style=LIGHT, dark=False, foot=True):
    global page
    page += 1
    got, want = words_of(body), DRAFT[str(page)]
    if got != want:
        raise SystemExit(f'Draft page {page} differs from its approved words. Added: {dict(Counter(got) - Counter(want))}. Missing: {dict(Counter(want) - Counter(got))}')
    cls = 'sl sl-dark' if dark else 'sl'
    slides[page] = f'<section data-label="{{L}}" style="{style}" class="{cls}">\n{body}\n{footer(dark) if foot else ""}\n</section>'


def bullets(items, size=33, pad=19, dark=False, serif=False, last=True):
    """The draft's bullets, set as hairline rows."""
    edge = RULE_D if dark else LINE
    tone = CREAM if dark else INK2
    face = f'{SERIF};line-height:1.16;letter-spacing:-.02em' if serif else 'line-height:1.28;letter-spacing:-.014em'
    out = ''
    for i, t in enumerate(items):
        bottom = f'border-bottom:2px solid {edge};' if last and i == len(items) - 1 else ''
        out += f'<div style="border-top:2px solid {edge};{bottom}padding:{pad}px 0 {pad + 2}px;font-size:{size}px;{face};color:{tone}">{t}</div>'
    return out


def study(title, year, items, shot, size=60, width=590, text=33, pad=19):
    """A paper: its title, its year, the draft's points, and the draft's screenshot of it."""
    add(f'''
  <div>
    <div style="{SERIF};font-style:italic;font-size:44px;line-height:1;color:{GREEN_DEEP}">({year})</div>
    <h2 style="margin:18px 0 0;{SERIF};font-size:{size}px;line-height:1.08;letter-spacing:-.028em;color:{INK}">{title}</h2>
    <div style="margin-top:36px">{bullets(items, text, pad)}</div>
  </div>
  <img class="ir-build" src="assets/draft/{shot}.webp" alt="" style="--d:.35s;display:block;width:{width}px;height:auto;background:#fff;border:2px solid {LINE};border-radius:8px" loading="eager" decoding="async">''',
        LIGHT + f'padding:70px 120px 96px;display:grid;grid-template-columns:1fr {width}px;column-gap:70px;align-items:center')


# 1 ── Title ───────────────────────────────────────────────────────────────────
add(f'''
  <img src="assets/logos/Optimal-Logo-Inverted.png" alt="" style="position:absolute;top:84px;left:120px;height:52px;width:auto" loading="eager" decoding="async">
  <h1 style="margin:0;{SERIF};font-size:216px;line-height:.98;letter-spacing:-.05em;color:{CREAM}">Iron<br>Deficiency<br>in <em>Women</em></h1>''',
    DARK + 'padding:0 120px 100px;display:flex;align-items:flex-end', dark=True, foot=False)


# 2 ── Pyramid ─────────────────────────────────────────────────────────────────
def pyramid():
    tiers = [
        (GREEN, 'Neutraceuticals, Additional Supplements'),
        (SAGE, 'Protein, Carb, Fat intake, goal specific activity'),
        (SAGE300, 'Activity'),
        (SAGE200, 'Mental Well Being'),
        (SAGE100, 'Adequate rest, caloric intake, hydration, safety'),
    ]
    rh, gap, half = 172, 8, 300
    total = 5 * rh - gap
    polys, labels = [], []
    for i, (fill, text) in enumerate(tiers):
        y0, y1 = i * rh, i * rh + rh - gap
        h0, h1 = half * y0 / total, half * y1 / total
        d = f'{(4 - i) * 0.17 + 0.2:.2f}s'
        polys.append(f'<polygon class="ir-tier" style="--d:{d}" points="{half - h0:.1f},{y0} {half + h0:.1f},{y0} {half + h1:.1f},{y1} {half - h1:.1f},{y1}" fill="{fill}"/>')
        edge = f'border-top:2px solid {LINE};' if i else ''
        labels.append(f'<div class="ir-build" style="--d:{d};height:{rh}px;box-sizing:border-box;{edge}display:flex;align-items:center;{SERIF};font-size:38px;line-height:1.14;letter-spacing:-.022em;color:{INK}">{text}</div>')
    return (f'<svg viewBox="0 0 {half * 2} {total}" style="width:{half * 2}px;height:{total}px;display:block;overflow:visible" aria-hidden="true">{"".join(polys)}</svg>'
            f'<div>{"".join(labels)}</div>')


add(f'''
  <h2 style="margin:0;{SERIF};font-size:52px;line-height:1.14;letter-spacing:-.026em;color:{GREEN}"><em>focus on foundations,</em> without pre-existing strong foundations any money spent on neutraceuticals is going to be limited in how effective it could be.</h2>
  {pyramid()}''', LIGHT + 'padding:62px 120px 96px;display:grid;grid-template-columns:1fr 600px 430px;column-gap:50px;align-items:center')


# 3 ── Six around one ──────────────────────────────────────────────────────────
def hexagon():
    cx, cy, rn, rh, rc = 500, 450, 332, 136, 118
    names = ['protein', 'Water', 'Neutraceuticals', 'Fatty Acids', 'Vitamins', 'Minerals']
    pts = ' '.join(f'{cx + rh * math.cos(math.radians(a)):.1f},{cy + rh * math.sin(math.radians(a)):.1f}' for a in range(-90, 270, 60))
    parts = []
    for i, n in enumerate(names):
        a = math.radians(-90 + i * 60)
        x, y = cx + rn * math.cos(a), cy + rn * math.sin(a)
        ix, iy = cx + rh * math.cos(a), cy + rh * math.sin(a)
        ex, ey = cx + (rn - rc) * math.cos(a), cy + (rn - rc) * math.sin(a)
        d = 0.45 + i * 0.1
        parts.append(f'<line class="ir-draw" pathLength="1" style="--d:{d - .16:.2f}s;--dur:460ms" x1="{ix:.1f}" y1="{iy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{SAGE}" stroke-width="3"/>'
                     f'<g class="ir-pop" style="--d:{d:.2f}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="{rc}" fill="{SAGE50}" stroke="{GREEN}" stroke-width="3"/>'
                     f'<text x="{x:.1f}" y="{y + 13:.1f}" text-anchor="middle" {SVGSER} font-size="{31 if n == "Neutraceuticals" else 38}" fill="{INK}">{n}</text></g>')
    return (f'<svg viewBox="0 0 1000 900" style="width:920px;height:828px;display:block;overflow:visible" aria-hidden="true">'
            f'<g class="ir-pop" style="--d:.15s"><polygon points="{pts}" fill="{GREEN}"/>'
            f'<text x="{cx}" y="{cy + 17}" text-anchor="middle" {SVGSER} font-style="italic" font-size="52" fill="{CREAM}">dietary</text></g>'
            f'{"".join(parts)}</svg>')


add(f'''
  <h2 style="margin:0;{SERIF};font-size:60px;line-height:1.12;letter-spacing:-.028em;color:{INK}">Vitamins and Minerals exist as a foundational piece similar to protein/fat/carbs often over looked. <em>We will talk about why</em></h2>
  {hexagon()}''', LIGHT + 'padding:50px 120px 110px;display:grid;grid-template-columns:1fr 920px;column-gap:50px;align-items:center')


# 4 ── Agenda ──────────────────────────────────────────────────────────────────
add(f'''
  <h2 style="margin:0;{SERIF};font-style:italic;font-size:150px;line-height:1;letter-spacing:-.04em;color:{CREAM}">Agenda</h2>
  <div>{bullets(['How we evaluate iron', 'Iron roles', 'Consequences of high/low iron', 'Treatment Options'], 76, 40, dark=True, serif=True)}</div>''',
    DARK + 'padding:88px 120px 120px;display:grid;grid-template-columns:560px 1fr;column-gap:60px;align-items:center', dark=True)


# 5, 6 ── The report, then the magnifier finds ferritin ────────────────────────
def report(tube=False):
    """The draft's test-results clipboard, drawn in the deck's ink."""
    def lines(x0, x1, ys):
        return ''.join(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{SAGE300}" stroke-width="4"/>' for y in ys)
    boxes = ''.join(f'<rect x="64" y="{y}" width="48" height="48" fill="none" stroke="{SAGE}" stroke-width="4"/>' + lines(148, 492, (y + 6, y + 26, y + 46)) for y in (372, 452, 532))
    vial = ''
    if tube:
        vial = (f'<g class="ir-pop" style="--d:.45s">'
                f'<rect x="442" y="350" width="152" height="430" rx="30" fill="{CREAM}" stroke="{GREEN}" stroke-width="5"/>'
                f'<path d="M447 500 H589 V750 a25 25 0 0 1 -25 25 H472 a25 25 0 0 1 -25 -25 Z" fill="#8E2B2A"/>'
                f'<rect x="430" y="318" width="176" height="52" rx="10" fill="{GREEN}"/>'
                f'<rect x="498" y="430" width="96" height="124" rx="6" fill="{CREAM}" stroke="{GREEN}" stroke-width="3"/>'
                f'<text x="546" y="474" text-anchor="middle" {SVGTXT} font-size="22" font-weight="700" fill="#8E2B2A">BLOOD</text>'
                f'<text x="546" y="502" text-anchor="middle" {SVGTXT} font-size="22" font-weight="700" fill="#8E2B2A">TEST</text>'
                f'{lines(512, 580, (518, 532))}</g>')
    return (f'<rect x="0" y="40" width="556" height="730" rx="24" fill="{GREEN}"/>'
            f'<rect x="34" y="82" width="488" height="618" fill="{CREAM}"/>'
            f'<rect x="168" y="28" width="220" height="86" rx="18" fill="{DEEP}"/>'
            f'<rect x="232" y="0" width="92" height="40" rx="14" fill="{DEEP}"/>'
            f'<text x="278" y="172" text-anchor="middle" {SVGTXT} font-size="42" font-weight="700" letter-spacing="1" fill="{INK}">TEST RESULTS</text>'
            f'<line x1="64" y1="204" x2="492" y2="204" stroke="{GREEN}" stroke-width="4"/>'
            f'<rect x="64" y="228" width="112" height="112" fill="{SAGE200}"/>'
            f'{lines(204, 492, (240, 266, 292, 318))}{boxes}{vial}')


add(f'''
  <svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px;display:block" aria-hidden="true">
    <g class="ir-build" style="--d:.1s"><g transform="translate(120 130)">{report(tube=True)}</g></g>
    <g class="ir-lens5">
      <line x1="1470" y1="690" x2="1740" y2="960" stroke="{GREEN}" stroke-width="66" stroke-linecap="round"/>
      <circle cx="1240" cy="460" r="306" fill="{CREAM}" stroke="{GREEN}" stroke-width="54"/>
      <path d="M1056 450 A186 186 0 0 1 1236 268" fill="none" stroke="{SAGE200}" stroke-width="30" stroke-linecap="round"/>
    </g>
  </svg>''')

add(f'''
  <svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;width:1920px;height:1080px;display:block" aria-hidden="true">
    <defs><clipPath id="ir-lens-clip"><circle cx="770" cy="560" r="340"/></clipPath></defs>
    <g class="ir-clip6"><g transform="translate(272 96)">{report()}</g></g>
    <g class="ir-lens6">
      <line x1="1020" y1="812" x2="1280" y2="1072" stroke="{GREEN}" stroke-width="72" stroke-linecap="round"/>
      <circle cx="770" cy="560" r="340" fill="{CREAM}"/>
      <g clip-path="url(#ir-lens-clip)">
        <g class="ir-lens-word">
          <text x="640" y="526" {SVGSER} font-style="italic" font-size="124" fill="{GREEN}">Ferritin</text>
          <g stroke="{SAGE300}" stroke-width="5">
            <line x1="640" y1="572" x2="1110" y2="572"/><line x1="640" y1="616" x2="1110" y2="616"/>
            <line x1="640" y1="696" x2="1110" y2="696"/><line x1="640" y1="740" x2="1110" y2="740"/>
            <line x1="560" y1="806" x2="1110" y2="806"/>
          </g>
        </g>
      </g>
      <circle cx="770" cy="560" r="340" fill="none" stroke="{GREEN}" stroke-width="60"/>
      <path d="M552 560 A218 218 0 0 1 770 342" fill="none" stroke="{SAGE200}" stroke-width="28" stroke-linecap="round"/>
    </g>
  </svg>''')


# 7 ── Two circles ─────────────────────────────────────────────────────────────
add(f'''
  <svg viewBox="0 0 1400 840" style="width:1400px;height:840px;display:block;overflow:visible" aria-hidden="true">
    <defs><clipPath id="ir-venn-clip"><circle cx="500" cy="420" r="410"/></clipPath></defs>
    <circle class="ir-venn-l" cx="500" cy="420" r="410" fill="{SAGE}"/>
    <circle class="ir-venn-r" cx="900" cy="420" r="410" fill="{SAGE100}"/>
    <g class="ir-fade" style="--d:.8s"><circle cx="900" cy="420" r="410" fill="{GREEN}" clip-path="url(#ir-venn-clip)"/></g>
  </svg>''', LIGHT + 'padding:50px 120px 130px;display:flex;align-items:center;justify-content:center')


# 8 ── The ferritin bar and the paper ──────────────────────────────────────────
def segment(pct, fill, tone, html, size=26):
    return f'<div style="width:{pct}%;background:{fill};color:{tone};display:flex;align-items:center;justify-content:center;text-align:center;font-size:{size}px;line-height:1.2;letter-spacing:-.012em">{html}</div>'


def tick(pct, num, label, anchor):
    shift = {'c': 'translateX(-50%)', 'r': 'translateX(-100%)', 'l': 'none'}[anchor]
    nudge = {'c': 0, 'r': 26, 'l': -26}[anchor]
    return (f'<div style="position:absolute;left:{pct}%;top:0;width:2px;height:16px;background:{INK2}"></div>'
            f'<div style="position:absolute;left:{pct}%;top:22px;transform:translateX(-50%);{SERIF};font-size:44px;line-height:1;color:{INK}">{num}</div>'
            f'<div style="position:absolute;left:calc({pct}% + {nudge}px);top:72px;transform:{shift};white-space:nowrap;font-size:25px;letter-spacing:-.01em;color:{INK2}">{label}</div>')


add(f'''
  <div>
    <div class="ir-wipe" style="--dur:1200ms;--d:.2s;display:flex;height:300px;border-radius:8px;overflow:hidden">
      {segment(15, DEEP, CREAM, 'Absolute<br>iron<br>deficiency', 24)}
      {segment(11, GREEN, CREAM, 'Iron<br>deficiency', 24)}
      {segment(33, SAGE, INK, 'Possible iron deficiency<br>Confirm with TSAT<br>or other tests')}
      {segment(41, SAGE100, INK, 'Iron sufficiency')}
    </div>
    <div style="position:relative;height:118px;margin-top:10px">
      {tick(15, '15', 'Absolute ID cutoff', 'r')}
      {tick(26, '26', 'RI lower limit', 'l')}
      {tick(59, '59', 'FRL', 'c')}
    </div>
    <div style="margin-top:22px;text-align:center;font-size:27px;letter-spacing:-.01em;color:{MUTED}">Ferritin (ng/mL)</div>
  </div>
  <img class="ir-build" src="assets/draft/p08-paper.webp" alt="" style="--d:.5s;display:block;width:520px;height:auto;background:#fff;border:2px solid {LINE};border-radius:8px" loading="eager" decoding="async">''',
    LIGHT + 'padding:70px 120px 96px;display:grid;grid-template-columns:1fr 520px;column-gap:70px;align-items:center')


# 9 ── The curve and the paper ─────────────────────────────────────────────────
def bell():
    cx, s, base, peak = 520, 192, 620, 80
    y = lambda x: base - (base - peak) * math.exp(-0.5 * ((x - cx) / s) ** 2)

    def area(a, b):
        pts = ' '.join(f'L{x} {y(x):.1f}' for x in range(a, b + 1, 4))
        return f'M{a} {base} {pts} L{b} {base} Z'
    a, b, c = 140, 236, 331
    bands = [(cx - a, cx + a, SAGE), (cx - b, cx - a, SAGE300), (cx + a, cx + b, SAGE300), (cx - c, cx - b, SAGE100), (cx + b, cx + c, SAGE100)]
    fills = ''.join(f'<path d="{area(p, q)}" fill="{col}"/>' for p, q, col in bands)
    curve = f'M0 {y(0):.1f} ' + ' '.join(f'L{x} {y(x):.1f}' for x in range(4, 1041, 4))
    marks = [(47, 1.5, '', GREEN), (a, 4, '', INK), (b, 3, '12 10', INK), (c, 3, '3 9', INK)]
    verticals = ''.join(f'<line x1="{cx + sign * off}" y1="20" x2="{cx + sign * off}" y2="{base}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
                        for off, w, dash, col in marks for sign in (-1, 1))
    return f'''<svg viewBox="0 0 1040 660" style="width:1040px;height:660px;display:block;overflow:visible" aria-hidden="true">
  <g class="ir-wipe">{fills}</g>
  <g class="ir-fade" style="--d:1.2s">{verticals}</g>
  <path class="ir-draw" pathLength="1" d="{curve}" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linecap="round"/>
  <circle class="ir-ride" r="10" fill="{GREEN}" style="offset-path:path('{curve}')"/>
  <line x1="0" y1="{base}" x2="1040" y2="{base}" stroke="{INK2}" stroke-width="3"/>
</svg>'''


add(f'''
  {bell()}
  <img class="ir-build" src="assets/draft/p09-paper.webp" alt="" style="--d:.5s;display:block;width:570px;height:auto;background:#fff;border:2px solid {LINE};border-radius:8px" loading="eager" decoding="async">''',
    LIGHT + 'padding:70px 120px 96px;display:grid;grid-template-columns:1040px 570px;column-gap:70px;align-items:center')


# 10 ── Iron Impacts on Women: merged into page 21, as the clinical lead suggested ──
IMPACTS = ['There are studies that indicate the impact on low iron or suboptimal iron can extend past anema and present much earlier than the current cut offs.',
           'The available evidence is mixed.',
           'Studies available have small sample sizes and look at a limited period of time',
           'There is insufficient information to state any of these findings as strong recommendations that should be applied to everyone',
           'There is enough evidence to say that it is an area that should be explored further and should be considered as a part of a multimodal approach to a variety of concerns.']
page += 1


# 11 ───────────────────────────────────────────────────────────────────────────
study('Impact of Optimizing the Lower Limit of Normal for Ferritin on Iron Deficiency Diagnosis and Treatment Patterns: A Pre &amp; Post Intervention Study', 2026,
      ['globally under-diagnosed condition', 'adjusting the diagnostic parameters affected women more than men'], 'p11-paper', size=66, width=530, text=38, pad=24)


# 12 ── JObs of iron/ferritin ──────────────────────────────────────────────────
add(f'''
  <h2 style="margin:0 0 28px;{SERIF};font-size:88px;line-height:1;letter-spacing:-.035em;color:{INK}">JObs of iron/ferritin</h2>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;column-gap:40px;min-height:0">
    <div>
      <div style="{SERIF};font-style:italic;font-size:54px;line-height:1;margin:6px 0 20px;color:{GREEN}">Iron</div>
      {bullets(['DNA Synthesis', 'Mylination', 'Energy Metabolism', 'Neurotransmitter Synthesis', 'Oxygen transport &amp; storage', 'Hematopoeisis', 'Mitocondrial energy production', 'Cellular proliferation - including osteoblast production'], 38, 14, serif=True, last=False)}
    </div>
    <div style="background:linear-gradient(160deg,{GREEN} 0%,{DEEP} 100%);border-radius:8px;padding:30px 44px 26px;box-sizing:border-box">
      <div style="{SERIF};font-style:italic;font-size:54px;line-height:1;margin-bottom:20px;color:{CREAM}">Ferritin</div>
      {bullets(['Iron storage', 'Bioavailability buffer', 'Cytoprotective detoxification', 'Inflammatory marker - inflammation increases it’s production', 'Protein', 'Principle iron storage and detoxification protein', 'Critically important in making iron both useable and non toxic'], 38, 14, dark=True, serif=True, last=False)}
    </div>
  </div>''', LIGHT + 'padding:62px 120px 96px;display:flex;flex-direction:column')


# 13 ───────────────────────────────────────────────────────────────────────────
study('Cyclical Iron Homeostasis: The Role of Sex Hormones in Female Iron Regulation', 2026,
      ['Estrogen &amp; Progesterone directly impact the degree of iron availability in the body', 'Iron follows a similar cyclical change',
       'Full implications are unknown but it does tell us that states like perimenopause can substantailly change iron status'], 'p13-paper', size=66, text=36, pad=22)


# 14 ── High Iron ──────────────────────────────────────────────────────────────
def plate(src, d):
    return (f'<div style="display:flex;align-items:center;justify-content:center;min-height:0">'
            f'<img class="ir-ink" src="assets/{src}.webp" alt="" style="--d:{d:.2f}s;--dur:1300ms;max-width:100%;max-height:420px;width:auto;height:auto;display:block" loading="eager" decoding="async"></div>')


add(f'''
  <h2 style="margin:0;{SERIF};font-size:172px;line-height:.98;letter-spacing:-.045em;color:{INK}">High <em>Iron</em></h2>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:424px 424px;gap:18px 30px">
    {plate('draft/p14-skeleton', .2)}{plate('images/liver', .32)}{plate('images/femur', .44)}
    {plate('images/breast', .56)}{plate('images/heart', .68)}{plate('images/apob-plaque', .8)}
  </div>''', LIGHT + 'padding:60px 120px 96px;display:grid;grid-template-columns:440px 1fr;column-gap:50px;align-items:center')


# 15 ── Low Iron ───────────────────────────────────────────────────────────────
add(f'''
  <h2 style="margin:0;{SERIF};font-size:96px;line-height:1.02;letter-spacing:-.04em;color:{INK}">Impact of Suboptimal <em>Iron</em></h2>
  <img class="ir-build" src="assets/draft/p15-figure.webp" alt="" style="--d:.35s;display:block;width:1190px;height:auto;background:#fff;border:2px solid {LINE};border-radius:8px" loading="eager" decoding="async">''',
    LIGHT + 'padding:60px 120px 96px;display:grid;grid-template-columns:440px 1190px;column-gap:50px;align-items:center')


# 16–21 ── The papers ──────────────────────────────────────────────────────────
study('The Complementary Roles of Iron and Estrogen in Menopausal Differences in Cardiometabolic Outcomes', 2024,
      ['iron metabolism changes with hormonal changes in menopause', 'after menopause, excessive iron can increase cardiometabolic risks',
       'Iron stores are lower than men’s before menopause but higher after'], 'p16-paper', size=66, text=36, pad=22)

study('Psychiatric and cognitive outcomes of iron supplementation in non-anemic children, adolescents, and menstruating adults: a meta analysis and systemic review', 2025,
      ['Despite iron being critical in energy metabolism and neurotransmitter synthesis, Iron deficiency is the most common nutritional deficiency world wide',
       'Meta analysis looked at 18 studies looking at iron status on psychiatric and cognitive outcomes',
       'Supplementation improved: anxiety, fatigue, wellbeing, cognitive intelligence and short term memory',
       'No improvement in attention.',
       'Benefits of supplementation were not found in adult males'], 'p17-paper', size=50, text=30, pad=15)

study('Non-anemic iron deficiency: Correlations between symptoms and iron status parameters', 2021,
      ['554 non anemic women with varying Ferritin levels (&lt;50, &lt;20, &lt;15)', 'Iron deficiency associated with symptoms after falling below 50'], 'p18-paper', size=70, text=38, pad=24)

study('Mild iron deficiency may affect female endurance and behavior.', 2019,
      ['Central Nervous System requires iron for functioning', 'Iron status was compared to perceived energy level and EEG findings',
       '23 women between 20-32 in their follicular phase', 'Those with lower ferritin levels reported lower activity and endurance',
       'The groups did not differ in intelligence however, the deficient group required more time to complete the assessment'], 'p19-paper', size=60, text=32, pad=17)

study('Iron Status Is associated with performance on executive functioning tasks in nonanemic young women.', 2016,
      ['127 females between 18-54 years', 'Iron status and executive funcitoning was measured',
       'Better iron status was associated with better attention (faster reaction time), inhibitory control, planning ability, and requiring less planning time,',
       'Other executive functions had no change, and working memory appeared to worsen with better iron status.', 'Limited study'], 'p20-paper', size=52, text=31, pad=15)

# 21 ── Take Aways: the 2011 paper and Iron Impacts on Women together, under her new title ──
add(f'''
  <h2 style="margin:0 0 24px;{SERIF};font-size:92px;line-height:1;letter-spacing:-.035em;color:{INK}">Take <em>Aways</em></h2>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;column-gap:40px;min-height:0">
    <div>
      <div style="{SERIF};font-style:italic;font-size:46px;line-height:1;margin:6px 0 18px;color:{GREEN}">Iron Impacts on Women</div>
      {bullets(IMPACTS, 31, 14, last=False)}
    </div>
    <div style="background:linear-gradient(160deg,{GREEN} 0%,{DEEP} 100%);border-radius:8px;padding:30px 40px 22px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between">
      <div style="display:grid;grid-template-columns:1fr 270px;column-gap:28px;align-items:start">
        <div>
          <div style="{SERIF};font-style:italic;font-size:36px;line-height:1;color:{SAGE100}">(2011)</div>
          <div style="margin-top:12px;{SERIF};font-size:33px;line-height:1.12;letter-spacing:-.018em;color:{CREAM}">Iron status and neuropsychological consequences in women of reproductive age: What do we know and where are we headed?</div>
        </div>
        <img class="ir-build" src="assets/draft/p21-paper.webp" alt="" style="--d:.45s;display:block;width:270px;height:auto;background:#fff;border-radius:6px" loading="eager" decoding="async">
      </div>
      <div style="margin-top:18px">{bullets(['iron status disproportionately affects infants, children, and women of reproductive age', 'indication to explore the interaction between iron status, cognition, emotions, and behavior',
                 'The question remains: What degree of iron deficiency associated with negative consequences?'], 31, 14, dark=True, last=False)}</div>
    </div>
  </div>''', LIGHT + 'padding:58px 120px 96px;display:flex;flex-direction:column')


# 22 ── Pill vs IV ─────────────────────────────────────────────────────────────
add(f'''
  <img class="ir-ink" src="assets/images/iron-tablets.webp" alt="" style="--d:.15s;--dur:1300ms;width:620px;height:auto;display:block" loading="eager" decoding="async">
  <div class="ir-pop" style="--d:.55s;width:330px;height:330px;border-radius:50%;background:{GREEN};display:flex;align-items:center;justify-content:center;{SERIF};font-style:italic;font-size:150px;letter-spacing:-.03em;color:{CREAM}">VS</div>
  <img class="ir-ink" src="assets/images/iv-bag.webp" alt="" style="--d:.8s;--dur:1300ms;--ang:180deg;height:800px;width:auto;display:block" loading="eager" decoding="auto">''',
    LIGHT + 'padding:50px 120px 110px;display:flex;align-items:center;justify-content:space-between')


# 23 ── dietary iron ───────────────────────────────────────────────────────────
add(f'''
  <h2 style="margin:0;{SERIF};font-size:150px;line-height:.98;letter-spacing:-.045em;color:{GREEN}">dietary <em>iron</em></h2>
  <div>{bullets(['maintaning iron stores requires at least 20mg elemental iron daily', 'insufficient to correct deficiency', 'animal sources have heme iron and are better absorbed',
                 'Heme iron is not affected by other foods eaten together, non heme iron absorption is greatly affected by cocurrent foods'], 48, 30, serif=True)}</div>''',
    LIGHT + 'padding:80px 120px 110px;display:grid;grid-template-columns:520px 1fr;column-gap:80px;align-items:center')


# 24 ── Pills ──────────────────────────────────────────────────────────────────
add('''
  <div class="dk-panel ir-breathe"><img class="ir-ink" src="assets/images/iron-tablets-cream.webp" alt="" style="--d:.15s;--dur:1600ms;width:1040px;height:auto;display:block" loading="eager" decoding="async"></div>''',
    DARK + 'padding:40px 120px 100px;display:flex;align-items:center;justify-content:center', dark=True)


# 25 ── Compare ────────────────────────────────────────────────────────────────
def salt(name, icons, i):
    pics = ''.join(f'<img class="ir-pop" src="assets/draft/{src}.webp" alt="" style="--d:{.45 + i * .1 + j * .12:.2f}s;width:{w}px;height:auto;display:block" loading="eager" decoding="async">' for j, (src, w) in enumerate(icons))
    return (f'<div style="border-top:2px solid {LINE};padding-top:20px;display:flex;flex-direction:column;align-items:center;text-align:center">'
            f'<div style="min-height:100px;{SERIF};font-size:42px;line-height:1.1;letter-spacing:-.022em;color:{INK}">{name}</div>'
            f'<div style="margin-top:22px;display:flex;flex-direction:column;align-items:center;gap:26px">{pics}</div></div>')


add(f'''
  <h2 style="margin:0;{SERIF};font-size:118px;line-height:1;letter-spacing:-.04em;color:{INK}">cokmpare ferr <em>salts</em></h2>
  <div style="flex:1;display:grid;grid-template-columns:repeat(6,1fr);column-gap:24px;align-content:center">
    {salt('Sulfate', [], 0)}
    {salt('Fumurate', [('p25-dollar-a', 56), ('p25-sponge', 170), ('p25-belly', 200)], 1)}
    {salt('Gluconate', [], 2)}
    {salt('Bilycinate', [('p25-question', 120)], 3)}
    {salt('Polysaccaride Complex', [('p25-chart', 230)], 4)}
    {salt('Maltol', [('p25-dollar-b', 56), ('p25-hand', 160)], 5)}
  </div>''', LIGHT + 'padding:64px 120px 96px;display:flex;flex-direction:column')


# 26 ── Recommendations ────────────────────────────────────────────────────────
add(f'''
  <div>
    <h2 style="margin:0 0 40px;{SERIF};font-size:104px;line-height:1;letter-spacing:-.04em;color:{INK}"><em>Recommendations</em></h2>
    {bullets(['Determine elemental iron dose', 'aim for 60-110 elemental iron daily', 'Empty stomach. Avoid with calcium/magnesium', 'With Vitamin C', 'Common Side Effects', 'taking it daily vs. every other day'], 42, 20, serif=True)}
  </div>
  <div style="display:flex;align-items:flex-end;justify-content:space-between">
    <img class="ir-build" src="assets/draft/p26-label-a.webp" alt="" style="--d:.45s;width:390px;height:auto;display:block" loading="eager" decoding="async">
    <img class="ir-build" src="assets/draft/p26-label-b.webp" alt="" style="--d:.65s;height:720px;width:auto;display:block" loading="eager" decoding="async">
  </div>''', LIGHT + 'padding:70px 120px 110px;display:grid;grid-template-columns:1fr 860px;column-gap:50px;align-items:center')


# 27 ── Close: the clinical lead's three points ─────────────────────────────────
def close_point(n, text):
    return (f'<div style="display:grid;grid-template-columns:120px 1fr;align-items:baseline;border-top:2px solid {RULE_D};padding:30px 0 34px">'
            f'<div style="{SERIF};font-size:50px;color:{SAGE100}">{n}</div>'
            f'<div style="{SERIF};font-size:54px;line-height:1.14;letter-spacing:-.024em;color:{CREAM}">{text}</div></div>')


add(f'''
  <h2 style="margin:0;{SERIF};font-size:104px;line-height:1.02;letter-spacing:-.035em;color:{CREAM}">Three things to <em>remember.</em></h2>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    {close_point('01', 'Iron is more than anemia')}
    {close_point('02', 'Iron may affect women differently')}
    {close_point('03', 'Focus on foundational health and support your body with a basic possibly overlooked requirement. Talk to your provider about iron intake vs. loss and supplementation options.')}
  </div>''', DARK + 'padding:80px 120px 100px;display:flex;flex-direction:column', dark=True)


assert sorted(ORDER) == sorted(slides), 'ORDER must list every slide once'
total = len(ORDER)
numbered = [slides[p].replace('{N}', f'{i + 1:02d} / {total}').replace('{L}', str(i + 1)) for i, p in enumerate(ORDER)]

# ── This talk's own diagram moves: the shared tools are in talks/tools/talk_chrome.py ──
IRON_CSS = '''<style>
  /* The magnifier comes in beside the report */
  .ir-lens5 { opacity: 0; transform: translateX(170px); }
  deck-stage > section.in-view .ir-lens5 { animation: ir-lens5 1100ms var(--deck-ease) .35s both; }
  @keyframes ir-lens5 { from { opacity: 0; transform: translateX(170px); } to { opacity: 1; transform: none; } }

  /* Then it travels from there onto the report, and ferritin comes up inside it */
  deck-stage > section.in-view .ir-lens6 { animation: ir-lens6 1250ms var(--deck-ease) .1s both; }
  @keyframes ir-lens6 { from { transform: translate(470px, -100px) scale(.9); } to { transform: none; } }
  deck-stage > section.in-view .ir-clip6 { animation: ir-clip6 1250ms var(--deck-ease) .1s both; }
  @keyframes ir-clip6 { from { transform: translate(-152px, 34px); } to { transform: none; } }
  .ir-lens-word { opacity: 0; }
  deck-stage > section.in-view .ir-lens-word { animation: dk-fade 600ms ease 1050ms both; }

  /* The two circles close the gap, then the overlap fills */
  deck-stage > section.in-view .ir-venn-l { animation: ir-venn-l 950ms var(--deck-ease) both; }
  deck-stage > section.in-view .ir-venn-r { animation: ir-venn-r 950ms var(--deck-ease) both; }
  @keyframes ir-venn-l { from { transform: translateX(-90px); opacity: 0; } to { transform: none; opacity: 1; } }
  @keyframes ir-venn-r { from { transform: translateX(90px); opacity: 0; } to { transform: none; opacity: 1; } }

  @media print, (prefers-reduced-motion: reduce) {
    .ir-lens5, .ir-lens6, .ir-clip6, .ir-lens-word, .ir-venn-l, .ir-venn-r {
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
html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{NAME}, a talk from Optimal Clinic, Barrie.">', html, count=1)
sub1('     Introductory Meeting — Optimal Clinic, Barrie\n', f'     {NAME} — Optimal Clinic, Barrie\n     Generated by talks/iron-deficiency/tools/build_deck.py. Edit the script, not this file.\n')
html = re.sub(r'The \d+ slides below are the design handoff recreated verbatim',
              f'The {len(slides)} slides below are the clinical team\'s draft, restyled, with the clinical lead\'s Nov 4 edits', html, count=1)
sub1('Slide copy is client-approved: change markup, not words.', 'Slide copy is the clinical team\'s, word for word: change markup, not words.')

sub1('<!-- Preparation: the front desk enters the patient\'s name before walking in -->', '<!-- Preparation: the presenter sets up before the talk starts -->')
sub1('All presentations</a>', 'All talks</a>')
sub1('<div class="prep-eyebrow">Introductory Meeting · Preparation</div>', f'<div class="prep-eyebrow">{NAME} · Preparation</div>')
sub1("Let's set up <em>this meeting</em>.", "Let's set up <em>this talk</em>.")
html = re.sub(r'<p class="prep-sub">.*?</p>', '<p class="prep-sub">If you export a PDF, the group or host goes in its file name. Leave it blank if you like. It stays in this browser tab.</p>', html, count=1, flags=re.S)
sub1('<span class="field-label">Patient name</span>', '<span class="field-label">Group or host</span>')
sub1('placeholder="e.g. Sarah"', 'placeholder="e.g. Pilates group"')
sub1('<span class="field-label">Date of meeting</span>', '<span class="field-label">Date of talk</span>')
sub1("getName() || 'Patient'", "getName() || 'Group'")
sub1('Export PDF for records', 'Export PDF')
sub1("'Optimal — Introductory Meeting — '", f"'Optimal — {NAME} — '")
html = re.sub(r'Note\s+that N counts deck slides.*?printed "02 / \d+"\.', 'N is the page number on the slide.', html, count=1, flags=re.S)
sub1('</head>', IRON_CSS + '</head>')
html = talk_chrome.apply(html)

assert 'Introductory' not in html
assert 'Sarah' not in html
(DECK / 'index.html').write_text(html)
print(f'wrote talks/iron-deficiency/index.html: {len(slides)} slides, each matching its approved words')
