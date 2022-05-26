from unittest import TestCase

from ...converters.range_converters import RangeConverter
from ..byte_layout import SingleValueByteLayout


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
