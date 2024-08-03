from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def pulse():
    # Create start bit
    wrap_target()
    mov(x, 15)
    # irq(block, 4)
    label("loop")
    set(pins, 1)[2]
    set(pins, 0)
    jmp(x_dec, "loop")
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, push_thresh=16, autopush=True)
def base():
    # Create start bit
    wrap_target()
    mov(x, 15) # this is the number of bits to check
    pull(block)
    irq(clear, 4)
     
    # Pull in bits
    label("next_bit")
    nop()[6]
    in_(pins, 1)[6]
    jmp(x_dec, "next_bit")
    irq(block, 0)
    wrap()




print("Start")


# Define the callback function
def pin_callback(pin):
    print("Pin state changed to high")

# Define the callback function
def pin_high_low_callback(pin):
    print("Pin state changed to low")


# Configure the pin (replace `PIN_NUMBER` with your pin)
pin0 = Pin(0, Pin.OUT)
pin0.value(0)

pin29 = Pin(29, Pin.IN)

# Attach the interrupt
pin29.irq(trigger=Pin.IRQ_FALLING, handler=pin_callback)

sm_base =  StateMachine(0, pulse, freq=3800, in_base=Pin(29))

sm_pulse = StateMachine(1, base, freq=3800 * 5, set_base=Pin(2))
sm_pulse.active(True)
sm_base.active(True)
 
start_time = time.time()  # Record the start time

# while (time.time() - start_time) <= 5:
sm_pulse.put(16)
time.sleep(1)
sm_pulse.put(8)
time.sleep(1)

print('End')        

sm_base.active(False)
sm_pulse.active(False)
   
