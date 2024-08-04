from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, push_thresh=16, autopush=False)
def base():
    # Create start bit
    wrap_target()
    set(x, 15) # this is the number of bits to check
   

    set(y, 20)
    label("loop")
    set(pins, 1)[1]
    set(pins, 0)[2]
    jmp(y_dec, "loop")

    nop()[31]
    nop()[29]

    label("next_bit")
    nop()[28]
    nop()[29]
    in_(pins, 1)
    nop()[30]
    jmp(x_dec, "next_bit")[28]


    push(block)
    irq(0)


    set(x, 31)
    label("wait_bit")
    nop()[31]
    nop()[27]
    jmp(x_dec, "wait_bit")[31]
    
    set(x, 31)
    label("wait_bit2")
    nop()[31]
    nop()[27]
    jmp(x_dec, "wait_bit2")[31]



    wrap()

class IrBase:
    def __init__(self, handler, receiver_pin = 15, transmitter_pin = 14) -> None:
        self.sm_base =  StateMachine(0, base, freq=(38_000 * 6), in_base=Pin(receiver_pin), set_base=Pin(transmitter_pin))
        self.sm_base.irq(self.pin_callback)  # Attach the IRQ handler
        self.handler = handler

    def pin_callback(self, pin):
        self.handler(bin(self.sm_base.get()))
        
    def start(self):
        self.sm_base.active(True)

    def end(self):
        self.sm_base.active(False)

if __name__ == '__main__':
    pin = Pin(29, Pin.IN, Pin.PULL_UP)
    print(f'pin {pin.value()}')


    def handler(sm):
        print(f'handler {sm}')

    print('start')
    base = IrBase(handler)
    base.start()
    
    # base.sm_base.put(16)
    # time.sleep(1)
    # base.sm_base.put(16)
    while True:
        time.sleep(1)
    # base.sm_base.get()
    # time.sleep(10)
    
    base.end()
    print('end')
