"""Build hbot/index.html — the HBOT patient briefing.

    python3 hbot/tools/build_deck.py      # from the repo root

The chrome (cover screens, reveal engine, PDF export, fullscreen) is copied from
../intro/index.html so every Optimal deck behaves the same. The slides are below.

Copy source: the beoptimal.ca HBOT page (BeOptimal/beoptimal-landing,
src/content/hbot/page.html). It carries Chantelle's Oct 24 edits (70590e0, 28a7386):
no Israel/Shamir/Sagol references, no "honest", the partner physician holds
clinical responsibility, no "who it may suit". When the page changes, mirror it
here and rebuild. Deck-only wording, approved by Peter on Oct 24, is listed in
../README.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = (ROOT / 'intro' / 'index.html').read_text()
OUT = ROOT / 'hbot' / 'index.html'
NAME = 'Hyperbaric Oxygen Therapy'
VERSION = 'hbot-deck v2.0.0'
NB = '  ·  '

# ── Tokens: the landing page's --op-* set, at the 1920 artboard's ~2x scale ──
CREAM, INK, INK2, MUTED = '#FFFCF7', '#040504', '#474747', '#76736D'
GREEN, GREEN_DEEP, SAGE, LINE, SAGE50 = '#2C4E25', '#1A500F', '#87A482', '#DFD7CA', '#F0F4EE'
NIGHT = '#0B1608'
EYEBROW = f"font-size:24px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:{GREEN_DEEP}"
EYEBROW_D = "font-size:24px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:rgba(255,252,247,.66)"
H2 = f"margin:22px 0 0;font-family:Castoro,serif;font-weight:400;font-size:76px;line-height:1.05;letter-spacing:-.03em;color:{INK}"
BODY = f"font-size:28px;line-height:1.5;letter-spacing:-.01em;color:{INK2}"
CAPS = f"font-size:22px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:{MUTED}"
SECTION = ("position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;"
           "font-family:'Public Sans',system-ui,sans-serif;")
LIGHT = SECTION + f"background:{CREAM};color:{INK};"
DARK = SECTION + f"background:linear-gradient(135deg,{GREEN} 0%,#1C3118 100%);color:{CREAM};"


def ring(word, inset='-8px -24px'):
    """The design system's hand-drawn ring. Two in the deck, where the page has them."""
    return (f'<span style="position:relative;display:inline-block"><em>{word}</em>'
            f'<span class="dk-ring" style="position:absolute;inset:{inset};border:3px solid rgba(26,80,18,.5);'
            f'border-radius:50%;transform:rotate(-2.5deg);pointer-events:none;--rot:-2.5deg"></span></span>')


def footer(dark=False, left=120, right=120):
    if dark:
        return (f'<div class="dk-footer" style="position:absolute;left:{left}px;right:{right}px;bottom:50px;display:flex;justify-content:space-between;align-items:center">'
                '<div style="font-size:24px;letter-spacing:-.01em;color:rgba(255,252,247,.5)"><span style="color:#FFFCF7;font-weight:600">{N}</span>  '
                f'{NAME} — Optimal Clinic, Barrie</div><img src="assets/logos/symbol-white.png" alt="" style="height:30px;opacity:.7" loading="eager" decoding="async"></div>')
    return (f'<div class="dk-footer" style="position:absolute;left:{left}px;right:{right}px;bottom:50px;display:flex;justify-content:space-between;align-items:center">'
            '<div style="font-size:24px;letter-spacing:-.01em;color:#8A867D"><span style="color:#1A500F;font-weight:600">{N}</span>  '
            f'{NAME} — Optimal Clinic, Barrie</div><img src="assets/logos/symbol-green-nobg.png" alt="" style="height:30px;opacity:.85" loading="eager" decoding="async"></div>')


def motion(key, alt, style=''):
    """A micrograph that moves: the still underneath (print, reduced motion, first
    paint), the seamless Kling loop on top. Plays only while its slide is up."""
    return (f'<div class="hb-motion-wrap" style="position:relative;overflow:hidden;background:{NIGHT};{style}">'
            f'<img class="hb-still" src="assets/images/micro-{key}.webp" alt="{alt}" loading="eager" decoding="async">'
            f'<video class="hb-motion" src="assets/video/{key}.mp4" poster="assets/images/micro-{key}.webp" muted loop playsinline preload="auto" aria-hidden="true"></video>'
            '</div>')


CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true" style="width:30px;height:30px;flex:none;margin-top:4px"><path d="M4 12.5l5 5L20 6.5"/></svg>')
DASH = ('<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" '
        'aria-hidden="true" style="width:30px;height:30px;flex:none;margin-top:4px"><path d="M5 12h14"/></svg>')

# ── Pictograms for "How it works": drawn in the brand's line language ──────────
PICTO_CHAMBER = f'''<svg class="hb-picto hb-chamber" viewBox="0 0 280 140" aria-hidden="true">
  <rect x="10" y="20" width="260" height="100" rx="50" fill="{SAGE50}" stroke="{GREEN}" stroke-width="3"/>
  <rect class="hb-press p1" x="28" y="36" width="224" height="68" rx="34" fill="none" stroke="{SAGE}" stroke-width="2.4"/>
  <rect class="hb-press p2" x="28" y="36" width="224" height="68" rx="34" fill="none" stroke="{SAGE}" stroke-width="2.4"/>
  <rect class="hb-press p3" x="28" y="36" width="224" height="68" rx="34" fill="none" stroke="{SAGE}" stroke-width="2.4"/>
  <circle cx="140" cy="70" r="7" fill="{GREEN}"/>
</svg>'''
PICTO_OXYGEN = f'''<svg class="hb-picto hb-oxygen" viewBox="0 0 280 140" aria-hidden="true">
  <rect x="10" y="30" width="260" height="80" fill="{SAGE50}"/>
  <path d="M10 30 H270 M10 110 H270" stroke="{GREEN}" stroke-width="3" fill="none" stroke-linecap="round"/>
  {''.join(f'<circle class="hb-o2" cx="{20 + i * 21}" cy="{48 + (i % 3) * 22}" r="{8 if i % 2 else 6}" fill="{GREEN if i % 3 else SAGE}" style="--d:{i * 0.42:.2f}s;--x:{20 + i * 21}px"/>' for i in range(12))}
</svg>'''
PICTO_SERIES = f'''<svg class="hb-picto hb-series" viewBox="0 0 280 140" aria-hidden="true">
  <path d="M24 70 H256" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>
  {''.join(f'<circle class="hb-dot" cx="{24 + i * 29}" cy="70" r="11" fill="{CREAM}" stroke="{GREEN}" stroke-width="3" style="--d:{i * 0.32:.2f}s"/>' for i in range(9))}
</svg>'''

