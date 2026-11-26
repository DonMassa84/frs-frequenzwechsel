# Videoeinbindung auf der Frequenzwechsel-Website

## 1. Situation

Der vorhandene 40-Sekunden-Teaser liegt unter `/home/schattenmacher/Videos/Frequenzwechsel-Teaser-2026-11-17/`. Seine SHA-256-Prüfsumme entspricht dem Produktionsbericht. GitHub Pages veröffentlicht `gh-pages` aus dessen Wurzelverzeichnis. Die aktive Website ist `https://donmassa84.github.io/frs-frequenzwechsel/`. `nachhall.pntr.dev` war bei der aktuellen Prüfung per DNS unerreichbar. Der Nutzer hat die Einbindung des fertigen Videos beauftragt. Der gemeldete Inventurstand `858e71b` ist vorhanden.

## 2. Ziel

Auf der öffentlichen Startseite lässt sich der Teaser mit Ton starten, pausieren und bis zum Ende abspielen. Der Player passt in mobile und breite Ansichten. Die veröffentlichte Datei dauert 40 Sekunden und enthält H.264 sowie AAC-Stereo. Der Bereich ist über `#teaser` erreichbar.

## 3. Stakeholder

Website-Besucher sehen die Sendungsidee und erreichen Gast-DJ-Bewerbung und Unterstützung direkt beim Video. Die Crew erhält eine nachprüfbare Veröffentlichung über ihren vorhandenen GitHub-Pages-Ablauf.

## 4. Ursachenanalyse

Die Website enthielt bisher keinen Videoplayer. Das Video nennt die frühere Custom-Domain auf zwei Tafeln. Die aktuelle DNS-Prüfung und die GitHub-Pages-Einstellungen bestätigen die GitHub-Adresse als erreichbaren Veröffentlichungsort.

## 5. Alternativen

Ein selbst gehosteter HTML-Videoplayer kann das lokale MP4 direkt ausliefern. Eine Descript-Einbettung benötigt eine zusätzliche Veröffentlichung. Die Webfassung lässt sich außerdem für geringeres Übertragungsvolumen optimieren.

## 6. Bewertung

Maßgeblich sind bestehender Veröffentlichungsweg, sichtbare Wiedergabesteuerung, mobile Lesbarkeit und Dateigröße. Der native Player passt zum statischen Aufbau. Die Webfassung kann ihre Hinweise direkt mit den Angeboten unterhalb des Players verbinden.

## 7. Auswahl

Ein nativer HTML-Videoplayer mit Poster, manueller Wiedergabe, Inline-Wiedergabe und einer Webfassung in 1280 × 720. Die Musik stammt aus der bereits fertiggestellten lokalen Fassung. Die Gast-DJ-Tafel verweist auf den Link unter dem Video. Die Spendentafel nennt den offiziellen FRS-Förderverein.

## 8. Umsetzung

Die RTX 3060 rendert die korrigierten Tafeln mit dem vorhandenen Produktionsskript. FFmpeg erzeugt eine komprimierte Webfassung und übernimmt die bestehende AAC-Spur. Das Video erscheint nach dem Einstieg der Startseite. Die veröffentlichten Assets liegen unter `website/assets/`. Die Quelländerung wird selektiv nach `main` übertragen und anschließend nach `gh-pages` veröffentlicht.

## 9. Kontrolle

- Die Webdatei ist 3.556.676 Byte groß. `ffprobe` meldet 40 Sekunden, 1280 × 720, H.264 und AAC-Stereo. Vollständiges Decodieren mit `ffmpeg -xerror` schloss mit Exit 0 ab.
- Der SHA-256-Wert der lokalen und der vollständig von GitHub Pages abgerufenen MP4 lautet jeweils `fb8d8e02ce50f68ce9915e273a6726a1a0117cde9dd618dc9b164f62f30fdade`.
- Die Audiopakete der ursprünglichen Fassung und der Webfassung ergeben jeweils `d1c64f770069afa54238c06a5547d0f250a735b8dfc2d06f429db1b06a00b3f1`.
- Die relativen HTML-Verweise, Videoattribute, JavaScript-Syntax und Git-Whitespace-Prüfung bestanden. Alle vier Videotafeln wurden als Standbilder geprüft.
- Bei 390 Pixel Viewportbreite misst der Player 347 Pixel. Die Seite hat keinen horizontalen Überlauf. Der temporäre Viewport wurde zurückgesetzt.
- Im In-App-Browser blieb die Wiedergabe bei Metadaten und Sekunde 0 stehen. Für den tatsächlichen Wiedergabenachweis wurde die öffentliche Seite in Chrome geprüft. Dort startete das Video, ließ sich bei 12,46 Sekunden pausieren und fortsetzen und erreichte 40 Sekunden mit `ended=true`, `muted=false` und ohne Medienfehler. Ein Sprung über die Zeitleiste funktionierte ebenfalls. Die Seite blieb als Ergebnis in Chrome geöffnet.
- GitHub Pages liefert die MP4 mit `Content-Type: video/mp4` und unterstützt Bereichsabrufe mit HTTP 206. Die Startseite enthält den Teaser samt Poster und Links.
- Quellcommit `299c2ba` baut auf Inventurstand `858e71b` auf. Veröffentlichungscommit auf `gh-pages` ist `b5d164f`. Der Lauf [45845685771](https://github.com/DonMassa84/frs-frequenzwechsel/actions/runs/45845685771) endete erfolgreich.

## 10. Nachhaltigkeit

Die ursprüngliche Videofassung und ihr Produktionsskript sind über ihren bisherigen Pfad verfügbar. Der ergänzende Web-Build liegt unter `/home/schattenmacher/Videos/Frequenzwechsel-Teaser-2026-11-26/build_web_teaser.py`. Für die Rücknahme lässt sich der Videoeinbindungs-Commit revertieren und dessen Website-Stand erneut nach `gh-pages` übertragen.

Für Folgeaufträge die aktive Pages-Adresse aus der Hosting-Konfiguration prüfen. Die öffentlich geladenen Videodaten mit dem geprüften Asset vergleichen und die Wiedergabe im Browser kontrollieren. Der in dieser Sitzung beobachtete Unterschied zwischen In-App-Browser und Chrome begrenzt den In-App-Nachweis auf Layout und Metadaten. Die erneute Nutzung von `nachhall.pntr.dev` hängt weiterhin von einer funktionierenden DNS-Zuordnung ab.
