from scripts.FinalFile import *
from scripts.inputs import *

# Help files
# How to use mido
# https://mido.readthedocs.io/en/latest/
# How to read midi files (Human)
# https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
# freq = 440*2**((n-69)/12)
# https://www.arduino.cc/reference/en/
# Arduino code

# Inputs
# Returns to song var after asking for filename
midi_file = get_midi_file()

# Returns if multi track or not
multi_tracks = get_multi_tracks()

# Returns if windows or arduino
oper_sys = get_oper_sys()
if oper_sys == "ARDUINO":
    pin = get_pin()


# Create the final file with either 1 track or many
if multi_tracks == False:
    # Returns which track is wanted
    get_track_wanted = get_track_wanted(midi_file)
    track_wanted = get_track_wanted[0]

    # Created the final file using that track
    FinalFile(enumerate_song(track_wanted, midi_file), oper_sys, track_wanted, midi_file)

else:
    # Returns which track is wanted
    max_track = get_max_track(midi_file)
    for x in range(max_track):
        FinalFile(enumerate_song(max_track, midi_file), oper_sys, x, midi_file)


