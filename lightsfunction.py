import globals
import config
import time

def set_traffic_lights(stageNumber, onChange):
    """
    Sets the traffic lights based on the given stage number.

    Parameters:
    - stageNumber (int): The stage number indicating the current state of the traffic lights.
    - onChange (function): A callback function to be executed when the stage number changes.
    Returns:
        None

    Executes the onChange callback function with the current stage number as an argument.
    """
    print("Stage Number: ", stageNumber+1) 
    if stageNumber==0:
        globals.numPedestrians = 0
        set_main_road_lights('green')
        set_side_road_lights('red')
        set_pedestrian_lights('red')
    elif stageNumber==1:
        set_main_road_lights('yellow')
        set_side_road_lights('red')
        set_pedestrian_lights('red')
    elif stageNumber==2:
        set_main_road_lights('red')
        set_side_road_lights('red')
        set_pedestrian_lights('red')
    elif stageNumber==3:
        set_main_road_lights('red')
        set_side_road_lights('green')
        set_pedestrian_lights('green')
    elif stageNumber==4:
        set_main_road_lights('red')
        set_side_road_lights('red')
        set_pedestrian_lights('green')
    elif stageNumber==5:
        set_main_road_lights('red')
        set_side_road_lights('red')
        set_pedestrian_lights('red')
    time.sleep(0.01)

    onChange(stageNumber)

latch_pin = config.ledLatchPin
clock_pin = config.ledClockPin
data_pin = config.ledDataPin


def set_main_road_lights(colour):
    """
    Sets the main road lights based on the given colour.

    Parameters:
    - colour (string): The colour to set the lights to. Can be 'red', 'yellow' or 'green'.
    Returns:
        None
    """
    RED_MASK = 0b00_000_001  
    YELLOW_MASK = 0b00_000_010  
    GREEN_MASK = 0b00_000_100  

    globals.currentLedState &= ~(RED_MASK | YELLOW_MASK | GREEN_MASK)

    if colour == 'red':
        globals.currentLedState |= RED_MASK
    elif colour == 'yellow':
        globals.currentLedState |= YELLOW_MASK
    elif colour == 'green':
        globals.currentLedState |= GREEN_MASK
    else:
        shift_out([globals.currentLedState])
    print("Current LED state: ", globals.currentLedState)
    shift_out([globals.currentLedState])

def set_side_road_lights(colour):
    """
    Sets the side road lights based on the given colour.

    Parameters:
    - colour (string): The colour to set the lights to. Can be 'red', 'yellow' or 'green'.
    Returns:
        None
    """
    RED_MASK = 0b00_001_000  
    YELLOW_MASK = 0b00_010_000  
    GREEN_MASK = 0b00_100_000  
    globals.currentLedState &= ~(RED_MASK | YELLOW_MASK | GREEN_MASK)

    if colour == 'red':
        globals.currentLedState |= RED_MASK
    elif colour == 'yellow':
        globals.currentLedState |= YELLOW_MASK
    elif colour == 'green':
        globals.currentLedState |= GREEN_MASK
    else:
        shift_out([globals.currentLedState])
    print("Current LED state: ", globals.currentLedState)
    shift_out([globals.currentLedState])

def set_pedestrian_lights(colour):
    """
    Sets the pedestrian lights based on the given colour.

    Parameters:
    - colour (string): The colour to set the lights to. Can be 'red' or 'green'.
    Returns:
        None
    """
    RED_MASK = 0b01_000_000  
    GREEN_MASK = 0b10_000_000   

    globals.currentLedState &= ~(RED_MASK | GREEN_MASK)

    if colour == 'red':
        globals.currentLedState |= RED_MASK
    elif colour == 'green':
        globals.currentLedState |= GREEN_MASK
    else:
        shift_out([globals.currentLedState])
    print("Current LED state: ", globals.currentLedState)
    shift_out([globals.currentLedState])

def overheight_car():
    """
    Sets the overheight car buzzers.
    Parameters:
        None
    Returns:
        None
    """
    globals.currentTimerStates = 0b00000011
    shift_out([globals.currentLedState])

def maintainence_mode():
    """
    Sets the maintainence mode lights.
    Parameters:
        None
    Returns:
        None
    """
    globals.currentTimerStates = 0b00000100
    shift_out([0b00000000])

def stage_5_buzzer():
    """
    Sets the stage 5 buzzer.
    Parameters:
        None
    Returns:
        None
    """
    globals.currentTimerStates = 0b00001000
    shift_out([globals.currentLedState])

def shift_out(data):
    """
    Shifts the given data out to the LEDs.

    Parameters:
    - data (list): A list of 8-bit values to shift out.
    Returns:
        None
    """
    globals.board.digital_write(latch_pin, 0)
    
    data.append(globals.currentTimerStates)

    for value in data: 
        for i in range(8):
            bit = (value >> (7 - i)) & 1
            globals.board.digital_write(data_pin, bit)
            time.sleep(0.001)  
            globals.board.digital_write(clock_pin, 1)
            time.sleep(0.001)  
            globals.board.digital_write(clock_pin, 0)
    
    globals.board.digital_write(latch_pin, 1)
    time.sleep(0.001)
    globals.board.digital_write(latch_pin, 0)

        