# ── One session, schematic: oxygen periods with air breaks between ramps ───────
def session_wave():
    w, h, base, top = 860, 190, 150, 46
    ramp = 90
    blocks, x = [], ramp + 10
    seg_o2, seg_air, n = 108, 30, 5
    for i in range(n):
        blocks.append(f'<rect class="hb-o2bar" x="{x}" y="{top}" width="{seg_o2}" height="{base - top}" rx="6" fill="{GREEN}" style="--d:{0.5 + i * 0.22:.2f}s"/>')
        x += seg_o2
        if i < n - 1:
            blocks.append(f'<rect class="hb-airbar" x="{x + 4}" y="{base - 34}" width="{seg_air - 8}" height="34" rx="4" fill="{SAGE}" style="--d:{0.6 + i * 0.22:.2f}s"/>')
            x += seg_air
    end = x + 10
    return f'''<svg class="hb-wave" viewBox="0 0 {w} {h + 40}" style="width:100%;height:auto;display:block" aria-label="Schematic of one session: oxygen periods with brief air breaks, between gradual pressure changes">
  <path class="hb-ramp" d="M0 {base} L{ramp} {top - 6}" stroke="{SAGE}" stroke-width="3" stroke-dasharray="7 7" fill="none"/>
  <path class="hb-ramp" d="M{end} {top - 6} L{w} {base}" stroke="{SAGE}" stroke-width="3" stroke-dasharray="7 7" fill="none"/>
  {''.join(blocks)}
  <path d="M0 {base + 2} H{w}" stroke="{LINE}" stroke-width="3"/>
  <text x="0" y="{h + 34}" font-family="Public Sans, system-ui, sans-serif" font-size="20" font-weight="600" letter-spacing="2.6" fill="{MUTED}">PRESSURE UP</text>
  <text x="{w}" y="{h + 34}" text-anchor="end" font-family="Public Sans, system-ui, sans-serif" font-size="20" font-weight="600" letter-spacing="2.6" fill="{MUTED}">PRESSURE DOWN</text>
  <g transform="translate({w / 2 - 128} {h + 16})"><rect width="22" height="22" rx="4" fill="{GREEN}"/><text x="34" y="18" font-family="Public Sans, system-ui, sans-serif" font-size="20" font-weight="600" letter-spacing="2.6" fill="{INK2}">OXYGEN</text>
  <rect x="160" width="22" height="22" rx="4" fill="{SAGE}"/><text x="194" y="18" font-family="Public Sans, system-ui, sans-serif" font-size="20" font-weight="600" letter-spacing="2.6" fill="{INK2}">AIR BREAK</text></g>
</svg>'''


slides = []

# 1 ── Title ───────────────────────────────────────────────────────────────────
slides.append(f'''<section data-label="Title" data-speaker-notes="Frame the service: hyperbaric oxygen therapy as a structured, physician-supervised longevity and wellness program. Investigational, evidence-informed, delivered at our partner facility." style="{LIGHT}padding:88px 120px 96px" class="sl">
  <div class="dk-panel hb-photo" style="position:absolute;top:88px;right:120px;width:700px;height:896px;border-radius:16px;overflow:hidden;box-shadow:0 8px 48px rgba(0,0,0,.07)">
    <img class="hb-drift" src="assets/images/chambers.webp" alt="Hyperbaric chambers at our partner facility" style="width:100%;height:100%;object-fit:cover;display:block" loading="eager" decoding="async">
  </div>
  <div style="width:880px;height:100%;display:flex;flex-direction:column">
    <div>
      <img src="assets/logos/OptimalLogo-Green.png" alt="Optimal" style="height:44px" loading="eager" decoding="async">
      <div style="margin-top:26px;padding-bottom:26px;border-bottom:2px solid {LINE};{CAPS};letter-spacing:.22em">Patient briefing{NB}2026{NB}Barrie, ON</div>
    </div>
    <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
      <div style="{EYEBROW}">A longevity &amp; wellness service from Optimal</div>
      <h1 style="margin:28px 0 0;font-family:Castoro,serif;font-weight:400;font-size:128px;line-height:1;letter-spacing:-.04em;color:{GREEN}">Hyperbaric<br><em>oxygen</em> therapy.</h1>
      <p style="margin:40px 0 0;max-width:760px;font-size:32px;line-height:1.45;letter-spacing:-.015em;color:{INK2}">Breathing oxygen at increased pressure, delivered as a structured, physician-supervised program.</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:36px;border-top:2px solid {LINE};padding-top:30px">
      <div><div style="{CAPS};font-size:20px">Administered by</div><div style="margin-top:12px;font-family:Castoro,serif;font-size:30px;letter-spacing:-.015em;color:{GREEN}">Physician (MD)</div></div>
      <div><div style="{CAPS};font-size:20px">Program</div><div style="margin-top:12px;font-family:Castoro,serif;font-size:30px;letter-spacing:-.015em;color:{GREEN}">A series of sessions</div></div>
      <div><div style="{CAPS};font-size:20px">Coverage</div><div style="margin-top:12px;font-family:Castoro,serif;font-size:30px;letter-spacing:-.015em;color:{GREEN}">HSA-eligible</div></div>
    </div>
  </div>
</section>''')

# 2 ── Agenda ──────────────────────────────────────────────────────────────────
def agenda_row(n, name, label, last=False):
    bottom = f'border-bottom:2px solid {LINE};' if last else ''
    return (f'<div style="display:grid;grid-template-columns:140px 1fr 520px;align-items:center;border-top:2px solid {LINE};{bottom}padding:30px 0">'
            f'<div style="font-family:Castoro,serif;font-size:44px;color:{GREEN_DEEP}">{n}</div>'
            f'<div style="font-family:Castoro,serif;font-size:42px;letter-spacing:-.02em">{name}</div>'
            f'<div style="text-align:right;{CAPS}">{label}</div></div>')

slides.append(f'''<section data-label="Agenda" data-speaker-notes="Five parts. What the research shows, and where it stops, comes before the sessions themselves." style="{LIGHT}padding:88px 120px 130px;display:flex;flex-direction:column" class="sl">
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div>
      <div style="{EYEBROW}">Today, step by step</div>
      <h2 style="{H2}">What we'll <em>cover</em>.</h2>
    </div>
    <div style="{CAPS};padding-bottom:14px">5 parts</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;justify-content:center">
    {agenda_row('01', 'How it works', 'Inside the protocol')}
    {agenda_row('02', 'What the research explores', 'Four areas')}
    {agenda_row('03', 'Where this fits, plainly', 'In plain terms')}
    {agenda_row('04', 'Who runs your sessions', 'What to expect')}
    {agenda_row('05', 'The evidence &amp; your questions', 'Next steps', last=True)}
  </div>
  {footer()}
</section>''')

