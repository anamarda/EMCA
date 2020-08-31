import time
import logging
from resources.global_variables import *
from utils.conversions import *
from body.domain.interfaces.ILimb import ILimb

class Tail(ILimb):
    '''
    Class which commands the tail of the robot.
    '''
    
    def __init__(self, 
                _channel, 
                _init_angle, 
                _message, 
                _bus, 
                _validator):
        '''
        Constructor.
        
        Parameters
        -----------
                _channel: hexa number, address of the channel corresponding
                        to the servomotor of the tail;
                _init_angle: integer, initial angle of the servomotor;
                _message: string, specifies the limb (RF/RB/LF/LB/head/tail),  
                        logging purposes;
                _bus: smbus, makes the I2C communication with hardware;
                _validator: AngleValidator, validation purposes.
        '''
        logging.basicConfig(filename=LOGGER_PATH, level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + 
                        '__init__' + ' : ' + _message)
          
        self.channel = _channel
        self.crt_angle = _init_angle
        self.message = _message        
        self.bus = _bus
        self.validator = _validator 
            
        self.__go_to_neutral_position()
        
    def __go_to_neutral_position(self):
        '''
        Moves the limb to the neutral position.
        '''
        logging.debug(self.__class__.__name__ + ' - ' + 
                        '__go_to_neutral_position')
        
        pulse = from_degrees_to_pulse(self.crt_angle)
        self.bus.write_word_data(ADDR, self.channel, 0)                   
        self.bus.write_word_data(ADDR, self.channel + 2, pulse)         
        time.sleep(NEUTRAL_TRANS_PAUSE)
        
    def move(self, param_list):
        '''
        Moves the limb's servomotor to a given angle with a given speed.
                
        Parameters
        -----------
                param_list: list, it has 2 elements with the following
                        meaning: angle for the servomotor,
                                 speed of transitions.
        '''
        logging.debug(self.__class__.__name__ + ' - ' +
                        'move' + ' ' + self.message)
        
        angle = param_list[0]
        steps = param_list[1]
        
        self.validator.check_angle(angle)            
        if self.crt_angle < angle:
            for angle_aux in range(self.crt_angle, angle, steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, self.channel + 2, pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle = angle
        else:
            for angle_aux in range(self.crt_angle, angle, -steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, self.channel + 2, pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle = angle
