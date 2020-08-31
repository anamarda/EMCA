import time
import logging
import threading
from resources.global_variables import *
from utils.conversions import *
from body.domain.interfaces.ILimb import ILimb

class Head(ILimb):
    '''
    Class which commands the head of the robot.
    '''    
    
    def __init__(self, 
                _channel1, 
                _init_angle1, 
                _channel2, 
                _init_angle2, 
                _message, 
                _bus, 
                _validator):
        '''
        Constructor.
        
        Parameters
        -----------
                _channel1: hexa number, address of the channel corresponding
                        to the lower servomotor of the head;
                _init_angle1: integer, initial angle of the lower 
                        servomotor;
                _channel2: hexa number, address of the channel corresponding
                        to the upper servomotor of the leg;
                _init_angle2: integer, initial angle of the upper 
                        servomotor;
                _message: string, specifies the limb (RF/RB/LF/LB/head/tail), 
                        logging purposes;
                _bus: smbus, makes the I2C communication with hardware;
                _validator: AngleValidator, validation purposes.
        '''
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + 
                        '__init__' +' : ' + _message)
         
        self.channel1 = _channel1
        self.channel2 = _channel2
        self.crt_angle1 = _init_angle1
        self.crt_angle2 = _init_angle2
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
        
        pulse1 = from_degrees_to_pulse(self.crt_angle1)
        pulse2 = from_degrees_to_pulse(self.crt_angle2)
     
        self.bus.write_word_data(ADDR, self.channel1, 0)                   
        self.bus.write_word_data(ADDR, self.channel1 + OFFSET, pulse1)          
        time.sleep(NEUTRAL_TRANS_PAUSE)

        self.bus.write_word_data(ADDR, self.channel2, 0)                   
        self.bus.write_word_data(ADDR, self.channel2 + OFFSET, pulse2)          
        time.sleep(NEUTRAL_TRANS_PAUSE)
        
    def __move_upper_head(self, angle, steps):
        '''
        Moves the upper servomotor to a given angle with a given speed.
        
        Parameters
        -----------
                angle: integer, the new angle;
                steps: integer, the speed with which the servomotor 
                        can move.
        '''
        if self.crt_angle1 < angle:
            for angle_aux in range(self.crt_angle1, angle, steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel1 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle
        else:
            for angle_aux in range(self.crt_angle1, angle, -steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel1 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle
                
    def __move_lower_head(self, angle, steps):
        '''
        Moves the lower servomotor to a given angle with a given speed.
        
        Parameters
        -----------
                angle: integer, the new angle;
                steps: integer, the speed with which the servomotor 
                        can move.
        '''
        if self.crt_angle2 < angle:
            for angle_aux in range(self.crt_angle2, angle, steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel2 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle
        else:
            for angle_aux in range(self.crt_angle2, angle, -steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel2 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle
        
    def move(self, param_list):
        '''
        Parallelizes the move of the two servomotors of the limb. 
        
        Parameters
        -----------
                param_list: list, it has 3 elements with the following
                        meaning: angle for the upper head servomotor, 
                                 angle for the lower head servomotor,
                                 speed of transitions.
        '''
        logging.debug(self.__class__.__name__ + ' - ' + 
                        'move' + ' ' + self.message)
        
        angle1 = param_list[0]
        angle2 = param_list[1]
        steps = param_list[2]
        
        self.validator.check_angle(angle1)
        self.validator.check_angle(angle2)

        t_upper = threading.Thread(target=self.__move_upper_head, 
                                        args=[angle1, steps])
        t_lower = threading.Thread(target=self.__move_lower_head, 
                                        args=[angle2, steps])
        t_upper.daemon = True
        t_lower.daemon = True
            
        t_upper.start()
        t_lower.start()
            
        t_upper.join()
        t_lower.join()          
