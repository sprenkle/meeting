from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from consolering import ConsoleRing
from positionstate import PositionState
from yesno import YesNo
import time


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def remote():
    #Wait for Start Bit
    wrap_target() 
    pull(block)
    #wrap_target() # uncomment this
    label("wait_start_bit")
    mov(x, osr)
    pull(noblock)
    
      
    set(y, 10) # sets timing on start bit

    label("continue_start_bit") 
    
    jmp(pin, "verify_start_bit")
    jmp("wait_start_bit") # Not the start bit start again
    label("verify_start_bit")

    jmp(y_dec, "continue_start_bit")

    # Wait to set my bit
    wait(0, pin, 0)[11]

    label("wait_bits") 
    jmp(x_dec, "jmp_over_bits")
    jmp("remote_bit")
    label("jmp_over_bits")
    jmp("wait_bits")[21]

    label("remote_bit")
    set(pins, 1)[5] # want pulse to be 6 long
    # set(pins, 0)

    wrap()



@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_RIGHT, push_thresh=16, pull_thresh=16, autopush=True)
def base():
    # Create start bit
    wrap_target()
    set(x, 15)
    set(pins, 1)[31]
    set(pins, 0)[5]
     
    # Pull in bits
    label("next_bit")
    nop()[10]
    in_(pins, 1)
    jmp(x_dec, "next_bit")[10]
    irq(0)[31]
    nop()[31]
    wrap()





console_ring = ConsoleRing()
position_state = PositionState(ConsoleRing.GREEN, ConsoleRing.YELLOW, ConsoleRing.RED, ConsoleRing.WHITE, ConsoleRing.BLACK)
position_state.first = 0b0
position_state.second = 0b0
console_ring.show(position_state)
jeopardy = Jeopardy(console_ring, position_state)

# jeopardy.processInput(0b10)
# jeopardy.processInput(0b100)
# jeopardy.processInput(0b1000)
# jeopardy.processInput(0b10000)
# jeopardy.processInput(0b100000)

# jeopardy.processInput(0b1)
# jeopardy.processInput(0b1)
# jeopardy.processInput(0b1)
# jeopardy.processInput(0b1)
# jeopardy.processInput(0b1)






games = [jeopardy, YesNo(console_ring, position_state)]
game = 0

old_value = -1
def base_interrupt(pio):
    global old_value, console_ring, position_state, game
    value = sm_base.get() >> 16
    print(f'base_interrupt value = {bin(value)}')
    if value == 0b10:
        game = 0 if game == 1 else 1
        print(f'game = {game}')
        return
    
    if old_value != value:
        old_value = value
        print(f'game = {game} value = {bin(value)}')
        games[game].processInput(value)

    


def set_remote(index):
    sm_remote.put(index)
    time.sleep(.5)  

print("Start")

sm_base   = StateMachine(0, base, freq=10000, set_base=Pin(15), in_base=Pin(14))

sm_remote = StateMachine(1, remote, freq=10000, set_base=Pin(14), in_base=Pin(15), jmp_pin=Pin(15))

rp2.PIO(0).irq(lambda pio: base_interrupt(pio))

# sm_remote.active(True)
sm_base.active(True)
 
start_time = time.time()  # Record the start time

# while (time.time() - start_time) <= 1:
#     pass
print('End')        

time.sleep(1)

set_remote(2)
set_remote(3)
set_remote(4)


# for i in range(2, 4):
#     #print(i)
#     set_remote(i)

    
# for i in range(0, 2):
#     #print(i)
#     set_remote(0)
    
# set_remote(1)

# set_remote(0)

# set_remote(5)
# set_remote(6)

time.sleep(5)


sm_remote.active(False)
sm_base.active(False)
   
