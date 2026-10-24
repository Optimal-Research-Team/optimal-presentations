// The 3-D hypothalamus has ONE master copy: optimal-anatomy-figures/figures/a2-hypothalamus (A2's model.mjs and
// gl/hypo3d-*.js). This deck keeps only its own wrapper (src/hypo3d.src.js, the <hypo-3d> element: slide
// play/pause, the tour, print snapshots) and src/hypo3d-stages.js (the stage readouts its lab page shows).
//
//   node tools/sync-hypo3d.mjs           copy the master files into src/a2/ and record them in src/a2/SOURCE.json
//   node tools/sync-hypo3d.mjs --check   fail if src/a2/ differs from SOURCE.json (someone edited a copy here)
//
// Fix or improve the 3-D brain in the anatomy repo, never in src/a2/. Then run this, then tools/build-hypo3d.sh
// (which runs --check first). FIGURES_DIR overrides where the anatomy repo is (default: next to this repo).
import { createHash } from "node:crypto";
import { execSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROUTE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const DEST = join(ROUTE, "src", "a2");
const FIGURES = process.env.FIGURES_DIR || resolve(ROUTE, "../../../optimal-anatomy-figures");
const A2 = join(FIGURES, "figures", "a2-hypothalamus");
// The same relative layout as the master, so the files' own imports ("../model.mjs", "./hypo3d-*.js") work unchanged.
const FILES = ["model.mjs", "gl/hypo3d-model.js", "gl/hypo3d-anatomy.js", "gl/hypo3d-geo.js", "gl/hypo3d-scene.js"];
const sha = (buf) => createHash("sha256").update(buf).digest("hex").slice(0, 16);

if (process.argv.includes("--check")) {
  const src = JSON.parse(readFileSync(join(DEST, "SOURCE.json"), "utf8"));
  const bad = FILES.filter((f) => !existsSync(join(DEST, f)) || sha(readFileSync(join(DEST, f))) !== src.files[f]);
  if (bad.length) {
    console.error(`sync-hypo3d: these copies were edited in the deck (or are missing): ${bad.join(", ")}.`);
    console.error("Make the change in optimal-anatomy-figures/figures/a2-hypothalamus, then run: node tools/sync-hypo3d.mjs");
    process.exit(1);
  }
  console.log(`sync-hypo3d: src/a2 matches anatomy-figures ${src.commit} (${FILES.length} files)`);
  process.exit(0);
}

if (!existsSync(A2)) {
  console.error(`sync-hypo3d: no anatomy-figures checkout at ${FIGURES} (set FIGURES_DIR).`);
  process.exit(1);
}
let commit = "unknown";
let dirty = false;
try {
  commit = execSync("git rev-parse --short HEAD", { cwd: FIGURES }).toString().trim();
  dirty = execSync(`git status --porcelain -- ${FILES.map((f) => `figures/a2-hypothalamus/${f}`).join(" ")}`, { cwd: FIGURES }).toString().trim().length > 0;
} catch {}
const files = {};
for (const f of FILES) {
  const body = readFileSync(join(A2, f));
  mkdirSync(dirname(join(DEST, f)), { recursive: true });
  writeFileSync(join(DEST, f), body);
  files[f] = sha(body);
}
writeFileSync(
  join(DEST, "SOURCE.json"),
  JSON.stringify(
    {
      note: "Copies of the 3-D hypothalamus's master files. Do not edit here: change them in the anatomy repo, then run node tools/sync-hypo3d.mjs.",
      source: "Optimal-Research-Team/optimal-anatomy-figures/figures/a2-hypothalamus",
      commit,
      dirty,
      syncedAt: new Date().toISOString(),
      files,
    },
    null,
    2,
  ) + "\n",
);
console.log(`sync-hypo3d: ${FILES.length} files from anatomy-figures ${commit}${dirty ? " (uncommitted changes there)" : ""} → src/a2/`);
