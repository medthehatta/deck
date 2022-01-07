from hashlib import sha1

from PIL import Image

import imgur
from layout import layout_pils


def mkguid(func):
    def _wrapped(*args, **kwargs):
        val = func(*args, **kwargs)
        guid = sha1(str(val).encode("utf-8")).hexdigest()
        val["GUID"] = str(guid).upper()[:6]
        return val

    return _wrapped


@mkguid
def board(image_url):
    return {
        "Name": "Custom_Board",
        "Transform": {
            "posX": 4.29940462,
            "posY": 2.00714159,
            "posZ": 5.20972157,
            "rotX": 0.0116666686,
            "rotY": 179.910736,
            "rotZ": 359.941925,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "scaleZ": 1.0,
        },
        "Nickname": "",
        "Description": "",
        "GMNotes": "",
        "ColorDiffuse": {"r": 0.7867647, "g": 0.7867647, "b": 0.7867647},
        "Locked": False,
        "Grid": True,
        "Snap": True,
        "IgnoreFoW": False,
        "MeasureMovement": False,
        "DragSelectable": True,
        "Autoraise": True,
        "Sticky": True,
        "Tooltip": True,
        "GridProjection": False,
        "HideWhenFaceDown": False,
        "Hands": False,
        "CustomImage": {
            "ImageURL": image_url,
            "ImageSecondaryURL": "",
            "ImageScalar": 1.0,
            "WidthScale": 0.9524941,
        },
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": "",
    }


@mkguid
def card(card_id):
    return {
        "Name": "Card",
        "Transform": {
            "posX": 0.0,
            "posY": 1.0,
            "posZ": -1.0,
            "rotX": 0.0,
            "rotY": 180.0,
            "rotZ": 180.0,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "scaleZ": 1.0,
        },
        "Nickname": "",
        "Description": "",
        "GMNotes": "",
        "ColorDiffuse": {"r": 1.0, "g": 1.0, "b": 1.0,},
        "Locked": False,
        "Grid": True,
        "Snap": True,
        "IgnoreFoW": False,
        "MeasureMovement": False,
        "DragSelectable": True,
        "Autoraise": True,
        "Sticky": True,
        "Tooltip": True,
        "GridProjection": False,
        "Hands": True,
        "CardID": f"{card_id}",
        "SidewaysCard": False,
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": "",
        "ContainedObjects": [],
    }


@mkguid
def deck(face_url, back_url, num_cards, num_width=10, num_height=7):
    deckids = list(range(100, 100 + num_cards))
    objects = [card(i) for i in deckids]
    return {
        "Name": "DeckCustom",
        "Transform": {
            "posX": 0.5,
            "posY": 1.0,
            "posZ": -1.0,
            "rotX": 0.0,
            "rotY": 180.0,
            "rotZ": 180.0,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "scaleZ": 1.0,
        },
        "Nickname": "",
        "Description": "",
        "GMNotes": "",
        "ColorDiffuse": {"r": 1.0, "g": 1.0, "b": 1.0,},
        "Locked": False,
        "Grid": True,
        "Snap": True,
        "IgnoreFoW": False,
        "MeasureMovement": False,
        "DragSelectable": True,
        "Autoraise": True,
        "Sticky": True,
        "Tooltip": True,
        "GridProjection": False,
        "HideWhenFaceDown": True,
        "Hands": False,
        "SidewaysCard": False,
        "DeckIDs": deckids,
        "CustomDeck": {
            "1": {
                "FaceURL": face_url,
                "BackURL": back_url,
                "NumWidth": num_width,
                "NumHeight": num_height,
                "BackIsHidden": True,
                "UniqueBack": True,
                "Type": 0,
            },
        },
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": "",
        "ContainedObjects": objects,
    }


def make_deck(face_pils, back_pil=None, back_pils=None):
    # If we don't provide a back, use a black card
    if not back_pil and not back_pils:
        first_face = face_pils[0]
        back_pil = Image.new(
            mode=first_face.mode,
            size=first_face.size,
            color=0,  # black
        )

    # Passing a "single" back_pil will dupe it across all the faces
    if back_pil and not back_pils:
        back_pils = [back_pil] * len(face_pils)

    faces = layout_pils(
        face_pils,
        num_width=10,
        num_height=7,
    )
    backs = layout_pils(
        back_pils,
        num_width=10,
        num_height=7,
    )
    imgr = imgur.get_default()
    face_url = imgr.upload_pil_get_url(faces)
    back_url = imgr.upload_pil_get_url(backs)
    return deck(face_url, back_url, len(face_pils))
