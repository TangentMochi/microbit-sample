import math
import mido

SAMPLE_RATE = 44100
IX_ON_MSEC = 0  # int note onの時間　単位はミリ秒
IX_OFF_MSEC = 1  # int note offの時間　単位はミリ秒
IX_NOTE_NUMBER = 2  # int ノート番号
IX_VELOCITY = 3  # float 音量　範囲は0-1.0
IX_DULATION = 4  # float 音の長さ　単位は秒

def print_midi(file_path: str):
    print('MIDI')
    file = mido.MidiFile(file_path)
    print(file)
    for track in file.tracks:
        #print(track)
        for message in track:
            print(message)

    mid2bit(file_path)

def mid2bit(file_path):
    tempo = 50000.0
    file = mido.MidiFile(file_path)
    ticks_per_beat = file.ticks_per_beat
    for track in file.tracks:
        now = 0
        abs_time_tick_msec = tempo / ticks_per_beat / 1000.0
        notes = []
        for event in track:
            now = now + event.time * abs_time_tick_msec
            if event.type == 'set_tempo':
                tempo = event.tempo
                abs_time_tick_msec = tempo / ticks_per_beat / 1000.0
                print("BPM = ", 60000000.0 / tempo)
            elif event.type == 'note_on' and event.channel == 9:
                pass
            elif event.type == 'note_off' or (event.type == 'note_on' and event.velocity == 0):
                for note in notes:
                    if (note[IX_OFF_MSEC] == 0) and (note[IX_NOTE_NUMBER] == event.note):
                        note[IX_OFF_MSEC] = now
                        note[IX_DULATION] = (note[IX_OFF_MSEC] - note[IX_ON_MSEC]) / 1000.0
                        note[IX_VELOCITY] = note[IX_VELOCITY] / 127.0
            elif event.type == 'note_on':
                notes.append([math.floor(now), 0, event.note, event.velocity, 0])
        if len(notes) > 0:
            print(len(notes))
            tmp_notes_list = notes2list(notes)
            print("MusicData>> ", tmp_notes_list)

def notes2list(notes):
    note_list = [[0, 0, 0, 0]]

    for note in notes:
        if note[IX_DULATION] > 0:
            freq = 440.0 * 2 ** ((note[IX_NOTE_NUMBER] - 69) / 12)
            dulation = note[IX_DULATION] * 1000
            start = note[IX_ON_MSEC]
            end = note[IX_OFF_MSEC]
            velocity = note[IX_VELOCITY]
            note_list.append([
                freq,
                start,
                end,
                velocity,
            ])

    final_list = []

    for note_index in range(len(note_list) - 1):
        note = note_list[note_index]
        next_note = note_list[note_index + 1]
        final_list.append([
            int(note[0]), int(note[2] - note[1])
        ])
        if next_note[1] - note[2] > 10:
            final_list.append([
                0, int(next_note[1] - note[2])
            ])
    
    return final_list

print_midi(input("File>>"))