from body.services.DecisionMaker import DecisionMaker
from body.services.Mover import Mover
from body.services.ControllerLimb import ControllerLimb
from body.persistence.FileRepository import FileRepository
from utils.Bus import Bus
from brain.Brain import Brain
from brain.train.Trainer import Trainer
from brain.register.Register import Register
from cat.implementation.Cat import Cat
from controller.Controller import Controller
from validation.AngleValidator import AngleValidator
from validation.GuiValidator import GuiValidator
from gui.GUI import GUI

try:
    b = Bus()
    bus = b.get_bus()
    repo = FileRepository()
    angle_val = AngleValidator()
    ctr = ControllerLimb(repo, bus, angle_val)
    mover = Mover(ctr)
    decision_maker = DecisionMaker(mover)
    emotion_detector = Brain()
    trainer = Trainer()
    motivation = Register()
    cat = Cat(decision_maker, emotion_detector, trainer, motivation)
    gui_val = GuiValidator()
    ctr = Controller(gui_val, cat)
    gui = GUI(ctr)
    gui.show()
except Exception as e:
    print(e.get_message())
finally:
    decision_maker.mirror_emotion("Neutral")

