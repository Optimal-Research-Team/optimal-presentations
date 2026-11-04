"""What every educational talk shares on top of the chrome copied from ../intro/index.html.

Each talk's build script calls apply(html) after it has spliced in its slides. Generated decks
stay self-contained: this file is only read at build time.

  1. No foliage. The patient decks' leaf wallpaper doesn't appear on talks, so the set-up and
     welcome screens sit on the same forest field as the part dividers.
  2. The motion layer: a true crossfade between slides, headlines that come into focus word by
     word, hairlines that draw, numbers that count, and engravings that ink in. The tools are
     utility classes (.ir-*) that a slide's own diagrams can use. Print and reduced motion
     always show the finished state.
"""
import re

COVER_CSS = '''<style>
  /* ==========================================================================
     TALK COVER SCREENS: flat forest, type and hairlines. No wallpaper.
     ========================================================================== */
  /* The field sits on the full window, so a screen that isn't 16:9 shows no edge. */
  #cover-stage { background: linear-gradient(135deg, #2C4E25 0%, #1C3118 100%); }
  .cover-field { background: none; overflow: visible; }
  /* The only thing that moves at rest: a slow, very soft light across the field. */
  .cover-field::before {
    content: ""; position: absolute; inset: -30%; pointer-events: none;
    background: radial-gradient(38% 38% at 34% 34%, rgba(135,164,130,.2), rgba(135,164,130,0) 72%);
    animation: cover-light 28s ease-in-out infinite alternate;
  }
  @keyframes cover-light {
    from { transform: translate3d(-5%, -4%, 0); }
    to   { transform: translate3d(16%, 14%, 0); }
  }

  /* Back links line up with the slides' 120px margin */
  .all-decks, .welcome-back {
    top: 52px; left: 120px; padding: 0; gap: 10px;
    font-size: 19px; color: rgba(255,252,247,.72);
    background: none; border: 0; border-radius: 0;
    -webkit-backdrop-filter: none; backdrop-filter: none;
  }
  .all-decks:hover, .all-decks:focus-visible, .welcome-back:hover {
    background: none; color: #FFFCF7; border: 0;
  }
  .all-decks svg { width: 20px; height: 20px; transition: transform .2s var(--deck-ease); }
  .all-decks:hover svg { transform: translateX(-3px); }
  .welcome-back .arr { font-size: 20px; }

  /* Set-up: the headline on the left, the form on the right */
  .prep-card .opt-logo { position: absolute; top: 44px; right: 120px; height: 44px; margin: 0; z-index: 2; }
  .prep-eyebrow { font-size: 22px; font-weight: 600; letter-spacing: .24em; color: rgba(255,252,247,.66); margin-bottom: 30px; }
  .prep-title { font-size: 124px; line-height: 1.02; letter-spacing: -.04em; color: #FFFCF7; margin-bottom: 36px; text-wrap: balance; }
  .prep-title em { color: #DDE7D2; }
  .prep-sub { font-size: 28px; line-height: 1.48; letter-spacing: -.01em; color: rgba(255,252,247,.76); margin: 0; max-width: 31em; text-wrap: pretty; }
  .prep-form { gap: 46px; }
  .prep-form .field { gap: 8px; }
  .prep-form .field-label { font-size: 17px; font-weight: 600; letter-spacing: .2em; color: rgba(255,252,247,.66); }
  .prep-form input, .prep-form .field--date input {
    background: none; border: 0; border-bottom: 2px solid rgba(255,252,247,.3); border-radius: 0;
    padding: 10px 0 16px; max-width: none; color: #FFFCF7;
  }
  .prep-form input { font-size: 48px; letter-spacing: -.02em; }
  .prep-form .field--date input { font-size: 30px; letter-spacing: -.01em; }
  .prep-form input::placeholder { color: rgba(255,252,247,.46); }
  .prep-form input:focus { background: none; border-bottom-color: #FFFCF7; box-shadow: none; }
  .prep-actions { gap: 14px; margin-top: 18px; flex-wrap: nowrap; }
  .prep-btn { font-size: 19px; padding: 18px 30px; white-space: nowrap; }
  .prep-btn.ghost { border-color: rgba(255,252,247,.34); color: rgba(255,252,247,.9); }
  .prep-btn:focus-visible, .welcome-begin:focus-visible, .all-decks:focus-visible, .welcome-back:focus-visible {
    outline: 3px solid #DDE7D2; outline-offset: 4px;
  }
  .prep-card > *:nth-child(2) { animation-delay: .12s; }
  .prep-card > *:nth-child(3) { animation-delay: .26s; }
  .prep-card .opt-logo { animation: dk-fade .8s ease .1s both; }

  /* Welcome: the logo the wallpaper used to carry, then the greeting */
  #welcome-screen { align-items: center; }
  .welcome-inner { padding: 0 120px; text-shadow: none; }
  .welcome-logo { display: block; height: 62px; width: auto; margin: 0 auto 76px; }
  .welcome-title { font-size: 172px; line-height: 1; letter-spacing: -.045em; color: #FFFCF7; text-wrap: balance; }
  .welcome-name { color: #DDE7D2; }
  .welcome-meta { font-size: 27px; letter-spacing: -.01em; color: rgba(255,252,247,.74); margin-top: 40px; }
  .welcome-begin { margin-top: 60px; font-size: 22px; padding: 20px 44px; }
  .welcome-hint { margin-top: 34px; font-size: 15px; color: rgba(255,252,247,.6); }
  #welcome-screen.is-on .welcome-inner > *:nth-child(1) { animation-delay: .25s; }
  #welcome-screen.is-on .welcome-inner > *:nth-child(2) { animation-delay: .42s; }
  #welcome-screen.is-on .welcome-inner > *:nth-child(3) { animation-delay: .62s; }
  #welcome-screen.is-on .welcome-inner > *:nth-child(4) { animation-delay: .76s; }
  #welcome-screen.is-on .welcome-inner > *:nth-child(5) { animation-delay: .9s; }

  @media print {
    #welcome-screen {
      background: linear-gradient(135deg, #2C4E25 0%, #1C3118 100%) !important;
      -webkit-print-color-adjust: exact; print-color-adjust: exact;
    }
    .cover-field::before { display: none !important; }
  }
  @media (prefers-reduced-motion: reduce) {
    .cover-field::before { animation: none; }
  }
</style>
'''

