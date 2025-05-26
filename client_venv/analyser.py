import tkinter
import tkinter as tk
import tkinter.messagebox
import threading
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
        self.server = servermp3.ServerMp3()

        # Set Frames
        self.buttons = tkinter.Frame(self.main, padx=120, pady=20)
        self.buttonList = []

        # Pack Frame
        self.buttons.pack(fill=tk.BOTH)

        # Creating Buttons
        self.start_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Play', command=self.play_clip)
        self.start_button.grid(row=0, column=0, padx=50, pady=5)
        self.stop_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop', command=lambda: self.stop_clip)
        self.stop_button.grid(row=0, column=1, columnspan=1, padx=50, pady=5)
        self.approve_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Approve', command=lambda: self.approve_clip)
        self.approve_button.grid(row=0, column=2, padx=50, pady=5)
        self.flag_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Flag', command=lambda: self.flag_clip)
        self.flag_button.grid(row=0, column=3, columnspan=1, padx=50, pady=5)
        self.flag_button = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='End Server', command=lambda: self.server.end_server)
        self.flag_button.grid(row=0, column=4, columnspan=1, padx=50, pady=5)

    def add_file(self, filename):
        clip = tkinter.Button(self.buttons, width=15, padx=10, pady=5, text=str(filename).split("/")[1], command=lambda text=filename: self.select_clip(text))
        clip.grid(row=self.row, column=self.column, padx=45, pady=5)
        self.column += 1
        self.buttonList.append(clip)

        if self.column < 5: return
        self.column = 0
        self.row += 1

    def select_clip(self, filename):
        print("[Analyser] Setting Filename")
        self.filename = filename

    def play_clip(self):
        print("[Analyser] Playing audio")
        chunk = 1024
        wf = wave.open(self.filename, 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input.
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # read data (based on the chunk size)
        data = wf.readframes(chunk)

        # play stream (looping from beginning of file to the end)
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)

        # cleanup stuff.
        wf.close()
        stream.close()    
        p.terminate()

    def stop_clip(self):
        pass

    def approve_clip(self):
        pass

    def flag_clip(self):
        pass

analyser = Analyser()
threading.Thread(target=analyser.server.start_server, args=(analyser.add_file,), daemon=True).start()
tkinter.mainloop()
