<!-- ===========================================================================
     AUTO-RENEW TAG — script. Paste this whole <script> block just before
     </body> in index.html, AFTER the <deck-stage> markup and after
     deck-stage.js has loaded (it already is, if you paste before </body>).

     It listens for the slidechange event every Optimal deck's deck-stage.js
     dispatches, and replays the tag's entrance each time its slide becomes
     active. It touches nothing but elements with class dk-tag.
     =========================================================================== -->
<script>
  (() => {
    const deck = document.querySelector('deck-stage');
    if (!deck) return;
    const arm = (slide) => {
      if (!slide) return;
      slide.querySelectorAll('.dk-tag').forEach((tag) => {
        tag.classList.remove('is-in');
        void tag.offsetWidth;            // force reflow so the animation restarts
        tag.classList.add('is-in');
      });
    };
    deck.addEventListener('slidechange', (e) => arm(e.detail && e.detail.slide));
    // The deck may have initialised before this ran; arm the current slide too.
    arm(deck.querySelector(':scope > section[data-deck-active]'));
  })();
</script>
