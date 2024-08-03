from machine import Pin, lightsleep
import time


pin = Pin(15, Pin.IN, Pin.PULL_UP)

old_value = -1
while True:
    value = pin.value()
    if value != old_value:
        old_value = pin.value()
        print(f'pin = {value}')
