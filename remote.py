from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time

# @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def remote():
#     #Wait for Start Bit
#     wrap_target()
#     wait(1, pin, 0)
#     wait(0, pin, 0)
  
#     nop() [16]
#     set(pins, 1)[5] # want pulse to be 5 long
#     set(pins, 0)[5]
#     wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def remote():
    #Wait for Start Bit
    wrap_target()  
    pull(block)
    mov(y, osr)
    label("wait_start_bit")
    set(x, 20)
    wait(0, pin, 0)
    wait(1, pin, 0)
    label("verify_start_bit")
    jmp(x_dec, "end_start_bit")
    jmp(pin, "verify_start_bit")
    jmp("wait_start_bit") # Not the start bit start again
    label("end_start_bit")
    # Wait to set my bit
    wait(0, pin, 0)[2]  #4, 14,  
    
    label("start_bits")
    jmp(y_dec, "bits") 
    jmp("nobits")
    label("bits")
    jmp("start_bits")[6]    
    label("nobits")
    set(pins, 1)[5] # want pulse to be 5 long
    set(pins, 0)
    wrap()

sm_remote = StateMachine(0, remote, freq=10000, set_base=Pin(15), in_base=Pin(26))

print('start')



sm_remote.active(True)
pin = Pin(26, Pin.IN, Pin.PULL_UP)

time.sleep(10)

sm_remote.active(False)
   
print('End')