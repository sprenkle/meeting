from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time, random

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def remote():
    #Wait for Start Bit
    wrap_target()
    pull(block)  
    mov(y, osr) # sets bit to turn on
    label("wait_start_bit")
    set(x, 10)

    label("continue_start_bit") 
    
    jmp(pin, "verify_start_bit")
    jmp("wait_start_bit") # Not the start bit start again
    label("verify_start_bit")

    jmp(x_dec, "continue_start_bit")

    # Wait to set my bit
    wait(0, pin, 0)[11]

    label("wait_bits") 
    jmp(y_dec, "jmp_over_bits")
    jmp("remote_bit")
    label("jmp_over_bits")
    jmp("wait_bits")[21]

    label("remote_bit")
    set(pins, 1)[5] # want pulse to be 6 long
    set(pins, 0)

    wrap()


# @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def remote():
#     #Wait for Start Bit
#     wrap_target()
#     # pull(block)  
#     mov(y, 8) # sets bit to turn on
#     label("wait_start_bit")
#     set(x, 8)
#     label("continue_start_bit") 
    
#     jmp(pin, "verify_start_bit")
#     jmp("wait_start_bit") # Not the start bit start again
#     label("verify_start_bit")

#     jmp(x_dec, "continue_start_bit")

#     # # Wait to set my bit
#     # wait(0, pin, 0)[11]

#     set(pins, 1)[31] # want pulse to be 6 long
#     set(pins, 0)[31]

#     nop()[31]

#     wrap()




# pin14 = Pin(14, Pin.OUT, Pin.PULL_DOWN)
# pin15 = Pin(15, Pin.IN, Pin.PULL_DOWN)

sm_remote = StateMachine(0, remote, freq=10000, set_base=Pin(8), in_base=Pin(7), jmp_pin=Pin(7))

print('startddds')

pinY = Pin(5, Pin.IN, Pin.PULL_UP)
pinW = Pin(7, Pin.IN, Pin.PULL_UP)
pinB = Pin(6, Pin.IN, Pin.PULL_UP)


sm_remote.active(True)

while True:
    sm_remote.put(5)
    button_state = pinY.value()
    while button_state == 0:
        print('Y')
        sm_remote.put(0b1)
        button_state = pinY.value()
        sm_remote.active(False)

    button_state = pinW.value()
    while button_state == 0:
        print('W')
        sm_remote.put(0b10)
        button_state = pinW.value()

    button_state = pinB.value()
    while button_state == 0:
        print('B')
        sm_remote.put(0b1000_0000)
        button_state = pinB.value()


# for i in range(31):
#     pin = Pin(i, Pin.IN, Pin.PULL_UP)
#     print(f'{i} = {pin.value()}')
#     time.sleep(1)



sm_remote.active(False)
   
print('End')