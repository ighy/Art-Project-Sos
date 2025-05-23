import tkinter
import tkinter as tk
import tkinter.messagebox
import pyaudio
import wave
import os
import servermp3

class Analyser:
    def __init__(self):
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('500x300')
        self.main.title('Analyze')

        # Other
        self.column = 0
        self.row = 1
        self.filename = ''
        self.server = servermp3.ServerMp3(self.add_file)

        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=120, pady=20)
        self.buttonList = []

        # Pack Frame
        self.buttons.pack(fill=tk.BOTH)

        # Creating Buttons
        self.start_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Play', command=lambda: self.play_clip)
        self.start_button.grid(row=0, column=0, padx=50, pady=5)
        self.stop_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop', command=lambda: self.stop_clip)
        self.stop_button.grid(row=0, column=1, columnspan=1, padx=50, pady=5)
        self.approve_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Approve', command=lambda: self.approve_clip)
        self.approve_button.grid(row=0, column=2, padx=50, pady=5)
        self.flag_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Flag', command=lambda: self.flag_clip)
        self.flag_button.grid(row=0, column=3, columnspan=1, padx=50, pady=5)

    def add_file(self, filename):
        clip = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text=filename, command=lambda str=filename: self.select_clip(str))
        clip.grid(row=self.row, column=self.column, padx=50, pady=5)
        self.column += 1
        self.buttonList.append(clip)

    def select_clip(self, filename):
        self.filename = filename

    def play_clip(self):
        pass

    def stop_clip(self):
        pass

    def approve_clip(self):
        pass

    def flag_clip(self):
        pass

analyser = Analyser()
tkinter.mainloop()
