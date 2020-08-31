import tkinter as tk
from tkinter import ttk, CENTER
from PIL import ImageTk, Image
from validation.GuiValidator import GuiException
import os
import sys

class GUI:
    '''
    Graphic Interface User class.
    '''    
        
    def __init__(self, _controller):
        '''
        Contructor.
        
        Parameters
        -----------
                _controller: Controller
        '''
        self.controller = _controller

        margin_clr = "gray10"
            
        self.root = tk.Tk()
        self.root.configure(bg=margin_clr, pady=10)
        self.root.title("EMCA")
        self.root.columnconfigure(2, weight=1)

        self.f1 = tk.Frame(self.root, 
                bg=margin_clr, 
                pady=20)
        self.f2 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
        self.f3 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
        self.f4 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
                
        self.f5 = tk.Frame(self.root, 
                bg="gray25", 
                pady=20, 
                highlightbackground=margin_clr, 
                highlightthickness=5)
        
        self.f1.grid(row=1, column=1)
        self.f2.grid(row=2, column=1)
        self.f3.grid(row=3, column=1)
        self.f4.grid(row=4, column=1)
        self.f5.grid(row=5, column=1)
        
        self.title_label = tk.Label(self.f1, 
                text="THE EMOTION CAT", 
                bg=margin_clr,
                fg='white',
                font='Helvetica 18 bold',
                )
        self.title_label.pack(side="top") 
        
        self.name_label = tk.Label(self.f2, 
                text="Owner:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.name_label.grid(row=1, column=0)
        
        self.combo = ttk.Combobox(self.f2, values=self.controller.get_owners())
        self.combo.grid(row=1, column=1, padx=1, pady=20)
        self.combo.bind("<<ComboboxSelected>>", self.__selectCombo)
        
        self.confirm_btn = tk.Button(self.f2, 
                text="CONFIRM", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__confirmButton) 
        self.confirm_btn.grid(row=2, column=0, columnspan=2, padx=150, pady=10)
        
        self.confirm_label = tk.Label(self.f2,
                text = " ",
                fg='red', 
                bg='gray25')
        self.confirm_label.grid(row=3, column=0, columnspan=2, padx=150, pady=10)
        
        self.new_name_label = tk.Label(self.f3, 
                text="New owner:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.new_name_label.grid(row=0, column=0)
        
        self.new_name = tk.Entry(self.f3)
        self.new_name.grid(row=0, column=1)
        
        self.register_btn = tk.Button(self.f3, 
                text="REGISTER", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__registerButton) 
        self.register_btn.grid(row=1, column=0, columnspan=2, padx=150, pady=10)
        
        self.register_label = tk.Label(self.f3,
                text = " ",
                fg='red', 
                bg='gray25')
        self.register_label.grid(row=4, column=0, columnspan=2, padx=150, pady=10)
        
        self.epochs_label = tk.Label(self.f4, 
                text="Epochs:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.epochs_label.grid(row=0, column=0)
        
        self.epochs = tk.Entry(self.f4)
        self.epochs.grid(row=0, column=1)
        
        self.lr_label = tk.Label(self.f4, 
                text="Learning rate:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.lr_label.grid(row=2, column=0)
        
        self.lr = tk.Entry(self.f4)
        self.lr.grid(row=2, column=1)
        
        self.decay_label = tk.Label(self.f4, 
                text="Decay:", 
                bg='gray25',
                fg='white',
                font=20,
                )
        self.decay_label.grid(row=1, column=0)
        
        self.decay = tk.Entry(self.f4)
        self.decay.grid(row=1, column=1)
        
        self.train_btn = tk.Button(self.f4, 
                text="TRAIN", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__trainButton) 
        self.train_btn.grid(row=3, column=0, columnspan=2, padx=150, pady=10)
        
        self.train_label = tk.Label(self.f4,
                text = " ",
                fg='red', 
                bg='gray25')
        self.train_label.grid(row=4, column=0, columnspan=2, padx=150, pady=10)
        
        self.quit_btn = tk.Button(self.f5, 
                text="QUIT", 
                width=25, 
                bg = 'medium aquamarine',
                fg='white',
                command=self.__quitButton) 
        self.quit_btn.grid(row=0, column=0, columnspan=2, padx=150, pady=5)

    def __selectCombo(self, event):
        pass
        
    def __confirmButton(self):
        '''
        This function starts the emotion detector, as well as the 
        body movement. 
        '''
        name = self.combo.get()
        
        try:
            self.confirm_label['text'] = " "
            self.controller.start_emotion_prediction(name)
        except GuiException as e:
            print(e.get_message())
            self.confirm_label['text'] = e.get_message()

    def __registerButton(self):
        '''
        This function handles the registration of a new owner.
        '''
        name = self.new_name.get()
        
        try:
            self.register_label['text'] = " "
            self.controller.register_owner(name)
            self.combo['values']=self.controller.get_owners()
        except GuiException as e:
            print(e.get_message())
            self.register_label['text'] = e.get_message()

    def __trainButton(self):
        '''
        This function starts the training process.
        '''
        lr = self.lr.get()
        decay = self.decay.get()
        epochs = self.epochs.get()
        
        try:
            self.train_label['text'] = " "
            self.controller.train(epochs, lr, decay)
        except GuiException as e:
            print(e.get_message())
            self.train_label['text'] = e.get_message()

    def __quitButton(self):
        '''
        This function quit the entire application.
        '''
        sys.exit()

    def show(self):
        '''
        Function that shows the main window.
        '''
        self.root.mainloop()

