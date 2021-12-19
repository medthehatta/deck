def split_to_multiple_fields(
    text,
    field_name,
    chars_per,
    max_lines,
):
    segments = []
    current_segment = []
    for word in text.split():
        if sum(len(w) for w in current_segment) + len(word) < chars_per:
            current_segment.append(word)
        else:
            segments.append(" ".join(current_segment))
            current_segment = [word]
    segments.append(" ".join(current_segment))

    default = {f"{field_name}#{i}": "" for i in range(1, max_lines + 1)}
    populated = {
        f"{field_name}#{i}": "".join(segment)
        for (i, segment) in enumerate(segments, start=1)
        if segment
    }
    if len(populated) > max_lines:
        raise ValueError(
            f"Need more lines; {max_lines} available, "
            f"{len(populated)} required to render '{text}'."
        )
    else:
        return {**default, **populated}


def gdoc(id_):
    return f"https://docs.google.com/spreadsheets/d/{id_}/edit#gid=0"
