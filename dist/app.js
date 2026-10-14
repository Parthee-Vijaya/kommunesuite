// SPDX-License-Identifier: EUPL-1.2
const products = JSON.parse(document.getElementById('product-data').textContent);
const dialog = document.getElementById('product-dialog');
const motionButton = document.getElementById('motion-toggle');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let activeProduct = 0;
let previousFocus = null;
let userMotionChoice = null;

function setMotion(paused) {
  document.documentElement.classList.toggle('motion-paused', paused);
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.setAttribute('aria-label', paused ? 'Start animationer' : 'Sæt animationer på pause');
  document.getElementById('motion-label').textContent = paused ? 'Start animation' : 'Pause animation';
}
setMotion(reduceMotion.matches);
motionButton.addEventListener('click', () => {
  userMotionChoice = !document.documentElement.classList.contains('motion-paused');
  setMotion(userMotionChoice);
});
reduceMotion.addEventListener('change', event => {
  if (userMotionChoice === null) setMotion(event.matches);
});

document.querySelectorAll('[data-filter]').forEach(button => {
  button.addEventListener('click', () => {
    const selected = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    document.querySelectorAll('.product-card').forEach(card => {
      card.hidden = selected !== 'all' && card.dataset.category !== selected;
      if (!card.hidden) count++;
    });
    document.getElementById('catalog-count').textContent = `Viser ${count} løsninger`;
  });
});

function displayProduct(index) {
  activeProduct = (index + products.length) % products.length;
  const product = products[activeProduct];
  dialog.style.setProperty('--product', product.color);
  dialog.style.setProperty('--product-dark', product.dark);
  dialog.style.setProperty('--product-light', product.light);
  document.getElementById('dialog-icon').src = `assets/${product.id}.svg`;
  document.getElementById('dialog-title').textContent = product.name;
  document.getElementById('dialog-description').textContent = product.details;
  document.getElementById('dialog-tagline').textContent = product.tagline;
  document.getElementById('dialog-index').textContent = `0${activeProduct + 1} / 09`;
  document.getElementById('dialog-position').textContent = `${activeProduct + 1} af ${products.length}`;
  const features = document.getElementById('dialog-features');
  features.replaceChildren(...product.features.map(text => {
    const li = document.createElement('li');
    li.textContent = text;
    return li;
  }));
  document.getElementById('dialog-example').textContent = product.example;
  document.getElementById('dialog-boundary').textContent = product.boundary;
  document.getElementById('dialog-connections').textContent = product.connections;
  dialog.querySelector('details').open = false;
  if (!dialog.open) {
    previousFocus = document.activeElement;
    dialog.showModal();
    document.body.classList.add('dialog-open');
  }
  dialog.scrollTop = 0;
  document.getElementById('dialog-title').focus({preventScroll:true});
}

function routeProduct() {
  const id = location.hash.startsWith('#produkt/') ? location.hash.slice(9) : null;
  const index = products.findIndex(product => product.id === id);
  if (index >= 0) displayProduct(index);
  else if (dialog.open) dialog.close();
}

document.querySelectorAll('a[href^="#produkt/"]').forEach(link => {
  link.addEventListener('click', event => {
    event.preventDefault();
    const hash = link.getAttribute('href');
    if (location.hash === hash) routeProduct();
    else {
      history.pushState(null, '', hash);
      routeProduct();
    }
  });
});

document.getElementById('dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('dialog-open');
  if (location.hash.startsWith('#produkt/')) history.replaceState(null, '', location.pathname + location.search + '#loesninger');
  if (previousFocus instanceof HTMLElement && previousFocus.isConnected) previousFocus.focus({preventScroll:true});
});
for (const [id, change] of [['previous-product', -1], ['next-product', 1]]) {
  document.getElementById(id).addEventListener('click', () => {
    const next = (activeProduct + change + products.length) % products.length;
    history.replaceState(null, '', `#produkt/${products[next].id}`);
    displayProduct(next);
  });
}
window.addEventListener('hashchange', routeProduct);
window.addEventListener('popstate', routeProduct);
routeProduct();

if ('IntersectionObserver' in window && !reduceMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {threshold:0.1});
  document.querySelectorAll('.section-heading, .workflow-visual, .principle-grid, .vision-banner').forEach(element => {
    element.classList.add('reveal');
    observer.observe(element);
  });
}
