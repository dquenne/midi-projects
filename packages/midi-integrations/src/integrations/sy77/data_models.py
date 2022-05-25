from typing import NamedTuple


class Sy77ParameterValue(NamedTuple):
    """
    SY77 sysex messages store their values in 2 bytes, V1 and V2. V1 is the most
    significant byte and V2 is the least significant byte. Many parameters exclusively
    use V2. The most significant bit of each byte is unused.
    """

    msb_v1: int
    lsb_v2: int

    def __repr__(self):
        return f"Sy77ParameterValue(V1(MSB)=0x{self.msb_v1:02x}, V2(LSB)=0x{self.lsb_v2:02x})"
