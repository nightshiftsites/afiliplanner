# -*- coding: utf-8 -*-
"""Site footer'ina sosyal medya hesaplarini ekler.

Kullanim: python tools/add-social.py <facebook_url> <instagram_url> <pinterest_url>
Tekrar calistirilirsa eski blogu bulup linkleri gunceller.
"""
import io, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), '..', 'public')
fb, ig, pin = sys.argv[1:4]

ICONS = {
    'fb': '<path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4V10.5H7.8v3h2.6V21h3.1z"/>',
    'ig': '<path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21 8.1c-.1-1.6-.4-3-1.6-4.2S16.8 2.1 15.2 2 8.8 2 7.2 2.1 4.4 2.5 3.2 3.7 1.4 6.4 1.3 8.1s-.1 6.3 0 7.9.4 3 1.6 4.2 2.6 1.5 4.2 1.6 6.4.1 8 0 3-.4 4.2-1.6 1.5-2.6 1.6-4.2.1-6.3 0-7.9zm-2 9.7a3.2 3.2 0 0 1-1.8 1.8c-1.3.5-4.2.4-5.3.4s-4 .1-5.3-.4a3.2 3.2 0 0 1-1.8-1.8c-.5-1.3-.4-4.2-.4-5.3s-.1-4 .4-5.3a3.2 3.2 0 0 1 1.8-1.8C7.9 4.9 10.8 5 12 5s4-.1 5.3.4a3.2 3.2 0 0 1 1.8 1.8c.5 1.3.4 4.2.4 5.3s.1 4-.4 5.3z"/>',
    'pin': '<path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.2-5s-.3-.6-.3-1.5c0-1.4.8-2.5 1.8-2.5.9 0 1.3.7 1.3 1.4 0 .9-.6 2.2-.9 3.4-.2 1 .5 1.9 1.6 1.9 1.9 0 3.3-2 3.3-4.9 0-2.6-1.8-4.4-4.5-4.4-3 0-4.8 2.3-4.8 4.6 0 .9.4 1.9.8 2.4l.1.4-.3 1.2c0 .2-.2.3-.4.2-1.4-.6-2.2-2.6-2.2-4.2 0-3.4 2.5-6.6 7.2-6.6 3.8 0 6.7 2.7 6.7 6.3 0 3.7-2.3 6.8-5.6 6.8-1.1 0-2.1-.6-2.5-1.3l-.7 2.6c-.2 1-.9 2.2-1.4 2.9A10 10 0 1 0 12 2z"/>',
}
LINKS = [('fb', 'Facebook', fb), ('ig', 'Instagram', ig), ('pin', 'Pinterest', pin)]

def svg(key):
    return (f'<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" '
            f'aria-hidden="true">{ICONS[key]}</svg>')

row = '    <!-- SOCIAL:BEGIN -->\n    <nav class="social" aria-label="Afili Planner social">\n'
for key, name, url in LINKS:
    row += (f'      <a href="{url}" target="_blank" rel="noopener me" '
            f'aria-label="Afili Planner on {name}">{svg(key)}</a>\n')
row += '    </nav>\n    <!-- SOCIAL:END -->\n'

CSS = """  /* SOCIAL:CSS */
  .social { display: flex; gap: 10px; order: -1; width: 100%; margin-bottom: 6px; }
  .social a {
    width: 38px; height: 38px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    border: 1px solid var(--border, #1E2A44); color: var(--muted, #8A94AC);
    transition: color .15s, border-color .15s, transform .15s;
  }
  .social a:hover { color: var(--text, #EDF1F9); border-color: var(--violet, #8B5CF6); transform: translateY(-1px); }
  .social a:focus-visible { outline: 2px solid var(--blue, #3E8BFF); outline-offset: 2px; }
"""

LD_START, LD_END = '<!-- SOCIAL:LD -->', '<!-- /SOCIAL:LD -->'
ld = (LD_START + '<script type="application/ld+json">'
      '{"@context":"https://schema.org","@type":"Organization","name":"Afili Labs",'
      '"url":"https://afiliplanner.com","logo":"https://afiliplanner.com/s/icon.png",'
      f'"sameAs":["{fb}","{ig}","{pin}"]}}</script>' + LD_END)

p = os.path.join(ROOT, 'index.html')
t = io.open(p, encoding='utf-8').read()

# footer satiri: varsa degistir, yoksa footer'in basina ekle
if '<!-- SOCIAL:BEGIN -->' in t:
    t = re.sub(r'    <!-- SOCIAL:BEGIN -->.*?<!-- SOCIAL:END -->\n', row, t, flags=re.S)
else:
    anchor = '  <div class="wrap foot">\n'
    assert t.count(anchor) == 1, 'footer bulunamadi'
    t = t.replace(anchor, anchor + row)

if '/* SOCIAL:CSS */' not in t:
    anchor = '  .foot .nav-spacer { flex: 1; }\n'
    assert t.count(anchor) == 1, 'foot css bulunamadi'
    t = t.replace(anchor, anchor + CSS)

# arama motorlari icin hesap baglantilari (sameAs)
if LD_START in t:
    t = re.sub(re.escape(LD_START) + '.*?' + re.escape(LD_END), ld, t, flags=re.S)
else:
    t = t.replace('</head>', ld + '\n</head>', 1) if '</head>' in t else t.replace('<style>', ld + '\n<style>', 1)

io.open(p, 'w', encoding='utf-8').write(t)
print('index.html guncellendi:', fb, ig, pin)
