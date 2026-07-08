// Konstruas la pakaĵojn per esbuild:
//   dist/bundle.css  – Fira-Sans + Bootstrap + main.css + vortaro.css (+ files/)
//   dist/bundle.js   – jQuery, Bootstrap, typeahead, main.js, vortaro.js
//   dist/hejmo.js    – la memstara skripto de la lingvo-startpaĝo
//
// La vendaj JS-dosieroj estas jam minigitaj kaj estas nur KUNMETITAJ (ne ESM-
// pakitaj), por ke jQuery kaj ĝiaj kromaĵoj registru siajn globalajn variablojn
// same kiel antaŭe. Nia propra kodo estas nur minigita (transform), do ĝia
// tutmonda amplekso restas — grave, ĉar vortaro.js legas la globalan `vortlisto`
// el la aparta, po-lingve generita vortlisto.js.
import * as esbuild from 'esbuild';
import { readFile, writeFile, mkdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const dir = path.dirname(fileURLToPath(import.meta.url)); // fonto/aktivoj
const root = path.resolve(dir, '..', '..');               // deponeja radiko
const nodeModules = path.join(root, 'node_modules');
const dist = path.join(dir, 'dist');

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

// 1) CSS-pakaĵo: esbuild solvas la @import-ojn kaj kopias la tiparojn.
await esbuild.build({
  entryPoints: [path.join(dir, 'stilo.css')],
  bundle: true,
  minify: true,
  loader: { '.woff2': 'file', '.woff': 'file' },
  assetNames: 'files/[name]',
  outfile: path.join(dist, 'bundle.css'),
  logLevel: 'warning',
});

// 2) Minigu nian propran JS (transform → konservas la tutmondan amplekson).
async function minify(relative) {
  const code = await readFile(path.join(root, relative), 'utf8');
  const result = await esbuild.transform(code, { minify: true, loader: 'js' });
  return result.code;
}
const [mainMin, vortaroMin, hejmoMin] = await Promise.all([
  minify('fonto/js/main.js'),
  minify('fonto/js/vortaro.js'),
  minify('fonto/js/hejmo.js'),
]);

// 3) JS-pakaĵo: venda kodo (jam minigita) + nia kodo, kunmetitaj laŭvice.
const vendorRelatives = [
  'jquery/dist/jquery.min.js',
  'bootstrap/dist/js/bootstrap.bundle.min.js',
  'typeahead.js/dist/typeahead.bundle.min.js',
];
const vendor = await Promise.all(
  vendorRelatives.map((relative) => readFile(path.join(nodeModules, relative), 'utf8')),
);
const bundleJs = [...vendor, mainMin, vortaroMin].join('\n;\n');

await writeFile(path.join(dist, 'bundle.js'), bundleJs);
await writeFile(path.join(dist, 'hejmo.js'), hejmoMin);

console.log('Pakaĵoj kreitaj en ' + path.relative(root, dist));
