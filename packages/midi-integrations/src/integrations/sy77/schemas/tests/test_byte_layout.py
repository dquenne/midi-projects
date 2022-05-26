from unittest import TestCase

from ...converters.boolean_converter import BooleanConverter
from ...converters.range_converters import RangeConverter
from ..byte_layout import MultiValueByteLayout, SingleValueByteLayout


class TestMultiValueByteLayout(TestCase):
    def test_success(self):
        layout = MultiValueByteLayout(
            1, {0: ("val_1", RangeConverter(0, 127, num_bytes=1))}
        )

        self.assertEqual(layout.num_bytes, 1)

    def test_last_bit_for_one_byte(self):
        layout = MultiValueByteLayout(1, {6: ("val_1", BooleanConverter())})

        self.assertEqual(layout.num_bytes, 1)

    def test_last_bit_for_two_bytes(self):
        layout = MultiValueByteLayout(2, {13: ("val_1", BooleanConverter())})

        self.assertEqual(layout.num_bytes, 2)

    def test_too_long_for_one_byte(self):
        with self.assertRaises(ValueError) as exception_context:
            MultiValueByteLayout(1, {1: ("val_1", RangeConverter(0, 127, num_bytes=1))})

        self.assertIn("extends beyond last bit (b6)", str(exception_context.exception))

    def test_too_long_for_two_bytes(self):
        with self.assertRaises(ValueError) as exception_context:
            MultiValueByteLayout(2, {1: ("val_1", RangeConverter(0, 127, num_bytes=2))})

        self.assertIn("extends beyond last bit (b13)", str(exception_context.exception))

    def test_offset_bit_too_large_one_byte(self):
        with self.assertRaises(ValueError) as exception_context:
            MultiValueByteLayout(1, {7: ("val_1", BooleanConverter())})

        self.assertIn("extends beyond last bit (b6)", str(exception_context.exception))

    def test_offset_bit_too_large_two_bytes(self):
        with self.assertRaises(ValueError) as exception_context:
            MultiValueByteLayout(2, {14: ("val_1", BooleanConverter())})

        self.assertIn("extends beyond last bit (b13)", str(exception_context.exception))

    def test_convert(self):
        layout = MultiValueByteLayout(1, {3: ("val_1", BooleanConverter())})

        converted_bytes = layout.convert({"val_1": True})

        self.assertEqual(converted_bytes.lsb_v2, 0b00001000)


class TestSingleValueByteLayout(TestCase):
    def test_success(self):
        layout = SingleValueByteLayout(1, RangeConverter(0, 127, num_bytes=1))

        self.assertEqual(layout.num_bytes, 1)

    def test_convert(self):
        layout = SingleValueByteLayout(1, RangeConverter(0, 127, num_bytes=1))

        converted_bytes = layout.convert(50)

        self.assertEqual(converted_bytes.lsb_v2, 0b00110010)

    def test_two_bytes(self):
        layout = SingleValueByteLayout(2, RangeConverter(0, 10000, num_bytes=2))

        converted_bytes = layout.convert(9000)  # 0b00_10001100101000

        self.assertEqual(converted_bytes.msb_v1, 0b0_1000110)
        self.assertEqual(converted_bytes.lsb_v2, 0b0_0101000)