# 3 ── How it works ────────────────────────────────────────────────────────────
def step(n, picto, title, body):
    return (f'<div style="border-top:2px solid {LINE};padding-top:30px">'
            f'<div style="display:flex;align-items:center;justify-content:space-between">'
            f'<div style="font-family:Castoro,serif;font-style:italic;font-size:56px;line-height:1;color:{SAGE}">{n}</div>'
            f'<div style="width:300px">{picto}</div></div>'
            f'<h3 style="margin:22px 0 0;font-family:Castoro,serif;font-weight:400;font-size:44px;letter-spacing:-.02em;color:{INK}">{title}</h3>'
            f'<p style="margin:16px 0 0;{BODY};font-size:26px">{body}</p></div>')

slides.append(f'''<section data-label="How it works" data-speaker-notes="The mechanism in one idea: controlled swings in oxygen that the body reads as a signal. It is the repetition across a series, not one session, that the research associates with change." style="{LIGHT}padding:88px 120px 130px;display:flex;flex-direction:column" class="sl">
  <div style="display:grid;grid-template-columns:1fr 760px;gap:120px;align-items:end">
    <div>
      <div style="{EYEBROW}">How it works</div>
      <h2 style="{H2};font-size:96px"><em>Oxygen</em>, under pressure.</h2>
    </div>
    <p style="{BODY}">Inside a pressurized chamber, you breathe oxygen at a concentration and pressure far above normal air. Researchers describe the underlying idea as the &ldquo;hyperoxic-hypoxic paradox&rdquo; — repeated, controlled swings in oxygen that the body responds to as a signal.</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:64px;align-content:center">
    {step('01', PICTO_CHAMBER, 'Pressurized chamber', 'You rest in a clear chamber while pressure is gently raised — similar to the sensation of a plane&rsquo;s descent. Sessions are calm and monitored throughout.')}
    {step('02', PICTO_OXYGEN, 'Elevated oxygen', 'Higher pressure lets far more oxygen dissolve into the blood and plasma than breathing ordinary air ever could, reaching tissues throughout the body.')}
    {step('03', PICTO_SERIES, 'Repeated sessions', 'The protocol is a series of sessions over weeks. In studies, it&rsquo;s the repeated cycling — not any single session — that is associated with the biological changes.')}
  </div>
  {footer()}
</section>''')

# 4 ── Inside the protocol ─────────────────────────────────────────────────────
def stat(big, small):
    return (f'<div style="border-top:2px solid {LINE};padding-top:20px">'
            f'<div style="font-family:Castoro,serif;font-size:52px;line-height:1;letter-spacing:-.025em;color:{GREEN};white-space:nowrap">{big}</div>'
            f'<div style="margin-top:12px;font-size:20px;line-height:1.38;color:{INK2}">{small}</div></div>')

slides.append(f'''<section data-label="Inside the protocol" data-speaker-notes="The program follows the structured protocol used in the published research: intermittent oxygen across a series of sessions. The schematic shows the shape of one session only. Exact parameters are discussed and decided with the administering physician." style="{LIGHT}padding:80px 120px 124px 900px;display:flex;flex-direction:column;justify-content:center" class="sl">
  <div class="dk-panel" style="position:absolute;top:0;left:0;bottom:0;width:780px;overflow:hidden">
    <img class="hb-drift" src="assets/images/chamber-controls.webp" alt="A hyperbaric chamber's control panel at our partner facility" style="width:100%;height:100%;object-fit:cover;display:block" loading="eager" decoding="async">
  </div>
  <div style="{EYEBROW}">The protocol we follow</div>
  <h2 style="{H2}">Inside the <em>protocol</em>.</h2>
  <p style="margin:26px 0 0;{BODY};font-size:26px">Our program is modelled on the structured protocol used in the published research on HBOT and aging-associated biomarkers. Rather than continuous oxygen, the protocol uses <strong style="font-weight:600;color:{INK}">intermittent oxygen breathing</strong> within each session — the pattern researchers associate with the &ldquo;hyperoxic-hypoxic paradox.&rdquo;</p>
  <div style="margin-top:34px;padding:26px 30px 18px;border:2px solid {LINE};border-radius:16px;background:#fff">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:14px"><span style="{CAPS};color:{GREEN_DEEP};font-size:19px">One session, schematic</span><span style="font-size:19px;font-style:italic;color:{MUTED}">Exact parameters are decided with the physician</span></div>
    {session_wave()}
  </div>
  <div style="margin-top:30px;display:grid;grid-template-columns:repeat(4,1fr);gap:30px">
    {stat('~<span class="hb-count" data-to="90">90</span> min', 'per session, including gradual pressure changes')}
    {stat('Series', 'a course of repeated sessions over several weeks')}
    {stat('Cycled O<sub style="font-size:.55em">2</sub>', 'intermittent oxygen with brief air breaks')}
    {stat('MD-led', 'supervised by the administering physician throughout')}
  </div>
  {footer(left=900)}
</section>''')

# 5–6 ── What the research explores (two areas per slide, micrographs in motion) ──
def area(key, alt, title, body, caveat):
    return (f'<div style="display:flex;flex-direction:column;border:2px solid {LINE};border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 8px 48px rgba(0,0,0,.05)">'
            f'{motion(key, alt, "height:330px")}'
            f'<div style="padding:32px 40px 34px;display:flex;flex-direction:column;flex:1">'
            f'<h3 style="margin:0;font-family:Castoro,serif;font-weight:400;font-size:42px;letter-spacing:-.02em;color:{INK}">{title}</h3>'
            f'<p style="margin:14px 0 0;{BODY};font-size:25px">{body}</p>'
            f'<p style="margin:auto 0 0;padding-top:18px;border-top:2px solid {LINE};font-size:22px;line-height:1.4;font-style:italic;color:{MUTED}">{caveat}</p>'
            f'</div></div>')

INTRO = ('A growing body of peer-reviewed research explores how HBOT interacts with the biology of aging. Here&rsquo;s what studies have observed across four '
         'areas — described plainly, with every source cited at the end.')

