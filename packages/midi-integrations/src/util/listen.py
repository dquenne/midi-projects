from mido import get_input_names, open_input


def log_incoming_midi_messages():
    """
    Very barebones utility to open a MIDI port and log messages as they come in.
    """
    available_midi_ports = get_input_names()

    if len(available_midi_ports) > 1:
        port_names_list = "\n ".join(
            [f"{idx}: {port}" for idx, port in enumerate(available_midi_ports)]
        )
        port_index = input(f"Please select from the following:\n {port_names_list}\n")
        port_name = available_midi_ports[int(port_index)]
    else:
        port_name = available_midi_ports[0]

    if not port_name:
        return

    with open_input(port_name) as in_port:
        print(f"listening on port: {port_name}...")
        for message in in_port:
            print(message)
