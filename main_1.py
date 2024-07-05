import array, time, random
import machine
from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState

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

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, push_thresh=16, autopush=True)
def base():
    # Create start bit
    wrap_target()
    set(x, 15)
    set(pins, 1)[31]
    set(pins, 0)
     
    # Pull in bits
    nop()[6]
    label("next_bit")
    in_(pins, 1)
    jmp(x_dec, "next_bit")[6]
    irq(block, rel(0))
    wrap()


def display(var):
    value = str(var)
    print(value)
    value = value[2:]
    for i in range(16 - len(value)):
        value = "0" + value
    print(f'{value[0:4]} {value[4:8]} {value[8:12]} {value[12:16]}')



ring = Ring()
position_state = PositionState(Ring.GREEN, Ring.YELLOW, Ring.RED, Ring.WHITE)
jeopardy = Jeopardy(ring, position_state)

long_presses = [0] * 16

def base_interrupt(pio):
    value = sm_base.get()
    if value > 0:
        jeopardy.processInput(value) 
        # print(f'interupt = {bin(value)}')
    # else:
    #     print(f'irq hit zero1')
    #rp2.PIO(0).irq(lambda pio:  base_interrupt())
    




sm_base   = StateMachine(0, base, freq=8000000, set_base=Pin(2), in_base=Pin(1))
sm_remote = StateMachine(4, remote, freq=8000000, set_base=Pin(1), in_base=Pin(2))

rp2.PIO(0).irq(lambda pio: base_interrupt(pio))

sm_remote.active(True)
sm_base.active(True)

sm_remote.put(1) # this is the pause count
time.sleep(.25)    
#rp2.PIO(0).irq(lambda pio:  base_interrupt())
sm_remote.put(2)  
time.sleep(.25)    
# sm_remote.put(3)  

# sm_remote.active(False)
# sm_base.active(False)
   
