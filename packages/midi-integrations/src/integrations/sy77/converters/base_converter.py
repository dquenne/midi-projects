from abc import ABC
from typing import Optional

from ..data_models import Sy77ParameterValue


class BaseConverter(ABC):
    def validate(self, value) -> Optional[str]:
        raise NotImplementedError()

    def convert(self, value) -> Sy77ParameterValue:
        """
        Convert to 2-byte value. Returns a tuple of the form (MSB, LSB)
        """
        raise NotImplementedError()
