from datetime import datetime

def log(*values, showDate = False, colourBackground = False):
    """
    Logs the given values in green colour with an optional timestamp and optional background highlighting.

    Parameters:
        *values (str): The values to be logged.
        showDate (bool, optional): Whether to include the timestamp in the log message. Defaults to True.
        colourBackground (bool, optional):  Whether to colour the background or not. Defaults to False.

    Returns:
        None
    """

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Color codes
    blue = "\033[34m"
    green = "\033[32m"
    greenBackground = "\033[42m"
    reset = "\033[0m"
    
    # Join the values into a single string separated by spaces
    message = ' '.join(values)

    displayColour = greenBackground if colourBackground else green
    
    # Print the date and message in green, then reset the color
    if showDate:
        print(f"{blue}{date_str} --> {displayColour}[LOG] {message}{reset}")
    else:
        print(f'{displayColour}[LOG] {message}{reset}')

def error(*values: str, showDate: bool = False, colourBackground: bool = False) -> None:
    """
    Error Logs the given values in red colour with an optional timestamp and optional background highlighting.

    Parameters:
        *values (str): The values to be logged.
        showDate (bool, optional): Whether to include the timestamp in the log message. Defaults to True.
        colourBackground (bool, optional):  Whether to colour the background or not. Defaults to False.

    Returns:
        None
    """

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Color codes
    blue = "\033[34m"
    red = "\033[31m"
    redBackground = "\033[41m"
    reset = "\033[0m"
    
    # Join the values into a single string separated by spaces
    message = ' '.join(values)

    displayColour = redBackground if colourBackground else red
    
    # Print the date and message in red, then reset the color 
    if showDate: 
        print(f"{blue}{date_str} --> {displayColour}[ERROR] {message}{reset}")
    else:
        print(f'{displayColour}[ERROR] {message}{reset}')

def alert(*values: str, showDate: bool = False, colourBackground: bool = False) -> None:
    """
    Alert Logs the given values in yellow colour with an optional timestamp and optional background highlighting.

    Parameters:
        *values (str): The values to be logged.
        showDate (bool, optional): Whether to include the timestamp in the log message. Defaults to True.
        colourBackground (bool, optional):  Whether to colour the background or not. Defaults to False.

    Returns:
        None
    """

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Color codes
    blue = "\033[34m"
    yellow = "\033[33m"
    yellowBackground = "\033[43m"
    reset = "\033[0m"
    
    # Join the values into a single string separated by spaces
    message = ' '.join(values)

    displayColour = yellowBackground if colourBackground else yellow
    
    # Print the date and message in yellow, then reset the color
    if showDate:
        print(f"{blue}{date_str} --> {displayColour}[ALERT] {message}{reset}")
    else:
        print(f'{displayColour}[ALERT] {message}{reset}')
