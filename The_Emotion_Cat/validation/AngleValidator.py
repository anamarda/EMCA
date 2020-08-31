from resources.global_variables import ANGLE_MAX, ANGLE_MIN, LOGGER_PATH
import logging

class AngleException(Exception):
    '''
    Class for domain exceptions.
    '''
    
    def __init__(self, _message):
        '''
        Constructor.
        
        Paramaters
        -----------
            - _message: string, the error message
        '''
        self.message = _message
        
    def get_message(self):
        '''
        Getter of the message field.
        
        Return
        -------
            - string, the error message
        '''
        return self.message

class AngleValidator:
    '''
    Class that validates data for domain.
    '''
    
    def __init__(self):
        '''
        Constructor.
        '''
        logging.basicConfig(filename=LOGGER_PATH, level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
        
    def check_angle(self, angle):
        '''
        Angle validation.
        
        Paramaters
        -----------
            - angle: integer
        
        Raise
        ------
            - AngleException, if the angle is not between 0 and 90 degrees.
        '''
        logging.debug(self.__class__.__name__ + ' - ' + 'check_angle')        
        if angle > ANGLE_MAX:
            raise AngleException("[ERR] " + str(angle) + " > " + str(ANGLE_MAX))
        if angle < ANGLE_MIN:
            raise AngleException("[ERR] " + str(angle) + " < " + str(ANGLE_MIN))
