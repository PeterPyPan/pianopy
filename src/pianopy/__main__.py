import pygame

from pianopy import colors
from pianopy.midi import MidiMessage, close_midi_connection, setup_midi_connection
from pianopy.piano import Piano

N_OCTAVES = 10
SCREEN_SIZE = (1300, 200)
FPS = 30
BG_COLOR = colors.BLACK


def midi_data_callback(message, piano: Piano):
    # dismantle midi message and create MidiMessage
    (command, note, velocity), delta_time = message
    msg = MidiMessage(
        command=command, note=note, velocity=velocity, delta_time=delta_time
    )
    # make the piano handle the midi message
    piano.handle_key_press(midi_msg=msg)


def main():
    # pygame init
    pygame.init()

    # create a pygame display
    display = pygame.display.set_mode(SCREEN_SIZE)
    display.fill(BG_COLOR)

    # create a clock for fps control
    fps_clock = pygame.time.Clock()

    # Create a piano
    piano = Piano(n_octaves=N_OCTAVES, screen_width=SCREEN_SIZE[0])

    # setup midi connection
    midi_in = setup_midi_connection(data=piano, callback=midi_data_callback)

    # start the pygame loop
    while True:
        # handle the pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_midi_connection(midi_conn=midi_in)
                pygame.quit()
                quit()

            if event.type in (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEBUTTONDOWN,
            ):
                piano.handle_collisions(
                    mouse_pos=event.pos, mouse_pressed=pygame.mouse.get_pressed()[0]
                )

        # redraw the piano
        piano.draw(display=display, bg_color=BG_COLOR)

        pygame.display.update()

        # handle fps
        fps_clock.tick(FPS)


if __name__ == '__main__':
    main()
