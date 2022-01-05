from diskcache import Cache
import requests

from httprr import DefaultHandlers


cache = Cache(__name__)


# Cache for one week
@cache.memoize(expire=3600*24*7)
def svg(name):
    if name.endswith(".svg"):
        name = name.replace(".svg", "")
    name = name.strip("/")
    res = requests.get(
        f"https://game-icons.net/icons/ffffff/000000/1x1/{name}.svg"
    )
    return DefaultHandlers.raise_or_return_text(res)


def colored_svg(name, color_code="#f00"):
    svg_ = svg(name)
    color_code = f"#{color_code.lstrip('#')}"
    return svg_.replace('fill="#fff"', f'fill="{color_code}"')
