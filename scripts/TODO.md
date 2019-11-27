## TODO
### Broken:  
- Something to do with the name "Happy-Birthday-To-You-2"  
- Don't think create_exes is always being called  
- Something to do with  
`Traceback (most recent call last):  
  File "E:/.Newcastle/PyCharm/MidToC_Converter/scripts/main.py", line 15, in <module>  
    midi_file_full = get_midi_file()  
  File "E:\.Newcastle\PyCharm\MidToC_Converter\scripts\inputs.py", line 23, in get_midi_file  
    song = mido.MidiFile(str(midi_file_path.upper() + ".MID"))  
  File "C:\Users\green\AppData\Local\Programs\Python\Python37-32\lib\site-packages\mido\midifiles\midifiles.py", line 315, in __init__  
    with io.open(filename, 'rb') as file:  
FileNotFoundError: [Errno 2] No such file or directory: 'E:\\.NEWCASTLE\\PYCHARM\\MIDTOC_CONVERTER\\TEST.MID'"`  
  
- Still not certain about timing.

### Update  
- Maybe change the windows beeps to be MessageBeep s instead
/* Include one of these in a function */   
MessageBeep(MB_OK);              /* play Windows default beep */  
MessageBeep(MB_ICONINFORMATION); /* play asterisk sound */  
MessageBeep(MB_ICONQUESTION);    /* play question sound */  
MessageBeep(MB_ICONWARNING);     /* play warning sound */  
Then different tracks can have different sounds