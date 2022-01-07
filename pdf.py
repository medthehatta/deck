import os
from tempfile import TemporaryDirectory

from PyPDF2 import PdfFileMerger


def merge_pdfs(pdf_paths, output):
    pdf = PdfFileMerger()
    for pdf_path in pdf_paths:
        pdf.append(pdf_path)
    pdf.write(output)
    return pdf


def merge_pils_to_pdf(pils, outfile):
    pdf_names = []
    with TemporaryDirectory() as prefix:
        for (i, pil) in enumerate(pils):
            name = os.path.join(prefix, f"out{i}.pdf")
            pil.save(name, subsampling=0, quality=100)
            pdf_names.append(name)
        return merge_pdfs(pdf_names, outfile)
