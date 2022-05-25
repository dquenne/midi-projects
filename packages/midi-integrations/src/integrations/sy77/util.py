def check_is_within_number_of_bits(*, num_bits: int, value: int):
    return (2**num_bits - 1) & value == value
