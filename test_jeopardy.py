import unittest
from jeopardy import Jeopardy
from consolering import ConsoleRing
from unittest.mock import Mock

class JeopardyTests(unittest.TestCase):
    def setUp(self):
        self.consoleRing = Mock()
        self.jeopardy = Jeopardy(self.consoleRing)

    def test_clear(self):
        self.jeopardy.clear()
        self.consoleRing.Clear.assert_called_once()

    # def test_display(self):
    #     var = "test"
    #     self.jeopardy.display(var)
    #     # Add assertions here to check if the display method works as expected

    def test_show(self):
        self.jeopardy.show()
        self.consoleRing.show.assert_called_once()

    def test_processInput(self):
        input = 0b10
        self.jeopardy.processInput(input)
        # Add assertions here to check if the processInput method works as expected

    # def test__button_list(self):
    #     buttons = [1, 2, 3]
    #     self.jeopardy._button_list(buttons)
    #     # Add assertions here to check if the _button_list method works as expected

    # def test__remove(self):
    #     button = 1
    #     self.jeopardy._remove(button)
    #     # Add assertions here to check if the _remove method works as expected

    # def test__show_all(self):
    #     self.jeopardy._show_all()
    #     # Add assertions here to check if the _show_all method works as expected

    # def test___str__(self):
    #     result = str(self.jeopardy)
    #     # Add assertions here to check if the __str__ method works as expected

if __name__ == '__main__':
    unittest.main()