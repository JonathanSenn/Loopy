from signal import pause
from time import sleep
from gpiozero import Button, LED

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

def start_rec():
    print("rec on!")
    led_rec.on()

def stop_rec():
    print("rec off!")
    led_rec.off()
    
def start_play():
    print("play on")
    led_play.on()
    
def stop_play():
    print("play off!")
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
