from hashlib import sha1

from PIL import Image

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
def bag_of(objects):
    return {
      "Name": "Bag",
      "Transform": {
	"posX": 0.0,
	"posY": 0.0,
	"posZ": 0.0,
	"rotX": 0.0,
	"rotY": 0.0,
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
	"r": 0.7058823,
	"g": 0.366520882,
	"b": 0.0
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
      "MaterialIndex": -1,
      "MeshIndex": -1,
      "Bag": {
	"Order": 0
      },
      "LuaScript": "",
      "LuaScriptState": "",
      "XmlUI": "",
      "ContainedObjects": objects,
    }


@mkguid
def token(image_url, nickname="", scale=1.0):
    return {
      "Name": "Custom_Token",
      "Transform": {
        "posX": 0.0,
        "posY": 1.0,
        "posZ": -1.0,
        "rotX": 0.0,
        "rotY": 180.0,
        "rotZ": 0.0,
        "scaleX": scale,
        "scaleY": 1.0,
        "scaleZ": scale,
      },
      "Nickname": nickname,
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
def card(card_id, nickname="", scale=1.0):
    return {
        "Name": "Card",
        "Transform": {
            "posX": 0.0,
            "posY": 1.0,
            "posZ": -1.0,
            "rotX": 0.0,
            "rotY": 180.0,
            "rotZ": 180.0,
            "scaleX": scale,
            "scaleY": 1.0,
            "scaleZ": scale,
        },
        "Nickname": nickname,
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
def deck(
    face_url,
    back_url,
    num_cards,
    card_names=None,
    num_width=10,
    num_height=7,
    scale=1.0,
):
    deckids = list(range(100, 100 + num_cards))
    if card_names is None:
        card_names = ["" for _ in deckids]
    objects = [
        card(i, nickname=name, scale=scale)
        for (name, i) in zip(card_names, deckids)
    ]
    return {
        "Name": "DeckCustom",
        "Transform": {
            "posX": 0.5,
            "posY": 1.0,
            "posZ": -1.0,
            "rotX": 0.0,
            "rotY": 180.0,
            "rotZ": 180.0,
            "scaleX": scale,
            "scaleY": 1.0,
            "scaleZ": scale,
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
