# guardtypes ⚡

`guardtypes` is a package that enforces type annotations at runtime. It ensures that the arguments and return values of a function match the specified types.

## Installation

To install `guardtypes`, clone the repository and install the package:

```bash
git clone https://github.com/bvolesky/guardtypes.git
cd guardtypes
pip install .
```

## Usage

To use the `guardtypes` decorator, simply import it and apply it to your function:

```python
import guardtypes


@guardtypes.enforce
def add(a: int, b: int) -> int:
    return a + b


# This will raise a TypeError because 'b' is not an int
add(1, '2')
```

The `guardtypes` decorator also handles local context, allowing you to use class types within the same function:

```python
import guardtypes


class Cat:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    @guardtypes.enforce
    def create(name: str) -> 'Cat':
        return Cat(name)


# This will create an instance of Cat
cat = Cat.create("Whiskers")

# This will raise a TypeError because 'name' should be a str
cat = Cat.create(123)
```
