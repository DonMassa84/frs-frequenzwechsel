# FRS Frequenzwechsel

Lokale Musikvorbereitung für eine elektronische Sendung beim Freien Radio Stuttgart.

## Sendungsprofil

**FRS Frequenzwechsel** verbindet Deep House, House, Techno, Trance, Electro, EDM/Dance und ruhige elektronische Übergänge. Die erste Auswahl ist als musikalische Reise aufgebaut: Ankommen, Groove, Verdichtung, Nachtfahrt und Ausklang.

## Website & Plenum-Pitch

- `website/index.html` – öffentlicher Sendeleitfaden mit Studio-Termin, Sendekonzept, Voraussetzungen, Workshops und Set-Übersicht
- `website/plenum.html` – aktualisierter Plenum-Pitch mit Pilotoptionen, DJ-Technik und offenen Entscheidungen (Stand 24.11.2026)
- [Plenum-Brief vom 07.10.2026](docs/plenum-brief-2026-10-07.md) – ursprünglicher Vorschlag für ein einmaliges Vinyl-Special
- Navigation in der Präsentation: Pfeiltasten oder PageUp/PageDown. `N` blendet Sprechernotizen ein.

Für statisches Hosting ist `website/` das Veröffentlichungsverzeichnis. Für die lokale Audiovorschau im Repository-Root `python3 -m http.server` starten und `http://localhost:8000/website/` öffnen. Die Audiovorschau erscheint bei der Set-Auswahl, wenn die lokalen Playlists vorhanden sind.

## Inhalt

- `playlists/sendung_01_frs_frequenzwechsel.m3u` – nummerierte Playlist
- `playlists/sendung_01_manifest.csv` – Originalpfad, lokale Kopie, Größe und SHA-256
- `sendung_01/audio/` – kopierte und nummerierte Audiodateien
- `scripts/build_playlist.py` – reproduzierbarer Auswahl- und Kopiervorgang

Die Auswahl umfasst 28 lokale Titel aus sieben elektronischen Familien. Identische Kopien wurden nach Dateigröße und Dateiname zusammengeführt. Die Originalbestände bleiben unverändert.

## Nutzung und Rechte

Die Audiodateien bleiben lokal und werden nicht in Git eingecheckt. Für eine öffentliche Ausstrahlung müssen die Senderechte und die beim FRS erforderliche Musikmeldung vorab geklärt werden. Dieses Repository enthält deshalb nur lokale Arbeitsmaterialien und Verweise auf die Originalbestände.

## Technischer Hinweis

Die M3U-Datei verwendet relative Pfade und funktioniert innerhalb dieses Repositorys. Wird der Ordner verschoben, muss die Playlist mit `python3 scripts/build_playlist.py` neu erzeugt werden.
