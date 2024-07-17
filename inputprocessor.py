# Description: This file contains the InputProcessor class which is 
# responsible for processing the input data from the controller.
# not sure if i am going to use it 
class InputProcessor:
    def __init__(self):
        # Add your initialization code here
        self.input_data = 0
        self.button_map = {1: 0b100, 
                            2: 0b1000,
                            3: 0b10000,
                            4: 0b100000,
                            5: 0b1000000,
                            6: 0b10000000,
                            7: 0b100000000,
                            8: 0b1000000000,
                            9: 0b10000000000,
                            10: 0b100000000000,
                            11: 0b1000000000000,
                            12: 0b10000000000000,
                            13: 0b100000000000000,
                            14: 0b1000000000000000}

    def process_input(self, input_data):
        self.input_data = input_data

    def get_input(self):
        return self.input
        
    def is_main_button_pressed(self):
        return self.input_data & 0b1
    
    def is_secondary_button_pressed(self):
        return self.input_data & 0b10
    
    def is_button_pressed(self, button):
        return self.input_data & self.button_map[button]

