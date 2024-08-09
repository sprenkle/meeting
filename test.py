from machine import Pin, lightsleep
import time


pin = Pin(0, Pin.OUT)

while True:
    pin.value(1)
    time.sleep(0.5)
    pin.value(0)
    time.sleep(0.5)
    lightsleep(1000)    