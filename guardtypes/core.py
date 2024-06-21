"""
Module for enforcing type annotations at runtime.

This module provides a decorator, `enforce`, that can be used to enforce
type annotations on function arguments and return values. It utilizes
Python's type hints to check that arguments passed to a function and
the values returned by the function match the specified types. If a type
mismatch is detected, a `TypeError` is raised.

Functions:
    enforce(func: Callable) -> Callable:
        A decorator that enforces type annotations for the given function.
"""

import inspect
from functools import wraps
from typing import _GenericAlias  # type: ignore
from typing import (
    Any,
    Callable,
    Dict,
    FrozenSet,
    List,
    Set,
    Tuple,
    Union,
    get_type_hints,
)


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

        def check_type(value, expected_type, param_name="Value"):
            if expected_type is Any:
                return
            if isinstance(expected_type, _GenericAlias):
                origin = expected_type.__origin__
                if origin is Union:
                    if not any(isinstance(value, t) for t in expected_type.__args__):
                        raise TypeError(
                            f"{param_name} must be {expected_type}, got {type(value)}"
                        )
                elif origin in (list, List):
                    if not isinstance(value, (list, List)) or not all(
                        isinstance(item, expected_type.__args__[0]) for item in value
                    ):
                        raise TypeError(
                            f"{param_name} must be {expected_type}, got {type(value)}"
                        )
                elif origin in (tuple, Tuple):
                    if not isinstance(value, (tuple, Tuple)):
                        raise TypeError(
                            f"{param_name} must be {expected_type}, got {type(value)}"
                        )
                    if expected_type.__args__ and expected_type.__args__[1] is Ellipsis:
                        if not all(
                            isinstance(item, expected_type.__args__[0])
                            for item in value
                        ):
                            raise TypeError(
                                f"{param_name} must be {expected_type}, got {type(value)}"
                            )
                    else:
                        if len(value) != len(expected_type.__args__):
                            raise TypeError(
                                f"{param_name} must be {expected_type}, got {type(value)}"
                            )
                        for item, subtype in zip(value, expected_type.__args__):
                            check_type(item, subtype, param_name)
                elif origin in (dict, Dict):
                    key_type, val_type = expected_type.__args__
                    if not all(
                        isinstance(k, key_type) and isinstance(v, val_type)
                        for k, v in value.items()
                    ):
                        raise TypeError(
                            f"{param_name} must be {expected_type}, got {type(value)}"
                        )
                elif origin in (set, Set, frozenset, FrozenSet):
                    if not all(
                        isinstance(item, expected_type.__args__[0]) for item in value
                    ):
                        raise TypeError(
                            f"{param_name} must be {expected_type}, got {type(value)}"
                        )
            elif not isinstance(value, expected_type):
                raise TypeError(
                    f"{param_name} must be {expected_type}, got {type(value)}"
                )

        for name, value in bound_args.arguments.items():
            if name in annotations:
                check_type(value, annotations[name], name)

        result = func(*args, **kwargs)

        if "return" in annotations:
            check_type(result, annotations["return"], "return value")

        return result

    return wrapper
