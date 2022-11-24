import queue
from signal import pause
from time import sleep

import threading
import soundfile
import time
import sounddevice as sd
import soundfile as sf
import sys

from gpiozero import Button, LED

button_ch1 = Button(19)
button_ch2 = Button(16)
button_ch3 = Button(26)
button_ch4 = Button(13)
button_switch = Button(21)

led_ch1 = LED(14)
led_ch2 = LED(2)
led_ch3 = LED(3)
led_ch4 = LED(4)
led_rec = LED(15)

all_leds = [led_rec, led_ch1, led_ch2, led_ch3, led_ch4]

rec_mode = False

CHUNK = 1024
CHANNELS = 2
RATE = 44100
channel = 1
current_frame = 0

ch1_mode = 0
ch2_mode = 0
ch3_mode = 0
ch4_mode = 0

player_event = threading.Event()
stop_thread = threading.Event()


t_play = threading.Thread()
t_rec = threading.Thread()
q = queue.Queue()


def record(track):
    stop_thread.clear()
    global q

    def callback(indata, frames, duration, status):
        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    with soundfile.SoundFile(f"wav/raw_{track}.wav", mode='w', samplerate=RATE, channels=2) as f_out:
        with sd.InputStream(samplerate=44100, channels=2, callback=callback):
            while not stop_thread.is_set():
                f_out.write(q.get())
            stop_thread.clear()


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
            current_frame = 0
            # outdata[chunksize:] = 0
            # raise sd.CallbackStop()
        current_frame += chunksize

    stream = sd.OutputStream(samplerate=fs, channels=s_file_data.shape[1], callback=callback,
                             finished_callback=player_event.set)
    with stream:
        player_event.wait()
    player_event.clear()
    current_frame = 0


def start_rec(ch):
    global t_rec
    print("rec on!")
    led_rec.on()
    t_rec = threading.Thread(target=record, args=(ch,))
    t_rec.start()


def stop_rec():
    global t_rec
    print("rec off!")
    stop_thread.set()
    t_rec.join()
    led_rec.off()


def start_play(ch):
    global t_play
    print("play on")
    t_play = threading.Thread(target=play, args=(channel,))
    t_play.start()
    all_leds[ch].on()


def stop_play(ch):
    global t_play
    global current_frame
    print("play off!")
    player_event.set()
    current_frame = 0
    t_play.join()
    all_leds[ch].off()


def big_switch_on():
    global channel
    if rec_mode:
        start_rec(channel)


def big_switch_off():
    if rec_mode:
        stop_rec()


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


def ch1_pressed():
    global ch1_mode
    global channel
    global rec_mode
    rec_mode = False
    if ch1_mode == 0:
        channel = 1
        ch1_mode = 1
        led_ch1.on()
    elif ch1_mode == 1:
        rec_mode = True
        channel = 1
        ch1_mode = 2
        led_ch1.blink(0.5, 0.5)
    else:
        ch1_mode = 0
        led_ch1.off()


def ch2_pressed():
    global ch2_mode
    global channel
    global rec_mode
    rec_mode = False
    if ch2_mode == 0:
        channel = 2
        ch2_mode = 1
        led_ch2.on()
    elif ch2_mode == 1:
        rec_mode = True
        channel = 2
        ch2_mode = 2
        led_ch2.blink(0.5, 0.5)
    else:
        ch2_mode = 0
        led_ch2.off()


def ch3_pressed():
    global ch3_mode
    global channel
    global rec_mode
    rec_mode = False
    if ch3_mode == 0:
        channel = 3
        ch3_mode = 1
        led_ch3.on()
    elif ch3_mode == 1:
        rec_mode = True
        channel = 3
        ch3_mode = 2
        led_ch3.blink(0.5, 0.5)
    else:
        ch3_mode = 0
        led_ch3.off()


def ch4_pressed():
    global ch4_mode
    global channel
    global rec_mode
    rec_mode = False
    if ch4_mode == 0:
        channel = 4
        ch4_mode = 1
        led_ch4.on()
    elif ch4_mode == 1:
        rec_mode = True
        channel = 4
        ch4_mode = 2
        led_ch4.blink(0.5, 0.5)
    else:
        ch4_mode = 0
        led_ch4.off()


is_init = False

while not is_init:
    if button_switch.is_pressed:
        led_rec.blink()
        button_switch.wait_for_release()
    else:
        is_init = True

led_rec.off()

button_switch.when_pressed = big_switch_on
button_switch.when_released = big_switch_off

button_ch1.when_pressed = ch1_pressed
button_ch2.when_pressed = ch2_pressed
button_ch3.when_pressed = ch3_pressed
button_ch4.when_pressed = ch4_pressed
pause()

# #
# if __name__ == '__main__':
#     play(1)
