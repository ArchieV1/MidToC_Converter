import mido
import os

dir_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.dirname(dir_path)


def get_midi_file():
    """Get the name of the input file. Returns mido.midifiles.midifiles.MidiFile"""
    midi_file_name = str(parent_path + "\\" + input("Link to midi file\nFile should be in source root\n"))
    # Set default midi file
    if midi_file_name == str(parent_path + "\\"):
        midi_file_path = str(parent_path + "\\ELO - do ya.mid")
    # Determine if .mid needs appending or not
    try:
        if midi_file_path.upper()[-4:] == ".MID":
            song = mido.MidiFile(midi_file_path.upper())
            print("Loaded:\n" + midi_file_path + "\n")

        else:
            song = mido.MidiFile(str(midi_file_path.upper() + ".MID"))
            print("Loaded:\n" + midi_file_path + ".mid\n")

        # Just return the name of the midi file not the path
        return song, midi_file_path.split("\\")[-1]

    except AssertionError:
        print("Failed to find midi file\n"
              "Please input the exact name (Case does not matter)")
        get_midi_file()


def get_multi_tracks():
    """Ask whether multi tracks or single track"""
    multi_tracks = input("Do you want multiple tracks? Yes or No\n")
    if multi_tracks.upper() == "YES":
        multi_tracks = True
    elif multi_tracks.upper() == "NO":
        multi_tracks = False
    else:
        print("Please input either \"yes\" or \"no\". You will be asked for track number next")
        get_multi_tracks()
    return multi_tracks


def get_oper_sys():
    """Check whether for arduino or windows"""
    oper_sys = input("Will this be run on an Arduino or Windows Machine? Ard or Win\n")
    if oper_sys.upper() == "WIN" or oper_sys.upper() == "WINDOWS":
        return "WINDOWS"
    elif oper_sys.upper() == "ARD" or oper_sys.upper() == "ARDUINO":
        return "ARDUINO"
    else:
        print("Did not recognise given platform. Please input either \"Ard\" or \"Win\"")
        return get_oper_sys()


def get_pin():
    """Ask which is the output pin for arduino"""
    try:
        pin = int(input("Which is the output pin?\n"))
        return pin
    except ValueError:
        print("Please enter an integer value")
        return get_pin()


def get_track_wanted():
    """Ask which track is wanted"""
    try:
        track_wanted = int(input("Which numerical track do you want?\n"))
        return track_wanted
    except ValueError:
        print("Please only input integer track numbers")
        return get_track_wanted()


def get_max_track(song):
    # Print track options
    max_track = 0
    for i, track in enumerate(song.tracks):
        # What the track has on it. eg guitar
        track_info = str(song.tracks[i]).split("\'")
        print("Track", i, track_info[1])
        print(track_info[2].strip()[:-1])
        if int(i) > int(max_track):
            max_track = int(i)
    return max_track
