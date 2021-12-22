import os

from layout import portrait_cards_on_letter
from pdf import merge_pils_to_pdf


class Emitter:

    def __init__(self, generator, client):
        self.generator = generator
        self.client = client

    def render(self):
        return self.generator.render(self.client)

    def render_flat(self):
        return sum(self.render().values(), [])

    def pdf_sample(self, output_path):
        # Render card types into separate PDFs
        # Join all the card types
        rendered = self.render_flat()
        # Merge to one PDF
        return merge_pils_to_pdf(
            portrait_cards_on_letter(rendered),
            output_path,
        )

    def sheet_image_sample(self, output_path, ext="png"):
        rendered = self.render_flat()
        pages = portrait_cards_on_letter(rendered)
        if not os.path.isdir(output_path):
            os.makedirs(output_path, exist_ok=True)
        for (i, page) in enumerate(pages, start=1):
            page.save(os.path.join(output_path, f"page{i}.{ext}"))
        return pages
