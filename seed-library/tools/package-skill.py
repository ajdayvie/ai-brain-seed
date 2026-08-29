#!/usr/bin/env python3
"""Build a .skill bundle from a master, for upload to the Claude account store.

    python tools/package-skill.py skills/<name>

Writes <name>.skill beside the skills/ folder and prints its SHA-256.

WARNING: do not build a bundle with PowerShell Compress-Archive. It writes backslash
path separators inside the zip, and the skills UI rejects the archive with an error
about characters in the path. That error points at the file's location rather than at
the bytes inside, so the wrong thing gets debugged. This packager uses zipfile, which
always writes a forward slash, and it checks the raw header bytes before it finishes.

The build is deterministic. Entries are sorted and every timestamp is fixed, so an
unchanged master rebuilds byte-identical. That turns "is the uploaded copy current?"
into a hash comparison instead of a memory test.
"""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

# Only these frontmatter keys round-trip through the skills UI. Extra keys can make an
# upload land the SKILL.md alone and silently drop every other file in the bundle.
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}

FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SKIP_NAMES = {".DS_Store", "Thumbs.db", ".keep"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_frontmatter(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        fail(f"{skill_md} has no YAML frontmatter block.")
    keys = set()
    for line in match.group(1).splitlines():
        found = re.match(r"^([A-Za-z0-9_-]+):", line)
        if found:
            keys.add(found.group(1))
    extra = keys - ALLOWED_FRONTMATTER_KEYS
    if extra:
        fail(
            f"{skill_md} frontmatter has keys the skills UI cannot accept: "
            f"{', '.join(sorted(extra))}. Keep only: name, description."
        )
    for required in ("name", "description"):
        if required not in keys:
            fail(f"{skill_md} frontmatter is missing the required key '{required}'.")
    name_line = re.search(r"^name:[ \t]*(\S+)[ \t]*$", match.group(1), re.MULTILINE)
    if not name_line:
        fail(f"{skill_md} has no single-word value for 'name:'.")
    return name_line.group(1)


def has_backslash_in_entry_names(raw: bytes) -> bool:
    """Scan local file headers for a backslash in the stored path.

    zipfile.namelist() normalizes a backslash to a forward slash on read, so it cannot
    see this defect. The raw bytes can.
    """
    marker = b"PK\x03\x04"
    at = raw.find(marker)
    while at != -1:
        name_length = int.from_bytes(raw[at + 26:at + 28], "little")
        start = at + 30
        if b"\\" in raw[start:start + name_length]:
            return True
        at = raw.find(marker, at + 4)
    return False


def collect(source: Path) -> list[Path]:
    files = [
        p for p in sorted(source.rglob("*"))
        if p.is_file() and p.name not in SKIP_NAMES
    ]
    if not files:
        fail(f"{source} holds no files to package.")
    return files


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: python tools/package-skill.py skills/<name>")

    source = Path(sys.argv[1]).resolve()
    if not source.is_dir():
        fail(f"{source} is not a folder.")

    skill_md = source / "SKILL.md"
    if not skill_md.is_file():
        fail(f"{source} has no SKILL.md.")

    declared = check_frontmatter(skill_md)
    if declared != source.name:
        fail(
            f"frontmatter name '{declared}' does not match the folder name "
            f"'{source.name}'. They must agree."
        )

    build_notes = source / "BUILD.md"
    if build_notes.is_file():
        fail(
            f"{build_notes} is inside the skill folder. Build notes go BESIDE it, as "
            f"{source.name}.BUILD.md, or the packager sweeps them into the bundle."
        )

    files = collect(source)
    out = source.parent / f"{source.name}.skill"

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            arcname = f"{source.name}/{path.relative_to(source).as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIMESTAMP)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, path.read_bytes())

    raw = out.read_bytes()
    if has_backslash_in_entry_names(raw):
        fail(f"{out} stores a backslash path separator. Do not upload it.")

    digest = hashlib.sha256(raw).hexdigest()
    print(f"wrote {out} ({out.stat().st_size:,} bytes, {len(files)} entries)")
    for path in files:
        print(f"  {source.name}/{path.relative_to(source).as_posix()}")
    print(f"sha256 {digest}")
    print("Record that hash and today's date in the skill's BUILD.md when you upload it.")


if __name__ == "__main__":
    main()
