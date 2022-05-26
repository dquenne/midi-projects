"""
-1 0xF0
 0 0x43
 1 Device Number
 2 Message group (Parameter change 0x34 vs Bulk dump 0x7A)
 3 Parameter ID (b0-b3) + operator number (b4-6)
 4 (a) MIDI Note (b0-b6)
   (b) element number (b5-b6) + filter number (b0-b2)
   (c) element number (b5-b6)
   (d) voice channel number (b0-b3)
   (e) memory number (b0-b4)
 5 N1
 6 N2
 7 V1 (MSB)
 8 V2 (LSB)
 9 0xF7
"""
from mido import Message

from .converters.base_converter import BaseConverter
from .data_models import Sy77ParameterValue
from .types import ParameterChangeType, VoiceElement
from .util import check_is_within_number_of_bits


class ParameterChangeMessageSchema:
    BYTE_0 = 0x43
    MESSAGE_GROUP = 0x34
    DEVICE_NUMBER = 0x5  # FIXME: Make configurable - this is user-set and shouldn't be part of the schema

    def __init__(
        self,
        parameter_change_type: ParameterChangeType,
        n1: int,
        n2: int,
    ):
        if not check_is_within_number_of_bits(
            value=parameter_change_type.value, num_bits=4
        ):
            raise ValueError("parameter_change_type must be 4 bits")
        self.parameter_change_type = parameter_change_type
        self.parameter_id_lsb_n1 = n1
        self.parameter_id_msb_n2 = n2

    def _build_sysex_message(
        self,
        *,
        value: Sy77ParameterValue,
        operator_number: int = 0b000,
        fourth_byte: int = 0x00,
    ):

        if not check_is_within_number_of_bits(value=operator_number, num_bits=3):
            raise ValueError("operator_number must be 3 bits")

        return Message(
            "sysex",
            data=[
                self.BYTE_0,
                0b00010000 ^ self.DEVICE_NUMBER,
                self.MESSAGE_GROUP,
                (operator_number << 4) + self.parameter_change_type.value,
                fourth_byte,
                self.parameter_id_lsb_n1,
                self.parameter_id_msb_n2,
                value.msb_v1,
                value.lsb_v2,
            ],
        )


class MultiCommonDataMessageSchema(ParameterChangeMessageSchema):
    def __init__(self, n2: int, value_converter: BaseConverter):
        super().__init__(
            parameter_change_type=ParameterChangeType.MULTI_COMMON_DATA, n1=0, n2=n2
        )
        self.value_converter = value_converter

    def create_sysex_message(self, value):
        converted_value = self.value_converter.convert(value)

        return self._build_sysex_message(
            value=converted_value,
        )


class VoiceCommonDataSchema(ParameterChangeMessageSchema):
    def __init__(self, n2: int, value_converter: BaseConverter):
        super().__init__(
            parameter_change_type=ParameterChangeType.VOICE_COMMON_DATA, n1=0, n2=n2
        )
        self.value_converter = value_converter

    def create_sysex_message(self, value):
        converted_value = self.value_converter.convert(value)

        return self._build_sysex_message(
            value=converted_value,
        )


class VoiceElementDataSchema(ParameterChangeMessageSchema):
    def __init__(self, n2: int, value_converter: BaseConverter):
        super().__init__(
            parameter_change_type=ParameterChangeType.VOICE_ELEMENT_DATA, n1=0, n2=n2
        )
        self.value_converter = value_converter

    def create_sysex_message(self, voice_element: VoiceElement, value):
        converted_value = self.value_converter.convert(value)

        fourth_byte = (
            voice_element.value << 5
        )  # voice_element is defined by bits 5 and 6 of byte 4

        return self._build_sysex_message(
            fourth_byte=fourth_byte,
            value=converted_value,
        )
