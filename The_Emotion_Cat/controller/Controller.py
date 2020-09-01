from resources.global_variables import OWNERS_PATH
import os 

class Controller:
    '''
    This class manages the main functionalities of the application.
    '''
    
    def __init__(self, _validator, _cat):
        '''
        Constructor.
        
        Parameters
        -----------
                _validator: GuiValidator;
                _cat: Cat, the robot with both body control and intelligent
                        agent.
        '''
        self.validator = _validator
        self.cat = _cat
        
    def get_owners(self):
        '''
        Getter for all the owners.
        
        Returns
        --------
            - a list of strings
        '''
        return [f for f in os.listdir(OWNERS_PATH)]

    def start_emotion_prediction(self, name):
        '''
        Starts the emotion detection algorithm.
        
        Parameters
        -----------
            - name: string, the chosen owner.
        '''
        self.validator.validate_name(name)
        self.cat.start(name)
        
    def register_owner(self, name):
        '''
        Registers a new owner.
        
        Parameters
        -----------
            - name: string, the new owner.
        '''
        self.validator.validate_name(name)
        self.cat.register(name)
