from unittest import TestCase

from ..boolean_converter import BooleanConverter


class TestBooleanConverter(TestCase):
    def setUp(self):
        self.converter = BooleanConverter()

    def test_true(self):
        value = True

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, 0x01)

    def test_false(self):
        value = False

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, 0x00)

    def test_invalid_boolean(self):
        value = "True"

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("not a boolean", str(exception_context.exception))
