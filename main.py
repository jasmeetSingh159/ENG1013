from pymata4 import pymata4
from graphing import graph
from lightsfunction import shift_out
from maintainence import maintainence_service
from polling_loop import polling_loop
from logger import error
import config
import globals
import time

def run_polling_loop():
    """
    Runs the polling loop indefinitely.
    Parameters:
        None
    Returns:
        None
    """
    while True:
        globals.currentTimerStates = 0b00000000
        globals.nextStage = 1
        globals.nextStageChange = time.time() + config.stageIntervalsInSeconds[0]
        shift_out([globals.currentLedState])
        polling_loop(config.pollingInterval)

def servicesMenu(): 
    """
    Displays the services menu and prompts the user to select an operation mode.
    Parameters:
        None
    Returns:
        None
    """
    print("""
          Please select operation mode

          1. Normal Operation
          2. Maintenance
          3. Data Observation
          """)
    mode = input("Please select mode (1-3) >> ")
    try:
        mode = int(mode)
        match(mode):
            case 1:
                run_polling_loop()
            case 2:
                maintainence_service()
            case 3:
                graph()
                print("data observation mode")
    except ValueError:
        error("Invalid Value")

def main():
    """
    The main entry point of the program.
    Parameters:
        None
    Returns:
        None
    """
    globals.stageChangedAt = time.time()
    globals.nextStageChange = time.time()
    initialise()
    while True:
        try:
            servicesMenu()
        except KeyboardInterrupt:
            pass
        except EOFError:
            globals.board.shutdown()
            time.sleep(1)
            print("\nExiting...\r\n")
            exit(0)
            
        

def initialise():
    """
    Initialises the board and sets up the pin modes.
    Parameters:
        None
    Returns:
        None
    """
    globals.programStartTime = time.time()

    globals.board.set_pin_mode_digital_input(config.buttonPin)

    globals.board.set_pin_mode_digital_output(config.segLatchPin)
    globals.board.set_pin_mode_digital_output(config.segClockPin)
    globals.board.set_pin_mode_digital_output(config.segDataPin)

    globals.board.set_pin_mode_digital_output(config.digLatchPin)
    globals.board.set_pin_mode_digital_output(config.digClockPin)
    globals.board.set_pin_mode_digital_output(config.digDataPin)

    globals.board.set_pin_mode_digital_output(config.ledLatchPin)
    globals.board.set_pin_mode_digital_output(config.ledClockPin)
    globals.board.set_pin_mode_digital_output(config.ledDataPin)

    globals.board.set_pin_mode_digital_input(config.maintenanceSwitchPin)

    globals.board.set_pin_mode_analog_input(config.temperatureSensorPin)
    globals.board.set_pin_mode_analog_input(config.ldrPin)

    globals.board.set_pin_mode_sonar(config.ultrasonicTriggerPin, config.ultrasonicEchoPin, timeout=80000)
    globals.board.set_pin_mode_sonar(config.heightSensorTriggerPin, config.heightSensorEchoPin, timeout=80000)


if __name__ == '__main__':

    main()
