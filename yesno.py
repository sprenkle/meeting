import time
from machine import Timer

class YesNo:
    def __init__(self, ring, position_state, valid_buttons = 0b11_1111_1111_1111):
        self.ring = ring
        # self.vote = 0
        # self.count = 0
        # self.count_down = 0
        self.process_state = position_state
        self.clear()
        self.all = 0b111110
        self.timer_running = 0b0
        self.timer = Timer(-1)
        self.valid_buttons = valid_buttons

    def clear(self):
        self.process_state.first = 0
        self.vote = 0
        self.count = 0
        self.count_down = 0
        self.yes = 0b0

    def _show_all(self):
        self.ring.show(self.position_state)

    def processInput(self, input):
        print(f'Processing Input {input & 0b1}  {input & 0b1 & ~self.timer_running}')
        if input & 0b1 & ~self.timer_running:
            self.process_state.clear()
            print('Button 0 pressed')
            self.count = 0
            self.timer_running = 0b1
            self.timer.init(mode=Timer.PERIODIC, period=250, callback=self.on_timer)  # Triggers every 2 seconds
            print('Timer started')
            return
        
        self.all = self.all | input
        if self.timer_running:
            self.yes = self.yes | input
            print(f'yes = {bin(self.yes)}')
        

    

    def show(self):
        print('showing')
        self.ring.show()


    def on_timer(self, something):
        # print(f'timer {self.count}')
        self.process_state.first = self.process_state.first + (1 << self.count) 

        if self.count < 16:
            self.ring.show(self.process_state)
          #  threading.Timer(0.075, self.start_timer).start()  # Reschedule timer for the next call
        else:
            print(f'Done timer {bin(self.all)}  {bin(self.process_state.first)}')
            self.timer.deinit()
            self.process_state.first = 0
            self.process_state.second = self.yes
            self.process_state.rest = self.all & ~self.yes
            print(f'all={bin(self.all)}  first = {self.process_state.first} second={bin(self.process_state.second)} rest = {bin(self.process_state.rest)}')
            self.ring.show(self.process_state)
            
            
        
        self.count += 1


    def __str__(self):
        return f'Jeperody: {1 + 1} elf.date, self.time, self.location'


if __name__ == '__main__':
    from consolering import ConsoleRing as Ring
    from positionstate import PositionState

    print('starting')

    position_state = PositionState(Ring.BLUE, Ring.GREEN, Ring.RED, Ring.WHITE, Ring.BLACK)   
    ring = Ring()

    yes_no = YesNo(ring, position_state)
    yes_no.processInput(0b1 << 5)
    time.sleep(.25)
    yes_no.processInput(0b1 << 6)
    time.sleep(.25)
    yes_no.processInput(0b1 << 7)
    time.sleep(.25)


    yes_no.processInput(0b1 << 0)
    time.sleep(.25)
    yes_no.processInput(0b1 << 1)
    time.sleep(.25)
    yes_no.processInput(0b1 << 2)
    time.sleep(.25)
    yes_no.processInput(0b1 << 3)
    time.sleep(.25)
    yes_no.processInput(0b1 << 4)
    time.sleep(.25)
    time.sleep(5)
    print('Done')

