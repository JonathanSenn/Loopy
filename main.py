import sounddevice as sd
import numpy as np

import soundfile
from threading import Event
import time
import math
import matplotlib.pylab as plt

def simple_player():
    s_file_data, fs = soundfile.read('wav-file.wav')
    sd.play(s_file_data, fs)
    Event().wait(200)
    sd.play(s_file_data, fs)
    sd.wait(5)


s_file_data, fs = soundfile.read('rhcp.wav')
s_file_data_2, fs_2 = soundfile.read('wav-file.wav')

s_file_data_3 = s_file_data_2
s_file_data_3[:,1] = np.sin(s_file_data_3[:,1])
print(s_file_data_2)
print(type(s_file_data_2), s_file_data_2.shape)
print(type(s_file_data_3), s_file_data_3.shape)
print(s_file_data_3)
fig = plt.figure()
p1 = fig.add_subplot(2,1,1)
p1.plot(s_file_data_2)
p2 = fig.add_subplot(2,1,2)
p2.plot(s_file_data_3)
plt.show()
current_frame = 0
event = Event()


def callback(outdata, frames, duration, status):
    global current_frame
    if status:
        print(status)
    chunksize = min(len(s_file_data) - current_frame, frames)
    outdata[:chunksize] = s_file_data[current_frame:current_frame + chunksize]
    if chunksize < frames:
        # outdata[chunksize:] = 0
        # raise sd.CallbackStop()
        current_frame = 0
    current_frame += chunksize


def callback2(outdata, frames, duration, status):
    global current_frame
    if status:
        print(status)
    chunksize = min(len(s_file_data_3) - current_frame, frames)
    outdata[:chunksize] = s_file_data_3[current_frame:current_frame + chunksize]
    if chunksize < frames:
        # outdata[chunksize:] = 0
        # raise sd.CallbackStop()
        current_frame = 0
    current_frame += chunksize


stream = sd.OutputStream(samplerate=fs, channels=s_file_data.shape[1], callback=callback, finished_callback=event.set)
stream_2 = sd.OutputStream(samplerate=fs_2, channels=s_file_data_3.shape[1], callback=callback2, finished_callback=event.set)

# with stream:
#     event.wait()
with stream_2:
    event.wait()
    # for i in range(10):
    #     print(i)
    #     print(stream.cpu_load)
    #     time.sleep(1)
    # event.set()

event.clear()


#
# current_frame = 0
# event.clear()
# stream = sd.OutputStream(samplerate=fs, channels=s_file_data.shape[1], callback=callback, finished_callback=event.set)
# with stream:
#     event.wait(5)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
