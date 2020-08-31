import time
import threading 
import math 
import logging
from resources.global_variables import LOGGER_PATH, MOVE_PAUSE

class Mover:
    def __init__(self, _controller):
        '''
        Constructor.
        
        Parameters
        -----------
            _controller: ControllerLimb
        '''
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
    
        self.controller = _controller
        self.fct_list = [
            self.__move_RB, 
            self.__move_RF, 
            self.__move_LB, 
            self.__move_LF, 
            self.__move_tail, 
            self.__move_head,
                ]
        
    def __move_RF(self, point):
        '''
        Sends a list of parameters to the right front leg. 
        
        Parameters
        -----------
            - point: Point
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__move_RF')
        xin = point.x
        yin = point.y
        self.controller.move_limb('leg_right_front', [xin, yin])

    def __move_LF(self, point):
        '''
        Sends a list of parameters to the left front leg. 
        
        Parameters
        -----------
            - point: Point
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__move_LF')
        xin = point.x
        yin = point.y
        self.controller.move_limb('leg_left_front', [xin, yin])

    def __move_RB(self, point):
        '''
        Sends a list of parameters to the right bac leg. 
        
        Parameters
        -----------
            - point: Point
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__move_RB')
        xin = point.x
        yin = point.y
        self.controller.move_limb('leg_right_back', [xin, yin])

    def __move_LB(self, point):
        '''
        Sends a list of parameters to the left back leg. 
        
        Parameters
        -----------
            - point: Point
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__move_LB')
        xin = point.x
        yin = point.y
        self.controller.move_limb('leg_left_back', [xin, yin])
        
    def __move_tail(self, pair):
        '''
        Sends a list of parameters to the tail. 
        
        Parameters
        -----------
            - pair: Point
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__move_tail')
        angle = pair.x
        steps = pair.y
        self.controller.move_limb('tail', [angle, steps])
        
    def __move_head(self, tupl):
        '''
        Sends a list of parameters to the head. 
        
        Parameters
        -----------
            - tupl: tuple
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__move_head')
        angle1 = tupl[0]
        angle2 = tupl[1]
        steps = tupl[2]
        self.controller.move_limb('head', [angle1, angle2, steps])

    def __kitty_move(self, actions_parameters_list):
        '''
        Parallelizying the movement of each limb. 
        
        Parameters
        -----------
            - actions_parameters_list: list of objects representing
            a parameter list for each limb in order to move.
        '''
        logging.debug(self.__class__.__name__ + ' - ' + '__kitty_move')
        threads = []
        for action, fct in zip(actions_parameters_list, self.fct_list):
            t = threading.Thread(target=fct, args = [action])   
            t.daemon         
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            
    def move(self, move_list):
        '''
        Function that loops through a set of actions and sends them 
        as commands.
        
        Parameters
        -----------
            - move_list: list of lists, each element has a command for
            each leg, head and tail.
        '''
        logging.debug(self.__class__.__name__ + ' - ' + 'move')
        for move in move_list:
            self.__kitty_move(move)
            time.sleep(MOVE_PAUSE)
        time.sleep(1)
