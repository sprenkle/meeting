from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio
from jeopardy import Jeopardy
from ring import Ring
from positionstate import PositionState
import time





class IrRemote:
    
    def __init__(self, handler, receiver_pin = 14, transmitter_pin = 28) -> None:
        self.sm_base =  StateMachine(0, self.pulse, freq=(38_000 * 6), in_base=Pin(receiver_pin), set_base=Pin(transmitter_pin))
        self.handler = handler
        self.pin = Pin(14, Pin.IN)
        self.pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.pin_handler)
        self.start_pulse = 0
        self.pulse_ = False
        self.sm_base.active(1)

    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
    def pulse():
        # Create start bit
        pull(block)
        set(x, osr)
        nop()[31]
        nop()[31]
        nop()[31]
        nop()[31]

        set(y, 10)
        label("loop")
        set(pins, 1)[1]
        set(pins, 0)[2]
        jmp(y_dec, "loop")

    def pin_handler(self, pin):
        if pin.value() == 1:
            if self.start_pulse == 0:
                self.start_pulse = time.ticks_us()
        else:
            pulse_length = time.ticks_us() - self.start_pulse
            # print(f'pulse_length {pulse_length}') #25843
            self.start_pulse = 0
            if pulse_length > 24843 and pulse_length < 26843:
                self.run_pulse()
                self.sm_base.put(16)
        # 

    def run_pulse(self):
        if not self.pulse_:
            print('pulse dd')
            # self.sm_base.active(1)  # Start the state machine
            # self.pulse_ = True
            # while self.sm_base.irq() == 0:
            #     pass  # Wait for the PIO program to complete
            # self.sm_base.active(0)  # Stop the state machine
            # self.pulse_ = False

    
if __name__ == '__main__':
  


    def handler(sm):
        print(f'handler {sm}')

    print('start')
    base = IrRemote(handler)
   
    
    # base.sm_base.put(16)
    # time.sleep(1)
    # base.sm_base.put(16)
    while True:
        time.sleep(1)