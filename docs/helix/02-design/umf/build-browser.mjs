// Builds a local UMF schema browser for the Tempo table specs.
// Usage: node docs/helix/02-design/umf/build-browser.mjs [outDir]
// Then serve outDir (default: docs/helix/02-design/umf/browser, git-ignored) and open assets/index.html.
import {execFileSync} from 'node:child_process';
import {cpSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';

const BROWSER_VERSION = '2.0.0'; // exact pin; verified by npm integrity on install
const here = dirname(fileURLToPath(import.meta.url));
const out = resolve(process.argv[2] ?? join(here, 'browser'));
const tables = join(here, 'tables');

const entries = readdirSync(tables).filter(f => f.endsWith('.yaml')).sort().map(file => {
  const text = readFileSync(join(tables, file), 'utf8');
  const name = file.replace(/\.yaml$/, '');
  const description = /^description:\s*"(.*)"$/m.exec(text)?.[1] ?? '';
  return {id: `tempo-${name}`, title: name, category: 'tempo', path: `tables/${file}`,
          format: 'yaml', schemaFormat: 'tablespec', description, text};
});

const work = mkdtempSync(join(tmpdir(), 'umf-schema-browser-'));
try {
  execFileSync('npm', ['install', '--prefix', work, '--no-audit', '--no-fund', '--ignore-scripts',
    `@documentdrivendx/umf-schema-browser@${BROWSER_VERSION}`], {stdio: 'inherit'});
  rmSync(out, {recursive: true, force: true});
  mkdirSync(out, {recursive: true});
  cpSync(join(work, 'node_modules/@documentdrivendx/umf-schema-browser/assets'), join(out, 'assets'), {recursive: true});
  writeFileSync(join(out, 'assets/schema-catalog.json'), JSON.stringify({version: 1, entries}) + '\n');
} finally {
  rmSync(work, {recursive: true, force: true});
}
console.log(`Schema browser written to ${out}\nServe it: python3 -m http.server -d "${out}" 8099\nOpen:     http://localhost:8099/assets/index.html`);
