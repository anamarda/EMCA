'''
Mathematical conversions.
'''

from resources.global_variables import *

def from_degrees_to_pulse(value):
    '''
    Function that converts a value from degrees to pulse.
    
    Parameters
    -----------
        - value: float, value that needs to be converted.
    
    Returns
    --------
        - float, the converted value.
    '''
    return int(PULSE_VAR1 + PULSE_VAR2 * value)
    
def from_radians_to_degrees(value):
    '''
    Function that converts a value from redians to degrees.
    
    Parameters
    -----------
        - value: float, value that needs to be converted.
    
    Returns
    --------
        - float, the converted value.
    '''
    return math.floor(value * DEGREES_VAR / PI)

def from_degrees_to_radians(value):
    '''
    Function that converts a value from degrees to radians.
    
    Parameters
    -----------
        - value: float, value that needs to be converted.
    
    Returns
    --------
        - float, the converted value.
    '''
    return value * PI / DEGREES_VAR
