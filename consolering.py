import array, time

class ConsoleRing():
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
        # Start the StateMachine, it will wait for data on its FIFO.
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        for i in range(0, len(self.ar)):
            self.set(i, ConsoleRing.BLACK)

    def clear(self):
        for i in range(0, 32):
            self.set(i, ConsoleRing.BLACK)

    def show(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.NUM_LEDS)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
        time.sleep(.00001)

    def set(self, i, color):
        self.ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

        
        

# consoleRing = ConsoleRing()
# consoleRing.thing()
# consoleRing.show()
# consoleRing.set(1, ConsoleRing.RED)
# consoleRing.show()
# consoleRing.set(2, ConsoleRing.GREEN)
# consoleRing.show()
# consoleRing.set(15, ConsoleRing.YELLOW)
# consoleRing.show()
# consoleRing.set(10, ConsoleRing.WHITE)
# consoleRing.show()

# consoleRing.clear()
# consoleRing.show()