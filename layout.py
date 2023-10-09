from cytoolz import partition_all
from PIL import Image


def oversize_portrait_cards_on_letter(pils):
    return layout_on_sheets_by_size(
        pils,
        sheet_x=8.5,
        sheet_y=11,
        card_x=2.8,
        card_y=3.65,
    )


def portrait_cards_on_letter(pils):
    return layout_on_sheets_by_size(
        pils,
        sheet_x=8.5,
        sheet_y=11,
        card_x=2.5,
        card_y=3.5,
    )


def landscape_cards_on_letter(pils):
    return layout_on_sheets_by_size(
        pils,
        sheet_x=11,
        sheet_y=8.5,
        card_x=3.5,
        card_y=2.5,
    )


def layout_on_sheets_by_size(
    pils,
    sheet_x,
    sheet_y,
    card_x,
    card_y,
):
    num_width = int(sheet_x / card_x)
    slop_width = sheet_x - card_x * num_width
    xpad = (slop_width / num_width) / card_x

    num_height = int(sheet_y / card_y)
    slop_height = sheet_y - card_y * num_height
    ypad = (slop_height / num_height) / card_y

    sheets = partition_all(num_width * num_height, pils)
    return [
        layout_pils(
            sheet,
            num_width=num_width,
            num_height=num_height,
            xpad=xpad,
            ypad=ypad,
        )
        for sheet in sheets
    ]


def layout_to_max_width(pils, max_width, xpadpx=0, ypadpx=0):
    if not pils:
        raise ValueError("Need to provide more than 0 pils")

    found_max_width = max(pil.width for pil in pils)
    if found_max_width > max_width:
        print(f"WARN: Extending max_width from {max_width} to {found_max_width}")
        max_width = found_max_width
    max_possible_height = sum((pil.height + ypadpx) for pil in pils)

    output = Image.new(
        mode="RGB",
        size=(max_width, max_possible_height),
        color=(255, 255, 255),
    )

    xpos = 0
    ypos = 0
    next_ypos = 0

    first = pils[0]
    next_xpos = xpos + first.width + xpadpx
    next_ypos = max(next_ypos, ypos + first.height + ypadpx)

    output.paste(pils[0], box=(0, 0))

    xpos = next_xpos

    for pil in pils[1:]:
        width = pil.width
        height = pil.height

        next_xpos = xpos + width + xpadpx

        if next_xpos > max_width:
            xpos = 0
            ypos = next_ypos
            next_ypos = ypos + height + ypadpx
            next_xpos = width + xpadpx
        else:
            next_ypos = max(next_ypos, ypos + height + ypadpx)

        output.paste(pil, box=(xpos, ypos))
        xpos = next_xpos

    return output


def layout_pils(
    pils,
    num_width,
    num_height,
    xpad=0,
    ypad=0,
):
    pils = iter(pils)
    first = next(pils)

    width = first.width
    height = first.height
    xpad_ = int(width * xpad)
    ypad_ = int(height * ypad)
    x2pad = xpad_ // 2
    y2pad = ypad_ // 2
    total_width = width * num_width + xpad_ * num_width
    total_height = height * num_height + ypad_ * num_height

    output = Image.new(
        mode="RGBA",
        size=(total_width, total_height),
        color=(255, 255, 255),
    )

    output.paste(first, box=(x2pad, y2pad))

    for vert in range(0, num_height):
        for horiz in range(0, num_width):
            if (horiz, vert) == (0, 0):
                # Skip the top-left, because that was `first`
                continue
            try:
                pil = next(pils)
            except StopIteration:
                break
            pos = (
                x2pad + int(width + xpad_) * horiz,
                y2pad + int(height + ypad_) * vert,
            )
            output.paste(pil, box=pos)

    return output