MOTION_CSS = '''<style>
  /* ==========================================================================
     TALK TYPE AND MOTION. One easing curve, no bounce. Everything is gated on
     .in-view, so it replays on every visit.
     ========================================================================== */
  deck-stage > section {
    font-kerning: normal; font-feature-settings: "kern", "liga", "calt";
    text-rendering: geometricPrecision; -webkit-font-smoothing: antialiased;
    text-wrap: pretty;
  }
  deck-stage > section :is(h1, h2) { text-wrap: balance; }
  .ir-tnum { font-variant-numeric: tabular-nums lining-nums; }

  /* Between slides: the new slide fades in over the old one, which holds at full
     strength underneath. No dip through the black stage. */
  deck-stage > section { transition: opacity 0s linear 460ms, visibility 0s linear 460ms; z-index: 0; }
  deck-stage > section[data-deck-active] { transition: opacity 440ms var(--deck-ease), visibility 0s; z-index: 1; }

  /* Content blocks: a longer, softer rise than the house default */
  deck-stage > section.in-view .dk-rv {
    animation: ir-rise 760ms var(--deck-ease) both;
    animation-delay: calc(var(--rv, 0) * 72ms + 70ms);
  }
  @keyframes ir-rise {
    from { opacity: 0; transform: translate3d(0, 26px, 0); }
    to   { opacity: 1; transform: none; }
  }

  /* Headlines come into focus word by word */
  .ir-w { opacity: 0; filter: blur(10px); }
  deck-stage > section.in-view .ir-w {
    animation: ir-word 780ms var(--deck-ease) both;
    animation-delay: calc(var(--rv, 0) * 72ms + 90ms + var(--i) * 46ms);
  }
  @keyframes ir-word {
    from { opacity: 0; filter: blur(10px); }
    to   { opacity: 1; filter: blur(0); }
  }

  /* Hairlines draw left to right. The real border goes transparent and keeps the
     layout; a pseudo-element paints over it. */
  .ir-rt::before, .ir-rb::after {
    content: ""; position: absolute; left: 0; right: 0; pointer-events: none;
    transform: scaleX(0); transform-origin: left center;
  }
  .ir-rt::before { top: calc(-1 * var(--rt-w)); height: var(--rt-w); background: var(--rt-c); }
  .ir-rb::after { bottom: calc(-1 * var(--rb-w)); height: var(--rb-w); background: var(--rb-c); }
  deck-stage > section.in-view .ir-rt::before,
  deck-stage > section.in-view .ir-rb::after { animation: ir-grow 980ms var(--deck-ease) var(--rd, .1s) both; }

  /* The design system's ring is drawn, not faded */
  @property --ring-a { syntax: '<angle>'; inherits: false; initial-value: 360deg; }
  deck-stage > section .dk-ring {
    opacity: 1; --ring-a: 0deg;
    -webkit-mask: conic-gradient(from -80deg, #000 var(--ring-a), transparent 0);
    mask: conic-gradient(from -80deg, #000 var(--ring-a), transparent 0);
  }
  deck-stage > section.in-view .dk-ring { animation: ir-ring 1100ms var(--deck-ease) var(--ring-d, 950ms) both; }
  @keyframes ir-ring { from { --ring-a: 0deg; } to { --ring-a: 360deg; } }

  /* Engravings ink in along a soft diagonal */
  .ir-ink {
    -webkit-mask: linear-gradient(var(--ang, 105deg), #000 43%, transparent 57%) 100% 0 / 340% 100% no-repeat;
    mask: linear-gradient(var(--ang, 105deg), #000 43%, transparent 57%) 100% 0 / 340% 100% no-repeat;
  }
  deck-stage > section.in-view .ir-ink { animation: ir-ink var(--dur, 1500ms) var(--deck-ease) var(--d, .2s) both; }
  @keyframes ir-ink {
    from { -webkit-mask-position: 100% 0; mask-position: 100% 0; }
    to   { -webkit-mask-position: 0 0; mask-position: 0 0; }
  }

  /* A round field opens like a microscope iris and pulls into focus */
  .ir-iris { clip-path: circle(0% at 50% 50%); }
  deck-stage > section.in-view .ir-iris { animation: ir-iris 1700ms var(--deck-ease) .25s both; }
  @keyframes ir-iris {
    from { clip-path: circle(0% at 50% 50%); filter: blur(16px); transform: scale(1.1); }
    55%  { filter: blur(4px); }
    to   { clip-path: circle(72% at 50% 50%); filter: blur(0); transform: none; }
  }

  /* Diagram tools. --d is the delay, --dur the duration where it varies. */
  .ir-build { opacity: 0; }
  deck-stage > section.in-view .ir-build { animation: ir-rise 700ms var(--deck-ease) var(--d, 0s) both; }

  .ir-fade { opacity: 0; }
  deck-stage > section.in-view .ir-fade { animation: dk-fade 800ms ease var(--d, 0s) both; }

  .ir-pop { opacity: 0; transform: scale(.72); transform-box: fill-box; transform-origin: center; }
  deck-stage > section.in-view .ir-pop { animation: ir-pop 680ms var(--deck-ease) var(--d, 0s) both; }
  @keyframes ir-pop { from { opacity: 0; transform: scale(.72); } to { opacity: 1; transform: none; } }

  .ir-tier { opacity: 0; transform: scale(.88, .8); transform-box: fill-box; transform-origin: center bottom; }
  deck-stage > section.in-view .ir-tier { animation: ir-tier 760ms var(--deck-ease) var(--d, 0s) both; }
  @keyframes ir-tier { from { opacity: 0; transform: scale(.88, .8); } to { opacity: 1; transform: none; } }

  .ir-spread { transform: scaleX(0); transform-box: fill-box; transform-origin: center; }
  deck-stage > section.in-view .ir-spread { animation: ir-grow 800ms var(--deck-ease) var(--d, 0s) both; }

  .ir-wipe { clip-path: inset(-4% 100% -4% 0); }
  deck-stage > section.in-view .ir-wipe { animation: ir-wipe var(--dur, 1500ms) var(--deck-ease) var(--d, .3s) both; }
  @keyframes ir-wipe { from { clip-path: inset(-4% 100% -4% 0); } to { clip-path: inset(-4% 0 -4% 0); } }

  .ir-draw { stroke-dasharray: 1; stroke-dashoffset: 1; }
  deck-stage > section.in-view .ir-draw { animation: ir-draw var(--dur, 1500ms) var(--deck-ease) var(--d, .3s) both; }
  @keyframes ir-draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }

  /* The pen tip rides a curve as it draws, on the same clock, then lifts */
  .ir-ride { opacity: 0; offset-rotate: 0deg; offset-distance: 0%; }
  deck-stage > section.in-view .ir-ride { animation: ir-ride var(--dur, 1500ms) var(--deck-ease) var(--d, .3s) both; }
  @keyframes ir-ride {
    0%   { offset-distance: 0%; opacity: 0; }
    8%   { opacity: 1; }
    82%  { opacity: 1; }
    100% { offset-distance: 100%; opacity: 0; }
  }

  .ir-bar, .ir-grow, .ir-seg { transform: scaleX(0); transform-origin: left center; transform-box: fill-box; }
  .ir-bar { transform-box: border-box; }
  deck-stage > section.in-view .ir-bar,
  deck-stage > section.in-view .ir-grow { animation: ir-grow 980ms var(--deck-ease) var(--d, .45s) both; }
  deck-stage > section.in-view .ir-seg { animation: ir-grow 640ms var(--deck-ease) var(--d, 0s) both; }
  @keyframes ir-grow { from { transform: scaleX(0); } to { transform: none; } }

  /* Attention narrows: the rest of a diagram steps back from what we're zooming into */
  deck-stage > section.in-view .ir-dim { animation: ir-dim 900ms ease var(--dd, 2.1s) both; }
  @keyframes ir-dim { from { opacity: 1; } to { opacity: .44; } }

  /* Where we are in the talk: a hairline along the bottom edge */
  .ir-prog {
    position: absolute; left: 0; right: 0; bottom: 0; height: 5px; pointer-events: none;
    background: #2C4E25; transform-origin: left center; transform: scaleX(var(--to));
  }
  .sl-dark .ir-prog { background: rgba(255,252,247,.55); }
  deck-stage > section.in-view .ir-prog { animation: ir-prog 760ms var(--deck-ease) both; }
  @keyframes ir-prog { from { transform: scaleX(var(--from)); } to { transform: scaleX(var(--to)); } }

  @media print {
    .ir-prog { display: none !important; }
    .ir-ride { display: none !important; }
    .ir-rt { border-top-color: var(--rt-c) !important; }
    .ir-rb { border-bottom-color: var(--rb-c) !important; }
    .ir-rt::before, .ir-rb::after { display: none !important; }
  }
  @media print, (prefers-reduced-motion: reduce) {
    .ir-w, .ir-build, .ir-fade, .ir-pop, .ir-tier, .ir-spread, .ir-wipe, .ir-ink, .ir-iris,
    .ir-bar, .ir-grow, .ir-seg, .ir-dim {
      animation: none !important; opacity: 1 !important; transform: none !important;
      filter: none !important; clip-path: none !important; -webkit-mask: none !important; mask: none !important;
    }
    .ir-draw { animation: none !important; stroke-dashoffset: 0 !important; }
    deck-stage > section .dk-ring { -webkit-mask: none !important; mask: none !important; animation: none !important; }
  }
  @media (prefers-reduced-motion: reduce) {
    .ir-ride { display: none !important; }
    .ir-prog { animation: none !important; }
    .ir-rt::before, .ir-rb::after { animation: none !important; transform: none !important; }
    deck-stage > section { transition: none !important; }
  }
</style>
'''

