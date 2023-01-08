from dataclasses import dataclass


@dataclass
class MidiMessage:
    command: int
    note: int
    velocity: int
    delta_time: float
