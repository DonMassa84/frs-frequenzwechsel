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

Ausstehend sind Asset-Prüfung, Browser-Wiedergabe, responsive Ansicht und Pages-Veröffentlichung. Die tatsächlichen Ergebnisse werden nach der Prüfung ergänzt.

## 10. Nachhaltigkeit

Die ursprüngliche Videofassung und ihr Produktionsskript sind über ihren bisherigen Pfad verfügbar. Der ergänzende Web-Build liegt unter `/home/schattenmacher/Videos/Frequenzwechsel-Teaser-2026-11-26/build_web_teaser.py`. Für die Rücknahme lässt sich der Videoeinbindungs-Commit revertieren und dessen Website-Stand erneut nach `gh-pages` übertragen. Die bestätigten Prüfergebnisse und Commit-IDs werden hier festgehalten.
