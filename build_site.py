# SPDX-License-Identifier: EUPL-1.2
import json
import re
import zipfile
from pathlib import Path
from html import escape

root = Path(__file__).resolve().parent
products = json.loads((root / 'catalog.json').read_text())
if not products or len({p['id'] for p in products}) != len(products):
    raise ValueError('Product IDs must be unique and the catalog must not be empty.')
for product in products:
    if not re.fullmatch(r'[a-z][a-z0-9-]*', product['id']):
        raise ValueError(f"Invalid product ID: {product['id']}")
    if product['status'] not in ('beta', 'planned'):
        raise ValueError(f"Invalid product status: {product['id']}")


def danish_number(number):
    small = ['nul', 'ét', 'to', 'tre', 'fire', 'fem', 'seks', 'syv', 'otte',
             'ni', 'ti', 'elleve', 'tolv', 'tretten', 'fjorten', 'femten',
             'seksten', 'sytten', 'atten', 'nitten']
    if number < len(small):
        return small[number]
    tens = {20: 'tyve', 30: 'tredive', 40: 'fyrre', 50: 'halvtreds',
            60: 'tres', 70: 'halvfjerds', 80: 'firs', 90: 'halvfems'}
    if number < 100:
        unit, ten = number % 10, number // 10 * 10
        return (('en' if unit == 1 else small[unit]) + 'og' if unit else '') + tens[ten]
    return str(number)


total = len(products)
planned = sum(product['status'] == 'planned' for product in products)
out = root / 'dist'
(out / 'assets').mkdir(parents=True, exist_ok=True)
logo_colors = {0:'#5992ec',2:'#ed6754',3:'#9b7be3',4:'#e99a4e',6:'#6974d7',8:'#d5ad3f'}
logo_tiles = ''.join(f'<rect x="{(i%3)*10+1}" y="{(i//3)*10+1}" width="8" height="8" rx="2.2" fill="{logo_colors.get(i, "#e6e8eb")}"/>' for i in range(9))
(out / 'assets' / 'brand.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30">{logo_tiles}</svg>')
cards, orbit = [], []
labels = {'dokumenter':'Dokumenter', 'indsigt':'Indsigt & læring', 'medier':'Medier & filer'}
arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
for i, p in enumerate(products):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 80 80"><defs><linearGradient id="g" x2=".7" y2="1"><stop stop-color="{p['color']}"/><stop offset="1" stop-color="{p['dark']}"/></linearGradient><linearGradient id="s" x2="0" y2="1"><stop stop-color="white" stop-opacity=".38"/><stop offset=".55" stop-color="white" stop-opacity="0"/></linearGradient></defs><rect x="3" y="5" width="74" height="74" rx="20" fill="{p['dark']}"/><rect x="3" y="2" width="74" height="74" rx="20" fill="url(#g)"/><rect x="4" y="3" width="72" height="72" rx="19" fill="url(#s)" stroke="white" stroke-opacity=".2"/><g transform="translate(8 6)">{p['symbol']}</g></svg>'''
    (out / 'assets' / f"{p['id']}.svg").write_text(svg)
    icon = f'<img src="assets/{p["id"]}.svg" width="96" height="96" alt="" draggable="false">'
    status = 'Beta · privat Mac-RC1' if p['status'] == 'beta' else 'Planlagt'
    subtitle = f'<p class="product-subtitle">{escape(p.get("subtitle", p["short"]))}</p>'
    cards.append(f'''<article class="product-card" data-category="{p['category']}" style="--product:{p['color']};--product-dark:{p['dark']};--product-light:{p['light']};--order:{i}">
      <div class="card-top"><div class="card-icon">{icon}</div><span class="product-category">{labels[p['category']]}</span></div>
      <h3>{escape(p['name'])}</h3>
      {subtitle}
      <p>{escape(p['description'])}</p>
      <div class="card-bottom"><span class="planned"><span></span>{status}</span><a class="product-link" href="#produkt/{p['id']}" aria-label="Læs om {escape(p['name'])}">Læs mere {arrow}</a></div>
    </article>''')
    badge = '<span class="orbit-beta">Beta</span>' if p['status'] == 'beta' else ''
    orbit.append(f'<a href="#produkt/{p["id"]}" class="orbit-app orbit-{i}" style="--i:{i};--product:{p["color"]}" aria-label="Læs om {escape(p["name"])}">{badge}<span class="orbit-icon">{icon}</span><span class="orbit-label">{escape(p["short"])}</span></a>')
template = (root / 'index.template.html').read_text()
template = template.replace('<!-- PRODUCT_CARDS -->','\n'.join(cards)).replace('<!-- ORBIT_APPS -->','\n'.join(orbit))
template = template.replace('<!-- PRODUCT_DATA -->', json.dumps(products, ensure_ascii=False).replace('</','<\\/'))
replacements = {
    'PRODUCT_TOTAL': str(total),
    'PRODUCT_TOTAL_WORD': danish_number(total),
    'PRODUCT_TOTAL_WORD_CAP': danish_number(total).capitalize(),
    'PLANNED_TOTAL': str(planned),
    'PLANNED_TOTAL_WORD': danish_number(planned),
    'PLANNED_TOTAL_WORD_CAP': danish_number(planned).capitalize(),
    'PLANNED_LINKS': ' '.join(f'<a href="#produkt/{p["id"]}">{escape(p["name"])}</a>' for p in products if p['status'] == 'planned'),
}
for marker, value in replacements.items():
    template = template.replace(f'<!-- {marker} -->', value)
if re.search(r'<!-- (?:PRODUCT_|PLANNED_|ORBIT_)[A-Z_]+ -->', template):
    raise ValueError('A catalog template marker was not replaced.')
(out / 'index.html').write_text(template)
(out / 'LICENSE.txt').write_text((root / 'LICENSE').read_text())

# Publish only website source and assets. Never include Git, Vercel links or local files.
source_files = [root / name for name in ('README.md', 'build_site.py', 'catalog.json',
                'index.template.html', 'LICENSE', 'NOTICE', 'NAMES.md', 'vercel.json')]
source_files += [out / name for name in ('index.html', 'app.js', 'theme.css', 'brand-logos.css', 'LICENSE.txt')]
source_files += [path for path in (out / 'assets').rglob('*') if path.is_file()]
with zipfile.ZipFile(out / 'source.zip', 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(source_files):
        entry = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
        entry.compress_type = zipfile.ZIP_DEFLATED
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, path.read_bytes())
print(f'Built {total} product cards, {planned} planned apps and product content.')
