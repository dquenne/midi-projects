from unittest import TestCase

from ..message_schemas import VoiceCommonDataSchemas


class TestVoiceCommonDataSchemas(TestCase):
    SYSEX_TEMPLATE = "F0 43 10 34 02 00 00 {:02X} 00 {:02X} F7"

    def test_zero(self):
        test_cases = [
            (VoiceCommonDataSchemas.WHEEL_PITCH_BEND_RANGE, 0, 0x28, 0x00),
            (VoiceCommonDataSchemas.AFTER_TOUCH_PITCH_BEND_RANGE, 0, 0x29, 0x00),
            (VoiceCommonDataSchemas.PITCH_MOD_DEVICE_ASSIGN_CC, 0, 0x2A, 0x00),
            (VoiceCommonDataSchemas.PITCH_MOD_RANGE, 0, 0x2B, 0x00),
            (VoiceCommonDataSchemas.AMPLITUDE_MOD_DEVICE_ASSIGN_CC, 0, 0x2C, 0x00),
            (VoiceCommonDataSchemas.AMPLITUDE_MOD_RANGE, 0, 0x2D, 0x00),
            (VoiceCommonDataSchemas.FILTER_MOD_DEVICE_ASSIGN_CC, 0, 0x2E, 0x00),
            (VoiceCommonDataSchemas.FILTER_MOD_RANGE, 0, 0x2F, 0x00),
            (VoiceCommonDataSchemas.PAN_MOD_DEVICE_ASSIGN_CC, 0, 0x30, 0x00),
            (VoiceCommonDataSchemas.PAN_MOD_RANGE, 0, 0x31, 0x00),
            (
                VoiceCommonDataSchemas.FILTER_CUT_OFF_BIAS_DEVICE_ASSIGN_CC,
                0,
                0x32,
                0x00,
            ),
            (VoiceCommonDataSchemas.FILTER_CUT_OFF_BIAS_RANGE, 0, 0x33, 0x00),
            (VoiceCommonDataSchemas.PAN_BIAS_DEVICE_ASSIGN_CC, 0, 0x34, 0x00),
            (VoiceCommonDataSchemas.PAN_BIAS_RANGE, 0, 0x35, 0x00),
            (VoiceCommonDataSchemas.EG_BIAS_DEVICE_ASSIGN_CC, 0, 0x36, 0x00),
            (VoiceCommonDataSchemas.EG_BIAS_RANGE, 0, 0x37, 0x00),
            (VoiceCommonDataSchemas.VOICE_VOLUME_DEVICE_ASSIGN_CC, 0, 0x38, 0x00),
            (VoiceCommonDataSchemas.VOICE_VOLUME_LIMIT_LOW, 0, 0x39, 0x00),
            (VoiceCommonDataSchemas.MICRO_TUNING_TABLE_SELECT, 0, 0x3A, 0x00),
            (VoiceCommonDataSchemas.RANDOM_PITCH_FLUCTUATION, 0, 0x3B, 0x00),
            # (VoiceCommonDataSchemas.PORTAMENTO_MODE, 0, 0x3C, 0x00),
            (VoiceCommonDataSchemas.PORTAMENTO_TIME, 0, 0x3D, 0x00),
            (VoiceCommonDataSchemas.VOICE_VOLUME, 0, 0x3F, 0x00),
        ]

        for schema, input_value, n2, v2 in test_cases:
            sysex_message = schema.create_sysex_message(input_value)
            self.assertEqual(sysex_message.hex(), self.SYSEX_TEMPLATE.format(n2, v2))

    def test_max(self):
        test_cases = [
            (VoiceCommonDataSchemas.WHEEL_PITCH_BEND_RANGE, 12, 0x28, 0x0C),
            (VoiceCommonDataSchemas.AFTER_TOUCH_PITCH_BEND_RANGE, 12, 0x29, 0x0C),
            (VoiceCommonDataSchemas.PITCH_MOD_DEVICE_ASSIGN_CC, 121, 0x2A, 0x79),
            (VoiceCommonDataSchemas.PITCH_MOD_RANGE, 127, 0x2B, 0x7F),
            (VoiceCommonDataSchemas.AMPLITUDE_MOD_DEVICE_ASSIGN_CC, 121, 0x2C, 0x79),
            (VoiceCommonDataSchemas.AMPLITUDE_MOD_RANGE, 127, 0x2D, 0x7F),
            (VoiceCommonDataSchemas.FILTER_MOD_DEVICE_ASSIGN_CC, 121, 0x2E, 0x79),
            (VoiceCommonDataSchemas.FILTER_MOD_RANGE, 127, 0x2F, 0x7F),
            (VoiceCommonDataSchemas.PAN_MOD_DEVICE_ASSIGN_CC, 121, 0x30, 0x79),
            (VoiceCommonDataSchemas.PAN_MOD_RANGE, 127, 0x31, 0x7F),
            (
                VoiceCommonDataSchemas.FILTER_CUT_OFF_BIAS_DEVICE_ASSIGN_CC,
                121,
                0x32,
                0x79,
            ),
            (VoiceCommonDataSchemas.FILTER_CUT_OFF_BIAS_RANGE, 127, 0x33, 0x7F),
            (VoiceCommonDataSchemas.PAN_BIAS_DEVICE_ASSIGN_CC, 121, 0x34, 0x79),
            (VoiceCommonDataSchemas.PAN_BIAS_RANGE, 127, 0x35, 0x7F),
            (VoiceCommonDataSchemas.EG_BIAS_DEVICE_ASSIGN_CC, 121, 0x36, 0x79),
            (VoiceCommonDataSchemas.EG_BIAS_RANGE, 127, 0x37, 0x7F),
            (VoiceCommonDataSchemas.VOICE_VOLUME_DEVICE_ASSIGN_CC, 121, 0x38, 0x79),
            (VoiceCommonDataSchemas.VOICE_VOLUME_LIMIT_LOW, 127, 0x39, 0x7F),
            (VoiceCommonDataSchemas.MICRO_TUNING_TABLE_SELECT, 65, 0x3A, 0x41),
            (VoiceCommonDataSchemas.RANDOM_PITCH_FLUCTUATION, 7, 0x3B, 0x07),
            # (VoiceCommonDataSchemas.PORTAMENTO_MODE, 0, 0x3C, 0x00),
            (VoiceCommonDataSchemas.PORTAMENTO_TIME, 127, 0x3D, 0x7F),
            (VoiceCommonDataSchemas.VOICE_VOLUME, 127, 0x3F, 0x7F),
        ]

        for schema, input_value, n2, v2 in test_cases:
            sysex_message = schema.create_sysex_message(input_value)
            self.assertEqual(sysex_message.hex(), self.SYSEX_TEMPLATE.format(n2, v2))
