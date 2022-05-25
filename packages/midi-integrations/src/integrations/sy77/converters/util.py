from typing import Tuple


def split_14_bits_to_2_bytes(value: int) -> Tuple[int, int]:
    # split 14-bit number across lower 7 bits of two bytes
    most_significant_byte = value >> 7
    least_significant_byte = value & 0b0_1111111

    return (most_significant_byte, least_significant_byte)

