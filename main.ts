// news-image-20261120 entry (Node 22, standard library only).
// The image is entry.png beside this file: a front page drawn for Friday
// 20 November 2026 (THE WORLD — Kyiv missiles, Cyclone Akvan, COP31,
// the AI sell-off, the UK-EU reset, and the day's other stories).
// The program copies it to /output/entry.png, byte for byte, every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
copyFileSync(src, join(outDir, "entry.png"));
console.log("wrote " + join(outDir, "entry.png"));
