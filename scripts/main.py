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
# Returns the midi file and the midi file name
midi_file_full = get_midi_file()

# midi_file = "mido.midifiles.midifiles.MidiFile"
midi_file = midi_file_full[0]
# midi_file_name is the name asked for earlier
midi_file_name = midi_file_full[1]

# Returns if multi track or not and if it is which track to use
multi_tracks = get_multi_tracks()

oper_sys = get_oper_sys()
if oper_sys == "ARDUINO":
    pin = get_pin()
else:
    pin = None

# Create the final file with either 1 track or many
if multi_tracks == False:
    # Returns which track is wanted
    get_track_wanted = get_track_wanted()
    track_wanted = get_track_wanted

    # Create a list of notes to create music
    music = enumerate_song(track_wanted, midi_file)
    # Created the final file using that track
    FinalFile(music, track_wanted, midi_file_name, oper_sys)

else:
    # Returns which track is wanted
    max_track = get_max_track(midi_file)
    for track in range(max_track):
        music = enumerate_song(max_track, midi_file)
        FinalFile(music, track, midi_file_name, oper_sys)


