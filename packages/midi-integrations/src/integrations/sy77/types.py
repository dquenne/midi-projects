"""
Most data comes from SY77 MIDI Data Format Manual, retrieved on 2022-05-23 at
https://usa.yamaha.com/files/download/other_assets/1/317121/SY77E2.PDF
"""

from enum import IntEnum


class ParameterChangeType(IntEnum):
    """
    From SY77 MIDI Data Format Manual, Section 3.1

    Parameter ID is specified by one nibble.
    """

    MULTI_COMMON_DATA = 0x0
    MULTI_CHANNEL_DATA = 0x1
    VOICE_COMMON_DATA = 0x2
    VOICE_ELEMENT_DATA = 0x3
    VOICE_DRUM_SET_DATA = 0x4
    AFM_ELEMENT_COMMON_DATA = 0x5
    AFM_ELEMENT_OPERATOR_DATA = 0x6
    AWM_ELEMENT_DATA = 0x7
    EFFECT_DATA = 0x8
    FILTER_DATA = 0x9
    PAN_DATA = 0xA
    MICRO_TUNING_DATA = 0xB


class VoiceElementMode(IntEnum):
    """
    From SY77 MIDI Data Format Manual, Table 1-3, ELMODE data range
    """

    MODE_1_AFM_MONO = 0x00
    MODE_2_AFM_MONO = 0x01
    MODE_4_AFM_MONO = 0x02
    MODE_1_AFM_POLY = 0x03
    MODE_2_AFM_POLY = 0x04
    MODE_1_AWM_POLY = 0x05
    MODE_2_AWM_POLY = 0x06
    MODE_4_AWM_POLY = 0x07
    MODE_1_AFM_1_AWM_POLY = 0x08
    MODE_2_FM_2PCM_POLY = 0x09
    MODE_DRUM_SET = 0x0A


class PortamentoMode(IntEnum):
    """
    From SY77 MIDI Data Format Manual, Table 1-3, PORM data range
    """

    FINGERED = 0
    FULL_TIME = 1


class VoiceElement(IntEnum):
    """
    From SY77 MIDI Data Format Manual, Table 1-4, 1-6, 1-7, 1-8, 1-10

    Element ID is specified by two bits. On message creation, these bits are shifted to
    bits 5 and 6 of T2 (byte 4).
    """

    ELEMENT_1 = 0  # 0b00
    ELEMENT_2 = 1  # 0b01
    ELEMENT_3 = 2  # 0b10
    ELEMENT_4 = 3  # 0b11


class OperatorNumber(IntEnum):
    """
    From SY77 MIDI Data Format Manual, Table 1-7

    AFM operator number is specified by three bits. On message creation, these bits are
    shifted to bits 5-7 of T1 (byte 3).
    """

    OPERATOR_1 = 0
    OPERATOR_2 = 1
    OPERATOR_3 = 2
    OPERATOR_4 = 3
    OPERATOR_5 = 4
    OPERATOR_6 = 5
