# Import the necessary modules.
import tkinter
import tkinter as tk
from tkinter import ttk
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
        self.main.geometry('1000x500')
        self.main.configure(bg="lightblue")
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

        title = tk.Label(self.main, text="Welcome to the Dream Recording Booth", font=("Comic Sans MS", 35), bg="lightblue")
        title.pack()

        #This button will 'move' to the recording screen
        startButton = tk.Button(self.main, text="Record Your Dream", font=("Comic Sans MS", 30), bg="hotpink", command = self.recordingScreen)
        startButton.pack()

        self.main.mainloop()

    #Screen shown when recording is in progress
    def recordingScreen(self):

        timer = 60 

        self.clearScreen()

        #initialize timer, clock, and stop button
        title = tk.Label(self.main, text="Recording in Progress...", font=("Comic Sans MS", 35), bg="red")
        title.pack()
        clock = tk.Label(self.main, text=f"timer: {timer} seconds left", font=("Comic Sans MS", 20), bg="lightblue")
        clock.pack()
        message = tk.Label(self.main, text="If you are finished early or want to redo, press stop", font=("Comic Sans MS", 15), bg="lightblue")
        message.pack()
        stopButton = tk.Button(self.main, text="Stop Recording", font=("Comic Sans MS", 20), bg="hotpink", command=self.stop)
        stopButton.pack()
        self.tickTimer(timer + 1, clock)

        #start recording
        self.start_record()

        #To stop recording by any means, simply set self.st to 0
        if self.st == 0:
            #After recording is finished, loads the uploading screen
            self.uploadScreen()
            pass

    def confirmationScreen(self): 
        self.clearScreen()
        #Create two frames to allow both a pack and grid arrangement 
        frame1 = tk.Frame(self.main)
        frame1.pack()
        label = tk.Label(frame1, text="Recording complete!", font=("Comic Sans MS", 40), bg="lightblue") 
        label.pack()
        label2 = tk.Label(frame1, text="Would you like to upload your recording or try again?", font=("Comic Sans MS", 30), bg="lightblue")
        label2.pack()
        frame2 = tk.Frame(self.main)
        frame2.pack(pady=30)
        #Maybe implement a button that allows them to just quit and leave?
        uploadButton = tk.Button(frame2, text="Upload", font=("Comic Sans MS", 20), bg="hotpink", command=self.uploadScreen)
        retryButton = tk.Button(frame2, text="Try again", font=("Comic Sans MS", 20), bg="hotpink", command=self.recordingScreen)
        uploadButton.grid(row=0, column=0)
        retryButton.grid(row=0, column=1)
        #Apparently putting mainloop here prevents a bug where the program becomes unresponse after recording stops due to timeout
        self.main.mainloop()
    #Screen shown when uploads are in progress
    #maybe implement a progress bar??? idk
    def uploadScreen(self):
        self.saveAudio()
        self.clearScreen()
        title = tk.Label(self.main, text="Thanks for recording your dream :)", font=("Comic Sans MS", 20), bg="lightblue")
        title.pack()
        finishButton = tk.Button(self.main, text="Done", font=("Comic Sans MS", 30), bg="hotpink", command = self.introScreen)
        finishButton.pack()

        #after this, should show a quick thank you message before looping back to the intro screen

    #Clear the screen so different widgets don't show up where they are not supposed to. Should be called at the beginning of every screen-related function
    def clearScreen(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def get_directory(self):
        return f'audio_files/recording_{self.index}.mp3'

    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            #print("* recording")
            self.main.update()

        print("Loop exited")
        stream.close()

    #This function will stop the recording and move to the next screen
    def stop(self):
        self.st = 0
        print("Misson accomplished!")
        self.confirmationScreen()

    def tickTimer(self, timer, label):
        timer -= 1
        label.config(text=f"timer: {timer} seconds left")
        
        if timer > 0:
            self.main.after(1000, lambda t=timer, l=label: self.tickTimer(t, l))
        else:
            self.stop()

    def saveAudio(self):
        wf = wave.open(self.get_directory(), 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        self.client.handle_input(self.get_directory())
        self.index += 1

# Create an object of the ProgramGUI class to begin the program.
guiAUD = RecAUD()
