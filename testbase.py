from positionstate import PositionState
from ring import Ring

ring = Ring()
position_state = PositionState(Ring.GREEN, Ring.YELLOW, Ring.RED, Ring.WHITE)
position_state.first = 0b1010_1010_1010_1010
position_state.second = 0b0101_0101_0101_0101
position_state.rest = 0
ring.show(position_state)