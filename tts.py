from hashlib import sha1

from PIL import Image

import imgur
import image4io

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
def tile(image_url):
    return {
      "Name": "Custom_Token",
      "Transform": {
        "posX": 0.0,
        "posY": 1.0,
        "posZ": -1.0,
        "rotX": 0.0,
        "rotY": 180.0,
        "rotZ": 0.0,
        "scaleX": 1.0,
        "scaleY": 1.0,
        "scaleZ": 1.0
      },
      "Nickname": "",
      "Description": "",
      "GMNotes": "",
      "AltLookAngle": {
        "x": 0.0,
        "y": 0.0,
        "z": 0.0
      },
      "ColorDiffuse": {
        "r": 1.0,
        "g": 1.0,
        "b": 1.0
      },
      "LayoutGroupSortIndex": 0,
      "Value": 0,
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
        "WidthScale": 0.0,
        "CustomToken": {
          "Thickness": 0.1,
          "MergeDistancePixels": 15.0,
          "StandUp": False,
          "Stackable": True
        }
      },
      "LuaScript": "",
      "LuaScriptState": "",
      "XmlUI": ""
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


def game(objects):
    objects = objects or []
    if not isinstance(objects, (list, tuple)):
        objects = [objects]
    return {
        "SaveName": "",
        "GameMode": "",
        "Date": "",
        "Gravity": 0.5,
        "PlayArea": 0.5,
        "GameType": "",
        "GameComplexity": "",
        "Tags": [],
        "Table": "",
        "Sky": "",
        "Note": "",
        "Rules": "",
        "TabStates": {},
        "ObjectStates": objects,
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": "",
        "VersionNumber": "",
    }


def layout(pils):
    return layout_pils(pils, num_width=10, num_height=7)


def layout_and_upload(pils):
    return image4io.get_default().upload_pil_get_url(layout(pils))


def make_deck_pils(face_pils, back_pil=None, back_pils=None):
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

    faces = layout(face_pils)
    backs = layout(back_pils)
    return {
        "face": faces,
        "back": backs,
    }


def mplex_face_back(both, face_key="faces", back_key="backs"):
    return {
        "face_pils": both[face_key],
        "back_pils": both[back_key],
    }


def make_deck_urls(face_pils, back_pil=None, back_pils=None):
    deck_pils = make_deck_pils(
        face_pils,
        back_pil=back_pil,
        back_pils=back_pils,
    )
    faces = deck_pils["face"]
    backs = deck_pils["back"]
    imgr = image4io.get_default()
    face_url = imgr.upload_pil_get_url(faces)
    back_url = imgr.upload_pil_get_url(backs)
    return {
        "face": face_url,
        "back": back_url,
    }


def make_deck(face_pils, back_pil=None, back_pils=None):
    spec = make_deck_urls(face_pils, back_pil=back_pil, back_pils=back_pils)
    return deck(spec["face"], spec["back"], len(face_pils))
