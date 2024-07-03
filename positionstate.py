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
        return ~(self.first | self.second | self.rest)

    def promote(self, promote, new_second=0):
        # Moving the next button to the first group
        if promote & self.first:
            pass
        elif promote & self.second:
            self.second = self.second & ~promote
            self.first = self.first | promote

        if new_second & self.rest:
            self.rest = self.rest & ~new_second
            self.second = self.second | new_second


        
if __name__ == '__main__': 
    from consolering import ConsoleRing
    consoleRing = ConsoleRing()
    position_state = PositionState(ConsoleRing.GREEN, ConsoleRing.YELLOW, ConsoleRing.RED, ConsoleRing.WHITE)
    position_state.first = 0b10
    position_state.second = 0b100
    position_state.rest = 0b1000

    print(f'{bin(position_state.first)} {bin(position_state.second)} {bin(position_state.rest)}')
    position_state.remove(0b10)
    position_state.promote(0b100, 0b1000)
    print(f'{bin(position_state.first)} {bin(position_state.second)} {bin(position_state.rest)}')
    position_state.remove(0b100)
    position_state.promote(0b1000)
    print(f'{bin(position_state.first)} {bin(position_state.second)} {bin(position_state.rest)}')
    position_state.remove(0b1000)
    print(f'{bin(position_state.first)} {bin(position_state.second)} {bin(position_state.rest)}')
