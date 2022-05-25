from abc import ABC
from typing import Optional

from .data_models import Sy77ParameterValue


class Converter(ABC):
    def validate(self, value) -> Optional[str]:
        raise NotImplementedError()

    def convert(self, value) -> Sy77ParameterValue:
        """
        Convert to 2-byte value. Returns a tuple of the form (MSB, LSB)
        """
        raise NotImplementedError()


class BooleanConverter(Converter):
    def validate(self, value: bool):
        if not isinstance(value, bool):
            return "not a boolean"

        return None

    def convert(self, value: bool):
        if validation_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validation_error}")

        return Sy77ParameterValue(0x00, 1 if value else 0)


class RangeConverter(Converter):
    MAX_POSSIBLE_VALUE_1_BYTE = 0b0_1111111  # 7 bits
    MAX_POSSIBLE_VALUE_2_BYTES = 0b00_1111111_1111111  # 14 bits

    MIN_POSSIBLE_VALUE_1_BYTE = 0
    MIN_POSSIBLE_VALUE_2_BYTES = 0

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

        self._validate_setup_parameters()

    def _validate_setup_parameters(self):
        if not 1 <= self.num_bytes <= 2:
            raise ValueError(f"num_bytes must be 1 or 2, got {self.num_bytes}")

        if self.max_value <= self.min_value:
            raise ValueError("max_value must be greater than min_value")

        if self.max_value > self.MAX_POSSIBLE_VALUE_2_BYTES:
            raise ValueError(
                f"{self.MAX_VALUE_NAME} ({self.max_value}) must be no more than ({self.MAX_POSSIBLE_VALUE_2_BYTES if self.num_bytes == 2 else self.MAX_POSSIBLE_VALUE_1_BYTE})."
            )
        elif self.num_bytes == 1 and self.max_value > self.MAX_POSSIBLE_VALUE_1_BYTE:
            raise ValueError(
                f"{self.MAX_VALUE_NAME} ({self.max_value}) must be no more than ({self.MAX_POSSIBLE_VALUE_1_BYTE}). Did you mean to set num_bytes=2?"
            )

        if self.min_value < self.MIN_POSSIBLE_VALUE_2_BYTES:
            raise ValueError(
                f"{self.MAX_VALUE_NAME} ({self.min_value}) must be no less than ({self.MIN_POSSIBLE_VALUE_2_BYTES if self.num_bytes == 2 else self.MIN_POSSIBLE_VALUE_1_BYTE})."
            )
        elif self.num_bytes == 1 and self.min_value < self.MIN_POSSIBLE_VALUE_1_BYTE:
            raise ValueError(
                f"{self.MAX_VALUE_NAME} ({self.min_value}) must be no less than ({self.MIN_POSSIBLE_VALUE_1_BYTE}). Did you mean to set num_bytes=2?"
            )

    def validate(self, value: int):
        if not isinstance(value, int):
            return "not an integer"

        if value < self.min_value or value > self.max_value:
            return f"out of range ({self.min_value} to {self.max_value}, inclusive)"

        return None

    def convert(self, value: int):
        if validate_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validate_error}")

        most_significant_byte = value >> 7
        least_significant_byte = value & 0b0_1111111

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
    MAX_POSSIBLE_VALUE_1_BYTE = 0b0_0_111111  # 1 sign bit + 6 bits
    MAX_POSSIBLE_VALUE_2_BYTES = 0b00_0_111111_1111111  # 1 sign bit + 13 bits

    MIN_POSSIBLE_VALUE_1_BYTE = -1 * 0b0_0_111111  # 1 sign bit + 6 bits
    MIN_POSSIBLE_VALUE_2_BYTES = -1 * 0b00_0_111111_1111111  # 1 sign bit + 13 bits

    def _validate_setup_parameters(self):
        # As far as I can tell, no SY77 params use sign magnitude for value ranges
        # larger than -12 to 12
        if self.num_bytes != 1:
            raise NotImplementedError(
                "Sign magnitude conversion is not rigorously tested for 2-byte values"
            )
        super()._validate_setup_parameters()

    def convert(self, value: int):
        if validate_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validate_error}")

        is_negative = value < 0

        normalized_value = value * -1 if is_negative else value

        if self.num_bytes == 1:
            most_significant_byte = 0
            least_significant_byte = (normalized_value & 0b00_111111) + (
                is_negative << 6
            )
        else:  # num_bytes == 2
            is_negative = bool(normalized_value >> 13)
            most_significant_byte = normalized_value >> 7 & 0b00_111111 + (
                is_negative << 6
            )
            least_significant_byte = normalized_value & 0b0_1111111

        return Sy77ParameterValue(most_significant_byte, least_significant_byte)
