import os

from layout import portrait_cards_on_letter
from pdf import merge_pils_to_pdf


class Emitter:

    def __init__(self, generator, client):
        self.generator = generator
        self.client = client

    def pdf_sample(output_path):
        # Join all the card types
        rendered = sum(self.generator.render(self.client).values(), [])
        # Merge to one PDF
        return merge_pils_to_pdf(
            portrait_cards_on_letter(rendered),
            output_path,
        )

    def sheet_image_sample(output_path, ext="png"):
        rendered = sum(self.generator.render(self.client).values(), [])
        pages = portrait_cards_on_letter(rendered)
        if not os.path.isdir(output_path):
            os.makedirs(output_path, exist_ok=True)
        for (i, page) in enumerate(pages, start=1):
            page.save(os.path.join(output_path, f"page{i}.{ext}"))
        return pages
