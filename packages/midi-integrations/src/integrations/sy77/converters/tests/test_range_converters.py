from unittest import TestCase

from ..range_converters import (
    ByteOffsetRangeConverter,
    RangeConverter,
    SignMagnitudeRangeConverter,
)


class TestRangeConverter(TestCase):
    def setUp(self):
        self.converter = RangeConverter(0, 63)

    def test_success(self):
        value = 15

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, (0x00, 0x0F))

    def test_validates_max_value_for_7_bits(self):
        RangeConverter(0, 127)
        with self.assertRaises(ValueError):
            RangeConverter(0, 128)

    def test_invalid_number(self):
        value = "1"

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("not an integer", str(exception_context.exception))

    def test_out_of_range(self):
        value = 84

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("out of range", str(exception_context.exception))


class TestTwoByteRangeConverter(TestCase):
    def setUp(self):
        self.converter = RangeConverter(0, 10794, num_bytes=2)

    def test_success(self):
        value = 0b00_0111110_1101101  # 8045

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, (0b0_0111110, 0b0_1101101))

    def test_validates_max_value_for_14_bits(self):
        RangeConverter(0, 16383, num_bytes=2)

        with self.assertRaises(ValueError):
            RangeConverter(0, 16384, num_bytes=2)


class TestByteOffsetRangeConverter(TestCase):
    def setUp(self):
        self.converter = ByteOffsetRangeConverter(-64, 63, offset=64)

    def test_adjusts_offset(self):
        value = -10

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, (0x00, 0x36))

    def test_validates_min_value_and_offset(self):
        with self.assertRaises(ValueError):
            ByteOffsetRangeConverter(-64, 63, offset=0)

    def test_out_of_range_with_offset(self):

        value = -65

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("out of range", str(exception_context.exception))


class TestSignMagnitudeRangeConverter(TestCase):
    def setUp(self):
        self.converter = SignMagnitudeRangeConverter(-12, 12, sign_bit_index=4)

    def test_sets_magnitude_byte(self):
        value = -10

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, (0x00, 0b00010000 + 10))

    def test_handles_positive_numbers(self):
        value = 10

        converted_value = self.converter.convert(value)

        self.assertEqual(converted_value, (0x00, 10))

    def test_validates_min_value(self):
        with self.assertRaises(ValueError):
            SignMagnitudeRangeConverter(-64, 63, sign_bit_index=4)

    def test_validates_max_value(self):
        with self.assertRaises(ValueError):
            SignMagnitudeRangeConverter(-63, 64, sign_bit_index=4)

    def test_value_too_small(self):
        value = -13

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("out of range", str(exception_context.exception))

    def test_value_too_large(self):
        value = 13

        with self.assertRaises(ValueError) as exception_context:
            self.converter.convert(value)

        self.assertIn("out of range", str(exception_context.exception))

    def test_two_byte_values_not_supported(self):
        with self.assertRaises(NotImplementedError):
            SignMagnitudeRangeConverter(-3000, 3000, num_bytes=2, sign_bit_index=4)
