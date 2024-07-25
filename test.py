from machine import Pin, lightsleep
import time


pin = Pin(14, Pin.OUT)


while True:
    time.sleep(.1)
    pin.value(1)
    time.sleep(.1)
    pin.value(0)