"""
Most data comes from SY77 MIDI Data Format Manual, retrieved on 2022-05-23 at
https://usa.yamaha.com/files/download/other_assets/1/317121/SY77E2.PDF
"""


from .converters.enum_converter import EnumConverter
from .converters.range_converters import (
    ByteOffsetRangeConverter,
    RangeConverter,
    SignMagnitudeRangeConverter,
)
from .schema_builders import (
    AfmElementOperatorDataSchema,
    VoiceCommonDataSchema,
    VoiceElementDataSchema,
)
from .types import PortamentoMode, VoiceElementMode


class VoiceCommonDataSchemas:
    """
    From SY77 MIDI Data Format Manual, Table 1-3
    """

    # [header data]
    ELEMENT_MODE = VoiceCommonDataSchema(0x00, EnumConverter(VoiceElementMode))

    # VOICE_NAME_0 = VoiceCommonDataSchema(0x01, None)
    # VOICE_NAME_1 = VoiceCommonDataSchema(0x02, None)
    # VOICE_NAME_2 = VoiceCommonDataSchema(0x03, None)
    # VOICE_NAME_3 = VoiceCommonDataSchema(0x04, None)
    # VOICE_NAME_4 = VoiceCommonDataSchema(0x05, None)
    # VOICE_NAME_5 = VoiceCommonDataSchema(0x06, None)
    # VOICE_NAME_6 = VoiceCommonDataSchema(0x07, None)
    # VOICE_NAME_7 = VoiceCommonDataSchema(0x08, None)
    # VOICE_NAME_8 = VoiceCommonDataSchema(0x09, None)
    # VOICE_NAME_9 = VoiceCommonDataSchema(0x0A, None)

    # [Controllers]
    WHEEL_PITCH_BEND_RANGE = VoiceCommonDataSchema(0x28, RangeConverter(0, 12))
    AFTER_TOUCH_PITCH_BEND_RANGE = VoiceCommonDataSchema(
        0x29, SignMagnitudeRangeConverter(-12, 12, sign_bit_index=4)
    )

    PITCH_MOD_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x2A, RangeConverter(0, 121))
    PITCH_MOD_RANGE = VoiceCommonDataSchema(0x2B, RangeConverter(0, 127))

    AMPLITUDE_MOD_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x2C, RangeConverter(0, 121))
    AMPLITUDE_MOD_RANGE = VoiceCommonDataSchema(0x2D, RangeConverter(0, 127))

    FILTER_MOD_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x2E, RangeConverter(0, 121))
    FILTER_MOD_RANGE = VoiceCommonDataSchema(0x2F, RangeConverter(0, 127))

    PAN_MOD_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x30, RangeConverter(0, 121))
    PAN_MOD_RANGE = VoiceCommonDataSchema(0x31, RangeConverter(0, 127))

    FILTER_CUT_OFF_BIAS_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(
        0x32, RangeConverter(0, 121)
    )
    FILTER_CUT_OFF_BIAS_RANGE = VoiceCommonDataSchema(0x33, RangeConverter(0, 127))

    PAN_BIAS_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x34, RangeConverter(0, 121))
    PAN_BIAS_RANGE = VoiceCommonDataSchema(0x35, RangeConverter(0, 127))

    EG_BIAS_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x36, RangeConverter(0, 121))
    EG_BIAS_RANGE = VoiceCommonDataSchema(0x37, RangeConverter(0, 127))

    VOICE_VOLUME_DEVICE_ASSIGN_CC = VoiceCommonDataSchema(0x38, RangeConverter(0, 121))
    VOICE_VOLUME_LIMIT_LOW = VoiceCommonDataSchema(0x39, RangeConverter(0, 127))

    # [Only for Normal]
    MICRO_TUNING_TABLE_SELECT = VoiceCommonDataSchema(0x3A, RangeConverter(0, 65))

    RANDOM_PITCH_FLUCTUATION = VoiceCommonDataSchema(0x3B, RangeConverter(0, 7))

    PORTAMENTO_MODE = VoiceCommonDataSchema(0x3C, EnumConverter(PortamentoMode))
    PORTAMENTO_TIME = VoiceCommonDataSchema(0x3D, RangeConverter(0, 127))

    VOICE_VOLUME = VoiceCommonDataSchema(0x3F, RangeConverter(0, 127))


class VoiceElementDataSchemas:
    """
    From SY77 MIDI Data Format Manual, Table 1-4
    """

    ELEMENT_LEVEL = VoiceElementDataSchema(0x0, RangeConverter(0, 127))
    ELEMENT_DETUNE = VoiceElementDataSchema(
        0x1, SignMagnitudeRangeConverter(-7, 7, sign_bit_index=3)
    )
    ELEMENT_NOTE_SHIFT = VoiceElementDataSchema(
        0x2, ByteOffsetRangeConverter(-64, 63, offset=64)
    )

    ELEMENT_NOTE_LOW_LIMIT = VoiceElementDataSchema(0x3, RangeConverter(0, 127))
    ELEMENT_NOTE_HIGH_LIMIT = VoiceElementDataSchema(0x4, RangeConverter(0, 127))

    ELEMENT_VELOCITY_LOW_LIMIT = VoiceElementDataSchema(0x5, RangeConverter(0, 127))
    ELEMENT_VELOCITY_HIGH_LIMIT = VoiceElementDataSchema(0x6, RangeConverter(0, 127))

    PAN = VoiceElementDataSchema(0x7, RangeConverter(0, 95))

    # MICRO_TUNING_ENABLE_AND_OUTPUT_SELECT = VoiceElementDataSchema(0x8, None)


