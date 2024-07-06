class Game:
    def __init__(self, input_processor, games):
        self.game = 0
        self.games = games
        self.input_processor = input_processor
        self.buttons = 0
        # Initialize game variables here

    def process_input(self, buttons):
        self.input_processor.process_input(buttons)
        if self.input_processor.long_presses[0]:
            self.game = self.game + 1 if self.game < len(self.games) - 1 else 0

        self.games[self.game].processInput(self.input_processor)
        # Start the game logic here

    

if __name__ == "__main__":
    from inputprocessor import InputProcessor

    class TestGame0:
        def processInput(self, input_processor):
            print(f'Game 0 Processing buttons {bin(input_processor.button_count)}')
    class TestGame1:
        def processInput(self, input_processor):
            print(f'Game 1 Processing buttons {bin(buttons)}')
    game = Game(InputProcessor(), [TestGame0(), TestGame1()])
    game.process_input(0b10)
    