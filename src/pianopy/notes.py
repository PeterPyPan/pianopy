from mingus.core.chords import determine as determine_chords
from mingus.core.notes import int_to_note, note_to_int

# Equivalent notes
NOTE_EQUIVALENTS = {
    'C': 'C',
    'C#': 'Db',
    'D': 'D',
    'D#': 'Eb',
    'E': 'E',
    'F': 'F',
    'F#': 'Gb',
    'G': 'G',
    'G#': 'Ab',
    'A': 'A',
    'A#': 'Bb',
    'B': 'B',
}

UNKNOWN_CHORD = 'Unknown Chord'


def get_chord_from_notes(notes):
    # we expect notes with flats
    if not all(n in NOTE_EQUIVALENTS for n in notes):
        raise ValueError(f'Provided notes cannot contain flat notes ({str(notes)}).')

    # work with a unique set of notes
    notes_unique = set(notes)

    if len(notes_unique) < 3:
        # less than 3 different notes is not a chord
        return UNKNOWN_CHORD

    # sort based on note value
    int_notes = sorted([note_to_int(n) for n in notes_unique])

    # convert ints back to notes in normal and equivalent set
    notes_unique = [int_to_note(n) for n in int_notes]
    notes_unique_eq = [NOTE_EQUIVALENTS[n] for n in notes_unique]

    # determine chords of normal and equivalent set
    chord_list = determine_chords(notes_unique, True)
    chord_list += determine_chords(notes_unique_eq, True)

    # if the number of chords is 0, the chord is unknown
    if len(chord_list) == 0:
        return UNKNOWN_CHORD

    # sort the chord list based on string length as the simplest chord is probably
    # the right one
    chord_list = sorted(chord_list, key=len)

    return chord_list[0]
