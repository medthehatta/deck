import base64
from io import BytesIO
import json


from authentication import ApiKey
from authentication import BasicAuth
from httprr import Requester
from httprr import DefaultHandlers


def get_client_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return Requester(
        "https://api.image4.io/v1.0",
        BasicAuth(data["key"], data["secret"]),
    )


class Image4io:

    def __init__(self, cred_json_path, fmt="JPEG"):
        self.client = get_client_from_json(cred_json_path)
        self.fmt = fmt

    def _pil_binary(self, pil):
        buffered = BytesIO()
        pil.save(buffered, format=self.fmt)
        return buffered.getvalue()

    def upload_pil(self, pil):
        data = {
            "overwrite": "true",
            "useFilename": "false",
            "path": "/deck",
            "file": self._pil_binary(pil),
        }
        file_data = self._pil_binary(pil)
        return self.client.request(
            "POST",
            "uploadImage",
            data=data,
            files={"file": file_data},
        )

    def upload_pil_get_url(self, pil):
        res = self.upload_pil(pil)
        res.raise_for_status()
        return res.json()["uploadedFiles"][0]["url"]


def get_default():
    # FIXME: Ugh, configuring the client is painful.  Just setting it as a
    # constant from the file for now
    return Image4io("image4io.json")
