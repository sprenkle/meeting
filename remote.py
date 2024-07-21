from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time

#@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def remote():
#     #Wait for Start Bit
#     wrap_target()
#     wait(1, pin, 0)
#     wait(0, pin, 0)[16]
#     set(pins, 1)[3] # want pulse to be 5 long
#     set(pins, 0)
#     wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def remote():
    #Wait for Start Bit
    wrap_target()  
    # mov(y, 10) # sets bit to turn on

    label("wait_start_bit")
    set(x, 31)
    wait(1, pin, 0)

    label("verify_start_bit")
    jmp(x_dec, "continue_start_bit")
    jmp("end_start_bit") 
    label("continue_start_bit") 
    
    jmp(pins, "verify_start_bit")
    jmp("wait_start_bit") # Not the start bit start again
    
    label("end_start_bit")

    # Wait to set my bit
    wait(0, pin, 0)[6]   
    
   
    set(pins, 1)[16] # want pulse to be 5 long
    set(pins, 0)

    wrap()

sm_remote = StateMachine(0, remote, freq=10000, set_base=Pin(14), in_base=Pin(15))

print('start')

    


sm_remote.active(True)
# pinOut = Pin(14, Pin.OUT, Pin.PULL_UP)
# pinIn = Pin(15, Pin.IN, Pin.PULL_DOWN)

# def wait_low():
#     while pinIn.value() == 1:
#         pass

# def wait_high():
#     while pinIn.value() == 0:
#         pass


# wait_low()
# wait_high()
# print('High')


time.sleep(15)
sm_remote.active(False)
   
print('End')