for part, notes, a, b in [
    ('1 of 2', 'Two of four areas. Read the line under each card aloud: these are biomarker and biology findings, not proven outcomes.',
     ('telomeres', 'Fluorescence micrograph of cells and their nuclei, moving', 'Cellular aging markers', 'In trials, HBOT has been associated with longer telomeres and fewer senescent immune cells in the blood of aging adults, alongside signals of active DNA repair.', 'Early biomarker findings — not yet proven to change how we age.'),
     ('angiogenesis', 'Fluorescence micrograph of retinal blood vessels, moving', 'Tissue &amp; regeneration', 'Studies point to increased blood-vessel growth, shifts in skin collagen density, and better tissue oxygenation and wound-healing dynamics.', 'Reparative-biology signals, still being studied in healthy people.')),
    ('2 of 2', 'The other two areas. The brain findings come mainly from injury and impairment groups; the mitochondrial story is a plausible mechanism, not an established longevity link.',
     ('neurons', 'Fluorescence micrograph of neurons, moving', 'Brain &amp; neuroplasticity', 'In injury and impairment groups, HBOT has been linked to changes in cerebral blood flow and gains on some attention and executive-function measures.', 'Studied mainly after injury — not yet in healthy aging.'),
     ('mitochondria', 'Fluorescence micrograph of a cell&rsquo;s mitochondrial network, moving', 'Mitochondria &amp; oxidative signalling', 'Oxygen cycling appears to nudge mitochondrial signalling and the body&rsquo;s own antioxidant defenses through a hormesis — a beneficial small-stress adaptation — effect.', 'A plausible mechanism; the longevity link isn&rsquo;t established.')),
]:
    slides.append(f'''<section data-label="Research {part}" data-speaker-notes="{notes}" style="{LIGHT}padding:80px 120px 124px;display:flex;flex-direction:column" class="sl">
  <div style="display:grid;grid-template-columns:1fr 720px;gap:100px;align-items:end">
    <div>
      <div style="{EYEBROW}">What the research explores{NB}{part}</div>
      <h2 style="{H2};font-size:68px">Potential <em>longevity</em>-related benefits.</h2>
    </div>
    <p style="{BODY};font-size:24px">{INTRO}</p>
  </div>
  <div style="flex:1;margin-top:40px;display:grid;grid-template-columns:1fr 1fr;gap:40px">
    {area(*a)}
    {area(*b)}
  </div>
  {footer()}
</section>''')

# 7 ── The bottom line (dark statement, neurons in motion) ─────────────────────
slides.append(f'''<section data-label="The bottom line" data-speaker-notes="Say this plainly and pause. The patient should leave knowing exactly where the science stands." style="{DARK}padding:96px 120px 130px;display:flex;flex-direction:column;justify-content:center" class="sl sl-dark">
  <div class="dk-panel" style="position:absolute;top:0;right:0;bottom:0;width:680px">{motion('neurons', '', 'width:100%;height:100%')}</div>
  <div style="position:absolute;top:0;right:0;bottom:0;width:680px;background:linear-gradient(90deg,#24421F 0%,rgba(36,66,31,0) 34%)" class="dk-scrim"></div>
  <div style="max-width:1000px;position:relative">
    <div style="{EYEBROW_D}">The bottom line</div>
    <p style="margin:36px 0 0;font-family:Castoro,serif;font-size:58px;line-height:1.18;letter-spacing:-.025em;color:{CREAM}">These are early findings at the level of biology. A longer lifespan, disease prevention in healthy people, and reversal of aging haven&rsquo;t been proven as clinical outcomes — larger trials are ongoing.</p>
    <p style="margin:44px 0 0;max-width:860px;font-size:30px;line-height:1.5;color:rgba(255,252,247,.78)">We think the science is genuinely promising, and we&rsquo;d rather you see <em style="font-family:Castoro,serif;font-size:1.12em;color:#DDE7D2">exactly where it stands</em>.</p>
  </div>
  {footer(dark=True, right=800)}
</section>''')

# 8 ── Where this fits, plainly ────────────────────────────────────────────────
def trust(text):
    return (f'<div style="display:flex;gap:16px;align-items:flex-start;border-top:2px solid {LINE};padding-top:26px">'
            f'{CHECK.format(c=GREEN)}<div style="font-family:Castoro,serif;font-size:30px;line-height:1.25;letter-spacing:-.01em;color:{INK}">{text}</div></div>')

slides.append(f'''<section data-label="Where this fits" data-speaker-notes="Established for specific conditions, still being researched for longevity, not approved by Health Canada for aging, paid privately. Then the four commitments along the bottom." style="{LIGHT}padding:88px 120px 130px;display:flex;flex-direction:column" class="sl">
  <div style="{EYEBROW}">In plain terms</div>
  <h2 style="{H2};font-size:96px">Where this fits, <em>plainly</em>.</h2>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:96px;align-content:center">
    <p style="{BODY};font-size:30px">Hyperbaric oxygen therapy (HBOT) is a well-established treatment for a specific set of medical conditions. Its use for longevity, healthy aging and wellness is newer. That use is still being researched. Health Canada has not approved it as a treatment for aging or disease. We offer it on that basis.</p>
    <p style="{BODY};font-size:30px">This is a wellness service, not a covered medical treatment. It is not billed to OHIP. Most members pay privately. Some employer HSA plans may apply. Every claim in this presentation cites its source.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:44px">
    {trust('Physician-administered &amp; supervised')}
    {trust('Modelled on a published clinical protocol')}
    {trust('Every program begins with a medical screening')}
    {trust('HSA-eligible · not OHIP-covered')}
  </div>
  {footer()}
</section>''')

# 9 ── Who runs your sessions ──────────────────────────────────────────────────
def duty(text, on=True):
    mark = CHECK.format(c=GREEN) if on else DASH.format(c=MUTED)
    return (f'<li class="hb-duty" style="list-style:none;display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-top:2px solid {LINE}">'
            f'{mark}<span style="font-family:Castoro,serif;font-size:29px;line-height:1.25;color:{INK if on else MUTED}">{text}</span></li>')

slides.append(f'''<section data-label="Who runs your sessions" data-speaker-notes="Be exact about roles. The partner facility's physician screens, sets the protocol, supervises every session and holds clinical responsibility. Optimal's role is the introduction; the Optimal NP does not screen, manage the protocol or review results." style="{LIGHT}padding:80px 900px 124px 120px;display:flex;flex-direction:column;justify-content:center" class="sl">
  <div class="dk-panel" style="position:absolute;top:0;right:0;bottom:0;width:780px;overflow:hidden">
    <img class="hb-drift" src="assets/images/clinician-review.webp" alt="A physician reviewing results with a patient" style="width:100%;height:100%;object-fit:cover;object-position:60% center;display:block" loading="eager" decoding="async">
  </div>
  <div style="{EYEBROW}">The clinic behind it</div>
  <h2 style="{H2}">Who runs your <em>sessions</em>.</h2>
  <p style="margin:26px 0 0;{BODY};font-size:25px">Your hyperbaric sessions are delivered at our partner hyperbaric facility. The physician who runs that facility screens you, sets your protocol and supervises every session. Clinical responsibility for your HBOT care sits with them.</p>
  <p style="margin:16px 0 0;{BODY};font-size:25px">Optimal&rsquo;s role is limited to the introduction. Your Optimal nurse practitioner does not screen you for HBOT, does not set or manage your protocol, and does not review your results. Questions about whether HBOT suits you belong with the administering physician.</p>
  <div style="margin-top:34px;display:grid;grid-template-columns:1.25fr 1fr;gap:44px">
    <div>
      <div style="{CAPS};color:{GREEN_DEEP};font-size:19px;margin-bottom:6px">Partner physician (MD)</div>
      <ul style="margin:0;padding:0;border-bottom:2px solid {LINE}">{duty('Screens you')}{duty('Sets your protocol')}{duty('Supervises every session')}{duty('Holds clinical responsibility')}</ul>
    </div>
    <div>
      <div style="{CAPS};font-size:19px;margin-bottom:6px">Optimal</div>
      <ul style="margin:0;padding:0;border-bottom:2px solid {LINE}">{duty('The introduction')}{duty('No HBOT screening', False)}{duty('No protocol management', False)}{duty('No results review', False)}</ul>
    </div>
  </div>
  {footer(right=900)}
</section>''')

