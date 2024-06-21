from typing import Any, Dict, List, Optional, Tuple, Type, Union

import pytest

from guardtypes import enforce


class TestTypingTypes:
    @enforce
    def process_list(self, items: List[int]) -> int:
        return sum(items)

    @enforce
    def accept_any(self, value: Any) -> str:
        return str(value)

    @enforce
    def manage_dict(self, data: Dict[str, int]) -> int:
        return sum(data.values())

    @enforce
    def handle_optional(self, value: Optional[int]) -> int:
        return value if value is not None else 0

    @enforce
    def process_union(self, value: Union[int, str]) -> str:
        return str(value)

    @enforce
    def handle_tuple(self, value: Tuple[int, ...]) -> int:
        return sum(value)

    @enforce
    def check_type(self, expected_type: Type, value: Any) -> bool:
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected type {expected_type}, got {type(value)}")
        return True

    @enforce
    def func_with_fixed_length_tuple(self, a: Tuple[int, str, float]):
        return f"{a[0]}, {a[1]}, {a[2]}"

    @enforce
    def func_with_tuple_arg(self, a: Tuple[int, int]):
        return sum(a)

    def test_process_list(self):
        assert self.process_list([1, 2, 3]) == 6

    def test_process_list_incorrect(self):
        with pytest.raises(TypeError):
            self.process_list([1, "2", 3])

    def test_accept_any(self):
        assert self.accept_any("test") == "test"
        assert self.accept_any(123) == "123"

    def test_manage_dict(self):
        assert self.manage_dict({"a": 1, "b": 2}) == 3

    def test_manage_dict_incorrect(self):
        with pytest.raises(TypeError):
            self.manage_dict({1: "a", 2: "b"})

    def test_handle_optional(self):
        assert self.handle_optional(5) == 5
        assert self.handle_optional(None) == 0

    def test_process_union_correct(self):
        assert self.process_union(123) == "123"
        assert self.process_union("abc") == "abc"

    def test_process_union_incorrect(self):
        with pytest.raises(TypeError):
            self.process_union(123.45)  # Should raise TypeError for invalid Union type

    def test_handle_tuple_correct(self):
        assert self.handle_tuple((10, 20, 30)) == 60

    def test_handle_tuple_incorrect(self):
        with pytest.raises(TypeError):
            self.handle_tuple((10, "20", 30))

        with pytest.raises(TypeError):
            self.handle_tuple(
                [1, 2, 3]
            )  # Should raise TypeError for non-tuple argument

    def test_check_type_correct(self):
        assert self.check_type(int, 5) is True

    def test_check_type_incorrect(self):
        with pytest.raises(TypeError):
            self.check_type(int, "not an int")

    # Additional tests for List, Dict, and Tuple
    def test_process_list_additional(self):
        assert self.process_list([1, 2, 3, 4]) == 10

        with pytest.raises(TypeError):
            self.process_list([1, "2", 3, 4])

    def test_manage_dict_additional(self):
        assert self.manage_dict({"key1": 1, "key2": 2, "key3": 3}) == 6

        with pytest.raises(TypeError):
            self.manage_dict({"key1": 1, "key2": "2", "key3": 3})

    def test_handle_tuple_fixed_length_correct(self):
        assert self.func_with_fixed_length_tuple((1, "test", 3.0)) == "1, test, 3.0"

    def test_argument_must_be_tuple(self):
        with pytest.raises(TypeError, match=".*"):
            self.func_with_tuple_arg([1, 2])

        with pytest.raises(TypeError, match=".*"):
            self.func_with_tuple_arg("not a tuple")

        # Test with correct type
        assert self.func_with_tuple_arg((1, 2)) == 3

    def test_handle_tuple_fixed_length_incorrect(self):
        with pytest.raises(TypeError, match=".*"):
            self.func_with_fixed_length_tuple((1, "test"))

        with pytest.raises(TypeError, match=".*"):
            self.func_with_fixed_length_tuple((1, "test", "not a float"))


