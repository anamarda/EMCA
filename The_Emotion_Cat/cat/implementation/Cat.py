import time 
from cat.interface.ICat import ICat 

class Cat(ICat):
    '''
    Class that connects the body control with the intelligent agent.
    '''
    
    def __init__(self, 
                _decision_maker, 
                _emotion_detector, 
                _trainer, 
                _motivation_to_meet_a_new_human):
        '''
        Constructor.
        
        Parameters
        -----------
            _decision_maker: DecisionMaker;
            _emotion_detector: EmotionDetector;
            _trainer: Trainer, handles the training of a new model for 
                emotion detection;
            _motivation_to_meet_a_new_human: Register, handles the 
                registration of a new owner.
        '''
        self.decision_maker = _decision_maker
        self.emotion_detector = _emotion_detector
        self.trainer = _trainer
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
        while True:
            detected_emotion = self.emotion_detector.get_emotion()
            print("[INFO] Detected emotion: " + detected_emotion)
            self.decision_maker.mirror_emotion(detected_emotion)
            self.decision_maker.mirror_emotion("Neutral")
            time.sleep(0.5)
            print(self.emotion_detector.stopped)
            if self.emotion_detector.stopped:
                print("===========DA")
                return
                
    def train(self, epoch, lr, decay):
        '''
        Trains a new model for emotion detection.
        
        Parameters
        -----------
            - epochs: integer;
            - lr: float, learning rate;
            - decay: float.
        '''
        self.trainer.train(epoch, lr, decay)

    def register(self, name):
        '''
        Handles the registration of a new owner.
        
        Parameters
        -----------
            - name: string.
        '''
        self.motivation_to_meet_a_new_human.register(name)
