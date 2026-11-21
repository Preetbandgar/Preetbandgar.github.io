#!/usr/bin/env python3
"""Build one standalone HTML file for phone testing: python3 build_preview.py
Needs beautifulsoup4 (pip install beautifulsoup4). Not used for deployment.
Pages become hash routes (#/home, #/index, #/<project>, #/cv, #/certificates). Images, videos and
the CV PDF are embedded once as base64 and turned into blob URLs at runtime. The page behaviour comes
from assets/portfolio.js (window.PB.init), so there is no second copy of the logic to keep in sync."""
import base64, html, json, re
from pathlib import Path
from bs4 import BeautifulSoup

R = Path(__file__).resolve().parent
MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
        '.mp4': 'video/mp4', '.pdf': 'application/pdf'}
MEDIA = {}


def embed(path):
    key = path.relative_to(R).as_posix()
    if key not in MEDIA:
        MEDIA[key] = [MIME[path.suffix.lower()], base64.b64encode(path.read_bytes()).decode('ascii')]
    return key


pages = [('home', R / 'index.html'), ('index', R / 'projects/index.html')]
pages += [(f.stem, f) for f in sorted((R / 'projects').glob('*.html')) if f.stem != 'index']
pages += [('cv', R / 'cv.html'), ('certificates', R / 'certificates.html')]
route_of = {p.resolve(): n for n, p in pages}

templates = []
for name, path in pages:
    body = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser').body
    for s in body.select('script'):
        s.decompose()
    for tag in body.find_all(['img', 'video', 'a']):
        for attr in ('src', 'poster', 'href'):
            v = tag.get(attr)
            if not v or v.startswith(('http', 'mailto:', 'data:', '#')):
                continue
            target = (path.parent / v.split('#')[0]).resolve()
            frag = v.split('#')[1] if '#' in v else ''
            if target in route_of:  # internal page link
                tag['href'] = f'#/{route_of[target]}' + (f'/{frag}' if frag else '')
            elif target.exists() and target.suffix.lower() in MIME:
                tag['data-media-' + attr] = embed(target)
                del tag[attr]
        if tag.name == 'a' and tag.get('href', '').startswith('#') and not tag['href'].startswith('#/'):
            tag['href'] = f'#/{name}/' + tag['href'][1:]
    for v in body.find_all('video'):  # <source> children do not re-resolve after insertion; put the key on the video
        s = v.find('source')
        if s and s.get('src'):
            v['data-media-src'] = embed((path.parent / s['src']).resolve())
            s.decompose()
    for o in body.select('object'):
        p = BeautifulSoup('<p>Use <strong>Open PDF</strong> above to read the CV on your phone.</p>', 'html.parser')
        o.replace_with(p)
    templates.append(f'<template id="route-{html.escape(name)}">' + ''.join(str(x) for x in body.contents) + '</template>')

script = r'''
const host = document.getElementById('site');
const urls = {};
function mediaURL(key) {
  if (!urls[key]) {
    const [mime, b64] = MEDIA[key], bin = atob(b64), bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    urls[key] = URL.createObjectURL(new Blob([bytes], { type: mime }));
  }
  return urls[key];
}
function route() {
  const [req, ...rest] = (location.hash || '#/home').replace(/^#\/?/, '').split('/');
  const name = document.getElementById('route-' + req) ? req : 'home';
  host.replaceChildren(document.getElementById('route-' + name).content.cloneNode(true));
  for (const attr of ['src', 'poster', 'href']) {
    host.querySelectorAll('[data-media-' + attr + ']').forEach(el => {
      el.setAttribute(attr, mediaURL(el.getAttribute('data-media-' + attr)));
      if (attr === 'href' && el.getAttribute('data-media-href').endsWith('.pdf')) { el.target = '_blank'; }
    });
  }
  host.querySelectorAll('video[data-media-src]').forEach(v => { v.src = mediaURL(v.dataset.mediaSrc); });
  document.title = (host.querySelector('h1')?.textContent || 'Pritam Bandgar').replace(/\s+/g, ' ').trim() + ' · Portfolio preview';
  PB.init(host);
  const id = rest.join('/');
  requestAnimationFrame(() => id ? document.getElementById(id)?.scrollIntoView() : scrollTo(0, 0));
  setTimeout(PB.syncJump, 120);
}
addEventListener('hashchange', route);
route();
'''
css = (R / 'assets/portfolio.css').read_text(encoding='utf-8')
js = (R / 'assets/portfolio.js').read_text(encoding='utf-8')
fonts = 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
out = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       '<meta name="theme-color" content="#171b19"><title>Pritam Bandgar · Phone preview</title>'
       f'<link rel="stylesheet" href="{fonts}"><style>{css}</style></head><body><div id="site"></div>'
       + ''.join(templates) + f'<script>const MEDIA={json.dumps(MEDIA)};</script><script>{js}</script><script>{script}</script></body></html>')
dest = R.parent / 'Pritam_Portfolio_V18_Mobile_Preview.html'
dest.write_text(out, encoding='utf-8')
print('wrote', dest.name, round(len(out) / 1e6, 2), 'MB,', len(templates), 'pages,', len(MEDIA), 'media files')
