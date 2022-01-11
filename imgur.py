import base64
from io import BytesIO


from authentication import ApiKey
from httprr import Requester
from httprr import DefaultHandlers


#DEFAULT_IMGUR_CLIENT_ID = "54bdf86b7b696fe"
DEFAULT_IMGUR_CLIENT_ID = "10123ac4cd0c5b5"


def get_client_v3(client_id):
    return Requester(
        "https://api.imgur.com/3",
        ApiKey("Authorization", f"Client-ID {client_id}"),
    )


class Imgur:

    def __init__(self, client_id, fmt="JPEG"):
        self.client = get_client_v3(client_id)
        self.fmt = fmt

    def _base64(self, pil):
        buffered = BytesIO()
        pil.save(buffered, format=self.fmt)
        return base64.b64encode(buffered.getvalue())

    def upload_pil(self, pil):
        data = {"type": "base64", "image": self._base64(pil)}
        return self.client.request("POST", "image", data=data)

    def upload_pil_get_url(self, pil):
        res = self.upload_pil(pil)
        res.raise_for_status()
        return res.json()["data"]["link"]


def get_default():
    return Imgur(DEFAULT_IMGUR_CLIENT_ID)
