---
name: image-metadata-cleaner
description: "Clean privacy-sensitive metadata from user-owned images by writing sanitized copies. Use only when the user explicitly asks to remove image metadata for privacy, publishing hygiene, or file-size cleanup. Do not use to hide AI authorship, evade provenance checks, bypass platform labels, or misrepresent an image's origin."
license: MIT-0
metadata:
  version: "3.0.0"
  author: "aiwork4me"
  reviewed-for: "Claude Code Skills safety and quality"
---

# AIwork4me/image-metadata-cleaner

`image-metadata-cleaner` cleans privacy-sensitive metadata from user-owned image
files by writing separate sanitized copies. This skill is for privacy hygiene
and reproducible file preparation, not for hiding authorship, evading provenance
checks, bypassing platform labels, or misrepresenting where an image came from.

## Safety boundary

- Use this skill only for images the user owns or is authorized to process.
- Do not run it for requests whose stated purpose is to bypass AI labels,
  defeat detection systems, fake provenance, or violate a platform's disclosure
  rules. In those cases, explain that you can help with privacy-preserving
  metadata cleanup, but not deception or evasion.
- Never edit the original image in place. The script refuses an output path that
  resolves to the same file as the input.
- Do not use `--overwrite` unless the user explicitly asks to replace existing
  output copies.

## Before running

Confirm the input path, output location, and output format unless the user
explicitly invoked this skill with those arguments. If the request is a folder
operation, prefer the default `metadata-cleaned/` output folder so generated
copies are separated from source files.

Run a dry run when the user asks to preview changes:

```bash
uv run --with pillow==12.2.0 python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<file-or-folder>" --dry-run
```

## Execution

Single file, safe default output name beside the input:

```bash
uv run --with pillow==12.2.0 python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<file_path>" --manifest
```

Single file with an explicit output file:

```bash
uv run --with pillow==12.2.0 python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<file_path>" --output "<output_path>" --manifest
```

Folder batch, writing copies into `<folder>/metadata-cleaned/`:

```bash
uv run --with pillow==12.2.0 python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<folder_path>" --manifest
```

Recursive folder batch with a separate output directory:

```bash
uv run --with pillow==12.2.0 python "${CLAUDE_SKILL_DIR}/scripts/strip.py" "<folder_path>" --recursive --output-dir "<output_folder>" --manifest
```

Output format defaults to `preserve`: JPEG inputs stay JPEG, and other supported
formats are written as PNG to avoid unexpected lossy conversion. If the user
provides an explicit `--output` path ending in `.jpg`, `.jpeg`, or `.png`, the
script follows that extension unless `--format` is set. Use `--format jpg` only
when the user explicitly wants JPEG output; transparent images will be
composited onto a white background.

## After running

Report the script results without overstating them:

1. Number of files processed, previewed in dry-run mode, or failed.
2. Output filenames and where the manifest was written.
3. File size before and after.
4. Dimensions reported after re-encoding.
5. Whether the verification scan found common metadata keys or provenance marker
   strings in the output.

Do not claim that all possible watermarks or provenance signals were removed.
The script removes file-level metadata visible to Pillow-style re-encoding and
performs a basic marker scan; it does not remove pixel-level watermarks,
fingerprints, or external platform records.

## Supported inputs

`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.tif`

## Troubleshooting

- **No supported image files found**: The folder contains no files with supported
  image extensions, or all candidates are inside the output directory.
- **Output already exists**: The user supplied an explicit output path that
  exists. Choose another path or rerun with `--overwrite` only after user
  confirmation.
- **Unsupported image / cannot identify image file**: The file extension looks
  supported, but Pillow could not decode the file. Report the file and continue
  with any other batch items.
- **uv not available**: Ask the user before falling back to a local Python
  environment with Pillow installed.

## Technical details

For implementation notes, verification limits, and metadata caveats, read
`references/technical-details.md`.
