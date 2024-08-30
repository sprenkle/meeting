from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time

@rp2.asm_pio(set_init=(rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW, rp2.PIO.OUT_LOW), in_shiftdir=rp2.PIO.SHIFT_RIGHT, push_thresh=32, autopush=False)
def base():
    # Create start bit
    wrap_target()
    set(x, 31) # this is the number of bits to check

    set(y, 20)
    label("loop")
    # new start
    mov(pins, isr)[1]
    mov(pins, invert(isr))[2]
    # end of start
#    set(pins, 1)[1]
#    set(pins, 0)[2]
    jmp(y_dec, "loop")  # 120 cycles

    set(y, 7)
    label("start_wait")
    nop()[31]
    jmp(y_dec, "start_wait") # 60 cycles

    set(x, 31) # 60 cycles
    label("next_bit")
    nop()[28]
    #in_(pins, 1) [1]






    # start of in
    in_(pins, 8)
    mov(y, invert(isr))  
    jmp(not_y, "y_not_one")
    set(y, 1)
    jmp("set_output")

    label("y_not_one")
    set(y, 0)[1]

    label("set_output")
    in_(y, 1)
    # end of in  




    nop()[26]
    nop()[31] 
    nop()[31] 
    jmp(x_dec, "next_bit")[24] # 60 cycles

    # DONE don't worry about what is after
    push(block)
    irq(0)


    set(y, 2)
    label("wait_long")
    set(x, 31)
    label("wait_bit2")
    nop()[31]
    nop()[27]
    jmp(x_dec, "wait_bit2")[31]
    jmp(y_dec, "wait_long")


    wrap()

class IrBase:
    def __init__(self, handler, receiver_pin = 9, transmitter_pin = 16) -> None:
        self.sm_base =  StateMachine(0, base, freq=(38_000 * 6), in_base=Pin(receiver_pin), set_base=Pin(transmitter_pin))
        self.sm_base.irq(self.pin_callback)  # Attach the IRQ handler
        self.handler = handler

    def pin_callback(self, pin):
        self.handler(self.sm_base.get())

        
    def start(self):
        self.sm_base.active(True)

    def end(self):
        self.sm_base.active(False)

if __name__ == '__main__':
    
    # def invert_unsigned(x, bit_width):
    #     mask = (1 << bit_width) - 1  # Create a mask with the desired bit-width
    #     return ~x & mask  # Invert the bits and apply the mask
    #ring = Ring(led_pin=4, num_leds=32)
    def handler(sm):
        sm = sm ^ 0b1111_1111_1111_1111_1111_1111_1111_1111
        print(f'handler sm invert = {bin(sm)}')
        #ring.debug(sm ^ 0b1111_1111_1111_1111_1111_1111_1111_1111)
     #   ring.debug(sm)

    ir_base = IrBase(handler)
    ir_base.start()

    pin = Pin(16, Pin.OUT)

    while True:
        pin.value(1)
        time.sleep(.01)
        pin.value(0)
        time.sleep(.01)
    
    
    print('end')
    ir_base.end()