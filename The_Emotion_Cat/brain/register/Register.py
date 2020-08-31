from resources.global_variables import OWNERS_PATH
from resources.global_variables import NR_OWNER_PHOTOS
from resources.global_variables import OWNERS_PATH
from resources.global_variables import FACE_ENCODINGS_PATH
from picamera import PiCamera
from time import sleep
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

class Register:
    '''
    Class that handles the registration of a new owner for the robot.
    '''
    
    def __init__(self):
        '''
        Constructor.
        '''
        self.owner = None
        
    def __encode_faces(self):
        '''
        Encoding the images of a new owner in a new pickle file.    
        '''
        print("Encoding faces...")
        imagePaths = list(paths.list_images(OWNERS_PATH + '/' + self.owner))
        knownEncodings = []
        knownNames = []
        for (i, imagePath) in enumerate(imagePaths):
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(self.owner)
        print("Serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(FACE_ENCODINGS_PATH + self.owner + '.pickle', "wb")
        f.write(pickle.dumps(data))
        f.close()
	
    def register(self, name):
        '''
        Takes photos for the registration of a new owner.

        Parameters
        -----------
            - name: string, name of the new owner.
        '''
        self.owner = name
        folder = OWNERS_PATH + '/' + self.owner
        print(folder)
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        camera = PiCamera()
        camera.rotation = 180
        camera.start_preview()
        sleep(1)
        for i in range(NR_OWNER_PHOTOS):
            camera.capture(folder + '/' + str(i) + '.jpg')
            print(folder + '/' + str(i) + '.jpg')
            sleep(1)
        camera.stop_preview()
        del camera
        
        self.__encode_faces()
        