MOTION_JS = '''<script>
  /* ==========================================================================
     Talk motion: tags the slides once at load, then runs the count-ups.
     ========================================================================== */
  (() => {
    const deck = document.querySelector('deck-stage');
    const slides = [...document.querySelectorAll('deck-stage > section')];
    const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const PLAIN = new Set(['ir-num', 'ir-tnum', 'ir-cite']);

    // A diagram part animates on its own clock, so the structural reveal leaves it alone.
    document.querySelectorAll('.dk-rv').forEach((el) => {
      if ([...el.classList].some((c) => c.startsWith('ir-') && !PLAIN.has(c))) el.classList.remove('dk-rv');
    });

    // Headlines: wrap each word so it can come into focus on its own.
    const splitWords = (head) => {
      let i = 0;
      const walk = (node) => [...node.childNodes].forEach((n) => {
        if (n.nodeType === 1) {
          if (!n.classList.contains('dk-ring')) walk(n);
        } else if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\\s+)/).forEach((t) => {
            if (!t) return;
            if (!t.trim()) { frag.append(t); return; }
            const w = document.createElement('span');
            w.className = 'ir-w';
            w.style.setProperty('--i', i++);
            w.textContent = t;
            frag.append(w);
          });
          n.replaceWith(frag);
        }
      });
      walk(head);
    };
    document.querySelectorAll('deck-stage > section :is(h1, h2, [data-words])').forEach(splitWords);

    slides.forEach((slide, idx) => {
      // Hairlines: every inline top or bottom rule draws, in reading order.
      let order = 0;
      slide.querySelectorAll('[style*="border-top:"], [style*="border-bottom:"]').forEach((el) => {
        if (el.closest('.dk-footer')) return;
        const cs = getComputedStyle(el);
        const delay = `${(0.08 + Math.min(order++, 16) * 0.05).toFixed(2)}s`;
        if (cs.position === 'static') el.style.position = 'relative';
        el.style.setProperty('--rd', delay);
        if (el.style.borderTopStyle === 'solid') {
          el.style.setProperty('--rt-w', cs.borderTopWidth);
          el.style.setProperty('--rt-c', cs.borderTopColor);
          el.style.borderTopColor = 'transparent';
          el.classList.add('ir-rt');
        }
        if (el.style.borderBottomStyle === 'solid') {
          el.style.setProperty('--rb-w', cs.borderBottomWidth);
          el.style.setProperty('--rb-c', cs.borderBottomColor);
          el.style.borderBottomColor = 'transparent';
          el.classList.add('ir-rb');
        }
      });

      // Progress: the welcome screen is printed page 1, so this slide is page idx + 2.
      const pages = slides.length + 1;
      const bar = document.createElement('div');
      bar.className = 'ir-prog';
      bar.setAttribute('aria-hidden', 'true');
      bar.style.setProperty('--from', ((idx + 1) / pages).toFixed(4));
      bar.style.setProperty('--to', ((idx + 2) / pages).toFixed(4));
      slide.append(bar);
    });

    // Count-ups. The markup holds the real value, so print and no-JS are always right.
    const nums = [...document.querySelectorAll('.ir-num')].map((el) => {
      const node = [...el.childNodes].find((n) => n.nodeType === 3 && /\\d/.test(n.textContent));
      const final = node.textContent;
      const m = final.match(/\\d+(?:\\.\\d+)?/);
      return {
        el, node, final,
        to: parseFloat(m[0]),
        from: parseFloat(el.dataset.from || 0),
        dec: (m[0].split('.')[1] || '').length,
        pre: final.slice(0, m.index),
        post: final.slice(m.index + m[0].length),
        delay: parseFloat(el.dataset.delay || 650),
        slide: el.closest('section'),
      };
    });
    let frame = 0;
    const finishAll = () => {
      cancelAnimationFrame(frame);
      nums.forEach((n) => { n.node.textContent = n.final; });
    };
    const ease = (t) => 1 - Math.pow(1 - t, 3.4);
    const count = (slide) => {
      finishAll();
      if (calm || !slide) return;
      const live = nums.filter((n) => n.slide === slide);
      if (!live.length) return;
      live.forEach((n) => { n.node.textContent = n.pre + n.from.toFixed(n.dec) + n.post; });
      const start = performance.now();
      const tick = (now) => {
        let running = false;
        live.forEach((n) => {
          const t = Math.min(Math.max((now - start - n.delay) / 1150, 0), 1);
          if (t < 1) running = true;
          n.node.textContent = n.pre + (n.from + (n.to - n.from) * ease(t)).toFixed(n.dec) + n.post;
          if (t === 1) n.node.textContent = n.final;
        });
        if (running) frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);
    };

    deck.addEventListener('slidechange', (e) => count(e.detail.slide));
    window.addEventListener('beforeprint', finishAll);
    const replayActive = window.__replayActiveSlide;
    window.__replayActiveSlide = () => {
      replayActive();
      count(document.querySelector('deck-stage > section[data-deck-active]'));
    };
  })();
</script>
'''


