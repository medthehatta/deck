import os
from io import BytesIO
import hashlib
import subprocess
import tempfile


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


def mancer_upload_pils(pils):
    urls = []
    for pil in pils:
        buffered = BytesIO()
        pil.save(buffered, format="PNG")
        x = hashlib.sha1(buffered.getvalue()).hexdigest()
        with tempfile.NamedTemporaryFile("wb") as f:
            pil.save(f, format="PNG")
            remote_path = f"/var/www/files/deck/{x}.png"
            subprocess.check_call(
                f"rsync -p --chmod=F644 {f.name} med@mancer.in:{remote_path}",
                shell=True,
            )
        urls.append(f"https://files.mancer.in/deck/{x}.png")

    return urls
