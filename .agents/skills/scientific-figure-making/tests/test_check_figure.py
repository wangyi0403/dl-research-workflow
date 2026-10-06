"""Regression coverage for incomplete checks, PDF sizing and raster compatibility."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
from pypdf import PdfWriter
from pypdf.generic import FloatObject, NameObject, RectangleObject

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'check_figure.py'
spec = importlib.util.spec_from_file_location('figure_check', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class FigureCheckTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='agenthub-figure-', dir=os.environ.get('AGENTHUB_TEST_ROOT'))
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def pdf(self, name='figure.pdf', size=(3.5, 2.625), rotate=0, user_unit=1):
        writer = PdfWriter()
        page = writer.add_blank_page(width=size[0] * 72 / user_unit, height=size[1] * 72 / user_unit)
        if rotate:
            page.rotate(rotate)
        page[NameObject('/UserUnit')] = FloatObject(user_unit)
        path = self.root / name
        with path.open('wb') as handle:
            writer.write(handle)
        return path

    def cli(self, path, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(path), *args], capture_output=True, text=True)

    def verdict(self, issues, info):
        with contextlib.redirect_stdout(io.StringIO()):
            return checker.print_report('test', issues, info)

    def test_corrupt_pdf_fails_strict(self):
        path = self.root / 'corrupt.pdf'
        path.write_bytes(b'%PDF-1.4\nnot a valid pdf')
        result = self.cli(path, '--strict')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('FAIL', result.stdout)

    def test_pdf_matching_dimensions_pass(self):
        path = self.pdf()
        issues, info = checker.check_figure(str(path), target_inches=(3.5, 2.625))
        self.assertEqual(self.verdict(issues, info), 'PASS')
        self.assertEqual(info['page_sizes_inches'], [(3.5, 2.625)])
        self.assertEqual(self.cli(path, '--strict', '--width-in', '3.5', '--height-in', '2.625').returncode, 0)

    def test_pdf_mismatched_dimensions_fail(self):
        result = self.cli(self.pdf(), '--strict', '--width-in', '7', '--height-in', '5.25')
        self.assertEqual(result.returncode, 2)
        self.assertIn('visible size', result.stdout)

    def test_pdf_rotation_and_user_unit(self):
        path = self.pdf(rotate=90, user_unit=2)
        issues, info = checker.check_figure(str(path), target_inches=(2.625, 3.5))
        self.assertEqual(self.verdict(issues, info), 'PASS')
        self.assertEqual(info['page_sizes_inches'], [(2.625, 3.5)])

    def test_cropbox_is_visible_size(self):
        writer = PdfWriter()
        page = writer.add_blank_page(width=720, height=720)
        page[NameObject('/CropBox')] = RectangleObject([10, 20, 262, 209])
        path = self.root / 'crop.pdf'
        with path.open('wb') as handle:
            writer.write(handle)
        issues, info = checker.check_figure(str(path), target_inches=(3.5, 2.625))
        self.assertEqual(self.verdict(issues, info), 'PASS')

    def test_missing_pdf_dependencies_is_unknown_and_exit_three(self):
        path = self.pdf()
        with patch.dict(sys.modules, {'pypdf': None, 'PyPDF2': None}):
            issues, info = checker.check_figure(str(path))
            self.assertEqual(self.verdict(issues, info), 'UNKNOWN')
            with patch.object(sys, 'argv', [str(SCRIPT), str(path), '--strict']), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(checker._cli(), 3)

    def test_raster_metadata_and_low_dpi(self):
        path = self.root / 'figure.png'
        Image.new('RGB', (1050, 788), 'white').save(path, dpi=(300, 300))
        issues, info = checker.check_figure(str(path), target_inches=(3.5, 2.625))
        self.assertEqual(self.verdict(issues, info), 'PASS')
        Image.new('RGB', (1050, 788), 'white').save(path, dpi=(100, 100))
        self.assertEqual(self.cli(path, '--strict').returncode, 2)

    def test_raster_missing_dpi_can_use_display_size(self):
        path = self.root / 'figure.png'
        Image.new('RGB', (1050, 788), 'white').save(path)
        issues, info = checker.check_figure(str(path))
        self.assertEqual(self.verdict(issues, info), 'UNKNOWN')
        issues, info = checker.check_figure(str(path), target_inches=(3.5, 2.625))
        self.assertEqual(self.verdict(issues, info), 'WARN')
        issues, info = checker.check_figure(str(path), target_inches=(7, 5.25))
        self.assertEqual(self.verdict(issues, info), 'FAIL')

    def test_missing_pillow_is_unknown(self):
        path = self.root / 'figure.png'
        Image.new('RGB', (300, 300)).save(path, dpi=(300, 300))
        with patch.dict(sys.modules, {'PIL': None}):
            issues, info = checker.check_figure(str(path))
            self.assertEqual(self.verdict(issues, info), 'UNKNOWN')

    def test_cli_rejects_partial_or_invalid_dimensions(self):
        path = self.pdf()
        self.assertEqual(self.cli(path, '--width-in', '3.5').returncode, 2)
        self.assertEqual(self.cli(path, '--width-in', 'nan', '--height-in', '1').returncode, 2)

    def test_corrupt_raster_fails(self):
        path = self.root / 'bad.png'
        path.write_bytes(b'not an image')
        self.assertEqual(self.cli(path, '--strict').returncode, 2)

    def test_unsupported_eps_cannot_pass(self):
        path = self.root / 'figure.eps'
        path.write_text('%!PS-Adobe-3.0 EPSF-3.0', encoding='utf-8')
        self.assertEqual(self.cli(path, '--strict').returncode, 3)


if __name__ == '__main__':
    unittest.main()
