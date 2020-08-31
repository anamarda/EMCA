#!/usr/bin/env python3
from limb_control.DecisionMaker import DecisionMaker
from limb_control.Mover import Mover
from persistence.FileRepository import FileRepository
from limb_control.ControllerLimb import ControllerLimb
from validator.AngleValidator import AngleValidator
from utils.Bus import Bus
from brain.Brain import Brain
from Application import Application
from resources.global_variables import *
from signal import signal, SIGPIPE, SIG_DFL
import socket
import time

signal(SIGPIPE, SIG_DFL)

b = Bus()
bus = b.get_bus()
repo = FileRepository()
val = AngleValidator()
ctr = ControllerLimb(repo, bus, val)
mover = Mover(ctr)
decision_maker = DecisionMaker(mover)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    emotion = data.decode("utf-8")
                    '''
                    if not data:
                        break
                       ''' 
                    print(emotion)
                    decision_maker.mirror_emotion(emotion)            
                    conn.sendall(data)
                    time.sleep(2)
except Exception as e:
    print("======== [ERR]" + str(e))
finally:
    decision_maker.mirror_emotion("Neutral")
