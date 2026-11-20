// gta6-meme-x-01 entry (Node 22, standard library only): validates POST.json and copies it to
// /output/POST.json, where the gate reads it. The entry is the post itself: the meme posted on X
// from a public account with make.fun (a link or written out) and/or @makefunai plus the play code
// in its text; POST.json names that post and the house reads its first picture and text from X.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const STATUS_RE = /^https:\/\/(x\.com|twitter\.com)\/([A-Za-z0-9_]{1,15})\/status\/([1-9]\d*)\/?$/;

function fail(msg: string): never {
  console.error(msg);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
let raw: unknown;
try {
  raw = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf8'));
} catch (err) {
  fail(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
}
// POST.json is hand-edited input: narrow it at the boundary instead of asserting a shape.
const url =
  raw && typeof raw === 'object' && 'url' in raw && typeof raw.url === 'string' ? raw.url.trim() : '';
const m = STATUS_RE.exec(url);
if (!m) fail(`POST.json url must look like https://x.com/<handle>/status/<id>, got: ${url || '(missing)'}`);
// twitter.com status addresses open the same post on x.com; hand the gate one canonical form.
const canonical = `https://x.com/${m[2]}/status/${m[3]}`;
writeFileSync(join(OUTPUT_DIR, 'POST.json'), JSON.stringify({ url: canonical }) + '\n');
console.log(`post: ${canonical}`);
