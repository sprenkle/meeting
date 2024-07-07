from positionstate import PositionState
from ring import Ring

ring = Ring()
position_state = PositionState(Ring.GREEN, Ring.YELLOW, Ring.RED, Ring.WHITE)
position_state.first = 1
position_state.second = 2
position_state.rest = 0
ring.show(position_state)