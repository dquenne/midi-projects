from ..data_models import Sy77ParameterValue
from .base_converter import BaseConverter
from .util import split_14_bits_to_2_bytes


class RangeConverter(BaseConverter):
    MIN_VALUE_NAME = "min_value"
    MAX_VALUE_NAME = "max_value"

    def __init__(
        self,
        min_value: int,
        max_value: int,
        *,
        num_bytes: int = 1,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.num_bytes = num_bytes

        super().__init__(num_bits=num_bytes * 7)

    def _get_valid_values_range(self):
        if self.num_bytes == 2:
            return (0, 0b00_1111111_1111111)  # 14 bits

        return (0, 0b0_1111111)  # 7 bits

    def _validate_setup_parameters(self):
        if not 1 <= self.num_bytes <= 2:
            raise ValueError(f"num_bytes must be 1 or 2, got {self.num_bytes}")

        if self.max_value <= self.min_value:
            raise ValueError("max_value must be greater than min_value")

        min_possible, max_possible = self._get_valid_values_range()
        if self.max_value > max_possible:
            raise ValueError(
                f"{self.MAX_VALUE_NAME} ({self.max_value}) must be no more than ({max_possible})."
            )

        if self.min_value < min_possible:
            raise ValueError(
                f"{self.MAX_VALUE_NAME} ({self.min_value}) must be no less than ({min_possible})."
            )

        super()._validate_setup_parameters()

    def validate(self, value: int):
        if not isinstance(value, int):
            return "not an integer"

        if value < self.min_value or value > self.max_value:
            return f"out of range ({self.min_value} to {self.max_value}, inclusive)"

        return None

    def convert(self, value: int):
        if validate_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validate_error}")

        most_significant_byte, least_significant_byte = split_14_bits_to_2_bytes(value)

        return Sy77ParameterValue(most_significant_byte, least_significant_byte)


class ByteOffsetRangeConverter(RangeConverter):
    MIN_VALUE_NAME = "min_value + offset"
    MAX_VALUE_NAME = "max_value + offset"

    def __init__(
        self,
        min_value: int,
        max_value: int,
        *,
        offset: int,
        num_bytes: int = 1,
    ):
        self.offset = offset
        super().__init__(min_value + offset, max_value + offset, num_bytes=num_bytes)

    def convert(self, value: int):
        return super().convert(value + self.offset)


class SignMagnitudeRangeConverter(RangeConverter):
    """
    sign_bit_index -- index of bit used to indicate sign, starting from the
        least-significant bit. E.g. if the number is of the format 0b000svvvv, s is the
        sign bit, and vvvv are the four unsigned value bits, sign_bit_index is 4. The
        max possible sign_bit_index for a 2-byte magnitude is 14, where the last 13 bits
        are used for the unsigned value: 0b00svvvvv_vvvvvvvv or 0b0svvvvvv, 0b0vvvvvvv).
    """

    def __init__(
        self,
        min_value: int,
        max_value: int,
        *,
        sign_bit_index: int,
        num_bytes: int = 1,
    ):
        self.sign_bit_index = sign_bit_index

        super().__init__(min_value, max_value, num_bytes=num_bytes)

    def _get_max_sign_bit_index(self):
        if self.num_bytes == 2:
            return 13  # 0b00svvvvvvvvvvvvv

        return 6  # 0b0svvvvvv

    def _get_sign_bit_mask(self):
        return 1 << self.sign_bit_index

    def _get_value_bit_mask(self):
        return self._get_sign_bit_mask() - 1

    def _get_valid_values_range(self):
        max_sign_bit = self._get_max_sign_bit_index()

        # if max_sign_bit is 6 (0b0svvvvvv), then max_unsigned value is
        # 0b01000000 - 1 = 0b00111111
        max_unsigned_value = (1 << max_sign_bit) - 1

        return (-max_unsigned_value, max_unsigned_value)

    def _validate_setup_parameters(self):
        # As far as I can tell, no SY77 params use sign magnitude for value ranges
        # larger than -12 to 12
        if self.num_bytes != 1:
            raise NotImplementedError(
                "Sign magnitude conversion is not rigorously tested for 2-byte values"
            )

        min_sign_bit_index = 1
        max_sign_bit_index = self._get_max_sign_bit_index()
        if not min_sign_bit_index <= self.sign_bit_index <= max_sign_bit_index:
            raise ValueError(
                f"sign_bit_index must be in the range ({min_sign_bit_index}, {max_sign_bit_index}, inclusive). Got {self.sign_bit_index}"
            )
        super()._validate_setup_parameters()

    def convert(self, value: int):
        if validate_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validate_error}")

        is_negative = value < 0

        normalized_value = value * -1 if is_negative else value

        sign_bit = self._get_sign_bit_mask() * is_negative

        final_value = sign_bit ^ normalized_value

        # split 14-bit number across lower 7 bits of two bytes
        most_significant_byte, least_significant_byte = split_14_bits_to_2_bytes(
            final_value
        )

        return Sy77ParameterValue(most_significant_byte, least_significant_byte)
