# Nachhall: Live-Chat, Handoff und Gast-DJ-Bewerbung

## 1. Situation

Die bestehende Website unter `https://nachhall.pntr.dev/#radio` ist eine statische
GitHub-Pages-Seite. Sie enthält Sendeleitfaden, Sets und Produktionshinweise, aber
keinen Chat-Einstieg, keinen Handoff und keinen eigenen Gast-DJ-Bewerbungsweg.
Die Colorado-Referenz trennt Mix-Einsendungen von Studio-/Live-Bewerbungen und
fordert dafür kurze Angaben zur Person, Erfahrung und Audio-/Video-Samples.

## 2. Ziel

Besucher sollen in höchstens zwei Klicks entweder eine Frage an den Radio-Kontakt
übergeben oder eine strukturierte Gast-DJ-Bewerbung per E-Mail vorbereiten können.
Die Website muss sichtbar zwischen lokalem Chat-Demo und echter Übermittlung
unterscheiden; keine Nachricht darf ohne ausdrückliche Nutzeraktion versendet werden.

## 3. Stakeholder

- Gast-DJs: verständlicher, niedriger Bewerbungseinstieg.
- Frequenzwechsel-Crew: verwertbare Anfrage mit Samples und Verfügbarkeit.
- Roman Kalex / coloRadio: Referenz für das gewünschte Radio-Muster.
- FRS-Förderverein: offizieller Zielpunkt für Unterstützung und Spenden.
- Website-Besucher: nachvollziehbarer Datenschutz- und Übermittlungsweg.

## 4. Ursachenanalyse

Der aktuelle statische Aufbau besitzt weder Backend noch nachgewiesenen Live-Chat-
Dienst. Ein echtes synchrones Chat-System wäre deshalb eine zusätzliche externe
Abhängigkeit. Der vorhandene E-Mail-Weg ist technisch sofort umsetzbar und passt
zum Colorado-Muster.

## 5. Alternativen

1. Statischer Chat-Demo-Verlauf mit explizitem E-Mail-Handoff und Bewerbungs-
   formular: sofort nutzbar, keine Datenhaltung, aber kein synchroner Mehrnutzerchat.
2. Drittanbieter-Chat: echter Live-Chat, aber Anbieter, Datenschutzkonfiguration
   und Zugang fehlen.
3. Eigenes Backend: volle Kontrolle, aber für diese statische Projektseite
   unverhältnismäßig groß.

## 6. Bewertung

Variante 1 erfüllt den sofortigen Kontakt- und Bewerbungszweck mit der geringsten
technischen und datenschutzrechtlichen Abhängigkeit. Variante 2 und 3 bleiben als
spätere Ausbaustufen offen.

## 7. Auswahl

Ausgewählt wird Variante 1 nach dem Colorado-Muster. Der Handoff nutzt den
vorhandenen Radio-Kontaktweg; der Spendenlink führt ausschließlich zur offiziellen
FRS-Fördervereinsseite. Ein echtes Chat-Backend ist keine behauptete Funktion.

## 8. Umsetzung

- Navigation und Abschnitt „Live Chat / Handoff“ ergänzen.
- Lokalen Demo-Chat mit Eingabe, Status und Übergabe-Link ergänzen.
- Separaten Abschnitt „Gast-DJs“ mit Name, E-Mail, Stil, Erfahrung,
  Verfügbarkeit, Sample-Link und Nachricht ergänzen.
- Formulareingaben in eine `mailto:`-Nachricht überführen.
- Keine personenbezogenen Eingaben lokal oder serverseitig speichern.
- Support-CTA auf `https://www.freies-radio.de/foerderverein` ergänzen.

## 9. Kontrolle

HTML-Struktur, JavaScript-Syntax und Git-Diff prüfen. Die veröffentlichte Seite
mit Browser-UI auf Navigation, Chat-Demo, Übergabe-`mailto:` und Bewerbungs-
formular prüfen; keine Bewerbung tatsächlich absenden.

## 10. Nachhaltigkeit

Der Empfänger bleibt als zentrale Konstante in `website/app.js` dokumentiert.
Für einen echten Live-Chat müssen später Anbieter, Backend, Aufbewahrung,
Einwilligung und Handoff-Ziel separat entschieden und getestet werden.

## Erfolgskriterium

Die Live-Seite zeigt Chat/Handoff, Gast-DJ-Bewerbung und Supportlink; die beiden
Kontaktaktionen erzeugen nach lokaler Validierung eine korrekte, vorausgefüllte
E-Mail, ohne Nachricht oder Bewerbung automatisch zu versenden.
