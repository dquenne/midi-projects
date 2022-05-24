"""
Most data comes from SY77 MIDI Data Format Manual, retrieved on 2022-05-23 at
https://usa.yamaha.com/files/download/other_assets/1/317121/SY77E2.PDF
"""

from enum import Enum


class ParameterChangeType(Enum):
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


class VoiceCommonDataParameter(Enum):
    """
    From SY77 MIDI Data Format Manual, Table 1-3

    Voice Common Data Parameter ID is specified by one byte.
    """

    # [header data]
    ELEMENT_MODE = 0x00

    VOICE_NAME_0 = 0x01
    VOICE_NAME_1 = 0x02
    VOICE_NAME_2 = 0x03
    VOICE_NAME_3 = 0x04
    VOICE_NAME_4 = 0x05
    VOICE_NAME_5 = 0x06
    VOICE_NAME_6 = 0x07
    VOICE_NAME_7 = 0x08
    VOICE_NAME_8 = 0x09
    VOICE_NAME_9 = 0x0A

    # [Controllers]
    WHEEL_PITCH_BEND_RANGE = 0x28
    AFTER_TOUCH_PITCH_BEND_RANGE = 0x29

    PITCH_MOD_DEVICE_ASSIGN_CC = 0x2A
    PITCH_MOD_RANGE = 0x2B

    AMPLITUDE_MOD_DEVICE_ASSIGN_CC = 0x2C
    AMPLITUDE_MOD_RANGE = 0x2D

    FILTER_MOD_DEVICE_ASSIGN_CC = 0x2E
    FILTER_MOD_RANGE = 0x2F

    PAN_MOD_DEVICE_ASSIGN_CC = 0x30
    PAN_MOD_RANGE = 0x31

    FILTER_CUT_OFF_BIAS_DEVICE_ASSIGN_CC = 0x32
    FILTER_CUT_OFF_BIAS_RANGE = 0x33

    PAN_BIAS_DEVICE_ASSIGN_CC = 0x34
    PAN_BIAS_RANGE = 0x35

    EG_BIAS_DEVICE_ASSIGN_CC = 0x36
    EG_BIAS_RANGE = 0x37

    VOICE_VOLUME_DEVICE_ASSIGN_CC = 0x38
    VOICE_VOLUME_LIMIT_LOW = 0x39

    # [Only for Normal]
    MICRO_TUNING_TABLE_SELECT = 0x3A

    RANDOM_PITCH_FLUCTUATION = 0x3B

    PORTAMENTO_MODE = 0x3C
    PORTAMENTO_TIME = 0x3D

    VOICE_VOLUME = 0x3F


class VoiceElementMode(Enum):
    """
    From SY77 MIDI Data Format Manual, Table 1-3, ELMODE data range

    Voice Element Mode ID is specified by one byte.
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


class VoiceElement(Enum):
    """
    From SY77 MIDI Data Format Manual, Table 1-4, 1-6, 1-7, 1-8, 1-10

    Element ID is specified by two bits, shifted to the 2nd- and 3rd-most
    significant bits.
    """

    ELEMENT_1 = 0b00 << 5  # 0x00
    ELEMENT_2 = 0b01 << 5  # 0x20
    ELEMENT_3 = 0b10 << 5  # 0x40
    ELEMENT_4 = 0b11 << 5  # 0x60


class VoiceElementDataParameter(Enum):
    """
    From SY77 MIDI Data Format Manual, Table 1-4

    Voice Element Parameter ID is specified by one nibble.
    """

    ELEMENT_LEVEL = 0x0
    ELEMENT_DETUNE = 0x1
    ELEMENT_NOTE_SHIFT = 0x2

    ELEMENT_NOTE_LOW_LIMIT = 0x3
    ELEMENT_NOTE_HIGH_LIMIT = 0x4

    ELEMENT_VELOCITY_LOW_LIMIT = 0x5
    ELEMENT_VELOCITY_HIGH_LIMIT = 0x6

    PAN = 0x7

    MICRO_TUNING_ENABLE_AND_OUTPUT_SELECT = 0x8


class AfmElementCommonParameter(Enum):
    """
    From SY77 MIDI Data Format Manual, Table 1-6

    AFM Element Common Parameter ID is specified by one byte.
    """

    # Algorithm
    ALGORITHM_NUMBER = 0x00

    # Pitch Envelope Generator
    PITCH_EG_KEY_ON_RATE_1 = 0x01
    PITCH_EG_KEY_ON_RATE_2 = 0x02
    PITCH_EG_KEY_ON_RATE_3 = 0x03
    PITCH_EG_KEY_OFF_RATE_1 = 0x04

    PITCH_EG_KEY_ON_LEVEL_0 = 0x05
    PITCH_EG_KEY_ON_LEVEL_1 = 0x06
    PITCH_EG_KEY_ON_LEVEL_2 = 0x07
    PITCH_EG_KEY_ON_LEVEL_3 = 0x08
    PITCH_EG_KEY_OFF_LEVEL_1 = 0x09

    PITCH_EG_RANGE = 0x0A
    PITCH_EG_RATE_SCALING = 0x0B
    PITCH_EG_VELOCITY_SWITCH = 0x0C

    # Main LFO
    MAIN_LFO_SPEED = 0x0D
    MAIN_LFO_DELAY_TIME = 0x0E
    MAIN_LFO_PITCH_MOD_DEPTH = 0x0F
    MAIN_LFO_AMPLITUDE_MOD_DEPTH = 0x10
    MAIN_LFO_FILTER_MOD_DEPTH = 0x11
    MAIN_LFO_WAVE = 0x12
    MAIN_LFO_INITIAL_PHASE = 0x13

    # Sub LFO
    SUB_LFO_WAVE = 0x15
    SUB_LFO_SPEED = 0x16
    SUB_LFO_DELAY_DECAY_MODE = 0x17
    SUB_LFO_DELAY_DECAY_TIME = 0x18
    SUB_LFO_PITCH_MOD_DEPTH = 0x19


class AfmElementParameter(Enum):
    """
    From SY77 MIDI Data Format Manual, Table 1-7

    AFM Element Parameter ID is specified by one byte.
    """

    # Envelope Generator
    EG_KEY_ON_RATE_1 = 0x00
    EG_KEY_ON_RATE_2 = 0x01
    EG_KEY_ON_RATE_3 = 0x02
    EG_KEY_ON_RATE_4 = 0x03
    EG_KEY_OFF_RATE_1 = 0x04
    EG_KEY_OFF_RATE_2 = 0x05

    EG_KEY_ON_LEVEL_1 = 0x06
    EG_KEY_ON_LEVEL_2 = 0x07
    EG_KEY_ON_LEVEL_3 = 0x08
    EG_KEY_ON_LEVEL_4 = 0x09
    EG_KEY_OFF_LEVEL_1 = 0x0A
    EG_KEY_OFF_LEVEL_2 = 0x0B

    EG_SUSTAIN_LOOP_POINT = 0x0C
    EG_KEY_ON_HOLD_TIME = 0x0D
    EG_KEY_ON_LEVEL = 0x0E
    EG_RATE_SCALING = 0x0F

    AMPLITUDE_MOD_SENSITIVITY = 0x10
    VELOCITY_SENSITIVITY = 0x11

    # Algorithm Parameters

    # TODO ...
