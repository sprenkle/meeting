from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from consolering import ConsoleRing
from positionstate import PositionState
from yesno import YesNo
import time


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

games = [jeopardy, YesNo(console_ring, position_state)]
game = 0

old_value = -1
def base_interrupt(pio):
    global old_value, console_ring, position_state, game
    value = sm_base.get() >> 16
    # if old_value != value:
    #     print(f'base_interrupt value = {bin(value)}')
    if value == 0b10:
        game = 0 if game == 1 else 1
        # print(f'game = {game}')
        return
    
    if old_value != value:
        old_value = value
        # print(f'game = {game} value = {bin(value)}')
        games[game].processInput(value)

sm_base   = StateMachine(0, base, freq=10000, set_base=Pin(14), in_base=Pin(15))
rp2.PIO(0).irq(lambda pio: base_interrupt(pio))

sm_base.active(True)

while True:
    time.sleep(1)

sm_base.active(False)
   
