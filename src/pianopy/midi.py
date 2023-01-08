from dataclasses import dataclass

from rtmidi import NoDevicesError
from rtmidi.midiutil import open_midiinput


@dataclass
class MidiMessage:
    command: int
    note: int
    velocity: int
    delta_time: float


def setup_midi_connection(data, callback):
    try:
        midi_in, port_name = open_midiinput(0)
        midi_in.set_callback(func=callback, data=data)
    except NoDevicesError:
        print('No midi input devices found')
        midi_in = None
    return midi_in


def close_midi_connection(midi_conn):
    if midi_conn is None:
        return
    midi_conn.close_port()
