class IrRemote:
    
    def __init__(self) -> None:
        self.sm = 
        
    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
    def pulse(self):
        # Create start bit
        wrap_target()
        mov(x, 15)
        irq(clear, 4)
        label("loop")
        set(pins, 1)
        set(pins, 0)
        jmp(x_dec, "loop")
        wrap()

    