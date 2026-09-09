// Execute the actual inline catalog UI without network or browser dependencies.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'guides.html'), 'utf8');
const script = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(match => match[1]).find(source => source.includes('packages/catalog.json'));
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'packages/catalog.json')));

async function load(data = catalog, ok = true) {
  const elements = {}, errors = [];
  for (const id of ['search', 'cards', 'quant', 'os', 'delivery', 'status', 'sort',
                    'package-grid', 'result-count', 'catalog-summary', 'reset']) {
    elements[id] = {id, name: id, value: id === 'sort' ? 'newest' : '',
      tagName: id === 'search' ? 'INPUT' : 'SELECT', options: [], events: {},
      addEventListener(event, fn) { this.events[event] = fn; },
      appendChild(option) { this.options.push(option); }};
  }
  const context = {document: {getElementById: id => elements[id], createElement: () => ({})},
    fetch: async () => ({ok, status: 503, json: async () => data}),
    console: {error: error => errors.push(error)}, URLSearchParams,
    location: {pathname: '/guides.html', search: ''}, history: {replaceState() {}},
    navigator: {}, window: {setTimeout}};
  vm.runInNewContext(script, context);
  await new Promise(setImmediate);
  return {elements, errors};
}
const ids = page => [...page.elements['package-grid'].innerHTML.matchAll(/data-id="([^"]+)"/g)].map(m => m[1]);

test('real catalog renders; every sort/filter and reset handles pending headlines', async () => {
  const page = await load();
  assert.equal(page.errors.length, 0);
  assert.equal(ids(page).length, catalog.packages.length);
  for (const sort of ['newest', 'speed', 'name', 'cards']) {
    page.elements.sort.value = sort;
    page.elements.sort.events.change();
    assert.equal(ids(page).length, catalog.packages.length);
    if (sort === 'speed') {
      let pending = false;
      for (const id of ids(page)) {
        const metric = catalog.packages.find(item => item.id === id).library.featured_metric;
        if (!metric) pending = true;
        else assert.equal(pending, false, 'pending headlines must sort last');
      }
    }
  }
  for (const id of ['cards', 'quant', 'os', 'delivery']) {
    page.elements[id].value = String(page.elements[id].options[0].value);
    page.elements[id].events.change();
    assert.ok(ids(page).length > 0);
    page.elements.reset.events.click();
  }
  page.elements.search.value = 'no-such-model-xyz';
  page.elements.search.events.input();
  assert.match(page.elements['package-grid'].innerHTML, /No package matches/);
  page.elements.reset.events.click();
  assert.equal(ids(page).length, catalog.packages.length);
});

test('null and absent metrics show escaped pending status, not fabricated speeds', async () => {
  const data = structuredClone(catalog);
  data.packages = data.packages.slice(0, 2);
  data.packages[0].library.featured_metric = null;
  delete data.packages[1].library.featured_metric;
  data.packages[0].library.benchmark_status = '<script>bad</script>';
  const page = await load(data);
  assert.equal(page.errors.length, 0);
  assert.equal(ids(page).length, 2);
  assert.equal((page.elements['package-grid'].innerHTML.match(/Strict headline pending/g) || []).length, 2);
  assert.match(page.elements['package-grid'].innerHTML, /&lt;script&gt;bad&lt;\/script&gt;/);
  page.elements.sort.value = 'speed';
  assert.doesNotThrow(() => page.elements.sort.events.change());
});

test('real fetch failures retain the GitHub fallback', async () => {
  const page = await load(catalog, false);
  assert.equal(page.elements['result-count'].textContent, 'Catalog unavailable');
  assert.match(page.elements['package-grid'].innerHTML, /Browse packages on GitHub/);
});
