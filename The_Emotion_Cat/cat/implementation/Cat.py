import time 
from cat.interface.ICat import ICat 

class Cat(ICat):
    '''
    Class that connects the body control with the intelligent agent.
    '''
    
    def __init__(self, 
                _decision_maker, 
                _emotion_detector, 
                _motivation_to_meet_a_new_human):
        '''
        Constructor.
        
        Parameters
        -----------
            _decision_maker: DecisionMaker;
            _emotion_detector: EmotionDetector;
            _motivation_to_meet_a_new_human: Register, handles the 
                registration of a new owner.
        '''
        self.decision_maker = _decision_maker
        self.emotion_detector = _emotion_detector
        self.motivation_to_meet_a_new_human = _motivation_to_meet_a_new_human
        
    def start(self, name):
        '''
        Links the body control with the intelligent agent.
        
        Parameters
        -----------
            - name: string, name of the current owner.
        '''
        self.emotion_detector.set_owner(name)
        self.emotion_detector.start()
        moved = False
        
        while True:
            if self.emotion_detector.stopped:
                return
            if not self.emotion_detector.detect:
                if not moved:
                    detected_emotion = self.emotion_detector.get_emotion()
                    self.decision_maker.mirror_emotion(detected_emotion)
                    time.sleep(0.5)
                    moved = True
            else:
                moved = False
                continue

    def register(self, name):
        '''
        Handles the registration of a new owner.
        
        Parameters
        -----------
            - name: string.
        '''
        self.motivation_to_meet_a_new_human.register(name)
