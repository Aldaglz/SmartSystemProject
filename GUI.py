import os
import wave
import threading
import time
import tkinter as tk
import pyaudio

class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.root.title("Send your Voice Command")
        
        self.button = tk.Button(text="🎤", font=("Arial",120,"bold"),
                                command=self.click_handler)
        self.button.pack()
        self.label = tk.Label(text="00:00:00")
        self.label.pack()
        self.recording=False
        self.root.mainloop()
    
    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()
    
    def record(self):
        audio=pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, 
                             input=True, frames_per_buffer=2048)
        frames=[]

        start = time.time()

        while self.recording:
            data=stream.read(2048)
            frames.append(data)

            passd=time.time() - start
            secs = passd%60
            mins=passd//60
            hours=mins//60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        
        stream.stop_stream()
        stream.close()
        audio.terminate()

        exist = True
        i=1
        while exist:
            if os.path.exists(f"recording{i}.wav"):
                i = i+1
            else:
                exist =False
        sound_file = wave.open(f"recording{i}.wav","wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(16000)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

VoiceRecorder()