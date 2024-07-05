import array, time, random
import machine
from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio




@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


NUM_LEDS = 1
# Create the StateMachine with the ws2812 program, outputting on Pin(23).ws2812
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(16))#23-16
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
# Display a pattern on the LEDs via an array of LED RGB value
ar = array.array("I", [0 for _ in range(NUM_LEDS)])
ar[0] = (128<<16) + (0<<8) + 0
brightness = 0.5

sm.put(ar,8)