# class AfmElementCommonDataSchemas:
#     """
#     From SY77 MIDI Data Format Manual, Table 1-6

#     AFM Element Common Parameter ID is specified by one byte.
#     """

#     # Algorithm
#     ALGORITHM_NUMBER = Sy77Parameter("", 0x00, None)

#     # Pitch Envelope Generator
#     PITCH_EG_KEY_ON_RATE_1 = Sy77Parameter("", 0x01, None)
#     PITCH_EG_KEY_ON_RATE_2 = Sy77Parameter("", 0x02, None)
#     PITCH_EG_KEY_ON_RATE_3 = Sy77Parameter("", 0x03, None)
#     PITCH_EG_KEY_OFF_RATE_1 = Sy77Parameter("", 0x04, None)

#     PITCH_EG_KEY_ON_LEVEL_0 = Sy77Parameter("", 0x05, None)
#     PITCH_EG_KEY_ON_LEVEL_1 = Sy77Parameter("", 0x06, None)
#     PITCH_EG_KEY_ON_LEVEL_2 = Sy77Parameter("", 0x07, None)
#     PITCH_EG_KEY_ON_LEVEL_3 = Sy77Parameter("", 0x08, None)
#     PITCH_EG_KEY_OFF_LEVEL_1 = Sy77Parameter("", 0x09, None)

#     PITCH_EG_RANGE = Sy77Parameter("", 0x0A, None)
#     PITCH_EG_RATE_SCALING = Sy77Parameter("", 0x0B, None)
#     PITCH_EG_VELOCITY_SWITCH = Sy77Parameter("", 0x0C, None)

#     # Main LFO
#     MAIN_LFO_SPEED = Sy77Parameter("", 0x0D, None)
#     MAIN_LFO_DELAY_TIME = Sy77Parameter("", 0x0E, None)
#     MAIN_LFO_PITCH_MOD_DEPTH = Sy77Parameter("", 0x0F, None)
#     MAIN_LFO_AMPLITUDE_MOD_DEPTH = Sy77Parameter("", 0x10, None)
#     MAIN_LFO_FILTER_MOD_DEPTH = Sy77Parameter("", 0x11, None)
#     MAIN_LFO_WAVE = Sy77Parameter("", 0x12, None)
#     MAIN_LFO_INITIAL_PHASE = Sy77Parameter("", 0x13, None)

#     # Sub LFO
#     SUB_LFO_WAVE = Sy77Parameter("", 0x15, None)
#     SUB_LFO_SPEED = Sy77Parameter("", 0x16, None)
#     SUB_LFO_DELAY_DECAY_MODE = Sy77Parameter("", 0x17, None)
#     SUB_LFO_DELAY_DECAY_TIME = Sy77Parameter("", 0x18, None)
#     SUB_LFO_PITCH_MOD_DEPTH = Sy77Parameter("", 0x19, None)


class AfmElementOperatorDataSchemas:
    """
    From SY77 MIDI Data Format Manual, Table 1-7
    """

    # Envelope Generator
    EG_KEY_ON_RATE_1 = AfmElementOperatorDataSchema(0x00, RangeConverter(0, 63))
    EG_KEY_ON_RATE_2 = AfmElementOperatorDataSchema(0x01, RangeConverter(0, 63))
    EG_KEY_ON_RATE_3 = AfmElementOperatorDataSchema(0x02, RangeConverter(0, 63))
    EG_KEY_ON_RATE_4 = AfmElementOperatorDataSchema(0x03, RangeConverter(0, 63))
    EG_KEY_OFF_RATE_1 = AfmElementOperatorDataSchema(0x04, RangeConverter(0, 63))
    EG_KEY_OFF_RATE_2 = AfmElementOperatorDataSchema(0x05, RangeConverter(0, 63))

    EG_KEY_ON_LEVEL_1 = AfmElementOperatorDataSchema(0x06, RangeConverter(0, 63))
    EG_KEY_ON_LEVEL_2 = AfmElementOperatorDataSchema(0x07, RangeConverter(0, 63))
    EG_KEY_ON_LEVEL_3 = AfmElementOperatorDataSchema(0x08, RangeConverter(0, 63))
    EG_KEY_ON_LEVEL_4 = AfmElementOperatorDataSchema(0x09, RangeConverter(0, 63))
    EG_KEY_OFF_LEVEL_1 = AfmElementOperatorDataSchema(0x0A, RangeConverter(0, 63))
    EG_KEY_OFF_LEVEL_2 = AfmElementOperatorDataSchema(0x0B, RangeConverter(0, 63))

    EG_SUSTAIN_LOOP_POINT = AfmElementOperatorDataSchema(0x0C, RangeConverter(0, 3))
    EG_KEY_ON_HOLD_TIME = AfmElementOperatorDataSchema(0x0D, RangeConverter(0, 63))
    EG_KEY_ON_LEVEL = AfmElementOperatorDataSchema(0x0E, RangeConverter(0, 63))
    EG_RATE_SCALING = AfmElementOperatorDataSchema(
        0x0F, SignMagnitudeRangeConverter(-7, 7, sign_bit_index=3)
    )

    AMPLITUDE_MOD_SENSITIVITY = AfmElementOperatorDataSchema(0x10, RangeConverter(0, 7))
    VELOCITY_SENSITIVITY = AfmElementOperatorDataSchema(
        0x11, SignMagnitudeRangeConverter(-7, 7, sign_bit_index=3)
    )


#     # Algorithm Parameters

#     # TODO ...
