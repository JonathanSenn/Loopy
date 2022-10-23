import pyaudio
import wave
import threading
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


stop_thread = threading.Event()
print(stop_thread.is_set())


def record(track):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    while not stop_thread.is_set():
        data = stream.read(CHUNK)
        frames.append(data)
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #   data = stream.read(CHUNK)
    #   frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(f'raw_{track}.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
 
t1 = threading.Thread(target=record, args=(2,))

t1.start()

for i in range(10):
    print(f'sleeping {i} secs')
    time.sleep(1)

print('setting event')
stop_thread.set()
print(stop_thread.is_set())

t1.join()


# 
# class LoopyRec:
#     def __init__(self):
#         self.channels = []
#         self.is_recording = False
#         print("Recorder initialised")
# 
#     def record(self, channel):
#         p = pyaudio.PyAudio()
#         stream = p.open(format=FORMAT,
#                         channels=CHANNELS,
#                         rate=RATE,
#                         input=True,
#                         frames_per_buffer=CHUNK)
#         print("* recording")
#         frames = []
#         while self.is_recording:
#             data = stream.read(CHUNK)
#             frames.append(data)
#         # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         # 	data = stream.read(CHUNK)
#         #	frames.append(data)
#         print("* done recording")
#         stream.stop_stream()
#         stream.close()
#         p.terminate()
#         wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(p.get_sample_size(FORMAT))
#         wf.setframerate(RATE)
#         wf.writeframes(b''.join(frames))
#         wf.close()
#                                         

