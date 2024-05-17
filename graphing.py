from datetime import datetime
import config
import matplotlib.pyplot as plt
from logger import error
import globals

def graph():
 
    """
    Function graphing generates a graph from the last 20 seconds of data from the ultrasonic sensor
    Parameters:
        None
    Returns:
        None
    """
    if len(globals.ultrasonicSensorValues) == 0:
        error("Insufficient data to graph")
        return
    current_time = globals.ultrasonicSensorValues[-1]['timestamp']

    # Filter data for the last 20 seconds
    trafficDistanceY = [data['distance'] for data in globals.ultrasonicSensorValues if data['timestamp'] > current_time - 20]

    trafficDistanceX = []

    # If trafficDistanceY is not empty, calculate trafficDistanceX based on actual timestamps
    if trafficDistanceY:
        start_time = globals.ultrasonicSensorValues[-len(trafficDistanceY)]['timestamp']
        trafficDistanceX = [((start_time - data['timestamp']) + 20) for data in globals.ultrasonicSensorValues[-len(trafficDistanceY):]]


    if len(trafficDistanceX) < 20/(config.pollingInterval*config.numAverageValues) - 1: # Add 1 to account for values polling interval not being a factor of 20
        error("Insufficient data to graph")
        return

    plt.subplot(3, 1, 1)
    plt.plot(trafficDistanceX, trafficDistanceY, marker='o', label="Traffic Distance")
    plt.xlabel('Time (s)')
    plt.ylabel('Traffic Distance (m)')
    plt.title(f'Traffic Distance in the last 20 seconds')

    plt.subplot(3, 1, 2)
    temperatureY = [data['temperature'] for data in globals.temperatureSensorValues if data['timestamp'] > current_time - 20]
    temperatureX = []
    if temperatureY:
        start_time = globals.temperatureSensorValues[-len(temperatureY)]['timestamp']
        temperatureX = [((start_time - data['timestamp']) + 20) for data in globals.temperatureSensorValues[-len(temperatureY):]]
    plt.ylim(bottom=0, top=30)
    plt.plot(temperatureX, temperatureY, marker='o', label="Temperature")
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (C)')
    plt.title(f'Temperature in the last 20 seconds')

    plt.subplot(3, 1, 3)
    lightY = [data['numerical'] for data in globals.lightSensorValues if data['timestamp'] > current_time - 20]
    lightX = []
    if lightY:
        start_time = globals.lightSensorValues[-len(lightY)]['timestamp']
        lightX = [((start_time - data['timestamp']) + 20) for data in globals.lightSensorValues[-len(lightY):]]
    plt.ylim(bottom=0, top=2)
    plt.plot(lightX, lightY, marker='o', label="Light Level")
    plt.xlabel('Time (s)')
    plt.ylabel('Light Level')
    plt.title(f'Light Level in the last 20 seconds')


    plt.xlim(0, 20)
    if trafficDistanceY:  # Only set ylim if there is data
        plt.ylim(bottom=0, top=max(trafficDistanceY) + 1) 

    plt.savefig(f"graphs/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png")
    plt.show()
