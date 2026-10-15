import re, hashlib, os
from PIL import Image, ImageDraw, ImageFont
out='pwa/'
h=open('app/rd-kompendium.html').read()
i=h.index('</style>')+len('</style>')
head, body = h[:i], h[i:]
ver=hashlib.sha1(h.encode()).hexdigest()[:10]
pre='''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="RD-Nachschlag">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" href="icon-192.png">
'''
head=head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
sw_reg='''<script>
if ("serviceWorker" in navigator) { window.addEventListener("load", () => { navigator.serviceWorker.register("sw.js").catch(() => {}); }); }
</script>
'''
doc=pre+head+'\n</head>\n<body>\n'+body+'\n'+sw_reg+'</body>\n</html>\n'
open(out+'index.html','w').write(doc)
open(out+'manifest.webmanifest','w').write('''{
  "name": "RD-Kompendium Nachschlag",
  "short_name": "RD-Nachschlag",
  "lang": "de",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#1d2a33",
  "theme_color": "#1d2a33",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
''')
open(out+'sw.js','w').write('''// Offline-Cache: App-Dateien beim Installieren, Schriften beim ersten Laden.
const CACHE = "rd-nachschlag-%s";
const CORE = ["./", "index.html", "manifest.webmanifest", "icon-180.png", "icon-192.png", "icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  if (req.mode === "navigate") {
    // Netz zuerst (damit Updates ankommen), sonst Cache
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put("index.html", copy)); return r; }).catch(() => caches.match("index.html")));
    return;
  }
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
    if (r && (r.ok || r.type === "opaque")) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
    return r;
  }).catch(() => hit)));
});
''' % ver)
# Icon: dunkle Fläche, orangefarbenes Kreuz-Symbol, Text "RD"
def icon(s):
    im=Image.new('RGB',(s,s),'#1d2a33'); d=ImageDraw.Draw(im)
    c=s/2; a=s*0.36; w=s*0.12
    d.rounded_rectangle([c-w,c-a,c+w,c+a],radius=s*0.03,fill='#ff7a3d')
    d.rounded_rectangle([c-a,c-w,c+a,c+w],radius=s*0.03,fill='#ff7a3d')
    try: f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(s*0.16))
    except Exception: f=ImageFont.load_default()
    d.text((c,c),"RD",font=f,fill='#1d2a33',anchor='mm')
    return im
for s in (180,192,512): icon(s).save(out+f'icon-{s}.png')
open(out+'ANLEITUNG.txt','w').write('''RD-Kompendium Nachschlag – Offline-Web-App für iPhone / iPad

1. Diesen Ordner (alle Dateien) auf einen Webspace mit HTTPS hochladen,
   z. B. kostenlos per Drag-and-drop auf https://app.netlify.com/drop
2. Die Adresse, die du bekommst, auf dem iPhone/iPad in Safari öffnen.
3. Teilen-Symbol ➜ „Zum Home-Bildschirm“.
4. Die App einmal mit Internet öffnen und kurz durchtippen. Danach startet sie auch ohne Netz.

Updates: neue Dateien hochladen, App einmal mit Internet öffnen und neu starten.
Hinweis: Wer die Adresse kennt, kann die Seite öffnen. Vorher klären, ob die Inhalte veröffentlicht werden dürfen.
''')
print('ok',ver,len(doc))
