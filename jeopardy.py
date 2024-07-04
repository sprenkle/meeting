class Jeopardy:
    def __init__(self, ring, position_state):
        self.ring = ring
        self.position_state = position_state
        self.clear()

    def clear(self):
        self.position_state.clear()
        self.found_first = False
        self.found_second = False
        self.state = 0 # 0 = first, 1 = second, 2 = rest for statemachine
        self.order = []
        self.ring.clear()
        self.position_state.clear()

    def _show_all(self):
        self.ring.show(self.position_state)

    def processInput(self, input):
        if input & 0b1:
            print('Button 0 pressed')
            print(f'self.order={self.order} len={len(self.order)}')
            if len(self.order) > 1: # Check if we have more than one button in the order
                remove =  self.order.pop(0)
                promote = self.order[0]
                promote_second = self.order[1] if len(self.order) > 1 else 0
                self.position_state.remove(remove)
                self.position_state.promote(promote, promote_second)                        
                print(f'Post remove={bin(remove)} first={bin(self.position_state.first)} second={bin(self.position_state.second)} rest={bin(self.position_state.rest)}')
                self._show_all()
                return # button is command just return
            else:
                self.clear()
                self._show_all()
                return # button is command just return

        input = input & self.position_state.input_mask()

        if input == 0:
            return

        button_list = self._button_list(input)

        print(button_list)

        for button in button_list:
            self.order.append(button)
            print(f'Adding to order button={bin(button)}')

      
        if self.state == 0:
            print(f'Stage = 0 input = {input}')
            self.position_state.first = input
            self.state = 1
        
        elif self.state == 1:
            print(f'Stage = 1 input = {input}')
            self.position_state.second =  input  & ~self.position_state.first
            self.state = 2

        else:
            print(f'Stage = 2 input = {input}  stage = {self.state}')
            self.position_state.rest = (input | self.position_state.rest) & ~(self.position_state.first | self.position_state.second)

        self._show_all()

        
    def _button_list(self, buttons):
        button_list = []
        for i in range(16):
                #print(f'Button looking - {(buttons >> i)}')
                if (buttons >> i) & 1:
                    power_of_2 = 1 << i  # Calculate 2 to the power of i using bit shifting
                    button_list.append(power_of_2)
        return button_list

    # def _remove(self, button):
    #     # print(f'Remove first from button {bin(buttton)}')
    #     self.first = self.first & ~button
    #     self.second = self.second & ~button
    #     self.rest = self.rest & ~button
    #     for i in range(16):
    #         if (button >> i) & 1:
    #             power_of_2 = 1 << i  # Calculate 2 to the power of i using bit shifting
    #             return (button & ~power_of_2, power_of_2)
    #     return (button, -1)

    def show(self):
        print('showing')
        self.ring.show()

    def __str__(self):
        return f'Jeperody: {1 + 1} elf.date, self.time, self.location'


if __name__ == '__main__':
    from consolering import ConsoleRing
    from positionstate import PositionState

    position_state = PositionState(ConsoleRing.GREEN, ConsoleRing.YELLOW, ConsoleRing.RED, ConsoleRing.WHITE)   
    ring = ConsoleRing()

    jeopardy = Jeopardy(ring, position_state)
    jeopardy.processInput(0b10)
    jeopardy.processInput(0b100)
    jeopardy.processInput(0b1000)
    jeopardy.processInput(0b10000)
    jeopardy.processInput(0b100000)

    jeopardy.processInput(0b1)
    jeopardy.processInput(0b1)
    jeopardy.processInput(0b1)
    jeopardy.processInput(0b1)
    jeopardy.processInput(0b1)