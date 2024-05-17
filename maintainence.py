import time
import config
from lightsfunction import maintainence_mode
from logger import error, log

def authorise(pin, numberOfAttempts = 0) -> bool:
    """
    Authorizes the user by comparing the entered PIN with the provided PIN. If 3 times incorrect,
    the user will be locked out for 2 mins.

    Is recursive

    Parameters:
        pin (int): The correct PIN for authorization.
        numberOfAttempts (int, optional): The number of attempts made to enter the PIN. Defaults to 0.

    Returns:
        bool: True if the entered PIN matches the correct PIN, False otherwise.
    """

    # Check if the number of attempts is equal to 3
    if numberOfAttempts == 3:
        numberOfAttempts = 0 # Reset number of attempts
        error("LOCKED OUT FOR 2 MINUTES ...", showDate=False, colourBackground=True) # LOG ERROR
        time.sleep(2*60) # Lock out user for 2 mins


    # Get pin
    userInputPin = input("Please enter ADMIN Pin: ")

    # Try Catch Statement to catch non digit entries and return an error

    try:
        userInputPin = int(userInputPin)

        if userInputPin == pin: # If correct pin, return true
            return True
        
        # If incorrect, then give error and then recurse function

        error("Wrong Pin", showDate=False)
        if authorise(pin, numberOfAttempts+1):
            return True
        
        return False
    
    except:
        error("Please enter a number", showDate=False)
        if authorise(pin, numberOfAttempts):
            return True

        return False


    

def maintainence_service():
    """
    Function to handle maintenance service.

    This function prompts the user to update certain parameters related to maintenance.
    The user can update the polling interval value.

    Protected by pin

    Parameters:
        None
    Returns:
        None

    """
    global pollingInterval
    pin = 2479

    authorised = authorise(pin)

    timeEnd = time.time() + config.adminTimeoutMins*60

    maintainence_mode()

    if authorised:
        log("Successfully entered maintenance", showDate=False)
        while True:
            if time.time() > timeEnd:
                return
            print(f"""
                Updatable parameters
                1. Polling Interval = {config.pollingInterval} seconds
                2. Maintenance Timeout = {config.adminTimeoutMins} minutes
                3. Refreshes per Frame = {config.scrollTime} times per frame
            """)
            updateParameter = input("Which value do you want to update (Ctrl+C to exit) >> ")
            match updateParameter:
                case "1":
                    newValue = input("What would you like to change the value to (0.5s to 10s) >> ")
                    try:
                        newValue = float(newValue)
                        if newValue < 0.5 or newValue > 10:
                            error("Value outside of range")
                            continue
                        config.pollingInterval = newValue
                    except ValueError:
                        error("Invalid Value")
                case "2":
                    newValue = input("What would you like to change the value to (1 min to 5 min) >> ")
                    try:
                        newValue = float(newValue)
                        if newValue < 1 or newValue > 5:
                            error("Value outside of range")
                            continue
                        config.adminTimeoutMins = newValue
                    except ValueError:
                        error("Invalid Value")
                case "3":
                    newValue = input("What would you like to change the value to (5 to 20) >> ")
                    try:
                        newValue = int(newValue)
                        if newValue < 5 or newValue > 20:
                            error("Value outside of range")
                            continue
                        config.scrollTime = newValue
                    except ValueError:
                        error("Invalid Value")

                    
