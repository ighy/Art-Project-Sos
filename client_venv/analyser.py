import tkinter
import tkinter as tk
import tkinter.messagebox
#import pyaudio
import wave
import os

main = tkinter.Tk()
collections = []
main.geometry('500x300')
main.title('Analyze')

# Set Frames
buttons = tkinter.Frame(main, padx=120, pady=20)

# Pack Frame
buttons.pack(fill=tk.BOTH)

# Start and Stop buttons
index = 0

tkinter.mainloop()

def add_file(filename):
    play_clip = tkinter.Button(buttons, width=10, padx=10, pady=5, text=f'Play {filename}', command=lambda: play_clip(filename))
    play_clip.grid(row=0, column=0, padx=50, pady=5)
    approve_clip = tkinter.Button(buttons, width=10, padx=10, pady=5, text='Approve', command=lambda: approve_clip(filename))
    approve_clip.grid(row=1, column=0, columnspan=1, padx=50, pady=5)
    flag_clip = tkinter.Button(buttons, width=10, padx=10, pady=5, text='Flag', command=lambda: flag_clip(filename))
    flag_clip.grid(row=1, column=0, columnspan=1, padx=50, pady=5)

def play_clip(filename):
    pass

def approve_clip(filename):
    pass

def flag_clip(filename):
    pass

add_file("recording_0")
add_file("recording_1")