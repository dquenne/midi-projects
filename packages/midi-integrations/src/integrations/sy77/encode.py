from typing import List

from mido import Message

from .constants import ParameterChangeType, VoiceCommonDataParameter

COMMON_PARAMETER_CHANGE_HEADER = [
    0x43,
    0x12,
    0x34,
]


def encode_sy77_parameter_change_message(parameter_bytes_list: List[bytes]) -> Message:
    """
    Convert Sy77Message to mido.Message of type `sysex`
    """
    if len(parameter_bytes_list) != 6:
        raise ValueError(
            "parameter_bytes_list must have length 6 for SY77 parameter change messages"
        )

    bytes_list = COMMON_PARAMETER_CHANGE_HEADER + parameter_bytes_list
    return Message("sysex", data=bytes_list)


def encode_sy77_voice_common_data_message(
    parameter: VoiceCommonDataParameter, value: int
):
    return encode_sy77_parameter_change_message(
        [
            ParameterChangeType.VOICE_COMMON_DATA.value,
            0x00,
            0x00,
            parameter.value,
            0x00,
            value,
        ]
    )
