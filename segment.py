import globals
import config
import time


digit_register = {
    0: 0b01111110,
    1: 0b00110000,
    2: 0b01101101,
    3: 0b01111001,
    4: 0b00110011,
    5: 0b01011011,
    6: 0b01011111,
    7: 0b01110000,
    8: 0b01111111,
    9: 0b01111011,

    ' ': 0b00000000,
    '!': 0b10110000,
    '"': 0b00100010,
    '#': 0b00111111,
    '$': 0b01011011,
    '%': 0b10100101,
    '&': 0b00110001,
    "'": 0b00000010,
    '(': 0b01001010,
    ')': 0b01101000,
    '*': 0b01000010,
    '+': 0b00000111,
    "'": 0b00000100,
    '-': 0b00000001,
    '.': 0b10000000,
    '/': 0b00100101,
    '0': 0b01111110,
    '1': 0b00110000,
    '2': 0b01101101,
    '3': 0b01111001,
    '4': 0b00110011,
    '5': 0b01011011,
    '6': 0b01011111,
    '7': 0b01110000,
    '8': 0b01111111,
    '9': 0b01111011,
    ':': 0b01001000,
    ';': 0b01011000,
    '<': 0b01000011,
    '=': 0b00001001,
    '>': 0b01100001,
    '?': 0b11100101,
    '@': 0b01111101,
    'A': 0b01110111,
    'B': 0b00011111,
    'C': 0b01001110,
    'D': 0b00111101,
    'E': 0b01001111,
    'F': 0b01000111,
    'G': 0b01011110,
    'H': 0b00110111,
    'I': 0b00000110,
    'J': 0b00111100,
    'K': 0b01010111,
    'L': 0b00001110,
    'M': 0b01010100,
    'N': 0b01110110,
    'O': 0b01111110,
    'P': 0b01100111,
    'Q': 0b01101011,
    'R': 0b01100110,
    'S': 0b01011011,
    'T': 0b00001111,
    'U': 0b00111110,
    'V': 0b00111110,
    'W': 0b00101010,
    'X': 0b00110111,
    'Y': 0b00111011,
    'Z': 0b01101101,
    '[': 0b01001110,
    '\\': 0b00010011,
    ']': 0b01111000,
    '^': 0b01100010,
    '_': 0b00001000,
    '`': 0b00100000,
    'a': 0b01111101,
    'b': 0b00011111,
    'c': 0b00001101,
    'd': 0b00111101,
    'e': 0b01101111,
    'f': 0b01000111,
    'g': 0b01111011,
    'h': 0b00010111,
    'i': 0b00000100,
    'j': 0b00011000,
    'k': 0b01010111,
    'l': 0b00000110,
    'm': 0b00010100,
    'n': 0b00010101,
    'o': 0b00011101,
    'p': 0b01100111,
    'q': 0b01110011,
    'r': 0b00000101,
    's': 0b01011011,
    't': 0b00001111,
    'u': 0b00011100,
    'v': 0b00011100,
    'w': 0b00010100,
    'x': 0b00110111,
    'y': 0b00111011,
    'z': 0b01101101,
    '{': 0b00110001,
    '|': 0b00000110,
    '}': 0b00000111,
    '~': 0b01000000
}

config.segDataPin = 7
config.segClockPin = 5
config.segLatchPin = 6

# Shift register for digits
config.digDataPin = 10
config.digClockPin = 8
config.digLatchPin = 9

def send_to_shift_register(data_pin, clock_pin, latch_pin, byte):
    """ 
    Send a byte to a specific shift register
    Parameters:
        data_pin (int): The data pin of the shift register
        clock_pin (int): The clock pin of the shift register
        latch_pin (int): The latch pin of the shift register
        byte (int): The byte to send to the shift register
    Returns:
        None
    """
    for i in range(8):
        # Send bits (MSB first)
        globals.board.digital_write(data_pin, (byte >> i) & 1)
        globals.board.digital_write(clock_pin, 1)
        time.sleep(0.0001)  # Small delay to ensure the clock pulse is registered
        globals.board.digital_write(clock_pin, 0)
    globals.board.digital_write(latch_pin, 1)  # Enable slave select
    globals.board.digital_write(latch_pin, 0)  # Latch and disable slave select

def display_digit(digit, segments):
    """ 
    Display segments on a specific digit 
    Parameters:
        digit (int): The digit to display
        segments (int): The segments to display
    Returns:
        None
    """
    # Calculate the active digit pin (active-low for common cathode)
    digit_enable = 1 << (7 - digit)
    segments = digit_register[segments]
    # Send segment and digit data to their respective shift registers
    send_to_shift_register(config.digDataPin, config.digClockPin, config.digLatchPin, 0xFF)
    send_to_shift_register(config.segDataPin, config.segClockPin, config.segLatchPin, segments)
    send_to_shift_register(config.digDataPin, config.digClockPin, config.digLatchPin, ~digit_enable)
    time.sleep(0.0005)

def display_screens():
    """
    Display both screens and the scrolling animation
    Parameters:
        None
    Returns:
        None
    """
    message = f"S-0{globals.nextStage:.0f}  T-{globals.temperatureSensorValues[-1]['temperature']:02.1f}"
    height = f"H-{globals.lastCarHeight:02.0f}"

    display_digit(globals.display1Counter, message[::-1][globals.display1Counter-globals.scrollIndex])
    display_digit(globals.display2Counter+4, height[::-1][globals.display2Counter-4])
    if globals.display1Counter == 3:
        globals.dispCount += 1
        globals.display1Counter = 0
        if globals.dispCount >= config.scrollTime:
            globals.scrollIndex += 1
            if globals.scrollIndex >= len(message):
                globals.scrollIndex = 0
            globals.dispCount = 0
    else:
        globals.display1Counter = globals.display1Counter + 1
    
    if globals.display2Counter == 3:
        globals.display2Counter = 0
    else:
        globals.display2Counter = globals.display2Counter + 1
