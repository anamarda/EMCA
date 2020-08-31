class ILimb:
    '''
    Interface for the movement of the robot's limbs (legs, head, tail).
    '''    
    def move(self, param_list):
        '''
        Function that commands the limbs to move to a new position given
        by the param_list parameters.
        '''
        pass
