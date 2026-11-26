#!/usr/bin/env python3
"""FRS MP3 normalisation prototype.

PRE_PROJECT / prototype utility:
- scans MP3 files read-only,
- records raw ID3 evidence without implicit frame translation,
- normalises selected textual metadata into a canonical manifest,
- identifies concrete file bytes with SHA-256,
- keeps semantic/object identity explicitly unresolved,
- optionally copies files into a separate staging tree,
- optionally writes selected tags only to staged copies and only with an explicit ID3 target version.

The source files are never modified.
No assumptions are made about the final FRS inventory, Drupal schema, rights model,
or the final relationship between broadcasts, episodes and media files.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Iterable, Optional


CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]+")
SPACE_RE = re.compile(r"\s+")
BAD_FILENAME_RE = re.compile(r'[<>:"/\\|?*]+')
MULTI_SEP_RE = re.compile(r"[-_.]{2,}")
DATE_PATTERNS = (
    re.compile(r"(?<!\d)(20\d{2})[-_.](0[1-9]|1[0-2])[-_.](0[1-9]|[12]\d|3[01])(?!\d)"),
    re.compile(r"(?<!\d)(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)"),
    re.compile(r"(?<!\d)(0[1-9]|[12]\d|3[01])[.-](0[1-9]|1[0-2])[.-](20\d{2})(?!\d)"),
)


@dataclass
class AudioRecord:
    schema_version: str
    semantic_object_id: Optional[str]
    file_id: str
    source_path: str
    source_name: str
    sha256: str
    size_bytes: int
    id3_version: Optional[str]
    raw_id3: dict[str, str] = field(default_factory=dict)
    title_raw: str = ""
    title: str = ""
    creator_raw: str = ""
    creator: str = ""
    series_raw: str = ""
    series_candidate: str = ""
    date_raw: str = ""
    date: str = ""
    date_source: str = "unknown"
    date_confidence: str = "unknown"
    track_raw: str = ""
    track: str = ""
    genre_raw: str = ""
    genre: str = ""
    comment_raw: str = ""
    comment: str = ""
    duration_seconds: Optional[float] = None
    bitrate_kbps: Optional[int] = None
    sample_rate_hz: Optional[int] = None
    channels: Optional[int] = None
    proposed_staging_name: str = ""
    warnings: list[str] = field(default_factory=list)


def normalize_text(value: object) -> str:
    """Return conservative NFC-normalised single-line text."""
    if value is None:
        return ""
    text = unicodedata.normalize("NFC", str(value))
    text = CONTROL_RE.sub(" ", text)
    text = SPACE_RE.sub(" ", text).strip()
    return text


def safe_component(value: str, fallback: str = "unbekannt", max_length: int = 96) -> str:
    """Create a portable path component without changing semantic text more than needed."""
    value = normalize_text(value)
    value = BAD_FILENAME_RE.sub("-", value)
    value = value.replace("..", ".")
    value = SPACE_RE.sub("_", value)
    value = MULTI_SEP_RE.sub("-", value).strip(" .-_")
    if not value:
        value = fallback
    if value.upper() in {"CON", "PRN", "AUX", "NUL", "COM1", "LPT1"}:
        value = "_" + value
    return value[:max_length].rstrip(" .-_")


def valid_iso_date(value: str) -> str:
    value = normalize_text(value)
    if not value:
        return ""
    match = re.fullmatch(
        r"(20\d{2}-\d{2}-\d{2})(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:\d{2})?)?",
        value,
    )
    if not match:
        return ""
    candidate = match.group(1)
    try:
        date.fromisoformat(candidate)
        if value != candidate:
            datetime.fromisoformat(value)
    except ValueError:
        return ""
    return candidate


def date_from_filename(name: str) -> str:
    stem = Path(name).stem
    for index, pattern in enumerate(DATE_PATTERNS):
        match = pattern.search(stem)
        if not match:
            continue
        if index < 2:
            year, month, day = match.groups()
        else:
            day, month, year = match.groups()
        candidate = f"{year}-{month}-{day}"
        try:
            date.fromisoformat(candidate)
            return candidate
        except ValueError:
            continue
    return ""


def choose_date(tag_date: str, filename: str) -> tuple[str, str, str]:
    """Choose a date conservatively and expose provenance/confidence."""
    tag_iso = valid_iso_date(tag_date)
    file_iso = date_from_filename(filename)
    if tag_iso and file_iso and tag_iso == file_iso:
        return tag_iso, "id3+filename", "high"
    if tag_iso:
        return tag_iso, "id3", "medium" if not file_iso else "conflict"
    if file_iso:
        return file_iso, "filename", "low"
    return "", "unknown", "unknown"


def stat_signature(path: Path) -> tuple[int, int, int, int]:
    stat = path.stat()
    return (stat.st_size, stat.st_mtime_ns, stat.st_dev, stat.st_ino)


def reject_symlinks(path: Path) -> None:
    """Reject existing symlinks in every component of a local working path."""
    absolute = path.absolute()
    for component in (*reversed(absolute.parents), absolute):
        if component.is_symlink():
            raise RuntimeError(f"Symlink ist hier nicht zulässig: {component}")


def paths_overlap(first: Path, second: Path) -> bool:
    return first.is_relative_to(second) or second.is_relative_to(first)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_id_from_sha256(digest: str) -> str:
    """Technical file-byte identifier; not a semantic archive-object ID."""
    return f"frs-file-sha256-{digest[:20]}"


def frame_text(tags: object, key: str) -> str:
    if tags is None:
        return ""
    try:
        value = tags.get(key)
    except AttributeError:
        return ""
    if value is None:
        return ""
    text = getattr(value, "text", value)
    if isinstance(text, (list, tuple)):
        return str(text[0]) if text else ""
    return str(text)


def extract_comment(tags: object) -> str:
    if tags is None:
        return ""
    try:
        keys = list(tags.keys())
    except AttributeError:
        return ""
    for key in keys:
        if str(key).startswith("COMM"):
            return frame_text(tags, key)
    return ""


def raw_id3_snapshot(tags: object) -> dict[str, str]:
    if tags is None:
        return {}
    snapshot: dict[str, str] = {}
    for key in sorted(tags.keys(), key=str):
        frame = tags.get(key)
        if frame is None:
            continue
        try:
            snapshot[str(key)] = frame.pprint()
        except Exception:
            snapshot[str(key)] = repr(frame)
    return snapshot


def read_mp3(path: Path, base: Path) -> AudioRecord:
    reject_symlinks(path)
    if not path.resolve().is_relative_to(base.resolve()):
        raise RuntimeError("Quelldatei liegt außerhalb des Inventarverzeichnisses")
    try:
        from mutagen.id3 import ID3, ID3NoHeaderError
        from mutagen.mp3 import MP3
    except ImportError as exc:
        raise RuntimeError(
            "Mutagen fehlt. Installieren mit: "
            "python -m pip install -r 12_prototype_frs_archive/requirements.txt"
        ) from exc

    before = stat_signature(path)
    digest = sha256_file(path)

    try:
        tags = ID3(path, translate=False)
        id3_version = ".".join(str(part) for part in tags.version)
    except ID3NoHeaderError:
        tags = None
        id3_version = None

    audio = MP3(path)
    info = audio.info

    title_raw = frame_text(tags, "TIT2")
    creator_raw = frame_text(tags, "TPE1")
    series_raw = frame_text(tags, "TALB") or frame_text(tags, "TIT1")
    date_raw = frame_text(tags, "TDRC") or frame_text(tags, "TYER")
    track_raw = frame_text(tags, "TRCK")
    genre_raw = frame_text(tags, "TCON")
    comment_raw = extract_comment(tags)

    title = normalize_text(title_raw)
    creator = normalize_text(creator_raw)
    series_candidate = normalize_text(series_raw)
    track = normalize_text(track_raw)
    genre = normalize_text(genre_raw)
    comment = normalize_text(comment_raw)

    chosen_date, date_source, confidence = choose_date(date_raw, path.name)
    warnings: list[str] = []
    if not title:
        warnings.append("missing_title")
    if not creator:
        warnings.append("missing_creator")
    if not series_candidate:
        warnings.append("missing_series")
    if confidence == "conflict":
        warnings.append("date_conflict_id3_filename")
    if date_raw and not valid_iso_date(date_raw):
        warnings.append("unusable_id3_date")
    if not chosen_date:
        warnings.append("missing_date")
    if tags is None:
        warnings.append("missing_id3")

    after = stat_signature(path)
    if before != after:
        raise RuntimeError("Quelle während der Erfassung verändert")

    file_id = file_id_from_sha256(digest)
    proposed_staging_name = f"{file_id}.mp3"

    return AudioRecord(
        schema_version="0.2-preproject",
        semantic_object_id=None,
        file_id=file_id,
        source_path=str(path.relative_to(base)),
        source_name=path.name,
        sha256=digest,
        size_bytes=before[0],
        id3_version=id3_version,
        raw_id3=raw_id3_snapshot(tags),
        title_raw=title_raw,
        title=title,
        creator_raw=creator_raw,
        creator=creator,
        series_raw=series_raw,
        series_candidate=series_candidate,
        date_raw=date_raw,
        date=chosen_date,
        date_source=date_source,
        date_confidence=confidence,
        track_raw=track_raw,
        track=track,
        genre_raw=genre_raw,
        genre=genre,
        comment_raw=comment_raw,
        comment=comment,
        duration_seconds=round(float(info.length), 3) if getattr(info, "length", None) else None,
        bitrate_kbps=round(int(info.bitrate) / 1000) if getattr(info, "bitrate", None) else None,
        sample_rate_hz=int(info.sample_rate) if getattr(info, "sample_rate", None) else None,
        channels=int(info.channels) if getattr(info, "channels", None) else None,
        proposed_staging_name=proposed_staging_name,
        warnings=warnings,
    )


def discover_mp3(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() == ".mp3":
            yield path


def write_jsonl(records: list[AudioRecord], path: Path) -> None:
    reject_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(records: list[AudioRecord], path: Path) -> None:
    reject_symlinks(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [name for name in AudioRecord.__dataclass_fields__ if name != "raw_id3"]
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            row = asdict(record)
            row.pop("raw_id3", None)
            row["warnings"] = "|".join(row["warnings"])
            writer.writerow(row)


def write_normalized_tags(target: Path, record: AudioRecord, id3_version: int) -> None:
    """Write selected fields to a staged copy, never to the source."""
    from mutagen.id3 import ID3, ID3NoHeaderError, TALB, TCON, TDRC, TIT2, TPE1, TRCK

    try:
        tags = ID3(target, translate=False)
    except ID3NoHeaderError:
        tags = ID3()

    if id3_version == 4:
        tags.update_to_v24()
    else:
        tags.update_to_v23()

    encoding = 3 if id3_version == 4 else 1
    if record.title:
        tags.setall("TIT2", [TIT2(encoding=encoding, text=[record.title])])
    if record.creator:
        tags.setall("TPE1", [TPE1(encoding=encoding, text=[record.creator])])
    if record.series_candidate:
        tags.setall("TALB", [TALB(encoding=encoding, text=[record.series_candidate])])
    if record.date:
        tags.setall("TDRC", [TDRC(encoding=encoding, text=[record.date])])
    if record.track:
        tags.setall("TRCK", [TRCK(encoding=encoding, text=[record.track])])
    if record.genre:
        tags.setall("TCON", [TCON(encoding=encoding, text=[record.genre])])

    tags.save(target, v2_version=id3_version, v1=0)


def stage_files(
    records: list[AudioRecord], root: Path, stage: Path, write_tags: bool, id3_version: Optional[int]
) -> None:
    reject_symlinks(stage)
    root, stage = root.resolve(), stage.resolve()
    if paths_overlap(root, stage):
        raise RuntimeError("Quelle und Staging müssen getrennte Verzeichnisse sein")
    if write_tags and id3_version not in {3, 4}:
        raise RuntimeError("Tag-Schreiben erfordert ID3-Zielversion 3 oder 4")
    # Preflight the complete batch; an existing collision must not leave an
    # earlier copy behind. Equal bytes at multiple paths share one target.
    plan: dict[str, tuple[AudioRecord, Path, Path]] = {}
    for record in records:
        relative = Path(record.source_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"Ungültiger relativer Herkunftspfad: {record.source_path}")
        source = root / relative
        reject_symlinks(source)
        if not source.resolve().is_relative_to(root):
            raise RuntimeError(f"Quelle außerhalb des Inventarverzeichnisses: {source}")
        expected = file_id_from_sha256(record.sha256) + ".mp3"
        if record.file_id != file_id_from_sha256(record.sha256) or record.proposed_staging_name != expected:
            raise RuntimeError("Staging-Name passt nicht zur technischen Dateiidentität")
        target = stage / record.proposed_staging_name
        if target.exists() or target.is_symlink():
            raise RuntimeError(f"Zieldatei existiert bereits; kein Überschreiben: {target}")
        if sha256_file(source) != record.sha256:
            raise RuntimeError(f"Quelle seit Inventarisierung verändert: {source}")
        previous = plan.get(record.proposed_staging_name)
        if previous:
            prior_record = previous[0]
            if prior_record.sha256 != record.sha256:
                raise RuntimeError("Kollision gekürzter Datei-IDs bei unterschiedlichem SHA-256")
            if write_tags and any(
                getattr(prior_record, name) != getattr(record, name)
                for name in ("title", "creator", "series_candidate", "date", "track", "genre")
            ):
                raise RuntimeError("Gleiche Dateibytes mit widersprüchlichen Tag-Kandidaten")
            continue
        plan[record.proposed_staging_name] = (record, source, target)

    stage.mkdir(parents=True, exist_ok=True)
    for record, source, target in plan.values():
        with source.open("rb") as src, target.open("xb") as dst:
            shutil.copyfileobj(src, dst)

        if sha256_file(target) != record.sha256:
            target.unlink(missing_ok=True)
            raise RuntimeError(f"Staging-Kopie weicht von Quelle ab: {target}")

        if write_tags:
            assert id3_version in {3, 4}
            write_normalized_tags(target, record, id3_version)

        if sha256_file(source) != record.sha256:
            raise RuntimeError(f"Original wurde während Staging verändert: {source}")


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MP3-Bestand read-only inventarisieren und normalisierte Metadaten vorschlagen."
    )
    parser.add_argument("source", type=Path, help="Quellverzeichnis mit MP3-Dateien")
    parser.add_argument("--manifest", type=Path, default=Path("mp3-normalized.jsonl"))
    parser.add_argument("--csv", dest="csv_path", type=Path)
    parser.add_argument("--copy-to", type=Path, help="Optional: unveränderte Dateien in separates Staging kopieren")
    parser.add_argument(
        "--write-tags",
        action="store_true",
        help="Ausgewählte normalisierte Tags ausschließlich in Staging-Kopien schreiben",
    )
    parser.add_argument(
        "--id3-version",
        type=int,
        choices=[3, 4],
        help="Explizites Zielprofil für --write-tags; vor FRS-Bestandsaufnahme nicht vorentscheiden",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    source = args.source.resolve()
    if not source.is_dir():
        print(f"FEHLER: Quellverzeichnis fehlt: {source}", file=sys.stderr)
        return 2
    if args.write_tags and not args.copy_to:
        print("FEHLER: --write-tags ist nur zusammen mit --copy-to zulässig.", file=sys.stderr)
        return 2
    if args.write_tags and args.id3_version not in {3, 4}:
        print("FEHLER: --write-tags erfordert --id3-version 3 oder 4.", file=sys.stderr)
        return 2
    if args.id3_version and not args.write_tags:
        print("FEHLER: --id3-version ist nur zusammen mit --write-tags zulässig.", file=sys.stderr)
        return 2
    try:
        outputs = [args.manifest] + ([args.csv_path] if args.csv_path else [])
        for output in outputs:
            reject_symlinks(output)
            if output.resolve().is_relative_to(source):
                raise RuntimeError("Ausgabedateien dürfen nicht im Quellverzeichnis liegen")
            if output.exists():
                raise RuntimeError(f"Ausgabedatei existiert bereits: {output}")
        if len({path.resolve() for path in outputs}) != len(outputs):
            raise RuntimeError("Manifest und CSV benötigen verschiedene Ausgabepfade")
        if args.copy_to:
            reject_symlinks(args.copy_to)
            if paths_overlap(args.copy_to.resolve(), source):
                raise RuntimeError("Quelle und Staging müssen getrennte Verzeichnisse sein")
            if any(path.resolve().is_relative_to(args.copy_to.resolve()) for path in outputs):
                raise RuntimeError("Inventarausgaben müssen außerhalb des Stagings liegen")
    except (OSError, RuntimeError) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2

    paths = list(discover_mp3(source))
    records: list[AudioRecord] = []
    failures: list[dict[str, str]] = []
    for path in paths:
        try:
            records.append(read_mp3(path, source))
        except Exception as exc:
            failures.append({"source_path": str(path.relative_to(source)), "error": str(exc)})

    try:
        write_jsonl(records, args.manifest)
        if args.csv_path:
            write_csv(records, args.csv_path)
        if args.copy_to:
            stage_files(records, source, args.copy_to, args.write_tags, args.id3_version)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 2

    summary = {
        "mode": "staging-copy" if args.copy_to else "read-only-inventory",
        "mp3_found": len(paths),
        "normalised": len(records),
        "failed": len(failures),
        "manifest": str(args.manifest),
        "source_modified": False,
        "semantic_object_ids_assigned": False,
        "failures": failures,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
