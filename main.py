import mido
import os

# How to use mido
# https://mido.readthedocs.io/en/latest/

# How to read midi files (Human)
# https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
# freq = 440*2**((n-69)/12)

# https://www.arduino.cc/reference/en/
# Arduino code

midi_file = input("Link to midi file\n")
if midi_file == "":
    midi_file = "ELO - do ya"

pin = input("Which is the output pin?\n")
song = mido.MidiFile(str(midi_file.upper() + ".mid"))
oper_sys = input("Arduino or no?\n")

# Go through midi file
music = []

# Print track options
max_track = 0
for i, track in enumerate(song.tracks):
    # What the track has on it. eg guitar
    track_info = str(song.tracks[i]).split("\'")
    print("Track", i, track_info[1])
    print(track_info[2].strip()[:-1])
    if int(i) > int(max_track):
        max_track = int(i)


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


def FinalFile(music, oper_sys, track_wanted):
    """Creates the .c file for either windows or arduino"""
    enumerate_songs(track_wanted)
    loop = []
    # Start bit of code
    # Arduino or windows?
    if oper_sys.upper == "ARDUINO":
        # Setup code for an arduino
        code = "void setup(){ \n    //Setup code goes here \n    pinMode(" + \
               pin + \
               ", OUTPUT);\n    }\n" + \
               "void loop(){ \n    //Repeated code goes here\n"
    else:
        # Setup code for windows
        code = "//Import windows stuff \n" \
               "#include <stdio.h> \n" \
               "#include <stdlib.h>\n" \
               "#include <windows.h>\n" \
               "#include <dos.h>\n\n" \
               "main();\n" \
               "main(){\n"

    # Create and add middle bit of code
    for i in music:
        # If vel is 0 play no sound
        # delay(ms)
        if i[2] == 0:
            if oper_sys.upper() == "ARDUINO":
                code_line = "    delay(" + str(i[0]) + ");\n"
            else:
                code_line = "    Sleep(" + str(i[0]) + ");\n"
        # If vel isn't zero play a sound
        # tone(pin, frequency, duration)
        else:
            if oper_sys.upper() == "ARDUINO":
                # For arduino
                code_line = "    tone(" + str(pin) + ", " + str(i[0]) + ", " + str(i[1]) + "); \n"
            else:
                # For windows
                code_line = "    Beep(" + str(i[0]) + ", " + str(i[1]) + "); \n    printf(\"NOTE\");\n"
        code = code + str(code_line)

    # Finish code
    code = code + "}"

    # Set the OS to be windows for the file name
    if oper_sys.upper() != "ARDUINO":
        oper_sys = "Windows"

    # Make the final .c file
    if os.path.exists(midi_file) == False:
        os.mkdir(midi_file)
    open(str(midi_file + "\\" + midi_file + " - " + oper_sys.upper() + str(track_wanted) + ".c"), "w").write(code)

    # Try and compile C programs
    # CD to right dir
    dir = os.path.dirname(os.path.realpath(__file__)) + "\\" + midi_file
    os.chdir(dir)

    # Enumerate through all of the created .c files and convert them to .exe and delete the .c files
    for file_name in os.listdir(dir):
        print("Converting:" + file_name)
        create_exe = str("gcc \"" + midi_file + " - " + oper_sys.upper() + str(track_wanted) + "\" \"" + file_name + "\"")
        print(create_exe)
        os.system(create_exe)


# Multi tracks or single
multi_tracks = bool(input("Do you want multiple tracks? True or False\n"))
if multi_tracks == False:
    track_wanted = input("Which numerical track do you want?\n")
    FinalFile(music, oper_sys, track_wanted)
else:
    for x in range(max_track):
        FinalFile(music, oper_sys, x)
