from mido import Message, get_input_names, get_output_names, open_input, open_output


def get_port_name_prompt(available_midi_ports):

    if len(available_midi_ports) > 1:
        port_names_list = "\n ".join(
            [f"{idx}: {port}" for idx, port in enumerate(available_midi_ports)]
        )
        port_index = input(f"Please select from the following:\n {port_names_list}\n")
        port_name = available_midi_ports[int(port_index)]
    else:
        port_name = available_midi_ports[0]

    return port_name


def get_in_port_name_prompt():
    return get_port_name_prompt(get_input_names())


def get_out_port_name_prompt():
    return get_port_name_prompt(get_output_names())


def get_in_port():
    return open_input(get_in_port_name_prompt())


def get_out_port():
    return open_output(get_out_port_name_prompt())


def log_incoming_midi_messages():
    """
    Very barebones utility to open a MIDI port and log messages as they come in.
    """

    port_name = get_port_name_prompt(get_input_names())

    if not port_name:
        return

    with open_input(port_name) as in_port:
        print(f"listening on port: {port_name}...")
        for message in in_port:
            if message.type == "clock":
                continue
            print(message)
