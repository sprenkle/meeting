from consolering import ConsoleRing
from positionstate import PositionState
from jeopardy import Jeopardy

position_state = PositionState(ConsoleRing.GREEN, ConsoleRing.YELLOW, ConsoleRing.RED, ConsoleRing.WHITE, ConsoleRing.BLACK)   
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