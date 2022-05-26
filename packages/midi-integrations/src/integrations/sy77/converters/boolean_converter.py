from .base_converter import BaseConverter


class BooleanConverter(BaseConverter[bool]):
    def __init__(self, *, num_bits=1):
        super().__init__(num_bits=num_bits)

    def validate(self, value: bool):
        if not isinstance(value, bool):
            return "not a boolean"

        return None

    def convert(self, value: bool):
        if validation_error := self.validate(value):
            raise ValueError(f"Bad value ({value}): {validation_error}")

        return int(value)
