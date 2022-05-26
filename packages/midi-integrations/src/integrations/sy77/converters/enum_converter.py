from enum import IntEnum
from typing import Generic, Type, TypeVar

from ..data_models import Sy77ParameterValue
from ..util import check_is_within_number_of_bits
from .base_converter import BaseConverter

T = TypeVar("T", bound=IntEnum)


class EnumConverter(BaseConverter, Generic[T]):
    def __init__(self, enum_class: Type[T]):
        self.enum_class = enum_class

        if any(
            not isinstance(option.value, int)
            or not check_is_within_number_of_bits(num_bits=7, value=option.value)
            for option in self.enum_class
        ):
            raise ValueError(
                "Enums passed into EnumConverter must have exclusively 7-bit integer values"
            )

    def validate(self, value: T):
        if not isinstance(value, self.enum_class):
            return f"not an instance of {self.enum_class}"

        return None

    def convert(self, value: T):
        if validation_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validation_error}")

        return Sy77ParameterValue(0x00, value.value)
