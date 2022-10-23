from signal import pause
from time import sleep
from gpiozero import Button, LED
import pyaudio
import wave
import threading
import time


button_mode = Button(2)
button_channel = Button(3)
button_switch = Button(21)

led_rec = LED(20)
led_play = LED(16)
led_ch1 = LED(14)
led_ch2 = LED(4)

all_leds = [led_rec, led_play, led_ch1, led_ch2]

channel = 1
rec_mode = True
led_ch1.on()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100



stop_thread = threading.Event()
is_stopped = threading.Event()

t1 = None
t_play = None
print(stop_thread.is_set())

def record(track):
    
    recorder = pyaudio.PyAudio()
    stream = recorder.open(format=FORMAT,
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
    #p.terminate()
    wf = wave.open(f'raw_{track}.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(recorder.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
def play(channel):
    try:
        player.terminate()
        player = pyaudio.PyAudio()
    except Exception as ex:
        print(ex)
        player = pyaudio.PyAudio()
    wf = wave.open(f'raw_{channel}.wav', 'rb')

    stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output_device_index = 2,
                         output=True)
     
    data = wf.readframes(CHUNK)
    wf.rewind()
    while not is_stopped.is_set():
        
        
        stream.write(data)
        data = wf.readframes(CHUNK)
        if data == b'':
            wf.rewind()
    
    wf = None
    stream.stop_stream()
    stream.close()
    player.terminate()
    

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
    is_stopped.set()
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

