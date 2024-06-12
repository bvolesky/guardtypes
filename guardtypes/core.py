"""
Type Enforcement Decorator Module

This module provides a decorator `enforce` that ensures the types of arguments
and return values of functions match their type annotations. It evaluates
annotations even if they are specified as strings, allowing for forward
references and dynamic type checks.

Usage:
    import guardtypes

    @guardtypes.enforce
    def example_function(arg1: int, arg2: str) -> bool:
        return arg1 > 0 and arg2.isalpha()

    example_function(1, "test")  # Works
    example_function(1, 123)     # Raises TypeError

Functions:
    - enforce(func: Callable) -> Callable:
        A decorator that enforces type annotations for the decorated function.

Imports:
    - inspect: To retrieve the signature of the function and bind arguments.
    - functools: To preserve the metadata of the original function.
    - typing: To use typing hints like Any and Callable for documentation.
"""

import inspect
from functools import wraps
from typing import _GenericAlias  # type: ignore
from typing import Any, Callable, Union, get_type_hints


def enforce(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        frame = inspect.currentframe().f_back  # type: ignore
        context = frame.f_globals.copy()  # type: ignore
        context.update(frame.f_locals)  # type: ignore
        annotations = get_type_hints(func, context)

        for name, value in bound_args.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if expected_type is Any:
                    continue
                if isinstance(expected_type, _GenericAlias):
                    origin = expected_type.__origin__
                    if origin is Union:
                        if not any(
                            isinstance(value, t) for t in expected_type.__args__
                        ):
                            raise TypeError(
                                f"Argument '{name}' must be {expected_type}, got {type(value)}"
                            )
                    elif origin is list:
                        if not all(
                            isinstance(item, expected_type.__args__[0])
                            for item in value
                        ):
                            raise TypeError(
                                f"Argument '{name}' must be {expected_type}, got {type(value)}"
                            )
                    elif origin is dict:
                        key_type, value_type = expected_type.__args__
                        if not all(
                            isinstance(k, key_type) and isinstance(v, value_type)
                            for k, v in value.items()
                        ):
                            raise TypeError(
                                f"Argument '{name}' must be {expected_type}, got {type(value)}"
                            )
                    elif origin is tuple:
                        if not isinstance(value, tuple):
                            raise TypeError(
                                f"Argument '{name}' must be a tuple, got {type(value)}"
                            )
                        if (
                            len(expected_type.__args__) == 2
                            and expected_type.__args__[1] is Ellipsis
                        ):
                            if not all(
                                isinstance(v, expected_type.__args__[0]) for v in value
                            ):
                                raise TypeError(
                                    f"Argument '{name}' must be a tuple of {expected_type.__args__[0]}, got {type(value)}"
                                )
                        else:
                            if len(value) != len(expected_type.__args__):
                                raise TypeError(
                                    f"Argument '{name}' must be a tuple of {expected_type.__args__}, got {type(value)}"
                                )
                            if not all(
                                isinstance(v, t)
                                for v, t in zip(value, expected_type.__args__)
                            ):
                                raise TypeError(
                                    f"Argument '{name}' must be {expected_type}, got {type(value)}"
                                )
                elif not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' must be {expected_type}, got {type(value)}"
                    )

        result = func(*args, **kwargs)

        if "return" in annotations:
            expected_return_type = annotations["return"]
            if expected_return_type is not Any and not isinstance(
                result, expected_return_type
            ):
                raise TypeError(
                    f"Return value must be {expected_return_type}, got {type(result)}"
                )

        return result

    return wrapper
