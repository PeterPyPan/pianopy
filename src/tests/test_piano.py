import pygame

from pianopy.piano import Piano

pygame.init()


def test_piano():
    # test the number of keys for the number of octaves
    n_octaves_vals = range(1, 11)
    for n_octaves in n_octaves_vals:
        piano = Piano(n_octaves=n_octaves, screen_width=1200)
        assert len(piano._flat_key_rects) == n_octaves * 12
