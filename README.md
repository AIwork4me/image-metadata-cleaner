# AIwork4me/image-metadata-cleaner

`image-metadata-cleaner` cleans privacy-sensitive metadata from user-owned
images by writing sanitized copies. The skill is designed for legitimate privacy
hygiene, file preparation, and reproducible publishing workflows.

It is not designed or documented for hiding authorship, evading provenance
checks, bypassing AI labels, or misrepresenting an image's origin.

## What it does

- Re-encodes image pixels into a fresh output file.
- Writes copies instead of modifying originals in place.
- Defaults folder output to `metadata-cleaned/`.
- Refuses output paths that resolve to the same file as the input.
- Produces a human-readable summary and optional JSON manifest.
- Reopens outputs and scans for common metadata keys and provenance marker
  strings.

## Install

Copy this folder to your Claude Code skills directory:

```bash
# Global, all projects
cp -r image-metadata-cleaner ~/.claude/skills/

# Or project-level only
cp -r image-metadata-cleaner your-project/.claude/skills/
```

The skill name exposed to Claude is `image-metadata-cleaner`, matching the
`AIwork4me/image-metadata-cleaner` repository and installation directory for
official skill validation.

## Use in Claude Code

Ask for privacy metadata cleanup of images you own or are authorized to process:

> Clean privacy metadata from this folder of product images.

Or invoke directly:

> /image-metadata-cleaner /path/to/folder --manifest

## CLI examples

Preview planned outputs:

```bash
uv run --with pillow==12.2.0 python scripts/strip.py /path/to/images --dry-run
```

Clean one file and write `photo-clean.png` or `photo-clean.jpg` beside it:

```bash
uv run --with pillow==12.2.0 python scripts/strip.py /path/to/photo.png --manifest
```

Clean a folder into `/path/to/images/metadata-cleaned/`:

```bash
uv run --with pillow==12.2.0 python scripts/strip.py /path/to/images --manifest
```

Choose JPEG output explicitly:

```bash
uv run --with pillow==12.2.0 python scripts/strip.py /path/to/images --format jpg
```

## Supported inputs

`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.tif`

## Verification scope

The script verifies that common metadata keys and common C2PA/JUMBF marker
strings are not visible in the output file. This is a practical hygiene check,
not a cryptographic guarantee.

It does not remove pixel-level watermarks, image fingerprints, external platform
records, or any provenance signal outside the image file itself.

## Development

Run tests:

```bash
uv run --with pillow==12.2.0 python -m unittest discover -s tests
```

## License

MIT-0
