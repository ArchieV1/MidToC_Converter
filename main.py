import mido

#How to use mido
#https://mido.readthedocs.io/en/latest/

#How to read midi files (Human)
#https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
#freq = 440*2**((n-69)/12)

#https://www.arduino.cc/reference/en/
#Arduino code

midi_file = input("Link to midi file\n")
if midi_file == "":
    midi_file = "The_Cars_-_You_Might_Think.mid"

pin = input("Which is the output pin?\n")
song = mido.MidiFile(midi_file)

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
            #print("Frequency:", freq,"\nTime:", time, "\nVel:", vel, "\n")
            note = [freq, int(time), int(vel)]
            music.append(note)

print(music)

def FinalFile(music):
    loop = []
    #Start bit of code
    code = "void setup(){ \n    //Setup code goes here \n   pinMode(" + \
           pin + \
           "OUTPUT)\n}" +\
           "void loop(){ \n    //Repeated code goes here\n"

    #Create and add middle bit of code
    for i in music:
        #If vel is 0 play no sound
        #delay(ms)
        if i[2] == 0:
            code_line = "    delay(" + str(i[0]) + ");\n"
        #If vel isn't zero play a sound
        #tone(pin, frequency, duration)
        else:
            code_line = "    tone(" + str(pin) + ", " + str(i[0]) + ", " + str(i[1]) + "); \n"
        code = code + str(code_line)

    #Finish code
    code = code + "}"
    return code

print(FinalFile(music))