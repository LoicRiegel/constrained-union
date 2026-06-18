"""Example implementation of Shape union type with mandatory properties."""

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol


@dataclass
class Rectangle:
    width: float
    height: float

    @property
    def area(self) -> float:
        return self.width * self.height


@dataclass
class Circle:
    radius: float

    @property
    def area(self) -> float:
        return math.pi * (self.radius**2)


type Shape = Rectangle | Circle


class ShapeProperties(Protocol):
    @property
    def area(self) -> float: ...


if TYPE_CHECKING:
    from constrained_union import assert_union_implements

    assert_union_implements[Shape, ShapeProperties]()
