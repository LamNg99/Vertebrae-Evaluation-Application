#importing library
from tkinter import *
from PIL import ImageTk, Image 
import time

class SplashScreen:
    def __init__(self, win):
        self.win = win 
        self.win.overrideredirect(True) 
        self.width_of_window = 427
        self.height_of_window = 250
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.pos_x = (self.screen_width//2)-(self.width_of_window//2)
        self.pos_y = (self.screen_height//2)-(self.height_of_window//2)
        self.win.geometry(f'{self.width_of_window}x{self.height_of_window}+{self.pos_x}+{self.pos_y}')
        self.icon = PhotoImage(file = '../icon/bone.png')
        self.win.iconphoto(False, self.icon)
        #w.configure(bg='#ED1B76')

        self.photo = ImageTk.PhotoImage(Image.open('../icon/bone.png'))

        Frame(self.win, width=427, height=250).place(x=0,y=0)
        self.label1=Label(self.win, text='VertScan')
        self.label1.configure(font=("Calibri", 24))
        self.label1.place(x=160, y=90)

        self.label2 = Label(self.win, image=self.photo)
        self.label2.place(x=80, y=90)

        self.label3=Label(self.win, text='Loading...')
        self.label3.configure(font=("Calibri", 11))
        self.label3.place(x=10,y=215)

        #making animation

        image_a=ImageTk.PhotoImage(Image.open('../icon/d2.png'))
        image_b=ImageTk.PhotoImage(Image.open('../icon/d1.png'))

        for i in range(3):
            l1=Label(self.win, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            self.win.update()
            time.sleep(0.3)

            l1=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.win, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            self.win.update()
            time.sleep(0.3)

            l1=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.win, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            self.win.update()
            time.sleep(0.3)

            l1=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.win, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.win, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
            self.win.update()
            time.sleep(0.3)