# 10 ── What a session is like ─────────────────────────────────────────────────
def moment(n, title, body):
    return (f'<div style="border-top:2px solid {LINE};padding-top:30px">'
            f'<div style="{CAPS};color:{GREEN_DEEP}">{n}</div>'
            f'<h3 style="margin:18px 0 0;font-family:Castoro,serif;font-weight:400;font-size:38px;letter-spacing:-.02em;color:{INK}">{title}</h3>'
            f'<p style="margin:16px 0 0;{BODY};font-size:24px">{body}</p></div>')

slides.append(f'''<section data-label="What a session is like" data-speaker-notes="Walk a session end to end. Name the common, mild effects directly; less common effects are covered on the info call and at screening." style="{LIGHT}padding:88px 120px 130px;display:flex;flex-direction:column" class="sl">
  <div style="display:grid;grid-template-columns:1fr 720px;gap:100px;align-items:end">
    <div>
      <div style="{EYEBROW}">What to expect</div>
      <h2 style="{H2};font-size:88px">What a session is <em>like</em>.</h2>
    </div>
    <p style="{BODY};font-size:26px">HBOT is generally well tolerated. Every program begins with a medical screening, and the physician reviews your history before any session is booked.</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:repeat(4,1fr);gap:48px;align-content:center">
    {moment('Before', 'Arrival &amp; screening', 'Wear comfortable cotton clothing. You&rsquo;ll be checked for anything that shouldn&rsquo;t go into the chamber and briefed on how to equalize ear pressure.')}
    {moment('In the chamber', 'During the session', 'You rest, read, or listen to music while pressure is raised slowly. Most people feel only a fullness in the ears, like a flight or a dive.')}
    {moment('Good to know', 'Common, mild effects', 'Temporary ear or sinus pressure and lightheadedness are the most common. Less common effects, including temporary changes in near vision, are discussed on your call.')}
    {moment('After', 'Afterward', 'There&rsquo;s no downtime — you return to your day as normal. Your provider tracks how you tolerate each session across the series.')}
  </div>
  {footer()}
</section>''')

# 11 ── Who should not, or should wait ─────────────────────────────────────────
def item(text):
    return (f'<li style="display:flex;gap:18px;align-items:flex-start;border-top:2px solid {LINE};padding:26px 0;list-style:none">'
            f'{DASH.format(c=MUTED)}<span style="font-size:29px;line-height:1.45;color:{INK2}">{text}</span></li>')

slides.append(f'''<section data-label="Who should wait" data-speaker-notes="Screened for on every intake by the administering physician. The list is not complete; eligibility is the physician's call." style="{LIGHT}padding:88px 120px 130px;display:grid;grid-template-columns:640px 1fr;gap:120px;align-items:center" class="sl">
  <div>
    <div style="{EYEBROW};color:{MUTED}">Screened for on every intake</div>
    <h2 style="{H2};font-size:84px">Who should not — or should <em>wait</em>.</h2>
    <p style="margin:30px 0 0;font-size:26px;font-style:italic;color:{MUTED}">This is not a complete list.</p>
  </div>
  <ul style="margin:0;padding:0;border-bottom:2px solid {LINE}">
    {item('Untreated pneumothorax (collapsed lung) — a firm contraindication')}
    {item('Certain lung conditions, recent ear or sinus surgery, or active infection')}
    {item('Pregnancy, and some medications — reviewed individually with the physician')}
    {item('Claustrophobia or difficulty equalizing ear pressure — discussed before booking')}
  </ul>
  {footer()}
</section>''')

# 12 ── Where HBOT is an established treatment ─────────────────────────────────
def indication(text):
    return (f'<div style="border-top:2px solid {LINE};padding:28px 0 0">'
            f'<div style="font-family:Castoro,serif;font-size:40px;line-height:1.15;letter-spacing:-.02em;color:{INK}">{text}</div></div>')

slides.append(f'''<section data-label="Established treatment" data-speaker-notes="Context only: the recognized medical uses under UHMS guidelines. They are distinct from the wellness use we offer, and several are covered in the appropriate medical setting." style="{LIGHT}padding:88px 120px 130px;display:flex;flex-direction:column" class="sl">
  <div style="display:grid;grid-template-columns:1fr 760px;gap:100px;align-items:end">
    <div>
      <div style="{EYEBROW}">For context</div>
      <h2 style="{H2};font-size:84px">Where HBOT <em>is</em> an established treatment.</h2>
    </div>
    <p style="{BODY};font-size:26px">HBOT has recognized, evidence-based medical uses under clinical guidelines such as the Undersea and Hyperbaric Medical Society (UHMS) indications. These are distinct from the wellness use we offer, and several are covered in the appropriate medical setting.</p>
  </div>
  <div style="flex:1;display:grid;grid-template-columns:repeat(3,1fr);gap:20px 64px;align-content:center">
    {indication('Non-healing &amp; diabetic wounds')}
    {indication('Radiation tissue injury')}
    {indication('Carbon monoxide poisoning')}
    {indication('Decompression sickness')}
    {indication('Certain serious infections')}
    {indication('Compromised skin grafts &amp; flaps')}
  </div>
  {footer()}
</section>''')

# 13 ── What the research shows (evidence) ─────────────────────────────────────
def domain(n, title, refs):
    lis = ''.join(f'<li style="list-style:none;margin-top:10px;font-size:21px;line-height:1.4;color:{INK2}">{r}</li>' for r in refs)
    return (f'<div style="border-top:2px solid {LINE};padding:22px 0 18px">'
            f'<div style="display:flex;gap:18px;align-items:baseline"><span style="{CAPS};color:{GREEN_DEEP}">{n}</span>'
            f'<span style="font-family:Castoro,serif;font-size:32px;letter-spacing:-.015em;color:{INK}">{title}</span></div>'
            f'<ul style="margin:6px 0 0 0;padding:0 0 0 52px">{lis}</ul></div>')

