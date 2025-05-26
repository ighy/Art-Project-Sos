# Import the necessary modules.
import tkinter
import tkinter as tk
import tkinter.messagebox
import pyaudio
import wave
import os
import clientmp3

class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):

        # Start Tkinter and set Title
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('500x300')
        self.main.title('Record')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        #Other
        self.index = 0
        self.client = clientmp3.ClientMp3()

        while os.path.exists(self.get_directory()):
            self.index += 1


        #Start the main loop by going to the main screen
        self.introScreen()


    #Show the screen people will see when they first go to record

    def introScreen(self):
        self.clearScreen()

        title = tk.Label(self.main, text="Welcome to the Dream Recording Booth", font=("Ariel", 20))
        title.pack()

        #This button will 'move' to the recording screen
        startButton = tk.Button(self.main, text="Record Your Dream", font=("Ariel", 15), command = self.recordingScreen)
        startButton.pack()

        self.main.mainloop()

    #Screen shown when recording is in progress
    def recordingScreen(self):

        timer = 60 #TODO: Implement a timer function

        self.clearScreen()

        #initialize timer, clock, and stop button
        title = tk.Label(self.main, text="RECORDING IN PROGRESS", font=("Ariel", 40))
        title.pack()
        clock = tk.Label(self.main, text=f"timer: {timer} seconds left")
        clock.pack()
        self.tickTimer(timer + 1, clock)

        #start recording
        self.start_record()

        #To stop recording by any means, simply set self.st to 0
        if self.st == 0:
            #After recording is finished, loads the uploading screen
            self.uploadScreen()
            pass


    #Screen shown when uploads are in progress
    #maybe implement a progress bar??? idk
    def uploadScreen(self):
        self.clearScreen()
        title = tk.Label(self.main, text="Thanks for reqording your dream :)")
        title.pack()
        finishButton = tk.Button(self.main, text="Done", font=("Ariel", 15), command = self.introScreen)
        finishButton.pack()

        #after this, should show a quick thank you message before looping back to the intro screen

    #Clear the screen so different widgets don't show up where they are not supposed to. Should be called at the beginning of every screen-related function
    def clearScreen(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def get_directory(self):
        return f'audio_files/recording_{self.index}.wav'

    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            #print("* recording")
            self.main.update()

        stream.close()

        wf = wave.open(self.get_directory(), 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.client.handle_input(self.get_directory())
        self.index += 1

    def stop(self):
        self.st = 0
        print("Misson accomplished!")

    def tickTimer(self, timer, label):
        timer -= 1
        label.config(text=f"timer: {timer} seconds left")
        
        if timer > 0:
            self.main.after(1000, lambda t=timer, l=label: self.tickTimer(t, l))
        else:
            self.stop()

# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()
