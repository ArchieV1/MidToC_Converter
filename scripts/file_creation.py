from scripts.inputs import *
from mido import tick2second


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
                    time = message[4][5:]
                    print(time)
                    # Change ticks to seconds with a tempo of 500000 (120BMP)
                    # tempo = 500000
                    tempo = (1/125)*60*10**6
                    time = tick2second(int(time), int(song.ticks_per_beat), tempo)
                    print(time)

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
               "#include <Windows.h>\n" \
               "void main();\n" \
               "void main(){\n"

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
                code_line = "    tone(" + str(pin) + ", " + str(round(float(i[0]*1000))) + ", " + str(i[1]) + "); \n"
            else:
                # For windows
                code_line = "    Beep(" + str(i[0]) + ", " + str(round(float(i[1]*1000))) + "); \n    printf(\"NOTE\");\n"
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
        print("Directory created")

    # Create the file name in write mode.
    # Example line:
    # MidToC_Converter\ELO - do ya.mid\ELO - do ya.mid - WINDOWS6.c
    file_name = midi_file_name + "\\" + midi_file_name + " - " + oper_sys.upper() + str(track_wanted) + ".c"
    open(file_name, "w").write(code)


def create_exes(directory_path):
    # Try and compile C programs
    # CD to right dir

    os.chdir(directory_path)

    # Enumerate through all of the created .c files and convert them to .exe and delete the .c files
    for file_name in os.listdir(directory_path):
        print("Converting: " + file_name)
        # Example command
        # gcc -o "ELO - do ya.mid - WINDOWS6.exe" "ELO - do ya.mid - WINDOWS6.c"
        exe_name = file_name.replace(".mid", "mid").split(".")[0] + ".exe"
        # -o (Output) NEWFILENAME
        create_exe = "gcc -o \"{}\" \"{}\"".format(exe_name, file_name)
        os.system(create_exe)
        print(f"{exe_name} created\n")


