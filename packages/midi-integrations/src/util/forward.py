from mido import open_input, open_output
from src.converters.cc_to_sy77_converter.main_loop import (
    forward_and_convert_midi_messages,
)
from src.util.listen import get_in_port_name_prompt, get_out_port_name_prompt


def forward():

    print("for input port...")
    in_port_name = get_in_port_name_prompt()

    print("for output port...")
    out_port_name = get_out_port_name_prompt()

    if not in_port_name or not out_port_name:
        print("bad port names?")
        return

    with open_input(in_port_name) as in_port:
        print(f"listening on port: {in_port_name}...")
        with open_output(out_port_name) as out_port:
            print(f"forwarding to port: {out_port_name}...")
            forward_and_convert_midi_messages(in_port, out_port)

    print("done listening / forwarding!")


if __name__ == "__main__":
    forward()
