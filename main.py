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
#     pull(block)
#     mov(y, osr)
#     label("wait_start_bit")
#     set(x, 20)
#     wait(0, pin, 0)
#     wait(1, pin, 0)
#     label("verify_start_bit")
#     jmp(x_dec, "end_start_bit")
#     jmp(pin, "verify_start_bit")
#     jmp("wait_start_bit") # Not the start bit start again
#     label("end_start_bit")
#     # Wait to set my bit
#     wait(0, pin, 0)[2]  #4, 14,  
    
#     label("start_bits")
#     jmp(y_dec, "bits") 
#     jmp("nobits")
#     label("bits")
#     jmp("start_bits")[6]    
#     label("nobits")
#     set(pins, 1)[5] # want pulse to be 5 long
#     set(pins, 0)
#     wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, push_thresh=16, autopush=True)
def base():
    # Create start bit
    wrap_target()
    set(x, 15)
    set(pins, 1)[31]
    set(pins, 0)
     
    # Pull in bits
    label("next_bit")
    nop()[6]
    in_(pins, 1)
    jmp(x_dec, "next_bit")[6]
    irq(noblock, rel(0))
    wrap()




old_value = -1
def base_interrupt(pio):
    global old_value
    value = sm_base.get()
    # if value > 0:
    #     jeopardy.processInput(value) 
    if old_value != value:
        print(f'interupt = {bin(value)}')
        old_value = value
    # else:
    #     print(f'irq hit zero1')
    #rp2.PIO(0).irq(lambda pio:  base_interrupt())
    


print("Start")

sm_base   = StateMachine(0, base, freq=10000, set_base=Pin(14), in_base=Pin(15))
# sm_remote = StateMachine(1, remote, freq=8000000, set_base=Pin(14), in_base=Pin(15))

rp2.PIO(0).irq(lambda pio: base_interrupt(pio))

# sm_remote.active(True)
sm_base.active(True)
 
start_time = time.time()  # Record the start time

while True: #(time.time() - start_time) <= 20:
    # sm_remote.put(0b10)
    time.sleep(.5)

print('End')        

# sm_remote.active(False)
sm_base.active(False)
   
