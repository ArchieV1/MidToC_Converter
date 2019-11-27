from scripts.file_creation import *
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

# Get the OS and if it's arduino ask for pin number
oper_sys = get_oper_sys()
if oper_sys == "ARDUINO":
    pin = get_pin()
else:
    pin = None

# Create the final file with either 1 track or many
if multi_tracks:
    # Returns how many tracks there are
    max_track = get_max_track(midi_file)

    # Create a file for each track.
    # So a file with 6 tracks (With notes) will create 6 files
    for track in range(max_track):
        # Create a list of notes to create music
        music = enumerate_song(max_track, midi_file)
        create_file(music, track, midi_file_name, oper_sys, pin)

else:
    # Returns which track is wanted
    get_track_wanted = get_track_wanted()
    track_wanted = get_track_wanted

    # Create a list of notes to create music
    music = enumerate_song(track_wanted, midi_file)
    # Created the final file using that track
    create_file(music, track_wanted, midi_file_name, oper_sys, pin)

# Create the exes
directory_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + midi_file_name
create_exes(directory_path)