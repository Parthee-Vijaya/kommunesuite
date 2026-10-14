# SPDX-License-Identifier: EUPL-1.2
import json
from pathlib import Path
from html import escape

root = Path(__file__).resolve().parent
products = json.loads((root / 'catalog.json').read_text())
assert len(products) == 9 and len({p['id'] for p in products}) == 9
out = root / 'dist'
(out / 'assets').mkdir(parents=True, exist_ok=True)
logo_colors = {0:'#5992ec',2:'#ed6754',3:'#9b7be3',4:'#e99a4e',6:'#6974d7',8:'#d5ad3f'}
logo_tiles = ''.join(f'<rect x="{(i%3)*10+1}" y="{(i//3)*10+1}" width="8" height="8" rx="2.2" fill="{logo_colors.get(i, "#e6e8eb")}"/>' for i in range(9))
(out / 'assets' / 'brand.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30">{logo_tiles}</svg>')
cards, orbit = [], []
labels = {'dokumenter':'Dokumenter', 'arbejdsgange':'Arbejdsgange', 'indsigt':'Indsigt & læring'}
arrow = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
for i, p in enumerate(products):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="160" height="160" viewBox="0 0 80 80"><defs><linearGradient id="g" x2=".7" y2="1"><stop stop-color="{p['color']}"/><stop offset="1" stop-color="{p['dark']}"/></linearGradient><linearGradient id="s" x2="0" y2="1"><stop stop-color="white" stop-opacity=".38"/><stop offset=".55" stop-color="white" stop-opacity="0"/></linearGradient></defs><rect x="3" y="5" width="74" height="74" rx="20" fill="{p['dark']}"/><rect x="3" y="2" width="74" height="74" rx="20" fill="url(#g)"/><rect x="4" y="3" width="72" height="72" rx="19" fill="url(#s)" stroke="white" stroke-opacity=".2"/><g transform="translate(8 6)">{p['symbol']}</g></svg>'''
    (out / 'assets' / f"{p['id']}.svg").write_text(svg)
    icon = f'<img src="assets/{p["id"]}.svg" width="96" height="96" alt="" draggable="false">'
    cards.append(f'''<article class="product-card" data-category="{p['category']}" style="--product:{p['color']};--product-dark:{p['dark']};--product-light:{p['light']};--order:{i}">
      <div class="card-top"><div class="card-icon">{icon}</div><span class="product-category">{labels[p['category']]}</span></div>
      <h3>{escape(p['name'])}</h3>
      <p>{escape(p['description'])}</p>
      <div class="card-bottom"><span class="planned"><span></span>Planlagt</span><a class="product-link" href="#produkt/{p['id']}" aria-label="Læs om {p['name']}">Læs mere {arrow}</a></div>
    </article>''')
    orbit.append(f'<a href="#produkt/{p["id"]}" class="orbit-app orbit-{i}" style="--i:{i};--product:{p["color"]}" aria-label="Læs om {p["name"]}"><span class="orbit-icon">{icon}</span><span class="orbit-label">{escape(p["short"])}</span></a>')
template = (root / 'index.template.html').read_text()
template = template.replace('<!-- PRODUCT_CARDS -->','\n'.join(cards)).replace('<!-- ORBIT_APPS -->','\n'.join(orbit))
template = template.replace('<!-- PRODUCT_DATA -->', json.dumps(products, ensure_ascii=False).replace('</','<\\/'))
(out / 'index.html').write_text(template)
(out / 'LICENSE.txt').write_text((root / 'LICENSE').read_text())
print('Built 9 product cards, 9 app icons and product content.')