def _swap(html, old, new):
    assert old in html, f'chrome changed, update talk_chrome.py: {old[:70]}'
    return html.replace(old, new, 1)


def apply(html):
    # ── 1. Take the foliage out ────────────────────────────────────────────────
    html = _swap(html, '<link rel="preload" as="image" href="assets/leaves-overhead.jpg">\n', '')
    html, n = re.subn(r'  /\* Branded canopy backdrop.*?(?=  /\* ── Preparation card)', '', html, count=1, flags=re.S)
    assert n == 1, 'canopy backdrop block not found'
    html = _swap(html, '    .canopy::before { animation: none !important; transform: scale(1) !important; }\n', '')
    html = _swap(html, '    .canopy::before { animation: none; transform: scale(1); }\n', '')
    html, n = re.subn(r'  /\* ── Preparation card \(glass over the canopy\) ── \*/\n  \.prep-card \{.*?\n  \}\n',
                      '  /* ── Preparation: flat on the forest field ── */\n'
                      '  .prep-card {\n'
                      '    position: static; z-index: 1; width: 1680px;\n'
                      '    display: grid; grid-template-columns: 1fr 720px; column-gap: 110px; align-items: center;\n'
                      '  }\n', html, count=1, flags=re.S)
    assert n == 1, 'prep card block not found'
    html = html.replace('.canopy', '.cover-field').replace('class="canopy"', 'class="cover-field"')
    html = _swap(html, '<div class="welcome-inner">\n',
                 '<div class="welcome-inner">\n        <img class="welcome-logo" src="assets/logos/Optimal-Logo-Inverted.png" alt="Optimal">\n')
    assert 'canopy' not in html and 'leaves-overhead' not in html, 'foliage left behind'

    # ── 2. Engine patches ──────────────────────────────────────────────────────
    # A diagram is one thing: the structural reveal stops at the svg.
    html = _swap(html, '      while (guard++ < 4) {\n',
                 "      while (guard++ < 4 && cur.tagName.toLowerCase() !== 'svg') {\n")
    html = _swap(html, '      return (kids.length >= 2 && kids.length <= 9) ? kids : [u];',
                 "      return (kids.length >= 2 && kids.length <= 9 && u.tagName.toLowerCase() !== 'svg') ? kids : [u];")
    # Replaying a slide restarts everything on it, not only the house reveal classes.
    html = _swap(html, '    const replay = (slide) => {\n',
                 "    const replay = (slide) => {\n      slide.classList.remove('in-view');\n      void slide.offsetWidth;\n")
    # The outgoing slide holds its finished state while the new one fades in over it.
    html = _swap(html,
                 "      document.querySelectorAll('deck-stage > section').forEach((s) => s.classList.remove('in-view'));\n"
                 "      if (e.detail.slide) replay(e.detail.slide);\n",
                 "      const out = e.detail.previousSlide;\n"
                 "      document.querySelectorAll('deck-stage > section').forEach((s) => { if (s !== out) s.classList.remove('in-view'); });\n"
                 "      if (e.detail.slide) replay(e.detail.slide);\n"
                 "      if (out && out !== e.detail.slide) setTimeout(() => { if (!out.hasAttribute('data-deck-active')) out.classList.remove('in-view'); }, 480);\n")

    html = _swap(html, '</head>', COVER_CSS + MOTION_CSS + '</head>')
    html = _swap(html, '</body>', MOTION_JS + '</body>')
    return html
