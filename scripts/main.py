from FinalFile import *
from inputs import *

# How to use mido
# https://mido.readthedocs.io/en/latest/

# How to read midi files (Human)
# https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
# freq = 440*2**((n-69)/12)

# https://www.arduino.cc/reference/en/
# Arduino code
print(get_oper_sys())
song = get_midi_file()
multi_tracks = get_multi_tracks()

# Control rest of code from here
if multi_tracks == False:
    track_wanted = input("Which numerical track do you want?\n")
    FinalFile(music, oper_sys, track_wanted)
else:
    for x in range(max_track):
        FinalFile(music, oper_sys, x)


# Go through midi file
music = []
def enumerate_songs(track_wanted=1):
    """"Parses song and returns info on the track_wanted"""
    for i, track in enumerate(song.tracks):
        print("Enumerating through track:", i)
        if str(i) == str(track_wanted):
            for x in track:
                message = str(x).split()
                value = message[2]
                # Return the value along with the frequency
                if str(value[:5]) == "note=":
                    freq = 440 * 2 ** ((int(value[5:]) - 69) / 12)
                    freq = round(freq)
                    time = message[4][5:]
                    vel = message[3][9:]
                    # print("Frequency:", freq,"\nTime:", time, "\nVel:", vel, "\n")
                    note = [freq, int(time), int(vel)]
                    music.append(note)
        # print(music, i)


# Print track options
max_track = 0
for i, track in enumerate(song.tracks):
    # What the track has on it. eg guitar
    track_info = str(song.tracks[i]).split("\'")
    print("Track", i, track_info[1])
    print(track_info[2].strip()[:-1])
    if int(i) > int(max_track):
        max_track = int(i)
