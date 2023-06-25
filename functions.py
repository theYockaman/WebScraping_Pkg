import traceback
import sys
import time
    
# Syntax Printer
def printSyntax(syntax:str, toPrint:bool = True):
    """Prints Syntax

    :param syntax: Syntax of what you want to print out
    :type syntax: str
    :param toPrint: `True` Prints Syntax, `False` Does Not Prints Syntax, defaults to True
    :type toPrint: bool, optional
    """
    if toPrint is True:
        print(syntax)
        
# Print Traceback
def printTraceback() -> None:
    """Prints the Traceback of Current Ran Code and Quits the Code
    """
    print(traceback.format_exc())
    sys.exit()

# Check Duration of Code
class Duration: 
    def __init__(self) -> None:
        """Duration to find Length of time it takes to Run Code. Starts with the .start() function.
        """
        self.start()

    def start(self) -> None:
        """ Grabs Start Time with Setting Final Time to None
        """
        
        self._t0 = time.time()
        self._t1 = None

    def end(self) -> None:
        """Sets the End Time and Prints the Time from .start() to .end()
        """
        
        self._t1 = time.time()
        time_lapse = self._t1 - self._t0

        minutes = int(time_lapse//60)
        seconds = int(time_lapse-(minutes *60))
        milliseconds = round((time_lapse - seconds) * (1000),2)
        
        print("{} minutes, {} seconds, {} milliseconds".format(minutes,seconds,milliseconds))

# Checks Variable DataType
def checkType(variables:dict[list]) -> bool:
    """Check Types of Variables

    :param variables: Key: Variable Value: List of Values
    :type variables: dict[list]
    :raises ValueError: "Variables wrong type"
    :raises ValueError: "Value wrong type"
    :return: `True` Types Valid with Variables , `False` Types Not Valid with Variables
    :rtype: bool
    """
    
    if not isinstance(variables,dict): raise ValueError("Variables wrong type")
    
    for key, value in variables.items():
        
        if key is None and None not in value: return False

        if key is None and None in value: continue
        
        if not isinstance(value,list): raise ValueError("Value wrong type")
        
        if None in value: value.remove(None)
        
        if type(key) not in value: return False
        
    return True


