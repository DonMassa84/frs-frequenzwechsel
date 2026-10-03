# FRS Frequenzwechsel

Lokale Musikvorbereitung für eine elektronische Sendung beim Freien Radio Stuttgart.

## Sendungsprofil

**FRS Frequenzwechsel** verbindet Deep House, House, Techno, Trance, Electro, EDM/Dance und ruhige elektronische Übergänge. Die erste Auswahl ist als musikalische Reise aufgebaut: Ankommen, Groove, Verdichtung, Nachtfahrt und Ausklang.

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
