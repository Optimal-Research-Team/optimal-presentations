// <hypo-3d> stages: the deck's names for A2's four states, with the readouts its lab page shows.
// The numbers come from the master model (src/a2, synced from optimal-anatomy-figures; see tools/sync-hypo3d.mjs):
// each stage's estrogen target and receptor blocker are A2's STAGES, and the cell size is A2's kndyOf().
// The readout words, the hot-flash rates and the lines are A2's live.js setState() and build.mjs, as before.
import { STAGES as A2_STAGES, kndyOf } from "./a2/gl/hypo3d-model.js";

export const STAGE_ORDER = ["before", "after", "therapy", "nonhormonal"];
// Hot-flash rate readout = Fig 1's rateOf(e) as A2's build.mjs passes it in (DATA.rate):
// rateOf(1) ≈ 4.8e-12 (prints "Rare"), rateOf(0) = 1.1 per hour [Meldrum 1979; Freedman 1998; Low 2008].
const RATE = [4.807038969646711e-12, 1.1];
// A2 build.mjs LINES (the scene line under the figure), verbatim.
const LINES = [
  "Before menopause: estrogen keeps the KNDy cells small and their signal modest. The heat-loss centre idles, and everyday wanders in body heat pass unnoticed.",
  "After menopause: with little estrogen, the cells swell and send neurokinin B more often. The heat-loss centre runs close to its edge, and a small wander tips it into a hot flash.",
  "Hormone therapy, where it suits: estrogen is replaced, the KNDy cells quieten, and the heat-loss centre moves back from its edge.",
  "A non-hormonal prescription option: the cells still signal, but a neurokinin-receptor blocker stops the heat-loss centre from receiving it.",
];
/**
 * Per-stage readouts, computed exactly as A2 live.js setState(i) computes its three stat cells:
 *   estrogen   = ["Cycling", "Low", "Replaced", "Low"][i]
 *   kndySize   = i === 2 ? "Smaller" : `${Math.round(100 * kndyOf(target).area)}%`
 *   hotFlashes = i < 2 ? (rate[i] < 0.05 ? "Rare" : `≈ ${rate[i].toFixed(1)} an hour`) : "Fewer, typically"
 */
export const STAGES = Object.freeze(
  Object.fromEntries(
    STAGE_ORDER.map((name, i) => {
      const { e, blocked } = A2_STAGES[i];
      const s = kndyOf(e);
      return [
        name,
        Object.freeze({
          index: i,
          e,
          blocked,
          estrogen: ["Cycling", "Low", "Replaced", "Low"][i],
          kndySize: i === 2 ? "Smaller" : `${Math.round(100 * s.area)}%`,
          hotFlashes: i < 2 ? (RATE[i] < 0.05 ? "Rare" : `≈ ${RATE[i].toFixed(1)} an hour`) : "Fewer, typically",
          line: LINES[i],
        }),
      ];
    }),
  ),
);
