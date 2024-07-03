import array, time, random
import machine
from machine import Pin, lightsleep
import rp2
from rp2 import PIO, StateMachine, asm_pio


# Configure the number of WS2812 LEDs.
NUM_LEDS = 1


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def remote():
    pull(block)
    mov(y, osr)
    wrap_target()  
    #Wait for Start Bit
    label("wait_start_bit")
    set(x, 20)
    wait(0, pin, 0)
    wait(1, pin, 0)
    label("verify_start_bit")
    jmp(x_dec, "end_start_bit")
    jmp(pin, "verify_start_bit")
    jmp("wait_start_bit") # Not the start bit start again
    label("end_start_bit")
 
    # Wait to set my bit
    wait(0, pin, 0)  #4, 14,  
    
    label("start_bits")
    jmp(y_dec, "bits") 
    jmp("nobits")
    label("bits")
    jmp("start_bits")[6]    
    label("nobits")

    
    set(pins, 1)[5] # want pulse to be 5 long
    set(pins, 0)
    
    
    wrap()


@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, push_thresh=16, autopush=True)
def base():
    # Create start bit
    wrap_target()
    set(x, 15)
    set(pins, 1)[31]
    set(pins, 0)
     
    # Pull in bits
    nop()[6]
    label("next_bit")
    in_(pins, 1)
    jmp(x_dec, "next_bit")[6]
    # irq(noblock, rel(0))
    wrap()

sm_remote = StateMachine(1, remote, freq=8000000, set_base=Pin(1), in_base=Pin(2))
sm_base   = StateMachine(0, base, freq=8000000, set_base=Pin(2), in_base=Pin(1))

sm_remote.active(True)
sm_remote.put(15 - 0)
sm_base.active(True)
    
# meeting = Meeting()

print('meeting') 

time.sleep(.1)
value = str(bin(sm_base.get())) 
print(value)
value = value[2:]
for i in range(16 - len(value)):
    value = "0" + value
print(f'{value[0:4]} {value[4:8]} {value[8:12]} {value[12:16]}')
#print(f"{value:#016b}")
sm_base.active(False)
sm_remote.active(False)
print('done')