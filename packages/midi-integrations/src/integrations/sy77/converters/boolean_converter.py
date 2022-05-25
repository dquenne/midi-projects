from ..data_models import Sy77ParameterValue
from .base_converter import BaseConverter


class BooleanConverter(BaseConverter):
    def validate(self, value: bool):
        if not isinstance(value, bool):
            return "not a boolean"

        return None

    def convert(self, value: bool):
        if validation_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validation_error}")

        return Sy77ParameterValue(0x00, 1 if value else 0)
