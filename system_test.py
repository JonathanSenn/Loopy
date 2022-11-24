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

led_rec = LED(15)

led_ch1 = LED(14)
led_ch2 = LED(2)
led_ch3 = LED(3)
led_ch4 = LED(4)

all_leds = [led_rec, led_ch1, led_ch2, led_ch3, led_ch4]
for led in all_leds:
    led.off()

button_ch1 = Button(19)
button_ch2 = Button(16)
button_ch3 = Button(26)
button_ch4 = Button(13)

button_switch = Button(21)


def button_pressed(channel=None):
    print(f'Button {channel} pressed')
    # all_leds[channel].on()


def button_released(channel=None):
    print(f'Button {channel} released')
    # all_leds[channel].off()


def big_switch_on():
    print('Big Switch on')


def big_switch_off():
    print('Big Switch off')


button_switch.when_pressed = big_switch_on
button_switch.when_released = big_switch_off
button_ch1.when_pressed = button_pressed
button_ch2.when_pressed = button_pressed
button_ch3.when_pressed = button_pressed
button_ch4.when_pressed = button_pressed
button_ch1.when_released = button_pressed
button_ch2.when_released = button_pressed
button_ch3.when_released = button_pressed
button_ch4.when_released = button_pressed

pause()