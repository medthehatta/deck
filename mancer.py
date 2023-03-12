import os
from io import BytesIO
import hashlib


def mancer_pils(pils):
    urls = []
    for pil in pils:
        buffered = BytesIO()
        pil.save(buffered, format="PNG")
        x = hashlib.sha1(buffered.getvalue()).hexdigest()
        path = f"/var/www/files/deck/{x}.png"
        if not os.path.isfile(path):
            with open(path, "wb") as f:
                pil.save(f)
        urls.append(f"https://files.mancer.in/deck/{x}.png")

    return urls
