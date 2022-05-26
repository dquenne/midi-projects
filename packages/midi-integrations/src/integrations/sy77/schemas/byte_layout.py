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
