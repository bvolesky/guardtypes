# guardtypes

`guardtypes` is a Python library that enforces type annotations at runtime. It provides a decorator, `enforce`, that checks the types of function arguments and return values against their type hints, raising a `TypeError` if a mismatch is found.

## Installation

To install `guardtypes`, use pip:

```sh
pip install guardtypes
```

## Usage

### Basic Example

The `enforce` decorator can be used to enforce type annotations on function arguments and return values.

```python
from guardtypes import enforce


@enforce
def add(a: int, b: int) -> int:
    return a + b


# This will raise a TypeError because 'b' is not an int
add(1, '2')
```

### Handling Local Context

The `guardtypes` decorator also handles local context, allowing you to use class types within the same function.

```python
from guardtypes import enforce


class Cat:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    @enforce
    def create(name: str) -> 'Cat':
        return Cat(name)


# This will create an instance of Cat
cat = Cat.create("Whiskers")

# This will raise a TypeError because 'name' should be a str
cat = Cat.create(123)
```

## License

This project is licensed under the MIT License.
