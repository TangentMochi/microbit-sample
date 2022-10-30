from microbit import *
import music

# music template

music_list = [] #Your music data
while True:
    for note in music_list:
        if (note[0] == 0):
            sleep(note[1])
        else:
            music.pitch(note[0], note[1])
    sleep(5000)