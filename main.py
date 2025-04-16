# imports
import machine
import math
import time

#######################################
# Pin and constant definitions
#######################################
SEVEN_SEGMENT_START_PIN = 0
DISPLAY_COUNT = 4
MEASUREMENT_COUNT = 4  
DECIMAL_PRECISION = 3
BUTTON_PIN = 16
ANALOGUE_INPUT_PIN = 26
ADC_RANGE = float((math.pow(2, 16) - 1))
DEBOUNCE_DELAY = 100

# HEX values for 7 segment display values
digit_list_hex = [
    0x40,  # 0
    0x79,  # 1
    0x24,  # 2
    0x30,  # 3
    0x19,  # 4
    0x12,  # 5
    0x02,  # 6
    0x78,  # 7
    0x00,  # 8
    0x10,  # 9
    0x08,  # A
    0x03,  # B
    0x46,  # C
    0x21,  # D
    0x06,  # E
    0x0E,  # F
    0x7F   # Empty
]

#######################################
# Global variables
#######################################
display_value = 0
segment_pins = []
display_select_pins = []
current_display_index = DISPLAY_COUNT -1  # to keep track of which digit is currently being displayed
display_timer = None
counter_timer = None
prev_analogue_voltage = -1
last_button_press = 0

#######################################
# Function definitions
#######################################

# Function to read the ADC pin and
# to convert the digital value to a voltage level in the 0-3.3V range
# This function updates the value of the display_value global variable
def read_analogue_voltage(pin):
    """
    Reads the analogue voltage level 16 times, averages the reading, 
    and places the calculated average value into the display_value global variable.
    """
    global display_value, last_button_press
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_button_press) < DEBOUNCE_DELAY:
        return  # Debounce: ignore if pressed too soon

    last_button_press = current_time

    # Read the analogue input 16 times and calculate average voltage
    total = 0
    for _ in range(16):
        total += pin.read_u16()
    average = total / 16
    voltage = (average / ADC_RANGE) * 3.3  # Convert to voltage (0-3.3V)
    display_value = int(voltage * 1000)  # Scale voltage to display (0-3300 for 0.000-3.300V)
    print(f"Measured voltage: {voltage:.3f} V")  # Print for debugging

# Function to disable timer that triggers scanning 7 segment displays
def disable_display_timer():
    global display_timer
    display_timer.deinit()

# Function to enable timer that triggers scanning 7 segment displays
def enable_display_timer():
    global display_timer
    display_timer.init(period=30, mode=machine.Timer.PERIODIC, callback=scan_display)

# Function to handle scanning 7 segment displays
# Display the value stored in the display_value global variable
# on available 7-segment displays
def scan_display(timer_int):
    global current_display_index, display_value

    # Extract the digit corresponding to the current display index
    digit = int((display_value // math.pow(10, current_display_index))) % 10

    # Display the digit,
    # enable the decimal point if the current digit index equals to the set decimal precision
    display_digit(digit, current_display_index, 
        current_display_index == DECIMAL_PRECISION and 0 != DECIMAL_PRECISION)

    # Move to the next display
    current_display_index = (current_display_index - 1)
    if current_display_index < 0:
        current_display_index = DISPLAY_COUNT -1

# Function display the given value on the display with the specified index
# dp_enable specifies if the decimal pooint should be on or off
def display_digit(digit_value, digit_index, dp_enable=False):
    # Ensure the value is valid
    if digit_value < 0 or digit_value > len(digit_list_hex):
        return

    # Deselect all display select pins
    for pin in display_select_pins:
        pin.value(0)

    # Set the segments according to the digit value
    mask = digit_list_hex[digit_value]
    for i in range(7):  # 7 segments from A to G
        segment_pins[i].value((mask >> i) & 1)

    # Set the DP if it's enabled
    segment_pins[7].value(1 if dp_enable == False else 0)

    # If digit_index is -1, activate all display select pins
    if digit_index == -1:
        for pin in display_select_pins:
            pin.value(1)
    # Otherwise, ensure the index is valid and activate the relevant display select pin
    elif 0 <= digit_index < DISPLAY_COUNT:
        display_select_pins[digit_index].value(1)

# Function to test avaiable 7-segment displays
def display_value_test():
    global display_value

    disable_display_timer()
    current_display_index = 0

    for i in range(0, len(digit_list_hex)):
        display_digit(i, -1, i % 2 != 0)
        time.sleep(0.5)

    for i in range(0, len(digit_list_hex)):
        display_digit(i, DISPLAY_COUNT - 1 - (i % DISPLAY_COUNT), True)
        time.sleep(0.5)        

    display_digit(16, -1, False)
    enable_display_timer()

def count_display_value(timer_int):
    global display_value
    display_value += 1
    if display_value > 9999:
        display_value = 0
    #print(display_value)

# Function to setup GPIO/ADC pins, timers and interrupts
def setup():
    global segment_pins, display_select_pins, button_pin, analogue_voltage_pin
    global display_timer, counter_timer

    # Set up display select pins
    for i in range(SEVEN_SEGMENT_START_PIN + 8, SEVEN_SEGMENT_START_PIN + 8 + DISPLAY_COUNT):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.value(0)
        display_select_pins.append(pin)
    
    # Set up seven segment pins
    for i in range(SEVEN_SEGMENT_START_PIN, SEVEN_SEGMENT_START_PIN + 8):
        pin = machine.Pin(i, machine.Pin.OUT)
        pin.value(1)
        segment_pins.append(pin)

    # Setup button and ADC pins
    button_pin = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    analogue_voltage_pin = machine.ADC(ANALOGUE_INPUT_PIN)
    
    
    # Start the timer interrupt for scanning
    display_timer = machine.Timer()
    enable_display_timer()   

if __name__ == '__main__':
    setup()
    # display_value_test()

while True:
    if button_pin.value() == 0:
        voltage = read_analogue_voltage(analogue_voltage_pin)
    time.sleep(0.01)   

