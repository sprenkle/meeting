class PositionState:
    def __init__(self, first_color, second_color, rest_color, background_color):
        self.clear()
        self.first_color = first_color
        self.second_color = second_color
        self.rest_color = rest_color
        self.background_color = background_color

    def clear(self):
        self.first = 0
        self.second = 0
        self.rest = 0

    def remove(self, remove):
        self.first = self.first & ~remove
        self.second = self.second & ~remove
        self.rest = self.rest & ~remove

    def input_mask(self):
        return ~(self.position_state.first | self.position_state.second | self.position_state.rest)

    def promote(self, promote):
        # Moving the next button to the first group
        if next & self.first:
            pass
        elif next & self.second:
            self.second = self.second & ~next
            self.first = self.first | next

            if len(self.order) > 1:
                new_second = self.order[1]
                if new_second & self.rest:
                    self.rest = self.rest & ~new_second
                    self.second = self.second | new_second

        
if __name__ == '__main__': 
    from consolering import ConsoleRing
    consoleRing = ConsoleRing()
    position_state = PositionState(ConsoleRing.GREEN, ConsoleRing.YELLOW, ConsoleRing.RED, ConsoleRing.WHITE)
