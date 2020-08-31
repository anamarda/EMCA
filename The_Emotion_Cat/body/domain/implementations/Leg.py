import time
import math
import logging
import threading
from resources.global_variables import *
from utils.conversions import *
from body.domain.interfaces.ILimb import ILimb

class Leg(ILimb):
    '''
    Class which commands one leg of the robot.
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
                        to the upper servomotor of the leg;
                _init_angle1: integer, initial angle of the upper 
                        servomotor;
                _channel2: hexa number, address of the channel corresponding
                        to the lower servomotor of the leg;
                _init_angle2: integer, initial angle of the lower 
                        servomotor;
                _message: string, specifies the limb (RF/RB/LF/LB/head/tail),  
                        logging purposes;
                _bus: smbus, makes the I2C communication with hardware;
                _validator: AngleValidator, validation purposes.
        '''
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + 
                        '__init__' + ' : ' + _message)
         
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
                        '__init__' + self.message)
        
        pulse1 = from_degrees_to_pulse(self.crt_angle1)
        pulse2 = from_degrees_to_pulse(self.crt_angle2)

        self.bus.write_word_data(ADDR, self.channel1, 0)                   
        self.bus.write_word_data(ADDR, self.channel1 + OFFSET, pulse1)          
        time.sleep(NEUTRAL_TRANS_PAUSE)

        self.bus.write_word_data(ADDR, self.channel2, 0)                   
        self.bus.write_word_data(ADDR, self.channel2 + OFFSET, pulse2)          
        time.sleep(NEUTRAL_TRANS_PAUSE)

    def __correct_angles(self, q1, q2):
        '''
        Function that corrects the given angles according to the 
        specific limb. The left part limbs need the complement of 
        the current angle. 
        
        Parameters
        -----------
            q1: integer, angle for the upper servomotor; 
            q2: integer, angle for the lower servomotor.
            
        Returns
        --------
            - the two corrected angles
        '''
        if self.message in ['leg_right_front', 'leg_right_back']:
            return q1, q2
        if self.message in ['leg_left_front', 'leg_left_back']:
            return CORRECTING_VAR-q1, CORRECTING_VAR-q2

    def __move_upper_leg(self, angle1):
        '''
        Moves the upper servomotor to a given angle.
        
        Parameters
        -----------
                angle1: integer, the new angle;
        '''
        if self.crt_angle1 < angle1:
            for angle_aux in range(self.crt_angle1, angle1, LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel1 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle1
        else:
            for angle_aux in range(self.crt_angle1, angle1, -LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel1 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle1
        
    def __move_lower_leg(self, angle2):
        '''
        Moves the lower servomotor to a given angle.
        
        Parameters
        -----------
                angle2: integer, the new angle;
        '''
        if self.crt_angle2 < angle2:
            for angle_aux in range(self.crt_angle2, angle2, LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel2 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle2
        else:
            for angle_aux in range(self.crt_angle2, angle2, -LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel2 + OFFSET,
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle2
        
    def move_leg_with_given_angles(self, teta1, teta2):
        '''
        Parallelizes the move of the two servomotors of the limb. 
        
        Parameters
        -----------
                teta1: integer, angle in degrees (upper servomotor);
                teta2: integer, angle in degrees (lower servomotor).
        '''
        logging.debug(self.__class__.__name__ + ' - ' + 
                        'move_leg_with_given_angles' + ' ' + self.message)
        
        try:
            self.validator.check_angle(teta1)
            self.validator.check_angle(teta2)
            
            angle1 = int(teta1)
            angle2 = int(teta2)

            t_upper = threading.Thread(target=self.__move_upper_leg, 
                                        args=[angle1])
            t_lower = threading.Thread(target=self.__move_lower_leg, 
                                        args=[angle2])
            
            t_upper.daemon = True
            t_lower.daemon = True
            
            t_upper.start()
            t_lower.start()
            
            t_upper.join()
            t_lower.join()          
        except Exception as e:
            print(e.get_message())
    
    def move(self, param_list):
        '''
        This function uses the inverse kinematics to calculate 
        the angles for reaching a given location.
        
        Parameters
        -----------
            param_list: list, with the following elements:
                - a number on the Ox axis which specifies the 
                    end-effector location
                - a number on the Oy axis which specifies the 
                    end-effector location
        '''
        logging.debug(
            self.__class__.__name__ + ' - ' + 
            'move' + ' ' + self.message
                )
        
        x = param_list[0]
        y = param_list[1]
                 
        gamma = from_degrees_to_radians(LEG_ANGLE)
        a1 = THIGH_LENGTH
        a2 = CALF_LENGTH
            
        r = math.sqrt(x*x+y*y)
        phi1 = math.acos((a1*a1+r*r-a2*a2)/(IK_VAR*a1*r))
        phi2 = math.atan(y/x)
        q1 = phi2-phi1
        phi3 = math.acos((a1*a1+a2*a2-r*r)/(IK_VAR*a1*a2))
        q2 = phi3 - gamma
                        
        q1 = from_radians_to_degrees(q1)
        q2 = from_radians_to_degrees(q2)        
            
        q1, q2 = self.__correct_angles(q1, q2)         
        self.move_leg_with_given_angles(q1, q2)