slides.append(f'''<section data-label="What the research shows" data-speaker-notes="One mechanism underlies most of this research: the hyperoxic-hypoxic paradox. Every source is linked on our HBOT page; the QR code opens it." style="{LIGHT}padding:80px 120px 124px;display:grid;grid-template-columns:660px 1fr;gap:100px" class="sl">
  <div style="display:flex;flex-direction:column">
    <div style="{EYEBROW}">The evidence</div>
    <h2 style="{H2};font-size:76px">What the research {ring('shows', '-6px -20px')}.</h2>
    <p style="margin:26px 0 0;{BODY};font-size:23px">Most of the research rests on one mechanism, the hyperoxic-hypoxic paradox. Breathing oxygen under pressure and then returning to ordinary air, over and over, appears to trigger the same repair signals the body uses when oxygen runs short, without the shortage itself. Hadanny and Efrati set that mechanism out in <i>Biomolecules</i> in 2020.</p>
    <div style="margin-top:auto;display:flex;gap:28px;align-items:center;padding:24px;border:2px solid {LINE};border-radius:16px;background:#fff">
      <img src="assets/images/qr-evidence.svg" alt="QR code linking to every source on beoptimal.ca" style="width:160px;height:160px;flex:none" loading="eager" decoding="async">
      <div>
        <div style="{CAPS};color:{GREEN_DEEP}">Every source, linked</div>
        <div style="margin-top:10px;font-family:Castoro,serif;font-size:30px;line-height:1.2;color:{INK}">Scan to open the full reading list.</div>
        <div style="margin-top:10px;font-size:19px;color:{MUTED}">beoptimal.ca/services/hyperbaric-oxygen-therapy</div>
      </div>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:center;border-bottom:2px solid {LINE}">
    {domain('1', 'Cellular aging biomarkers', ['Hachmo Y, et al. (2020). <i>Aging (Albany NY)</i> 12(22) — telomere length &amp; immunosenescence', 'Hachmo Y, et al. (2021). <i>Aging (Albany NY)</i> 13(16) — telomeres &amp; DNA repair in aging adults'])}
    {domain('2', 'Tissue aging &amp; regeneration', ['Fischer I, et al. (2021). <i>Aging (Albany NY)</i> 13(18) — angiogenesis &amp; regeneration in human skin', 'Thom SR. (2011). <i>Plast Reconstr Surg</i> 127(Suppl 1) — mechanisms &amp; efficacy'])}
    {domain('3', 'Neurocognitive &amp; brain aging', ['Efrati S, et al. (2013). <i>J Neurotrauma</i> 30(3) — neuroplasticity in chronic deficits', 'Boussi-Gross R, et al. (2013). <i>PLoS ONE</i> 8(11) — post-concussion syndrome, RCT'])}
    {domain('4', 'Mitochondria &amp; oxidative signalling', ['Hadanny A, Efrati S. (2020). <i>Biomolecules</i> 10(6):958 — the hyperoxic-hypoxic paradox'])}
    {domain('5', 'Systematic reviews &amp; consensus', ['UHMS (2023). <i>Hyperbaric Oxygen Therapy Indications</i>, 15th Ed.', 'Clarke RE, et al. (2012). <i>Cochrane Database Syst Rev</i> CD004123'])}
  </div>
  {footer()}
</section>''')

# 14 ── Questions ──────────────────────────────────────────────────────────────
def qa(q, a):
    return (f'<div style="border-top:2px solid {LINE};padding-top:26px">'
            f'<h3 style="margin:0;font-family:Castoro,serif;font-weight:400;font-size:34px;line-height:1.2;letter-spacing:-.015em;color:{INK}">{q}</h3>'
            f'<p style="margin:14px 0 0;{BODY};font-size:23px">{a}</p></div>')

slides.append(f'''<section data-label="Questions" data-speaker-notes="The four questions patients ask most. The rest are on the HBOT page and the info call." style="{LIGHT}padding:84px 120px 124px;display:flex;flex-direction:column" class="sl">
  <div style="{EYEBROW}">Frequently asked</div>
  <h2 style="{H2};font-size:84px">Your {ring('questions', '-6px -24px')}, answered.</h2>
  <div style="flex:1;margin-top:20px;display:grid;grid-template-columns:1fr 1fr;gap:34px 96px;align-content:center">
    {qa('Is HBOT approved by Health Canada for longevity or anti-aging?', 'No. HBOT is approved by Health Canada for a defined set of medical conditions. Its use for aging, longevity, or general wellness is investigational and is not approved by Health Canada as a treatment for aging or disease prevention. We offer it as a private wellness service on that basis.')}
    {qa('Is this covered by OHIP or my insurance?', 'Not for this indication. Because it&rsquo;s offered as a longevity and wellness service — not an OHIP-eligible medical treatment — HBOT here is paid privately. Some employer Health Spending Accounts (HSA) may apply; we can discuss this on your info call.')}
    {qa('What protocol do you follow?', 'Our program is modelled on a published clinical protocol that uses intermittent oxygen breathing across a series of sessions. Exact parameters will be discussed and decided with the administering physician during your consultation.')}
    {qa('Will this make me live longer or reverse aging?', 'We can&rsquo;t say that, and we won&rsquo;t. Research has observed changes in some aging-associated biomarkers, but lifespan extension, disease prevention in healthy people, and reversal of biological aging have not been demonstrated as clinical outcomes.')}
  </div>
  {footer()}
</section>''')

# 15 ── Next steps ─────────────────────────────────────────────────────────────
def nxt(n, title, detail, last=False):
    bottom = f'border-bottom:2px solid {LINE};' if last else ''
    return (f'<div style="display:grid;grid-template-columns:100px 1fr 420px;align-items:center;border-top:2px solid {LINE};{bottom}padding:26px 0">'
            f'<div style="font-family:Castoro,serif;font-size:38px;color:{GREEN_DEEP}">{n}</div>'
            f'<div style="font-family:Castoro,serif;font-size:36px;letter-spacing:-.02em">{title}</div>'
            f'<div style="text-align:right;{CAPS}">{detail}</div></div>')

