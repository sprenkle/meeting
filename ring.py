import array, time, random
import machine
from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio




@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


class Ring:
    BLACK = (0, 0, 0)
    RED = (128, 0, 0)
    YELLOW = (128, 75, 0)
    GREEN = (0, 128, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (8, 8, 8)
    COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

    def __init__(self):
        self.NUM_LEDS = 32
        # Create the StateMachine with the ws2812 program, outputting on Pin(23).ws2812
        self.sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(6))#23-16
        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        self.set(0b1111_1111_1111_1111, Ring.BLACK)
        self.brightness = 0.5
        self.sm.put(self.ar,8)

    def clear(self):
        for i in range(0, 32):
            self.set(i, Ring.BLACK)
        self.sm.put(self.ar,8)
        


    #         r = int(((c >> 8) & 0xFF) * self.brightness)
    #         g = int(((c >> 16) & 0xFF) * self.brightness)
    #         b = int((c & 0xFF) * self.brightness)
    #         dimmer_ar[i] = (g<<16) + (r<<8) + b
    #     self.sm.put(dimmer_ar, 8)
    #     time.sleep(.00001)


    def set(self, buttons, color):
        for i in range(16):
            if (1 << i) & buttons:
                self.ar[i * 2] = (color[1]<<16) + (color[0]<<8) + color[2]
                self.ar[i * 2 + 1] = (color[1]<<16) + (color[0]<<8) + color[2]

    def show(self, position_state):
        # print('ring show')
        # print(f'ring show {position_state.first}')
        #print(f'show {position_state.first} {bin(position_state.second)} {bin(position_state.rest)}')
        if position_state.first == 0 :
            #print(f'clear')
            self.set(0b1111_1111_1111_1111, Ring.BLACK)
            self.sm.put(self.ar,8)
            return

        # print('ring show 1')
        
        other = ~(position_state.first | position_state.second | position_state.rest) 
        self.set(other, position_state.background_color if position_state.first else Ring.BLACK)
        self.set(position_state.second, position_state.second_color)
        self.set(position_state.first, position_state.first_color)
        self.set(position_state.rest, position_state.rest_color)
        # print('ring show 2')
        self.sm.put(self.ar,8)
        #print(f'show {bin(position_state.first)} {bin(position_state.second)} {bin(position_state.rest)} {bin(other)}')

if __name__ == '__main__':
    from positionstate import PositionState

    ring = Ring()
    position_state = PositionState(Ring.GREEN, Ring.YELLOW, Ring.RED, Ring.WHITE, Ring.BLACK)
    position_state.first = 1
    position_state.second = 2
    position_state.rest = 0
    for i in range(0, 3200):
        position_state.first = random.randint(0, 0xFFFF)
        ring.show(position_state)