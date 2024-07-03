from ring import Ring

class Jeopardy:
    def __init__(self, ring):
        self.ring = ring
        self.first = 0
        self.second = 0
        self.rest = 0
        self.found_first = False
        self.found_second = False
        self.stage = 0
        self.order = []
        

    def clear(self):
        print('Clear')
        self.first = 0
        self.second = 0
        self.rest = 0
        self.found_first = False
        self.found_second = False
        self.stage = 0
        self.order = []
        self.ring.Clear()

    def display(self, var):
        value = bin(var)
        print(value)
        value = value[2:]
        for i in range(16 - len(value)):
            value = "0" + value
        print(f'{value[0:4]} {value[4:8]} {value[8:12]} {value[12:16]}')

    def _show_all(self):
        self.ring.show(0b1111_1111_1111_1111, self.ring.WHITE)
        self.ring.show(self.first, self.ring.GREEN)
        self.ring.show(self.second, self.ring.YELLOW)
        self.ring.show(self.rest, self.ring.RED)

    def processInput(self, input):
        if input & 0b1:
            print('Button 0 pressed')
            print(f'self.order={self.order} len={len(self.order)}')
            if len(self.order) > 1: # Check if we have more than one button in the order
                remove =  self.order.pop(0)
                print(f'remove={bin(remove)} first={bin(self.first)} second={bin(self.second)} rest={bin(self.rest)}')
                self.first = self.first & ~remove
                self.second = self.second & ~remove
                self.rest = self.rest & ~remove

                print(f'Post remove button={bin(remove)} first={bin(self.first)} second={bin(self.second)} rest={bin(self.rest)}')

                next = self.order[0]

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
                        
                    
                # self.second, btn = self._remove(self.second)
                # print(f'Move up from second button={btn} first={bin(self.first)} second={bin(self.second)} rest={bin(self.rest)}')
                # if btn >= 0:
                #     self.first = self.first | btn
                    


                # self.rest, btn = self._remove(self.rest)
                # print(f'Move up from rest button={btn} first={bin(self.first)} second={bin(self.second)} rest={bin(self.rest)}')
                # if btn >= 0:
                #     self.second = self.second | btn

                # if not self.order:
                #     self.Clear()
                #     return

                print(f'Post remove={bin(remove)} first={bin(self.first)} second={bin(self.second)} rest={bin(self.rest)}')

                self._show_all()
                return # button is command just return
            else:
                self.clear()
                return # button is command just return

        input = input & ~(self.first | self.second | self.rest)

        if input == 0:
            return

        button_list = self._button_list(input)

        print(button_list)

        for button in button_list:
            self.order.append(button)
            print(f'Adding to order button={bin(button)} first={bin(self.first)} second={bin(self.second)} rest={bin(self.rest)}')

      
        if self.stage == 0:
            # print(f'Stage = 0 input = {input}')
            self.first = input
            self.stage = 1
        
        elif self.stage == 1:
            # print(f'Stage = 1 input = {input}')
            self.second =  input  & ~self.first
            self.stage = 2

        else:
            print(f'Stage = 2 input = {input}  stage = {self.stage}')
            self.rest = (input | self.rest) & ~(self.first | self.second)

        background = 0b1111_1111_1111_1111 & ~(self.first | self.second | self.rest)
        self.ring.show()
        
    def _button_list(self, buttons):
        button_list = []
        for i in range(16):
                #print(f'Button looking - {(buttons >> i)}')
                if (buttons >> i) & 1:
                    power_of_2 = 1 << i  # Calculate 2 to the power of i using bit shifting
                    button_list.append(power_of_2)
        return button_list

    def _remove(self, button):
        # print(f'Remove first from button {bin(buttton)}')
        self.first = self.first & ~button
        self.second = self.second & ~button
        self.rest = self.rest & ~button
        for i in range(16):
            if (button >> i) & 1:
                power_of_2 = 1 << i  # Calculate 2 to the power of i using bit shifting
                return (button & ~power_of_2, power_of_2)
        return (button, -1)

    def show(self):
        print('showing')
        self.ring.show()

    def __str__(self):
        return f'Jeperody: {1 + 1} elf.date, self.time, self.location'


# if __name__ == "__main__":
#     from consolering import ConsoleRing

#     consoleRing = ConsoleRing()
#     consoleRing.show()
#     consoleRing.set(1, Ring.RED)
#     consoleRing.show()
#     consoleRing.set(2, Ring.GREEN)
#     consoleRing.show()
#     consoleRing.set(15, Ring.YELLOW)
#     consoleRing.show()
#     consoleRing.set(10, Ring.WHITE)
#     consoleRing.show()

#     consoleRing.clear()
#     consoleRing.show()