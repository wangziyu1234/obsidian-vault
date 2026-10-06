const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const base = path.join(process.env.TEMP, 'codex-mathjax-check', 'node_modules', 'mathjax-full', 'js');
const {mathjax} = require(path.join(base, 'mathjax.js'));
const {TeX} = require(path.join(base, 'input/tex.js'));
const {SVG} = require(path.join(base, 'output/svg.js'));
const {liteAdaptor} = require(path.join(base, 'adaptors/liteAdaptor.js'));
const {RegisterHTMLHandler} = require(path.join(base, 'handlers/html.js'));
const {AllPackages} = require(path.join(base, 'input/tex/AllPackages.js'));
RegisterHTMLHandler(liteAdaptor());
const tex = new TeX({packages: AllPackages.filter(p => !['noerrors', 'noundefined'].includes(p)), formatError: (_, err) => {throw err;}});
const doc = mathjax.document('', {InputJax: tex, OutputJax: new SVG({fontCache: 'none'})});
const root = process.cwd();
const dir = path.join(root, '\u63a7\u5236\u7406\u8bba', '777\u4e60\u9898\u96c6');
const files = fs.readdirSync(dir).filter(n => n.startsWith('\u73b0\u63a7200\u9898\u57fa\u7840') && n.endsWith('.md')).map(n => path.join(dir, n));
for (const y of [2006, 2007]) files.push(path.join(root, '\u6570\u5b66', '\u8003\u7814\u6570\u5b66\u4e8c', `${y}\u5e74\u8003\u7814\u6570\u5b66\u4e8c\u7b54\u6848\u4e0e\u89e3\u6790.md`));
const explicitFiles = process.argv.slice(2).filter(x => x !== '--head');
if (explicitFiles.length) files.splice(0, files.length, ...explicitFiles.map(x => path.resolve(x)));
let count = 0, bad = 0;
for (const file of files) {
  const text = process.argv.includes('--head') ? cp.execFileSync('git', ['show', 'HEAD:' + path.relative(root, file).replaceAll('\\', '/')], {encoding: 'utf8'}) : fs.readFileSync(file, 'utf8');
  const regex = /\$\$([\s\S]*?)\$\$|(?<![\\$])\$(?!\$)((?:\\.|[^$\r\n])+)\$/g;
  for (const m of text.matchAll(regex)) {
    const source = (m[1] ?? m[2]).replace(/^\s*>\s?/gm, '').replace(/\\\|/g, '|');
    const line = text.slice(0, m.index).split('\n').length;
    try { doc.convert(source, {display: m[1] !== undefined}); count++; }
    catch (e) { bad++; console.log(JSON.stringify({file: path.basename(file), line, error: e.message, source})); }
  }
}
console.log(JSON.stringify({files: files.length, parsed: count, errors: bad}));
process.exitCode = bad ? 1 : 0;
