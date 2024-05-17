import time
import math
from lightsfunction import set_pedestrian_lights, set_traffic_lights, overheight_car, shift_out,stage_5_buzzer
import config
import globals
from logger import alert, log

from segment import display_screens

nextPollTime = 0

def polling_loop(interval):
    global nextPollTime
    """
    Executes a polling loop that performs various tasks at regular intervals.

    Parameters:
        interval (float): The time interval between each loop execution in seconds. Default is 3 seconds.
    Returns:
        None
    """

    display_screens()

    time.sleep(0.05)

    isMaintenance = globals.board.digital_read(config.maintenanceSwitchPin)[0]
    if isMaintenance:
        print("Maintenance mode")
        print("Please turn off switch to continue normal operation")
        raise KeyboardInterrupt
    

    if globals.nextStage == 5:
        stage_5_buzzer()
        if time.time() >= globals.nextBlink:
            print("Blinking pedestrian lights")
            if globals.isFlashing:
                set_pedestrian_lights('off')
                globals.isFlashing = False
            else:
                set_pedestrian_lights('green')
                globals.isFlashing = True
            globals.nextBlink = time.time() + 0.5
    else:
        globals.currentTimerStates = 0b00000000
        shift_out([globals.currentLedState])

    if nextPollTime <= time.time():
        startTime = time.time()
        poll()
        endTime = time.time()
        timeToCompleteLoop = endTime - startTime
        printSummary(timeToCompleteLoop, interval)
        nextPollTime = time.time() + interval - timeToCompleteLoop

    if not globals.isButtonPressed:
        button_press()
    
    if time.time() - globals.buttonPressTime > 0.5:
        globals.isButtonPressed = False

    if get_dv_dt() > 5:
        alert("Car approaching quickly")
    
    if globals.lastCarHeight >= config.maxCarHeight:
        alert("Overheight Car")
        overheight_car()
    else:
        globals.currentTimerStates = 0b00000000
        shift_out([globals.currentLedState])
    
    if globals.nextStage == 1:
        if globals.isButtonPressed:
            globals.nextStageChange = time.time() + 5

    if globals.ultrasonicSensorValues[-1]['distance'] <= config.keepYellowLightDistance:
        if globals.nextStage == 2:
            globals.nextStageChange += 3

    if globals.nextStage == 1:
        for i in range(len(globals.ultrasonicSensorValues[::-1])):
            value = globals.ultrasonicSensorValues[::-1][i]
            if value['distance'] <= config.keepYellowLightDistance:
                if 3 < globals.ultrasonicSensorValues[-1]['timestamp']-value['timestamp'] < 4:
                    if globals.ultrasonicSensorValues[-1]['distance'] == value['distance']:
                        alert("Car not moving")

    



def printSummary(timeToCompleteLoop, interval):
    """
    Prints a summary of the time taken to complete the loop and the interval between each loop execution.

    Parameters:
        timeToCompleteLoop (float): The time taken to complete the loop in seconds.
        interval (float): The time interval between each loop execution in seconds.
    Returns:
        None
    """
    log(f"""
        Time to complete loop: {timeToCompleteLoop:.3f}s, Interval: {interval}s
        Current Stage: {globals.nextStage}
        Number of pedestrians: {globals.numPedestrians}
        Temperature: {globals.temperatureSensorValues[-1]['temperature']:.2f}C
        Current Distance: {globals.ultrasonicSensorValues[-1]['distance']:.2f}cm
        Light Level: {globals.lightSensorValues[-1]['lightLevel']}
        Last Car Height: {globals.lastCarHeight:.2f}
        Rate of change of distance: {get_dv_dt():.2f}cm/s
        """)
    

def poll(): 
    """
    Performs the actual polling tasks.
    Parameters:
        None
    Returns:
        None
    """
    ultrasonic_sensor()
    get_temperature()
    get_light_level()
    height_sensor()
    
    if globals.nextStageChange <= time.time():
        set_traffic_lights(globals.nextStage, changeStage)

