import os
import pyaudio
import numpy as np
import aubio
import wave
import whisper
import spotipy
import threading
from spotipy.oauth2 import SpotifyOAuth

model = whisper.load_model("tiny")
device_id = ""
playlist_start = "https://open.spotify.com/playlist/4kLRvuenc9WPlR10Z8nsn2"

scope = "user-library-read,user-read-playback-state,user-modify-playback-state"
auth = SpotifyOAuth(scope=scope)
sp = spotipy.Spotify(auth_manager=auth)


# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
record_format = pyaudio.paInt32
n_channels = 1
samplerate = 44100

filename = "recorded"

record_seconds = 2

stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

stream2 = p.open(format=record_format,
                        channels=n_channels,
                        rate=samplerate,
                        input=True,
                        output=True,
                        frames_per_buffer=buffer_size)


# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

def thread_function(frames, i):
        wf = wave.open(f"{filename}{i}.wav", "wb")
        wf.setnchannels(n_channels)
        wf.setsampwidth(p.get_sample_size(pyaudio_format))
        wf.setframerate(samplerate)
        wf.writeframes(b"".join(frames))
        wf.close()
        try:
            result = model.transcribe(f"{filename}{i}.wav")
            if "Thank you" in result["text"]:
                os.remove(f"{filename}{i}.wav")
                x.remove(x[i-1])
                return 
            print(result["text"])
            if "spotify" in result["text"].lower():
                sp.start_playback(device_id=device_id,context_uri=playlist_start)
            elif "stop" in result["text"].lower():
                sp.pause_playback(device_id=device_id)
            elif "play" in result["text"].lower():
                sp.start_playback(device_id=device_id)
            elif "back" in result["text"].lower():
                sp.previous_track(device_id=device_id)
            elif "next" in result["text"].lower():
                sp.next_track(device_id=device_id)
            elif "vol" and "low" in result["text"].lower():
                sp.volume(20,device_id=device_id)
            elif "vol" and "mid" in result["text"].lower():
                sp.volume(50,device_id=device_id)    
            elif "vol" and "high" in result["text"].lower():
                sp.volume(80,device_id=device_id)    
            os.remove(f"{filename}{i}.wav")
            x.remove(x[i-1])
        except:
            os.remove(f"{filename}{i}.wav")
            x.remove(x[i-1])

running = True
x=[]
while running:
    frames = []
    
    while True:
        try:
            audiobuffer = stream.read(buffer_size)
            signal = np.fromstring(audiobuffer, dtype=np.float32)
            pitch = pitch_o(signal)[0]
            confidence = pitch_o.get_confidence()

            # print(f"{pitch}, {confidence}")
            if pitch > 80:
                print("*** starting recording")
                stream.stop_stream()
                stream2.start_stream()
                for i in range(int(samplerate / buffer_size * record_seconds)):
                    data = stream2.read(buffer_size)
                    frames.append(data)
                stream.start_stream()
                stream2.stop_stream()
                print("*** done recording")
                break

        except KeyboardInterrupt:
            print("*** Ctrl+C pressed, exiting")
            running = False
            break
    if running:
        x.append(threading.Thread(target=thread_function, args=[frames, len(x)]))
        x[-1].start()
    
stream.stop_stream()
stream.close()
stream2.close()
p.terminate()

    
