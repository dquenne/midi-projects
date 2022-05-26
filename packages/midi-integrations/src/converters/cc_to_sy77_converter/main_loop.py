from mido.ports import BaseInput, BaseOutput
from src.integrations.sy77.message_schemas import VoiceCommonDataSchemas

cc_table = {
    60: lambda cc_value: VoiceCommonDataSchemas.PORTAMENTO_TIME.create_sysex_message(
        cc_value
    )
}

# VERY simple / hacky tool to intercept CCs and convert them to sysex


def forward_and_convert_midi_messages(in_port: BaseInput, out_port: BaseOutput):
    try:
        for message in in_port:
            if message.is_cc():
                cc_number = message.control
                if cc_number in cc_table:
                    sysex = cc_table[cc_number](message.value)
                    print(f"lookup matched, sending sysex: {sysex}")

                    out_port.send(sysex)
                    continue

            print(f"forwarding message {message}")
            out_port.send(message)
    except KeyboardInterrupt:
        pass
