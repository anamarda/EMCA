import cv2
import os
import imutils
import time
import pickle
import face_recognition
import numpy as np
from threading import Thread
from imutils.video import VideoStream
from brain.utils.model import create_model
from resources.global_variables import *

class Brain:
    '''
    The intelligent agent class.
    '''
    
    def __init__(self):
        '''
        Constructor.
        '''
        self.crt_emotion = STARTING_EMOTION
        self.model_weighs_path = MODEL_WEIGHS_PATH
        self.owner = None
        self.stopped = False
        self.detect = False
        
    def set_owner(self, name):
        '''
        Setter of the owner.
        '''
        self.owner = name     
        
    def start(self):   
        '''
        Starts the thread that does the emotion detection of the 
        recognised owner.
        
        Returns
        --------
            - self
        '''
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
        
    def update(self):
        '''
        Main method that does the emotion detection of the recognised 
        owner.
        '''
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        model = create_model()
        model.load_weights(self.model_weighs_path)
        cv2.ocl.setUseOpenCL(False)

        emotion_dict = {
            0: ANGRY_STR, 
            1: DISGUSTED_STR, 
            2: FEARFUL_STR, 
            3: HAPPY_STR, 
            4: NEUTRAL_STR, 
            5: SAD_STR, 
            6: SURPRISED_STR
                }

        print("[INFO] starting video stream...")
        vs = VideoStream(src=0, usePiCamera=True).start()
        time.sleep(CAMERA_SLEEP)

        data = pickle.loads(open(FACE_ENCODINGS_PATH + self.owner + '.pickle', "rb").read())
        detector = cv2.CascadeClassifier(HAAR_PATH)

        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=FRAME_WIDTH)
            
            if self.detect is False:
                
                cv2.putText(frame, self.owner + " is " + self.crt_emotion, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else: 
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                face_rectangles = detector.detectMultiScale(
                        gray, 
                        scaleFactor=SCALE_FACTOR, 
                        minNeighbors=MIN_NEIGHBORS,
                        flags=cv2.CASCADE_SCALE_IMAGE)

                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in face_rectangles]

                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []

                for encoding in encodings:
                    matches = face_recognition.compare_faces(data["encodings"],encoding)
                    name = UNKNOWN_FACE
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        name = max(counts, key=counts.get)
                        
                    names.append(name)
                        
                emotions = []
                for ((x, y, w, h), name) in zip(boxes, names): 
                    if name != self.owner:
                        emotions.append("")
                        continue
                    try:
                        roi_gray = gray[y:y + h, x:x + w]
                        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                        prediction = model.predict(cropped_img)
                        maxindex = int(np.argmax(prediction))
                        emotions.append(emotion_dict[maxindex])
                    except Exception as e:
                        emotions.append("")
                        #print(e)
                        continue
                        
                    for ((top, right, bottom, left), name, emotion) in zip(boxes, names, emotions):
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        y = top - 15 if top - 15 > 15 else top + 15
                            
                        if name != self.owner:
                            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.75, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, name + " is " + emotion, (left, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 255, 0), 2)
                            self.crt_emotion = emotion
                    
            if cv2.waitKey(33) == ord('c'):
                self.detect = not self.detect
                print(self.detect)
                #print(self.crt_emotion)
                    
            if cv2.waitKey(33) == ord('q'):
                self.stopped = True
                break
            cv2.imshow("Frame", frame)
            
        cv2.destroyAllWindows()
        vs.stop()

    def get_emotion(self):
        '''
        Getter of the current detected emotion.
        
        Returns
        --------
            - string, signifying an emotion
        '''
        #print( "Neutral" if self.crt_emotion == "" else self.crt_emotion)
        return "Neutral" if self.crt_emotion == "" else self.crt_emotion
        
    def stop(self):
        '''
        Indicates that the thread should be stopped.
        '''
        self.stopped = True
