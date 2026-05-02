from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, PngImagePlugin


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "strip.py"
SPEC = importlib.util.spec_from_file_location("strip", SCRIPT_PATH)
strip = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules["strip"] = strip
SPEC.loader.exec_module(strip)


class StripScriptTest(unittest.TestCase):
    def run_main(self, args: list[str]) -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return strip.main(args)

    def test_single_file_writes_copy_and_removes_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src = root / "source.png"
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("Software", "test-suite")
            Image.new("RGB", (12, 8), (10, 20, 30)).save(src, pnginfo=pnginfo)

            exit_code = self.run_main([str(src), "--manifest"])

            self.assertEqual(exit_code, 0)
            dest = root / "source-clean.png"
            manifest = root / "metadata-clean-report.json"
            self.assertTrue(src.exists())
            self.assertTrue(dest.exists())
            self.assertTrue(manifest.exists())
            reports = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(reports[0]["status"], "ok")
            self.assertEqual(reports[0]["metadata_keys_found"], [])
            self.assertEqual(reports[0]["dimensions"], [12, 8])

    def test_refuses_in_place_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src = root / "photo.jpg"
            Image.new("RGB", (10, 10), (255, 0, 0)).save(src)

            exit_code = self.run_main([str(src), "--output", str(src), "--json"])

            self.assertEqual(exit_code, 1)

    def test_folder_rerun_does_not_process_output_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            Image.new("RGB", (10, 10), (255, 0, 0)).save(root / "a.png")
            Image.new("RGB", (8, 12), (0, 255, 0)).save(root / "b.jpg")

            first = self.run_main([str(root), "--manifest"])
            second = self.run_main([str(root), "--manifest"])

            self.assertEqual(first, 0)
            self.assertEqual(second, 0)
            output_dir = root / "metadata-cleaned"
            outputs = {path.name for path in output_dir.glob("*") if path.is_file()}
            self.assertEqual(
                outputs,
                {"a-clean.png", "a-clean-1.png", "b-clean.jpg", "b-clean-1.jpg", "metadata-clean-report.json"},
            )
            self.assertFalse((root / "0.jpg").exists())

    def test_bad_image_reports_error_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            bad = root / "bad.png"
            bad.write_text("not an image", encoding="utf-8")

            report = strip.process_file(
                bad,
                fmt="preserve",
                output=None,
                output_dir=None,
                quality=95,
                overwrite=False,
                batch=False,
                dry_run=False,
            )

            self.assertEqual(report.status, "error")
            self.assertIsNotNone(report.error)
            self.assertFalse((root / "bad-clean.png").exists())


if __name__ == "__main__":
    unittest.main()