def changeStage(stage):
    """
    Changes the current stage to the specified stage.

    Parameters:
        stage (int): The stage to change to.
    Returns:
        None
    """
    globals.nextStage = (stage + 1) % 6
    globals.stageChangedAt = time.time()
    globals.nextStageChange = time.time() + config.stageIntervalsInSeconds[stage]

def ultrasonic_sensor():
    """
    Reads the distance from the ultrasonic sensor and logs the value.
    Parameters:
        None
    Returns:
        (float): The distance in centimeters.
    """
    distance = globals.board.sonar_read(config.ultrasonicTriggerPin)[0]

    if globals.trafficDistanceCount >= config.numAverageValues:
        ultrasonicSensorObject = {
            "distance": globals.aggregatedTrafficDistance / config.numAverageValues,
            "timestamp": time.time()
        }
        print(ultrasonicSensorObject)
        globals.ultrasonicSensorValues.append(ultrasonicSensorObject)
        globals.trafficDistanceCount = 0
        globals.aggregatedTrafficDistance = 0
        return distance
    else:
        globals.aggregatedTrafficDistance += distance
        globals.trafficDistanceCount += 1

def height_sensor():
    """
    Reads the height from the height sensor and logs the value.
    Parameters:
        None
    Returns:
        (float): The height in centimeters.
    """
    height = globals.board.sonar_read(config.heightSensorTriggerPin)[0]
    globals.lastCarHeight = 28 - height
    return height

def get_temperature():
    """
    Reads the temperature from the temperature sensor and logs the value.

    Parameters:
        None
    
    Returns:
        float: The temperature in degrees Celsius.
    """
    temperature = globals.board.analog_read(config.temperatureSensorPin)[0]
    R1 = 6560
    c1 = 1.009249522e-03 
    c2 = 2.378405444e-04
    c3 = 2.019202697e-07
    R2 = R1 * (1023.0 / temperature - 1)
    logR2 = math.log(R2);
    T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2))
    T = T - 273.15
    """
    CODE ABOVE MODIFIED FROM https://www.circuitbasics.com/arduino-thermistor-temperature-sensor-tutorial/
    REWRITTEN TO USE PYTHON
    """
    T = T - 10 # Offset to compensate for the 10C offset in the thermistor

    temperatureSensorObject = {
        "temperature": T,
        "timestamp": time.time()
    }
    globals.temperatureSensorValues.append(temperatureSensorObject)

    return T

def get_light_level():
    """
    Reads the light level from the light sensor and logs the value.

    Parameters:
        None
    
    Returns:
        string: 'Light' or 'Dark'
    """
    lightLevel = globals.board.analog_read(config.ldrPin)[0]
    if lightLevel > 600:
        lightLevel = 'Light'
    else:
        lightLevel = 'Dark'

    lightSensorObject = {
        "lightLevel": lightLevel,
        "numerical": 1 if lightLevel == 'Light' else 0,
        "timestamp": time.time()
    }
    globals.lightSensorValues.append(lightSensorObject)
    return lightLevel

def get_dv_dt():
    """
    Calculates the rate of change of the distance with respect to time.

    Parameters:
        None
    Returns:
        float: The rate of change of the distance with respect to time.
    """
    if len(globals.ultrasonicSensorValues) < 2:
        return 0
    else:
        dv_dt = (globals.ultrasonicSensorValues[-1]['distance'] - globals.ultrasonicSensorValues[-2]['distance']) / (globals.ultrasonicSensorValues[-1]['timestamp'] - globals.ultrasonicSensorValues[-2]['timestamp'])
        return dv_dt

def button_press():
    """
    Reads the state of the button and logs the state.
    Parameters:
        None
    Returns:
        (bool): 1 or 0
    """
    buttonState = globals.board.digital_read(config.buttonPin)
    if (buttonState[0] == 1): 
        globals.numPedestrians = globals.numPedestrians + 1
        globals.isButtonPressed = True
        globals.buttonPressTime = time.time()
        
        time.sleep(0.01)
    return buttonState[0]

