import array, time

class ConsoleRing():
    BLACK = '*'
    RED = 'R'
    YELLOW = 'Y'
    GREEN = 'G'
    CYAN = 'C'
    BLUE = 'B'
    PURPLE = 'P'
    WHITE = '-'
    COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

    def __init__(self):
        self.NUM_LEDS = 32
        # Create the StateMachine with the ws2812 program, outputting on Pin(23).ws2812
        # Start the StateMachine, it will wait for data on its FIFO.
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = "****************"

    def clear(self):
        self.ar = "****************"

    def show(self, position_state):
        self.set(0b1111_1111_1111_1111, position_state.WHITE)
        self.set(position_state.first, position_state.GREEN)
        self.set(position_state.second, position_state.YELLOW)
        self.set(position_state.rest, position_state.RED)

        print(self.ar)

    # def show(self, color):
    #     for i in range(16):
    #         self.set(i, color)
    #     self.show()

    def set(self, buttons, color):
        print(f'buttons={buttons} color={color}')
        for i in range(16):
            if (1 << i) & buttons:
                self.ar = self.ar[:i] + color + self.ar[i+1:]

        
if __name__ == '__main__': 
    from positionstate import PositionState       
    consoleRing = ConsoleRing()
    # consoleRing.set(0b10, ConsoleRing.RED)
    # consoleRing.show()
    # consoleRing.set(0b100, ConsoleRing.GREEN)
    # consoleRing.show()
    # consoleRing.set(0b1000, ConsoleRing.YELLOW)
    # consoleRing.show()
    # consoleRing.set(0b10000, ConsoleRing.WHITE)
    # consoleRing.show()
    position_state = PositionState(ConsoleRing.GREEN, ConsoleRing.YELLOW, ConsoleRing.RED, ConsoleRing.WHITE)

    consoleRing.clear()
    consoleRing.show(position_state)