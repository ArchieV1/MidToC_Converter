import os

# Go through midi file (song) and add the notes to music[]
def enumerate_song(track_wanted, song):
    """"Parses song and returns info on the track_wanted"""
    music = []
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
    return music


def FinalFile(music, oper_sys, track_wanted, midi_file):
    """Creates the .c file for either windows or arduino"""
    enumerate_song(track_wanted)
    loop = []
    # Start bit of code
    # Arduino or windows?
    if oper_sys.upper() == "ARDUINO":
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

