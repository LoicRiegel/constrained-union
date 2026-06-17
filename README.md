# constrained-union

A mypy plugin that verifies every member of a union type implements a given protocol.
Catches missing protocol implementations at type-check time, not at runtime.

## Installation

### Get the package

Install with pip:

```bash
pip install constrained-union
```

Or add `constrained-union` to your project's dev dependencies:
```toml
[dependency-groups]
dev = ["constrained_union"]
```

### Plugin registration

Add to your `mypy.ini` (or `[tool.mypy]` section in `pyproject.toml`):

```ini
[mypy]
plugins = constrained_union.mypy_plugin
```

## Usage

Suppose we implement the following types:

```python
from dataclasses import dataclass


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


type Shape = Rectangle | Circle
```

Since `Shape` is a union type and not a true sum algebraic data type, and python does not provide a way to make sure that each variant of the union type implements certain methods or properties.
In this case, let's suppose we want to enforce that each `Shape` variant must implement an `area` property.

```python
from typing import Protocol

class ShapeProperties(Protocol):
    @property
    def area(self): ...
```

Adding the following code will trigger an mypy error when performing type checking.

```python
from typing import TYPE_CHECKING
from constrained_union import assert_union_implements

if TYPE_CHECKING:
    assert_union_implements[Shape, ShapeProperties]()
    # error: Union member "Circle" does not implement protocol "ShapeProperties"
    # error: Missing member: area
```

The call must be placed inside `if TYPE_CHECKING:` so it does not run at runtime.

## Contributing

Contributions are welcome! Feel free to open an issue to report a bug or suggest a feature, or submit a pull request directly.
Please follow the guidelines described in [CONTRIBUTING.md](CONTRIBUTING.md).
