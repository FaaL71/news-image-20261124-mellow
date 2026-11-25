// Entry point for the news-image-20261124 program entry.
// Runs draw.py (Python + PIL) and copies the finished entry.png into
// the output directory the harness mounts at /output.
import { execFileSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { join } from "node:path";

const outDir = process.argv[2] ?? "/output";
const root = new URL(".", import.meta.url).pathname;

mkdirSync(outDir, { recursive: true });
// Clean only the contents inside outDir, never outDir itself.
for (const name of readdirSync(outDir)) {
  rmSync(join(outDir, name), { recursive: true, force: true });
}

execFileSync("python3", [join(root, "draw.py")], { stdio: "inherit" });

const png = join(root, "entry.png");
if (!existsSync(png)) {
  throw new Error("draw.py did not produce entry.png");
}
copyFileSync(png, join(outDir, "entry.png"));
console.log("wrote", join(outDir, "entry.png"));
