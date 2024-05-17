from pymata4 import pymata4
import config
# Values that change over time

board = pymata4.Pymata4()

nextBlink = 0

currentLedState = 0b00000000

programStartTime = 0

isFlashing = False

nextStage = 0
nextStageChange = 0
stageChangedAt = 0 

numPedestrians = 0

isButtonPressed = False
buttonPressTime = 0

ultrasonicSensorValues = [{
    "distance": 0.00,
    "timestamp": 0.0 
}]
temperatureSensorValues = [
    {
        "temperature": 0.00,
        "timestamp": 0.0
    }
]
lightSensorValues = [
    {
        "lightLevel": "Dark",
        "numerical": 0,
        "timestamp": 0.0
    }
]

display1Counter = 0
display2Counter = 0

trafficDistanceCount = config.numAverageValues
aggregatedTrafficDistance = 0

scrollIndex = 0
dispCount = 0

lastCarHeight = 0

currentTimerStates = 0b00000000