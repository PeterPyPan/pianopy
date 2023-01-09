import pytest

from pianopy.notes import get_chord_from_notes


def test_get_chord_from_notes():
    assert get_chord_from_notes(notes=['C', 'E', 'G']) == 'CM'
    assert get_chord_from_notes(notes=['E', 'G', 'C']) == 'CM'
    assert get_chord_from_notes(notes=['G', 'C', 'E']) == 'CM'
    assert get_chord_from_notes(notes=['C', 'E', 'C', 'E', 'G']) == 'CM'
    assert get_chord_from_notes(notes=['C', 'E', 'G', 'B']) == 'CM7'
    assert get_chord_from_notes(notes=['C', 'D#', 'G']) == 'Cm'

    with pytest.raises(ValueError):
        get_chord_from_notes(notes=['C', 'Eb', 'G'])
