import numpy as np
import argparse
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from resources.global_variables import TRAIN_DIR, VAL_DIR
from resources.global_variables import NUM_TRAIN, NUM_VAL
from resources.global_variables import MODEL_WEIGHS_PATH
from resources.global_variables import BATCH_SIZE, PLOT_TITLE
from brain.utils.model import create_model
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Trainer:
    '''
    Class that trains a new model to detect emotions. 
    '''
    
    def __init__(self):  
        '''
        Constructor.
        '''
        self.model = create_model()
                  
        train_datagen = ImageDataGenerator(rescale=1./255)
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        self.train_generator = train_datagen.flow_from_directory(
                TRAIN_DIR,
                target_size=(48,48),
                batch_size=BATCH_SIZE,
                color_mode="grayscale",
                class_mode='categorical')

        self.validation_generator = val_datagen.flow_from_directory(
                VAL_DIR,
                target_size=(48,48),
                batch_size=BATCH_SIZE,
                color_mode="grayscale",
                class_mode='categorical')

    def __plot_model_history(self):
        '''
        Function that plots accuracy and loss curves given 
        the trained model.
        '''
        fig, axs = plt.subplots(1,2,figsize=(15,5))

        axs[0].plot(range(1,len(self.model_info.history['accuracy'])+1),
                                self.model_info.history['accuracy'])
        axs[0].plot(range(1,len(self.model_info.history['val_accuracy'])+1),
                                self.model_info.history['val_accuracy'])
        axs[0].set_title(PLOT_TITLE)
        axs[0].set_ylabel('Accuracy')
        axs[0].set_xlabel('Epoch')
        axs[0].set_xticks(np.arange(1,len(self.model_info.history['accuracy'])+1),
                                    len(self.model_info.history['accuracy'])/10)
        axs[0].legend(['train', 'val'], loc='best')

        axs[1].plot(range(1,len(self.model_info.history['loss'])+1),
                                self.model_info.history['loss'])
        axs[1].plot(range(1,len(self.model_info.history['val_loss'])+1),
                                self.model_info.history['val_loss'])
        axs[1].set_title('Model Loss')
        axs[1].set_ylabel('Loss')
        axs[1].set_xlabel('Epoch')
        axs[1].set_xticks(np.arange(1,len(self.model_info.history['loss'])+1),
                                    len(self.model_info.history['loss'])/10)
        axs[1].legend(['train', 'val'], loc='best')

        plt.show()

    def train(self, _epochs = 10, _lr = 0.001, _decay=1e-6):
        '''
        Function that trains a new model, plots the progress 
        and saves the resulted weights.
        
        Parameters
        -----------
                - _epochs: integer, number of epochs
                - _lr: float, learning rate
                - _decay: float, float
        '''
        print("Starting training...")
        self.model.compile(                                       
                loss='categorical_crossentropy',
                optimizer=Adam(lr=_lr, decay=_decay),
                metrics=['accuracy'])
        self.model_info = self.model.fit_generator(
                self.train_generator,
                steps_per_epoch=NUM_TRAIN // BATCH_SIZE,
                epochs=_epochs,
                validation_data=self.validation_generator,
                validation_steps=NUM_VAL // BATCH_SIZE)
        self.__plot_model_history()
        self.model.save_weights(MODEL_WEIGHS_PATH)
