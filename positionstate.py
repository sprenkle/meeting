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
        
