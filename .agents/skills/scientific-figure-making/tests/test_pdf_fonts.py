"""Verify both embedded and genuinely missing composite font descriptors."""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_figure.py"
spec = importlib.util.spec_from_file_location("figure_check", SCRIPT)
checker = importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)


class FontTests(unittest.TestCase):
    def test_composite_font_embedding(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        with tempfile.TemporaryDirectory(prefix="agenthub-font-", dir=os.environ.get("AGENTHUB_TEST_ROOT")) as directory:
            root = Path(directory)
            source = root / "embedded.pdf"
            with plt.rc_context({"pdf.fonttype": 42}):
                fig, ax = plt.subplots(); ax.set_title("Embedded font evidence")
                fig.savefig(source); plt.close(fig)
            self.assertEqual(checker._check_pdf_fonts(str(source)), [])
            reader = PdfReader(source); writer = PdfWriter()
            writer.clone_document_from_reader(reader)
            for page in writer.pages:
                for reference in page["/Resources"]["/Font"].get_object().values():
                    font = reference.get_object()
                    for child in font.get("/DescendantFonts", []):
                        descriptor = child.get_object()["/FontDescriptor"].get_object()
                        for key in ["/FontFile", "/FontFile2", "/FontFile3"]:
                            descriptor.pop(NameObject(key), None)
            broken = root / "unembedded.pdf"
            with broken.open("wb") as handle: writer.write(handle)
            self.assertTrue(any(level == "WARN" for level, _ in checker._check_pdf_fonts(str(broken))))


if __name__ == "__main__":
    unittest.main()
