#!/bin/bash

activate_ve() { source /home/pi/.virtualenvs/cv/bin/activate; }

activate_ve
cd ~/Desktop/EmotionCat/The_Emotion_Cat
python3 main.py
