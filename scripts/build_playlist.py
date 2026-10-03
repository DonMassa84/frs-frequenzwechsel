#!/usr/bin/env python3
"""Build a local, numbered FRS electronic pilot playlist from the mounted collection."""
from pathlib import Path
import csv, hashlib, os, shutil

ROOT = Path('/mnt/storage/03_MEDIEN/schattenmacher/Musik')
OUT = Path(__file__).resolve().parents[1]
AUDIO = OUT / 'sendung_01' / 'audio'
EXT = {'.mp3', '.m4a', '.flac', '.ogg'}
GENRES = {
    '01_deep-house': ['deep house', 'chilled house', 'lounge house'],
    '02_house': ['/house/', 'vocal house', 'classic house'],
    '03_techno': ['techno', 'schranz', 'minimal'],
    '04_trance': ['trance', 'goa', 'psytrance', 'progressive'],
    '05_electro': ['electro', 'electronica', 'synth'],
    '06_edm-dance': ['edm', 'dance', 'club', 'hardstyle', 'rave'],
    '07_downtempo': ['ambient', 'chillout', 'balearic', 'cosmic'],
}
EXCLUDE = ['aevo', 'hörbuch', 'metal', 'rock', 'podcast', 'unterweisung']

def key_for(path: Path):
    st = path.stat()
    return (st.st_size, path.name.casefold())

def genre_for(path: Path):
    s = ('/' + str(path.relative_to(ROOT)).casefold()).replace('\\', '/')
    if any(x in s for x in EXCLUDE):
        return None
    for genre, needles in GENRES.items():
        if any(n in s for n in needles):
            return genre
    return None

files = []
seen = set()
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.casefold() not in EXT:
        continue
    g = genre_for(p)
    if not g:
        continue
    k = key_for(p)
    if k in seen:
        continue
    seen.add(k)
    files.append((g, p))

selected = []
for genre in GENRES:
    candidates = sorted((p for g, p in files if g == genre), key=lambda p: (len(p.name), str(p).casefold()))
    # Four contrasting tracks per electronic family; deterministic and reviewable.
    selected.extend((genre, p) for p in candidates[:4])

if len(selected) < 20:
    raise SystemExit(f'Only {len(selected)} suitable tracks found')

AUDIO.mkdir(parents=True, exist_ok=True)
rows = []
for number, (genre, source) in enumerate(selected, 1):
    dest = AUDIO / f'{number:02d}__{source.stem}{source.suffix.lower()}'
    shutil.copy2(source, dest)
    rows.append((number, genre, str(source), str(dest.relative_to(OUT)), source.stat().st_size, hashlib.sha256(dest.read_bytes()).hexdigest()))

with (OUT / 'playlists' / 'sendung_01_frs_frequenzwechsel.m3u').open('w', encoding='utf-8') as f:
    f.write('#EXTM3U\n')
    for number, genre, source, rel, size, digest in rows:
        f.write(f'{rel}\n')

with (OUT / 'playlists' / 'sendung_01_manifest.csv').open('w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['nr', 'genre', 'source', 'local_copy', 'bytes', 'sha256'])
    w.writerows(rows)

print(f'copied {len(rows)} tracks, {sum(r[4] for r in rows)} bytes')
