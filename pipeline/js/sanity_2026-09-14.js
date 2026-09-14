const fs = require('fs');
const html = fs.readFileSync('docs/index.html', 'utf8');

function extract(name) {
  const s = html.indexOf('const ' + name + ' =');
  if (s < 0) { console.error(name + ': NOT FOUND'); process.exit(1); }
  const rest = html.slice(s);
  const start = rest.indexOf('{');
  let depth = 0, end = -1, inStr = null;
  for (let i = start; i < rest.length; i++) {
    const c = rest[i];
    if (inStr) {
      if (c === '\\') i++;
      else if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') inStr = c;
    else if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) { end = i; break; } }
  }
  return eval('(' + rest.slice(start, end + 1) + ')');
}

const fd = extract('forexData');
const changes = extract('dailyChanges');
const drivers = extract('macroDrivers');
const news = extract('newsData');

console.log('forexData: OK, keys=' + Object.keys(fd).join(', '));
console.log('dailyChanges: OK ' + JSON.stringify(changes));
console.log('macroDrivers: OK (' + Object.keys(drivers).length + ' pairs)');
console.log('newsData: OK, ' + news.items.length + ' items, updated=' + news.updated);
for (const [p, d] of Object.entries(fd)) {
  console.log(`${p.padEnd(8)} ${d.quote.padEnd(8)} ${d.bias.padEnd(6)} ${d.en.recommendation.padEnd(28)} rr=${d.en.rr} rrValue=${d.en.rrValue}`);
}
