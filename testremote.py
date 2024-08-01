from machine import Pin
import time

pinIn = Pin(15, Pin.OUT, Pin.PULL_DOWN)
pinIn.value(0)

time.sleep(10)

print('done')