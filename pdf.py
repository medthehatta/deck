import os
from tempfile import TemporaryDirectory

from PyPDF2 import PdfFileMerger


def merge_pils_to_pdf(pils, path):
    pdf = PdfFileMerger()
    with TemporaryDirectory() as prefix:
        for (i, pil) in enumerate(pils):
            name = os.path.join(prefix, f"out{i}.pdf")
            pil.save(name, subsampling=0, quality=100)
            pdf.append(name)
        pdf.write(path)
    return pdf
