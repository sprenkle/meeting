from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time

@rp2.asm_pio(
    out_init=(rp2.PIO.OUT_LOW) * 8, 
    set_init=(rp2.PIO.OUT_LOW) * 8, 
    in_shiftdir=rp2.PIO.SHIFT_RIGHT, 
    push_thresh=32, 
    autopush=True,
    fifo_join=PIO.JOIN_RX)
def base():
    # Create start bit
    wrap_target()
    set(x, 0) # this is the number of bits to check


    set(y, 20)
    label("loop")
    mov(pins, invert(x))[1]
    mov(pins, x)[2]
    jmp(y_dec, "loop")  # 120 cycles

    set(y, 7)
    label("start_wait")
    nop()[31]
    jmp(y_dec, "start_wait") # 60 cycles

    set(x, 31) # 60 cycles
    label("next_bit")
    nop()[27]
    in_(pins, 8) [1]

    # start of in
    # mov(y, invert(pins))                  # 1   1
    # jmp(not_y, "y_not_one")       # 3   3    
    # set(y, 1)                     # 4
    # jmp("set_output")             # 5

    # label("y_not_one")                  
    # set(y, 0)[1]                  #     4,5

    # label("set_output")
    # in_(y, 1)                     # 6    6
    # end of in  


    nop()[31] # was 31
    nop()[31] 
    nop()[31] 
    jmp(x_dec, "next_bit")[24] # 60 cycles

    # DONE don't worry about what is after
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
    def __init__(self, handler, receiver_pin = 7, transmitter_pin = 15) -> None:
        self.sm_base =  StateMachine(0, base, freq=(38_000 * 6), out_base=Pin(transmitter_pin), in_base=Pin(receiver_pin), set_base=Pin(transmitter_pin))
        self.sm_base.irq(self.pin_callback)  # Attach the IRQ handler
        self.handler = handler

    def pin_callback(self, pin):
        sm1 = self.sm_base.get();
        sm2 = self.sm_base.get();
        sm3 = self.sm_base.get();
        sm4 = self.sm_base.get();
        sm5 = self.sm_base.get();
        sm6 = self.sm_base.get();
        sm7 = self.sm_base.get();
        sm8 = self.sm_base.get();
        
        sm = int(bool((sm1 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) | \
             int(bool((sm1 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 1 | \
             int(bool((sm1 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 2 | \
             int(bool((sm1 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 3 | \
             int(bool((sm2 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 4 | \
             int(bool((sm2 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 5 | \
             int(bool((sm2 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 6 | \
             int(bool((sm2 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 7 | \
             int(bool((sm3 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 8 | \
             int(bool((sm3 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 9 | \
             int(bool((sm3 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 10 | \
             int(bool((sm3 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 11 | \
             int(bool((sm4 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 12 | \
             int(bool((sm4 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 13 | \
             int(bool((sm4 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 14 | \
             int(bool((sm4 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 15 | \
             int(bool((sm5 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 16 | \
             int(bool((sm5 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 17 | \
             int(bool((sm5 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 18 | \
             int(bool((sm5 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 19 | \
             int(bool((sm6 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 20 | \
             int(bool((sm6 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 21 | \
             int(bool((sm6 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 22 | \
             int(bool((sm6 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 23 | \
             int(bool((sm7 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 24 | \
             int(bool((sm7 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 25 | \
             int(bool((sm7 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 26 | \
             int(bool((sm7 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 27 | \
             int(bool((sm8 & 0b0000_0000_0000_0000_0000_0000_1111_1111))) << 28 | \
             int(bool((sm8 & 0b0000_0000_0000_0000_1111_1111_0000_0000))) << 29 | \
             int(bool((sm8 & 0b0000_0000_1111_1111_0000_0000_0000_0000))) << 30 | \
             int(bool((sm8 & 0b1111_1111_0000_0000_0000_0000_0000_0000))) << 31 

        self.handler(sm);
        
    def start(self):
        self.sm_base.active(True)

    def end(self):
        self.sm_base.active(False)

if __name__ == '__main__':
    
    # def invert_unsigned(x, bit_width):
    #     mask = (1 << bit_width) - 1  # Create a mask with the desired bit-width
    #     return ~x & mask  # Invert the bits and apply the mask
    ring = Ring()

    def handler(sm):
        print(f'handler sm invert = {bin(sm)} or = {bin(sm ^ 0b1111_1111_1111_1111_1111_1111_1111_1111)}')
        ring.debug(sm)

    ir_base = IrBase(handler)
    ir_base.start()
    
    while True:
       time.sleep(60)
    
    
    print('end')
    ir_base.end()