slides.append(f'''<section data-label="Next steps" data-speaker-notes="Close on the conversation, not a commitment. Info calls are booked with Peter. Invite questions; contact details are on screen." style="{LIGHT}padding:88px 120px 130px" class="sl">
  <div style="display:grid;grid-template-columns:1fr 620px;gap:90px;height:100%;box-sizing:border-box;align-items:stretch">
    <div style="display:flex;flex-direction:column;justify-content:center">
      <div style="{EYEBROW}">Next steps</div>
      <h2 style="{H2};font-size:80px">Curious whether HBOT is right for <em>you</em>?</h2>
      <p style="margin:26px 0 0;{BODY};font-size:26px;max-width:880px">Start with a conversation. No obligation, no pressure — just a clear look at the evidence and whether a program makes sense for you.</p>
      <div style="margin-top:40px">
        {nxt('01', 'Info call', 'No obligation')}
        {nxt('02', 'Medical screening', 'With the physician')}
        {nxt('03', 'Your program', 'A series over weeks', last=True)}
      </div>
      <p style="margin:26px 0 0;max-width:900px;font-size:19px;line-height:1.5;color:{MUTED}">Offered as an investigational longevity &amp; wellness service — not a Health Canada-approved treatment for aging, and not OHIP-covered. Treatment is delivered and administered by a physician (MD) at our partner hyperbaric clinic.</p>
    </div>
    <div style="background:linear-gradient(160deg,#2C4E25 0%,#1C3118 100%);color:#FFFCF7;border-radius:16px;padding:60px 54px;display:flex;flex-direction:column;margin:10px 0 40px;box-sizing:border-box;box-shadow:0 8px 48px rgba(0,0,0,.12)">
      <img src="assets/logos/symbol-white.png" alt="" style="height:42px;align-self:flex-start" loading="eager" decoding="async">
      <div style="margin-top:40px;font-family:Castoro,serif;font-size:62px;letter-spacing:-.03em"><em>Questions?</em></div>
      <p style="margin:18px 0 0;font-size:26px;line-height:1.5;color:rgba(255,252,247,.85)">We&rsquo;re happy to talk anything through — today or after you&rsquo;ve thought it over.</p>
      <div class="closing-export">
        <button type="button" class="export-cta" data-export-pdf>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
          Export as PDF
        </button>
      </div>
      <div style="margin-top:auto;border-top:1px solid rgba(255,252,247,.28);padding-top:34px;display:flex;flex-direction:column;gap:22px;font-size:28px">
        <div><span style="display:block;font-size:24px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,252,247,.6)">Call or text</span><span style="display:block;margin-top:8px">(437) 370-0291</span></div>
        <div><span style="display:block;font-size:24px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,252,247,.6)">Email</span><span style="display:block;margin-top:8px">care@beoptimal.ca</span></div>
        <div><span style="display:block;font-size:24px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,252,247,.6)">Web</span><span style="display:block;margin-top:8px">beoptimal.ca</span></div>
      </div>
    </div>
  </div>
  {footer()}
</section>''')

total = len(slides) + 1  # + the welcome screen, printed as 01
numbered = [s.replace('{N}', f'{i + 2:02d} / {total}') for i, s in enumerate(slides)]

# ── HBOT-only motion: the moving micrographs, pictograms, session schematic ────
HBOT_CSS = f'''<style>
  /* ==========================================================================
     HBOT deck motion. Same vocabulary as the house engine: one easing curve,
     no bounce, everything gated on .in-view so it replays on every visit.
     ========================================================================== */
  .hb-motion-wrap .hb-still, .hb-motion-wrap .hb-motion {{
    position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block;
  }}
  .hb-motion-wrap .hb-motion {{ opacity: 0; transition: opacity 900ms var(--deck-ease); }}
  .hb-motion-wrap .hb-motion.is-playing {{ opacity: 1; }}

  /* Photographs settle over the whole time a slide is up, slower than the house 6s. */
  deck-stage > section.in-view .hb-drift {{ animation: hb-drift 18s var(--deck-ease) both; }}
  @keyframes hb-drift {{ from {{ transform: scale(1.06); }} to {{ transform: scale(1); }} }}

  /* How it works: pressure rings close in on the chamber */
  .hb-picto {{ width: 100%; height: auto; display: block; overflow: visible; }}
  .hb-chamber .hb-press {{ transform-box: fill-box; transform-origin: center; opacity: 0; }}
  deck-stage > section.in-view .hb-chamber .hb-press {{ animation: hb-press 3.6s var(--deck-ease) infinite; }}
  deck-stage > section.in-view .hb-chamber .p2 {{ animation-delay: 1.2s; }}
  deck-stage > section.in-view .hb-chamber .p3 {{ animation-delay: 2.4s; }}
  @keyframes hb-press {{ 0% {{ opacity: 0; transform: scale(1.08); }} 30% {{ opacity: .9; }} 100% {{ opacity: 0; transform: scale(.45); }} }}

  /* ...oxygen streams into the vessel */
  .hb-oxygen .hb-o2 {{ opacity: 0; }}
  deck-stage > section.in-view .hb-oxygen .hb-o2 {{ animation: hb-flow 5s linear infinite; animation-delay: var(--d); }}
  @keyframes hb-flow {{ 0% {{ transform: translateX(calc(14px - var(--x))); opacity: 0; }} 12% {{ opacity: 1; }} 88% {{ opacity: 1; }} 100% {{ transform: translateX(calc(266px - var(--x))); opacity: 0; }} }}

  /* ...and sessions fill in, one after another */
  .hb-series .hb-dot {{ transition: fill .3s; }}
  deck-stage > section.in-view .hb-series .hb-dot {{ animation: hb-fill 6s var(--deck-ease) infinite; animation-delay: var(--d); }}
  @keyframes hb-fill {{ 0%, 6% {{ fill: {CREAM}; }} 14%, 82% {{ fill: {GREEN}; }} 100% {{ fill: {CREAM}; }} }}

  /* Inside the protocol: the session schematic builds left to right */
  .hb-wave .hb-o2bar, .hb-wave .hb-airbar {{ transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); }}
  deck-stage > section.in-view .hb-wave .hb-o2bar,
  deck-stage > section.in-view .hb-wave .hb-airbar {{ animation: hb-grow 700ms var(--deck-ease) both; animation-delay: var(--d); }}
  @keyframes hb-grow {{ from {{ transform: scaleY(0); }} to {{ transform: scaleY(1); }} }}
  .hb-wave .hb-ramp {{ opacity: 0; }}
  deck-stage > section.in-view .hb-wave .hb-ramp {{ animation: dk-fade 600ms ease .3s both; }}

  /* Who runs your sessions: duties tick in after the paragraphs */
  .hb-duty {{ opacity: 0; }}
  deck-stage > section.in-view .hb-duty {{ animation: dk-rise 520ms var(--deck-ease) both; }}
  {''.join(f'deck-stage > section.in-view ul > .hb-duty:nth-child({i}) {{ animation-delay: {0.9 + i * 0.12:.2f}s; }}' for i in range(1, 5))}

  @media print {{
    .hb-motion-wrap .hb-motion {{ display: none !important; }}
    .hb-wave .hb-o2bar, .hb-wave .hb-airbar, .hb-wave .hb-ramp, .hb-duty, .hb-chamber .hb-press, .hb-oxygen .hb-o2 {{
      animation: none !important; transform: none !important; opacity: 1 !important;
    }}
    .hb-drift {{ animation: none !important; transform: none !important; }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .hb-motion-wrap .hb-motion {{ display: none; }}
    .hb-drift, .hb-picto *, .hb-wave * {{ animation: none !important; transform: none !important; opacity: 1 !important; }}
    .hb-duty {{ animation: none !important; opacity: 1 !important; }}
  }}
</style>
'''

