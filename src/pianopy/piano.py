from enum import Enum

import numpy as np
import pygame
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

from pianopy import colors
from pianopy.midi import MidiMessage
from pianopy.notes import get_chord_from_notes

# z-order values for drawing layer by layer
Z_ORDER_VALS = [0, 1]

# piano key sizes and spacing
WHITE_KEY_SIZE = np.array((16, 80))
BLACK_KEY_SIZE = np.array((12, 40))
KEY_SPACING = 1

# vertical position of text
TEXT_Y_POS = 120

# white and black note names
WHITE_NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
BLACK_NOTES = ['C#', 'D#', None, 'F#', 'G#', 'A#', None]


class Piano:
    def __init__(self, screen_width, n_octaves=10):
        # calculate start position
        piano_width = get_piano_width(n_octaves=n_octaves)
        start_x = int((screen_width - piano_width) / 2)
        start_pos = np.array([start_x, 0])

        # z-order mapped keys
        self._key_rects = {z: [] for z in Z_ORDER_VALS}
        # flat list of keys
        self._flat_key_rects = _get_key_rects(n_octaves=n_octaves, start_pos=start_pos)
        # z-order mapped dict of list of keys
        for key_rect in self._flat_key_rects:
            self._key_rects[key_rect.z_order].append(key_rect)

        # initialize text related objects
        self._font_obj = pygame.font.SysFont(name='Arial', size=50)
        self._text_obj = None

    def _get_text_rect(self, display):
        x, y, w, h = self._text_obj.get_rect(center=display.get_rect().center)
        return (x, TEXT_Y_POS, w, h)

    def display_text(self, text, bg_color, display=None):

        if self._text_obj is not None:
            # if old text obj exists, draw a bg color box on top of it
            pygame.draw.rect(
                display, color=bg_color, rect=self._get_text_rect(display=display)
            )

        if display is not None:
            self._text_obj = self._font_obj.render(text, True, colors.WHITE)
            display.blit(self._text_obj, self._get_text_rect(display=display))

    def draw(self, display, bg_color):
        # draw bg colored rectangle over old text
        self.display_text(
            text=str(self.current_chord), display=display, bg_color=bg_color
        )

        # draw each layer
        for _z_order, z_key_rects in self._key_rects.items():
            for key_rect in z_key_rects:
                pygame.draw.rect(
                    display, color=key_rect.color, rect=key_rect.pygame_rect
                )

    @property
    def pressed_notes(self):
        return list(filter(None, (k.pressed_note for k in self._flat_key_rects)))

    @property
    def current_chord(self):
        return get_chord_from_notes(notes=self.pressed_notes)

    def handle_key_press(self, midi_msg: MidiMessage):
        try:
            key = self._flat_key_rects[midi_msg.note]
        except IndexError:
            print(f'out of bounds note: {midi_msg.note}')
            return

        if midi_msg.command == NOTE_ON:
            key.key_state = KeyState.DOWN
        elif midi_msg.command == NOTE_OFF:
            key.key_state = KeyState.UP

    def handle_collisions(self, mouse_pos, mouse_pressed):
        # first deactivate all keys
        for key in self._flat_key_rects:
            key.key_state = KeyState.UP

        # compute collision until first collision occurrence
        for z_order in reversed(self._key_rects.keys()):
            for key_rect in self._key_rects[z_order]:
                collision = key_rect.mouse_collision(
                    mouse_pos=mouse_pos, mouse_pressed=mouse_pressed
                )

                # stop collision detection as we want expect only 1 collision at most
                if collision:
                    return


class KeyState(Enum):
    UP = 'up'
    SELECT = 'select'
    DOWN = 'down'


class PianoKey:
    def __init__(self, pygame_rect: pygame.Rect, note: str):
        self.pygame_rect = pygame_rect
        self._note = note
        self._is_white_note = len(note) == 1
        self._z_order = len(note) - 1
        self._key_state = KeyState.UP

        # setup state-color map
        self._state_color_map = {
            KeyState.DOWN: colors.BLUE,
            KeyState.SELECT: colors.GREEN,
        }
        if self._is_white_note:
            self._state_color_map[KeyState.UP] = colors.WHITE
        else:
            self._state_color_map[KeyState.UP] = colors.BLACK

    @property
    def pressed_note(self):
        return self._note if self._key_state == KeyState.DOWN else None

    @property
    def z_order(self):
        return self._z_order

    @property
    def color(self):
        return self._state_color_map[self._key_state]

    @property
    def key_state(self):
        return self._key_state

    @key_state.setter
    def key_state(self, value: KeyState):
        self._key_state = value

    def mouse_collision(self, mouse_pos, mouse_pressed):
        collision = self.pygame_rect.collidepoint(mouse_pos[0], mouse_pos[1])
        if not collision:
            self.key_state = KeyState.UP
            return False

        if mouse_pressed:
            self.key_state = KeyState.DOWN
        else:
            self.key_state = KeyState.SELECT
        return True


def _get_key_rects(start_pos: np.ndarray, n_octaves: int = 3):
    key_coords, notes = _get_piano_coords(n_octaves=n_octaves)

    # add start_pos to key coords
    key_coords[:, 0] = key_coords[:, 0] + start_pos[0]

    rects = []
    for key_coord, note in zip(key_coords, notes):
        pygame_rect = pygame.Rect(tuple(key_coord))
        key_rect = PianoKey(pygame_rect=pygame_rect, note=note)
        rects.append(key_rect)

    return rects


def get_piano_width(n_octaves: int):
    n_whites = n_octaves * 7
    return n_whites * (WHITE_KEY_SIZE[0] + KEY_SPACING)


def _get_piano_coords(n_octaves: int):
    # draw white keys
    n_keys = n_octaves * 7
    white_coords = np.zeros((n_keys, 4))
    # start_x
    white_coords[:, 0] = np.arange(n_keys) * (WHITE_KEY_SIZE[0] + KEY_SPACING)
    # start_y
    white_coords[:, 1] = np.zeros(n_keys)
    # end_x
    white_coords[:, 2] = WHITE_KEY_SIZE[0]
    # end_y
    white_coords[:, 3] = WHITE_KEY_SIZE[1]

    # generate black coords
    black_coords = np.array(white_coords)
    # start_x of black keys is half a key width to the left
    black_coords[:-1, 0] = black_coords[1:, 0] - BLACK_KEY_SIZE[0] / 2.0
    # end_x of black keys is half of a key width to the right
    black_coords[:, 2] = BLACK_KEY_SIZE[0]
    # end_y
    black_coords[:, 3] = BLACK_KEY_SIZE[1]

    key_coords = []
    notes = []
    for i_key, (white_coord, black_coord) in enumerate(zip(white_coords, black_coords)):
        i_key_mod = i_key % 7
        # white notes
        white_note = WHITE_NOTES[i_key_mod]
        key_coords.append(white_coord)
        notes.append(white_note)

        # black notes
        black_note = BLACK_NOTES[i_key_mod]
        if black_note is not None:
            key_coords.append(black_coord)
            notes.append(black_note)

    return np.array(key_coords), notes
