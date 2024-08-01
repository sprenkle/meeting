import time
from machine import Pin
import rp2

# Define the PIO program for generating IR signals
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def ir_tx():
    wrap_target()
    set(pins, 1)   # Send a high signal for 32 cycles
    set(pins, 0)   # Send a low signal for 32 cycles
    wrap()

# Initialize the state machine with the PIO program
sm = rp2.StateMachine(0, ir_tx, freq=152000, set_base=Pin(14))

sm.active(1)  # Activate the state machine


time.sleep(5)  # Sleep for 1 second
sm.active(0)  # Deactivate the state machine

print("Done")  # Print "Done" to the console