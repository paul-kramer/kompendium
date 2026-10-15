# RD-Kompendium Nachschlag

Offline-fähige Web-App zum Nachschlagen im Rettungsdienst: Medikamente mit gewichtsbasierter Dosierhilfe, Notfallbilder / Leitsymptome und Kompetenzen je Rettungsdienstbereich.

Inhalte ausschließlich aus dem *Gemeinsamen Kompendium Rettungsdienst 2026* und dem *Begleitheft Medikamente 2026/2027*. Bei abweichenden Angaben gilt das Kompendium. Die App ersetzt nicht die lokal gültigen SAA / BPR, die Freigabe durch die Ärztliche Leitung Rettungsdienst oder die (tele-)notärztliche Anordnung.

## Auf iPhone / iPad installieren

1. Die GitHub-Pages-Adresse dieses Repos in Safari öffnen.
2. Teilen ➜ „Zum Home-Bildschirm“.
3. Die App einmal mit Internet öffnen. Danach startet sie auch ohne Netz.

## Aufbau

- `index.html`, `sw.js`, `manifest.webmanifest`, `icon-*.png`: die veröffentlichte App (Service Worker für den Offline-Betrieb).
- `quelle/`: Datenteile (`meds.js`, `notfaelle.js`, `komp.js`, `komp_meta.js`), Rechenlogik (`calc.js`), Seitenvorlage (`template.html`) sowie Build- und Testskripte. `build.py` setzt die Teile in die Vorlage ein, `build_pwa.py` erzeugt daraus die Offline-Dateien, `node test.js <ordner>` prüft die Dosisberechnungen.
