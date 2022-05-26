from abc import ABC
from typing import Dict, Generic, Tuple, TypeVar

from ..converters.base_converter import BaseConverter
from ..data_models import Sy77ParameterValue
from .util import split_14_bits_to_2_bytes

TValueNames = TypeVar("TValueNames", bound=str)
TInputValues = TypeVar("TInputValues")


class ByteLayout(ABC):
    num_bytes: int

    def _get_max_usable_bit(self) -> int:
        if self.num_bytes == 2:
            return 13

        return 6

    def convert(self, value_or_values) -> Sy77ParameterValue:
        raise NotImplementedError()


class MultiValueByteLayout(ByteLayout, Generic[TValueNames, TInputValues]):
    def __init__(
        self,
        num_bytes: int,
        fields: Dict[int, Tuple[TValueNames, BaseConverter[TInputValues]]],
    ):
        self.num_bytes = num_bytes
        self.fields_by_offset_bit = fields

        self._validate_fields_by_offset_bit()

    def _validate_fields_by_offset_bit(self):
        ordered_bit_offsets = sorted(self.fields_by_offset_bit.keys())

        next_unused_bit = 0
        max_usable_bit = self._get_max_usable_bit()

        for bit_offset in ordered_bit_offsets:
            (field_name, field_converter) = self.fields_by_offset_bit[bit_offset]
            if bit_offset < next_unused_bit:
                raise ValueError(
                    f"field {field_name} at bit b{bit_offset} overlaps with previous field"
                )

            final_bit = bit_offset + field_converter.num_bits - 1

            if final_bit > max_usable_bit:
                raise ValueError(
                    f"field {field_name} at bit b{bit_offset}, length {field_converter.num_bits} bits, extends beyond last bit (b{max_usable_bit})"
                )

            next_unused_bit = final_bit + 1

    def convert(self, value_or_values: Dict[TValueNames, TInputValues]):
        output_as_14bits = 0
        for (offset_bit, field) in self.fields_by_offset_bit.items():
            (field_name, field_converter) = field
            converted_value = field_converter.convert(value_or_values[field_name])

            output_as_14bits ^= converted_value << offset_bit

        return Sy77ParameterValue(*split_14_bits_to_2_bytes(output_as_14bits))


TValue = TypeVar("TValue", bound=str)


class SingleValueByteLayout(ByteLayout, Generic[TValue]):
    def __init__(self, num_bytes: int, converter: BaseConverter[TValue]):
        self.num_bytes = num_bytes
        self.converter = converter

        max_num_bits = self._get_max_usable_bit() + 1
        if self.converter.num_bits > max_num_bits:
            raise ValueError(
                f"converter generates {self.converter.num_bits} bits, exceeding maximum of {max_num_bits} bits"
            )

    def convert(self, value_or_values: TValue):
        output_as_14bits = self.converter.convert(value_or_values)
        return Sy77ParameterValue(*split_14_bits_to_2_bytes(output_as_14bits))


class SimpleByteLayout(SingleValueByteLayout):
    def __init__(self, converter: BaseConverter[TValue]):
        super().__init__(num_bytes=1, converter=converter)
