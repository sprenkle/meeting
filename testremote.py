from machine import Pin
import time

pinIn = Pin(15, Pin.IN, Pin.PULL_DOWN)

def wait_low():
    start_time = time.ticks_us()  # Get start time in microseconds
    while pinIn.value() == 1:
        pass
    end_time = time.ticks_us()  # Get end time in microseconds
    return time.ticks_diff(end_time, start_time)  # Calculate duration

def wait_high():
    start_time = time.ticks_us()  # Get start time in microseconds
    while pinIn.value() == 0:
        pass
    end_time = time.ticks_us()  # Get end time in microseconds
    return time.ticks_diff(end_time, start_time)  # Calculate duration


# Measure low pulse duration
low_pulse_duration = wait_low()
print(f'Low pulse duration: {low_pulse_duration} us')

# Measure high pulse duration
high_pulse_duration = wait_high()
print(f'High pulse duration: {high_pulse_duration} us')

# Measure low pulse duration
low_pulse_duration = wait_low()
print(f'Low pulse duration: {low_pulse_duration} us')

# Measure high pulse duration
high_pulse_duration = wait_high()
print(f'High pulse duration: {high_pulse_duration} us')