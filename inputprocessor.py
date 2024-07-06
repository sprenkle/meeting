class InputProcessor:
    def __init__(self):
        # Add your initialization code here
        self.button_count = [0] * 16
        self.long_presses = [False] * 16
        self.LONG = 2
        self.input_data = 0
        pass

    def process_input(self, input_data):
        self.long_presses = [0] * 16
        self.input_data = input_data
        for i in range(16):
            if input_data & (1 << i):
                self.button_count[i] += 1
                if self.button_count[i] >= self.LONG:
                    self.long_presses[i] = True
        
    

