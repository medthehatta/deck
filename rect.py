import itertools


class Vect2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def xhat(self):
        return type(self)(1, 0)

    @property
    def yhat(self):
        return type(self)(0, 1)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def __add__(self, other):
        return type(self)(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return type(self)(self.x * other.x, self.y * other.y)

    def __rmul__(self, num):
        return type(self)(num*self.x, num*self.y)

    def __truediv__(self, denom):
        return (1/denom) * self

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}({self.x}, {self.y})"


class Point(Vect2):
    pass


class Size(Vect2):
    pass


class Rect:

    @classmethod
    def from_anchor_size(cls, anchor_name: str, point: Point, size: Size):
        match anchor_name.lower():

            case "topleft":
                topleft = point

            case "topright":
                topleft = point - size.x * size.xhat
        
            case "bottomleft":
                topleft = point - size.y * size.yhat

            case "bottomright":
                topleft = (
                    point
                    - size.x * size.xhat
                    - size.y * size.yhat
                )

            case "center":
                topleft = point - size / 2

            case _:
                raise ValueError(f"Unknown anchor: {anchor_name}")

        return cls(topleft, size)

    def __init__(self, topleft: Point, size: Size):
        self.topleft = topleft
        self.size = size

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def anchor(self, anchor_name):
        match anchor_name.lower():

            case "topleft":
                return self.topleft

            case "topright":
                return self.topleft + self.size.x * self.size.xhat
        
            case "bottomleft":
                return self.topleft + self.size.y * self.size.yhat

            case "bottomright":
                return (
                    self.topleft
                    + self.size.x * self.size.xhat
                    + self.size.y * self.size.yhat
                )

            case "center":
                return (self.anchor("bottomright") - self.topleft) / 2

            case _:
                raise ValueError(f"Unknown anchor: {anchor_name}")

    def subdivide(self, rows=1, columns=1):
        return RectSubdivisions(self, rows, columns)

    def __repr__(self):
        cls = type(self).__name__
        return f"{cls}.from_anchor_size('topleft', {self.topleft}, {self.size})"


class RectSubdivisions:

    def __init__(self, rect, rows, columns):
        self.rect = rect
        self.rows = rows
        self.columns = columns

    def cell(self, row, column):
        rect = self.rect

        cell_size = Size(rect.size.x // self.columns, rect.size.y // self.rows)

        return Rect.from_anchor_size(
            "topleft",
            point=(
                rect.topleft
                + column * cell_size.x * cell_size.xhat
                + row * cell_size.y * cell_size.yhat
            ),
            size=cell_size,
        )

    def list_of_rows(self):
        return [
            [self.cell(row=r, column=c) for c in range(self.columns)]
            for r in range(self.rows)
        ]

    def list_of_columns(self):
        return [
            [self.cell(row=r, column=c) for r in range(self.rows)]
            for c in range(self.columns)
        ]

    def iter_rows_columns(self):
        return itertools.chain.from_iterable(self.list_of_columns())

    def iter_columns_rows(self):
        return itertools.chain.from_iterable(self.list_of_rows())
