from signal import pause
from time import sleep

import threading
import soundfile
import time
import sounddevice as sd
import soundfile as sf
import sys

from gpiozero import Button, LED
button_mode = Button(2)
button_channel = Button(3)
button_switch = Button(21)

led_rec = LED(20)
led_play = LED(16)
led_ch1 = LED(14)
led_ch2 = LED(4)

all_leds = [led_rec, led_play, led_ch1, led_ch2]


rec_mode = True
led_ch1.on()

CHUNK = 1024
CHANNELS = 2
RATE = 44100
current_frame = 0

player_event = threading.Event()
stop_thread = threading.Event()

t_play = threading.Thread()


def record(track):
    print("todo")


def play(channel):
    player_event.clear()
    s_file_data, fs = soundfile.read(f'wav/raw_{channel}.wav')

    def callback(outdata, frames, duration, status):
        global current_frame
        if status:
            print(status)
        chunksize = min(len(s_file_data) - current_frame, frames)
        outdata[:chunksize] = s_file_data[current_frame:current_frame + chunksize]
        if chunksize < frames:
            outdata[chunksize:] = 0
            current_frame = 0
            raise sd.CallbackStop()
            # current_frame = 0
        current_frame += chunksize

    stream = sd.OutputStream(samplerate=fs, channels=s_file_data.shape[1], callback=callback,
                             finished_callback=player_event.set)
    with stream:
        player_event.wait()
    player_event.clear()



def start_rec():
    global t1
    print("rec on!")
    led_rec.on()
    t1 = threading.Thread(target=record, args=(channel,))
    t1.start()


def stop_rec():
    global t1
    print("rec off!")
    stop_thread.set()
    t1.join()
    led_rec.off()


def start_play():
    global t_play
    print("play on")
    t_play = threading.Thread(target=play, args=(channel,))
    t_play.start()
    led_play.on()


def stop_play():
    global t_play
    print("play off!")
    t_play.join()
    led_play.off()


def big_switch_on():
    if rec_mode:
        start_rec()
    else:
        start_play()


def big_switch_off():
    if rec_mode:
        stop_rec()
    else:
        stop_play()


def switch_channel():
    global channel    
    if channel == 1:
        led_ch1.off()
        led_ch2.on()
        channel = 2
    else:
        led_ch2.off()
        led_ch1.on()
        channel = 1


def switch_mode():
    global rec_mode    
    if rec_mode:
        led_ch1.off()
        led_ch2.on()
        rec_mode = False
    else:
        led_ch2.off()
        led_ch1.on()
        rec_mode = True


button_switch.when_pressed = big_switch_on
button_switch.when_released = big_switch_off
button_channel.when_pressed = switch_channel
button_mode.when_pressed = switch_mode
pause()

# #
# if __name__ == '__main__':
#     play(1)
