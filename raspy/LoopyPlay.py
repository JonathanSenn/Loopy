import pyaudio
import wave
import threading
import time
import numpy

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

wf = wave.open('raw_1.wav', 'rb')
wf2 = wave.open('raw_2.wav', 'rb')

is_stopped = threading.Event()
p = pyaudio.PyAudio()


# def callback(in_data, frame_count, time_info, status):
# #     wf = wave.open(f'raw_{track}.wav', 'rb')
#     wf1 = wave.open(f'raw_1.wav', 'rb')
#     wf2 = wave.open(f'raw_2.wav', 'rb')
#     data1 = wf1.readframes(CHUNK)
#     data2 = wf2.readframes(CHUNK)
#     d1_decoded = numpy.fromstring(data1, numpy.int16)
#     d2_decoded = numpy.fromstring(data2, numpy.int16)
#     new_data = (d1_decoded + d2_decoded).astype(numpy.int16)
#     return (new_data.tostring(), pyaudio.paContinue)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    print("sleeping")
    time.sleep(0.1)
    
    # stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()

#     p = pyaudio.PyAudio()
# 
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)
# 
#     data = wf.readframes(CHUNK)
# 
#     while not is_stopped.is_set():
#         stream.write(data)
#         data = wf.readframes(CHUNK)
#         if data == b'':
#             wf.rewind()
# 
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

# t1 = threading.Thread(target=play, args=([1,2],))
# 
# 
# t1.start()
# 
# 
# for i in range(3):
#     print(f'sleeping {i} secs')
#     time.sleep(1)

print('setting event')
is_stopped.set()
