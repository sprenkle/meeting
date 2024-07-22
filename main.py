from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time


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
    irq(block, rel(0))
    wrap()


ring = Ring()
position_state = PositionState(Ring.GREEN, Ring.YELLOW, Ring.RED, Ring.WHITE, Ring.BLACK)
position_state.first = 0b0
position_state.second = 0b0
ring.show(position_state)
jeopardy = Jeopardy(ring, position_state)


old_value = -1
def base_interrupt(pio):
    global old_value, ring, position_state
    value = sm_base.get()
    # if value > 0:
    #     jeopardy.processInput(value) 
    if old_value != value:
        # print(f'interupt = {bin(value)}')
        old_value = value
        jeopardy.processInput(value)
        # print(position_state.first)
    # else:
    #     print(f'irq hit zero1')
    #rp2.PIO(0).irq(lambda pio:  base_interrupt())
    


print("Start")

sm_base   = StateMachine(1, base, freq=10000, set_base=Pin(8), in_base=Pin(12))

rp2.PIO(0).irq(lambda pio: base_interrupt(pio))

# sm_remote.active(True)
sm_base.active(True)
 
start_time = time.time()  # Record the start time

while (time.time() - start_time) <= 5:
    # sm_remote.put(0b10)
    time.sleep(1)

# print('End')        

# sm_remote.active(False)
sm_base.active(False)
   