class TestEnforce:
    @enforce
    def add(self, a: int, b: int) -> int:
        return a + b

    @enforce
    def concat(self, a: str, b: str) -> str:
        return a + b

    @enforce
    def repeat(self, s: str, n: int) -> str:
        return s * n

    def test_add_correct_types(self):
        assert self.add(1, 2) == 3

    def test_add_incorrect_types(self):
        with pytest.raises(TypeError):
            self.add(1, "2")

    def test_concat_correct_types(self):
        assert self.concat("hello", "world") == "helloworld"

    def test_concat_incorrect_types(self):
        with pytest.raises(TypeError):
            self.concat("hello", 123)

    def test_repeat_correct_types(self):
        assert self.repeat("a", 3) == "aaa"

    def test_repeat_incorrect_types(self):
        with pytest.raises(TypeError):
            self.repeat("a", "3")

    def test_return_type_correct(self):
        assert self.add(2, 3) == 5

    def test_return_type_incorrect(self):
        @enforce
        def add_incorrect_return(a: int, b: int) -> str:
            return a + b  # type: ignore

        with pytest.raises(TypeError):
            add_incorrect_return(1, 2)

    def test_decorate_class_methods(self):
        class Calculator:
            @enforce
            def add(self, a: int, b: int) -> int:
                return a + b

            @enforce
            def subtract(self, a: int, b: int) -> int:
                return a - b

        calc = Calculator()

        assert calc.add(2, 3) == 5
        assert calc.subtract(5, 2) == 3

    def test_decorate_static_methods(self):
        class StringUtils:
            @staticmethod
            @enforce
            def join_strings(a: str, b: str) -> str:
                return a + b

        assert StringUtils.join_strings("Hello, ", "World!") == "Hello, World!"

        with pytest.raises(TypeError):
            StringUtils.join_strings("Hello, ", 123)

    def test_class_methods(self):
        class Multiplier:
            factor = 2

            @classmethod
            @enforce
            def multiply(cls, x: int) -> int:
                return cls.factor * x

        assert Multiplier.multiply(3) == 6

        with pytest.raises(TypeError):
            Multiplier.multiply("3")

    def test_class_types(self):
        class Dog:
            def __init__(self, name: str):
                self.name = name

        @enforce
        def create_dog(name: str) -> Dog:
            return Dog(name)

        assert isinstance(create_dog("Buddy"), Dog)

        with pytest.raises(TypeError):
            create_dog(123)

    def test_function_with_string_annotation(self):
        @enforce
        def function_with_string_annotation(a: "int", b: "str") -> "bool":
            return isinstance(a, int) and isinstance(b, str)

        assert function_with_string_annotation(10, "hello")

        with pytest.raises(TypeError):
            function_with_string_annotation("10", "hello")

        with pytest.raises(TypeError):
            function_with_string_annotation(10, 123)

    def test_class_type_methods(self):
        class Cat:
            def __init__(self, name: str):
                self.name = name

            @staticmethod
            @enforce
            def create(name: str) -> "Cat":
                return Cat(name)

            @staticmethod
            @enforce
            def incorrect_create(name: int) -> "Cat":
                return Cat(str(name))

        assert isinstance(Cat.create("Whiskers"), Cat)

        with pytest.raises(TypeError):
            Cat.create(123)

        with pytest.raises(TypeError):
            Cat.incorrect_create("Whiskers")

        # Directly call incorrect_create with a valid integer argument
        cat_instance = Cat.incorrect_create(123)
        assert isinstance(cat_instance, Cat)
        assert cat_instance.name == "123"


class TestParamName:
    @enforce
    def func_with_type_checks(self, a: int, b: str) -> bool:
        return a > 0 and b.isalpha()

    def test_enforce_decorator(self):
        instance = TestParamName()

        # Test with valid inputs
        assert instance.func_with_type_checks(1, "hello")

        # Test with invalid type for 'a'
        with pytest.raises(
            TypeError, match="a must be <class 'int'>, got <class 'str'>"
        ):
            instance.func_with_type_checks("not an int", "hello")

        # Test with invalid type for 'b'
        with pytest.raises(
            TypeError, match="b must be <class 'str'>, got <class 'int'>"
        ):
            instance.func_with_type_checks(1, 123)

        # Test with invalid return type
        @enforce
        def invalid_return_type(a: int, b: str) -> str:
            return 42  # type: ignore

        with pytest.raises(
            TypeError,
            match="return value must be <class 'str'>, got <class 'int'>",
        ):
            invalid_return_type(1, "hello")
