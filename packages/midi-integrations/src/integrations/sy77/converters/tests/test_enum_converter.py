from enum import Enum, IntEnum
from unittest import TestCase

from ..enum_converter import EnumConverter


class TestBooleanConverter(TestCase):
    def setUp(self):
        class ExampleEnum(IntEnum):
            VAL_0 = 0
            VAL_1 = 1
            VAL_2 = 2

        self.enum_class = ExampleEnum
        self.converter = EnumConverter(self.enum_class)

    def test_success(self):
        value = self.enum_class.VAL_1

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, 0x01)

    def test_validates_enum_is_int_enum_on_initialization(self):
        class BadEnum(Enum):
            VAL_0 = 0
            VAL_STR = "not an integer"

        with self.assertRaises(ValueError) as exception_context:
            EnumConverter(BadEnum)

        self.assertIn(
            "exclusively 7-bit integer values", str(exception_context.exception)
        )

    def test_validates_enum_bounds_on_initialization(self):
        class BadEnum(IntEnum):
            VAL_0 = 0
            VAL_TOO_BIG = 0b10000000

        with self.assertRaises(ValueError) as exception_context:
            EnumConverter(BadEnum)

        self.assertIn(
            "exclusively 7-bit integer values", str(exception_context.exception)
        )

    def test_validates_enum_bounds(self):
        value = 0

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("Bad value", str(exception_context.exception))
