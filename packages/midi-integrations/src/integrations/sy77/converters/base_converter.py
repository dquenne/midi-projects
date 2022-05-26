from abc import ABC
from typing import Optional

from ..data_models import Sy77ParameterValue


class BaseConverter(ABC):
    def __init__(self, *args, num_bits=7, **kwargs):
        self.num_bits = num_bits

        self._validate_setup_parameters()

    def _validate_setup_parameters(self):
        if not 0 < self.num_bits <= 14:
            raise ValueError("num_bits must be at least 1 and no more than 14")

    def validate(self, value) -> Optional[str]:
        raise NotImplementedError()

    def convert(self, value) -> Sy77ParameterValue:
        """
        Convert to 2-byte value. Returns a tuple of the form (MSB, LSB)
        """
        raise NotImplementedError()
