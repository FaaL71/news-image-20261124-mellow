// The Day in the World — 24 November 2026 world news in one image.
// Entry point for the make.fun program/v1 entry: it copies the pre-rendered
// front page (entry.png, drawn at build time by draw.py) into the output
// directory. Node 22, standard library only, no network, no randomness.
// draw.py is the build-time script only and is never run here: the grader
// mounts the repository read-only, so regenerating the image at grade time
// cannot work.
import { copyFileSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const SOURCE_NAME = "entry.png";

const repoRoot = path.dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? process.argv[2] ?? "/output";

mkdirSync(outDir, { recursive: true });
// Clean only the contents inside outDir, never outDir itself.
for (const name of readdirSync(outDir)) {
  rmSync(path.join(outDir, name), { recursive: true, force: true });
}

const source = path.join(repoRoot, SOURCE_NAME);
const bytes = readFileSync(source);
if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error(`${SOURCE_NAME} is not a PNG file`);
}
const target = path.join(outDir, SOURCE_NAME);
copyFileSync(source, target);
const copied = statSync(target);
if (copied.size !== bytes.length) {
  throw new Error(`copied ${copied.size} bytes, expected ${bytes.length}`);
}
console.log(`wrote ${target} (${copied.size} bytes)`);
