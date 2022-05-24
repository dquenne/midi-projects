from unittest import TestCase

from ..constants import VoiceCommonDataParameter, VoiceElementMode
from ..encode import encode_sy77_voice_common_data_message


class TestEncodeSy77VoiceCommonDataMessage(TestCase):
    def test_success(self):
        sysex_message = encode_sy77_voice_common_data_message(
            VoiceCommonDataParameter.ELEMENT_MODE,
            VoiceElementMode.MODE_2_AFM_POLY.value,
        )
        self.assertEqual(sysex_message.hex(), "F0 43 12 34 02 00 00 00 00 04 F7")
