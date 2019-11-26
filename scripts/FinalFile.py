from scripts.inputs import *


# Go through midi file (song) and add the notes to music[]
def enumerate_song(track_wanted, song):
    """"Parses song and returns info on the track_wanted"""
    music = []
    for i, track in enumerate(song.tracks):
        # i is the track number (Starting at 0)
        # track is the actual track data

        print("Enumerating through track:", i)

        # Check this is the track that is actually wanted (If only 1 track if being done)
        if str(i) == str(track_wanted):
            for data in track:
                message = str(data).split()
                note = message[2]
                # Return the value along with the frequency
                if str(note[:5]) == "note=":
                    # The maths to get the freq right
                    # value[5:] is the number from "note=XX"
                    freq = 440 * 2 ** ((int(note[5:]) - 69) / 12)
                    freq = round(freq)

                    # Make time an int
                    time = int(message[4][5:])

                    # Make vel an int
                    vel = int(message[3][9:])

                    # print("Frequency:", freq,"\nTime:", time, "\nVel:", vel, "\n")
                    final_note = [freq, time, vel]
                    music.append(final_note)
    return music


def create_file(music, track_wanted, midi_file_name, oper_sys, pin):
    """
    Creates the .c file for either windows or arduino
    :param music: List of notes with timings and velocity (From enumerate_song)
    :param oper_sys: The operating system
    :param track_wanted: Which track(s) wanted from the midi file
    :param midi_file_name: Name of the midi_file_name
    :param pin: The pin for arduinos
    :return: None. Creates the .h files
    """
    # Not used anywhere??/
    #
    #enumerate_song(track_wanted, song)
    #loop = []
    #

    # Returns if windows or arduino


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
        # delay(ms) or Sleep(ms)
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
        # Append to the long "code" variable that will written to the .c file
        code = code + str(code_line)

    # Finish code
    code = code + "}"

    # Set the OS to be windows for the file name
    if oper_sys.upper() != "ARDUINO":
        oper_sys = "Windows"

    # Make the final .c file
    # If the folder doesn't exist create it
    if os.path.exists(midi_file_name) == False:
        os.mkdir(midi_file_name)

    # Create the file name in write mode.
    # Example line:
    # MidToC_Converter\ELO - do ya.mid\ELO - do ya.mid - WINDOWS6.c
    open(str(midi_file_name + "\\" +
             midi_file_name + " - " + oper_sys.upper() + str(track_wanted) + ".c"), "w").write(code)

    # Try and compile C programs
    # # CD to right dir
    # dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + midi_file
    # os.chdir(dir_path)
    #
    # # Enumerate through all of the created .c files and convert them to .exe and delete the .c files
    # for file_name in os.listdir(dir_path):
    #     print("Converting:" + file_name)
    #     create_exe = str("gcc \"" + midi_file + " - " + oper_sys.upper() + str(track_wanted) + "\" \"" + file_name + "\"")
    #     print(create_exe)
    #     os.system(create_exe)

