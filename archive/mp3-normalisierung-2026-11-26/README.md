# FRS MP3-Normalisierung – 2026-11-26

Read-only-Erfassung der Sendungs-Audiodateien und Ablegen eines Schema-Stagings.
Die **Quelldateien wurden nicht verändert** (nur Lesen + separate Kopien).

## Schema

- Staging-Name: `frs-file-sha256-<erste 20 Hex-Zeichen des SHA-256>.mp3`
- Datei-ID ist eine *technische Byte-Identität*; eine semantische Objekt-ID bleibt offen.
- Metadaten (Titel/Interpret/Serie/Datum/Track/Genre) werden normalisiert in den
  Manifesten vorgeschlagen, aber nur mit `--write-tags` in Staging-Kopien geschrieben
  (hier **nicht** angewendet – keine Tag-Veränderung).

## Inhalte

| Datei | Zweck |
|---|---|
| `manifest.jsonl` | Vollständige Inventur inkl. Roh-ID3 und Warnungen |
| `manifest.csv` | Tabellenform (ohne Roh-ID3) |
| `manifest-staging.jsonl` | Manifest des Staging-Durchlaufs |

## Kennzahlen

- Dateien: **28** (alle MP3), Gesamtgröße **239.827.487 Bytes**
- ID3-Versionen: 2.3 = 24, 2.4 = 4
- Datum: keine verwertbare Angabe (fehlt oder unbrauchbar; 20× „unusable_id3_date")
- Warnungen: fehlende Serie 8, fehlender Titel 4, fehlender Interpret 2

## Staging

- Ort (NAS-Partition i7): `/mnt/2tb/media/frs-frequenzwechsel/staging`
- Vom Ryzen erreichbar: `/mnt/nas-2tb/media/frs-frequenzwechsel/staging` (≈ 230 MB)
- 28 Dateien mit kanonischen Namen,SHA-256-prüfbar gegen das Manifest.

## Repo-Hinweis

Audiodateien selbst sind bewusst per `.gitignore` ausgeschlossen (`*.mp3`,
`sendung_*/audio/*`); es werden nur Metadaten/Manifeste versioniert.