HBOT_JS = '''<script>
  /* ==========================================================================
     HBOT deck motion — micrograph loops play only on the slide that's up (one
     decoder at a time, and every visit starts on the still's exact frame), and
     the ~90 min stat counts up when the protocol slide arrives.
     ========================================================================== */
  (() => {
    const deck = document.querySelector('deck-stage');
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const videos = [...document.querySelectorAll('.hb-motion')];

    const stopAll = () => videos.forEach((v) => { v.pause(); v.classList.remove('is-playing'); });
    const startIn = (slide) => {
      if (reduce || !slide) return;
      slide.querySelectorAll('.hb-motion').forEach((v) => {
        try { v.currentTime = 0; } catch (e) {}
        const p = v.play();
        if (p && p.then) p.then(() => v.classList.add('is-playing')).catch(() => {});
        else v.classList.add('is-playing');
      });
    };

    const countUp = (slide) => {
      if (!slide) return;
      slide.querySelectorAll('.hb-count').forEach((el) => {
        const to = +el.dataset.to || 0;
        if (reduce) { el.textContent = to; return; }
        const t0 = performance.now(), dur = 1400;
        const ease = (t) => 1 - Math.pow(1 - t, 3);
        const tick = (now) => {
          const t = Math.min(1, (now - t0) / dur);
          el.textContent = Math.round(to * ease(t));
          if (t < 1) requestAnimationFrame(tick);
        };
        el.textContent = 0;
        setTimeout(() => requestAnimationFrame(tick), 500);
      });
    };

    deck.addEventListener('slidechange', (e) => { stopAll(); startIn(e.detail.slide); countUp(e.detail.slide); });
    // Cover screens hide slide 1, which holds no video; nothing to start here.
    window.addEventListener('beforeprint', stopAll);
  })();
</script>
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
              '<meta name="description" content="Patient presentation for hyperbaric oxygen therapy at Optimal Clinic, Barrie: how it works, the protocol, what the research explores and where it stands, who runs your sessions, what a session is like, and next steps.">', html, count=1)
sub1('<link rel="preload" as="image" href="assets/leaves-overhead.jpg">', '<link rel="preload" as="image" href="assets/images/chambers.webp">')
sub1('     Introductory Meeting — Optimal Clinic, Barrie\n', f'     {NAME} — Optimal Clinic, Barrie\n     Generated by hbot/tools/build_deck.py. Edit the script, not this file.\n')
html = re.sub(r'The \d+ slides below are the design handoff recreated verbatim',
              f'The {len(slides)} slides below are built from the beoptimal.ca HBOT page', html, count=1)
sub1("Slide copy is client-approved: change markup, not words.", "Slide copy mirrors the HBOT page: change it there first, then here.")

# Cover screens: the partner facility's chambers instead of the leaf canopy.
sub1("background: url('assets/leaves-overhead.jpg') center center / cover no-repeat;",
     "background: url('assets/images/chambers.webp') center 40% / cover no-repeat;")
sub1("""  /* Branded canopy backdrop — the Optimal wordmark is composited into the
     centre of this wallpaper, so the image itself is the brand mark. */""",
     """  /* Cover backdrop: the hyperbaric chambers at our partner facility. The photo
     is bright clinical white, so both washes below run darker than the decks
     that sit on the leaf canopy, and the wordmark is placed as its own layer. */""")
html = re.sub(r"(\.canopy::after \{\n\s*content: \"\"; position: absolute; inset: 0;\n\s*background: )radial-gradient\([^;]*\);",
              r"\1linear-gradient(180deg, rgba(11,22,8,.62) 0%, rgba(11,22,8,.70) 55%, rgba(9,17,7,.90) 100%);", html, count=1)
html = re.sub(r"(#welcome-screen::after \{\n\s*background: )linear-gradient\([^;]*\);",
              r"\1linear-gradient(180deg, rgba(11,22,8,.58) 0%, rgba(11,22,8,.42) 40%, rgba(11,22,8,.62) 70%, rgba(9,17,7,.92) 100%);", html, count=1)
sub1('  /* ── Welcome screen ── */', '''  /* ── Welcome screen ── */
  .welcome-mark {
    position: absolute; left: 50%; top: 40%; z-index: 1; height: 112px; width: auto;
    transform: translate(-50%, -50%); opacity: 0;
  }
  #welcome-screen.is-on .welcome-mark { animation: dk-fade 1.1s ease .2s both; }''')
sub1('<button type="button" id="welcome-back" class="welcome-back"><span class="arr">←</span> Edit name</button>',
     '<button type="button" id="welcome-back" class="welcome-back"><span class="arr">←</span> Edit name</button>\n      <img class="welcome-mark" src="assets/logos/Optimal-Logo-Inverted.png" alt="Optimal">')

sub1('<div class="prep-eyebrow">Introductory Meeting · Preparation</div>', '<div class="prep-eyebrow">Hyperbaric Oxygen Therapy · Preparation</div>')
sub1("Let's set up <em>this meeting</em>.", "Let's set up <em>this briefing</em>.")
sub1('<span class="field-label">Date of meeting</span>', '<span class="field-label">Date</span>')
sub1("'Optimal — Introductory Meeting — '", f"'Optimal — {NAME} — '")
html = re.sub(r'the welcome screen is 01 of the printed \d+ but', f'the welcome screen is 01 of the printed {total} but', html)
html = re.sub(r'printed "02 / \d+"', f'printed "02 / {total}"', html)

sub1('</head>', HBOT_CSS + '</head>')
idx = html.rindex('</body>')
html = html[:idx] + HBOT_JS + html[idx:]

assert 'Introductory' not in html
assert 'leaves-overhead' not in html
for banned in ('Sagol', 'Shamir', 'Israel', 'honest', 'yourself'):
    assert banned.lower() not in html.lower(), f'"{banned}" is off the page; keep it off the deck'
OUT.write_text(html)
print(f'wrote {OUT.relative_to(ROOT)}: {len(slides)} slides, printed /{total}')
