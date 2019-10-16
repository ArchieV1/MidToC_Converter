import mido

#How to use mido
#https://mido.readthedocs.io/en/latest/

#How to read midi files (Human)
#https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
#freq = 440*2**((n-69)/12)

song = mido.MidiFile("mary.mid")

#Go through midi file

music = []
for i, track in enumerate(song.tracks):
    print("Track", i)
    for x in track:
        message = str(x).split()
        value = message[2]
        #print(x)
        #Return the value along with the frequency
        if str(value[:5]) == "note=":
            freq = 440*2**((int(value[5:])-69)/12)
            freq = round(freq)
            time = message[4][5:]
            vel = message[3][9:]
            print("Frequency:", freq,"\nTime:", time, "\nVel:", vel, "\n")
            note= [freq, int(time), int(vel)]
            music.append(note)

print(music)
