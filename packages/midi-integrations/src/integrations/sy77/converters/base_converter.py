from abc import ABC
from typing import Generic, Optional, TypeVar

TInputValue = TypeVar("TInputValue")


class BaseConverter(ABC, Generic[TInputValue]):
    def __init__(self, *args, num_bits=7, **kwargs):
        self.num_bits = num_bits

        self._validate_setup_parameters()

    def _validate_setup_parameters(self):
        if not 0 < self.num_bits <= 14:
            raise ValueError("num_bits must be at least 1 and no more than 14")

    def validate(self, value: TInputValue) -> Optional[str]:
        raise NotImplementedError()

    def convert(self, value: TInputValue) -> int:
        """
        Convert to value for use in a sysex message. Converted value must be an unsigned
        integer that is at most `self.num_bits` bits long.
        """
        raise NotImplementedError()
