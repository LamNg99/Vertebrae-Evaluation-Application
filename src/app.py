import tkinter as tk
from tkinter import Button, Checkbutton, Frame, Label, Scrollbar, filedialog, Text
from tkinter import END, RIGHT, Y, BOTTOM, LEFT, W
import loaddicomfile as ldf
import pydicom
import cv2
from PIL import ImageTk, Image


class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1000x800+0+0")
        self.root.title("Veterbrae Evaluation Software")
        #self.root.config(bg="skyblue")

        # Frames
        self.f1 = Frame(self.root)
        self.f1.grid(row=1, column=1, columnspan=2, rowspan=2)

        self.f2 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.f2.grid(row=4, column=0, padx=20, pady=20)

        self.f3 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.f3.grid(row=4, column=1, padx=20, pady=20, columnspan=2)

        # Scroll bar
        self.scroll_bar = Scrollbar(self.f1, width=10)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        # Labels
        self.l1 = Label(text='DICOM info', font=('Arial', 10))
        self.l1.grid(row=0, column=1)

        # Checkboxes
        self.var1 = tk.BooleanVar()
        self.c1 = Checkbutton(text='Protected Display', font=('Arial',10), variable=self.var1, onvalue='True', offvalue='False')
        self.c1.grid(row=0, column=2)

        # Text Boxes
        self.t1 = Text(self.f1, height=5, width=50, yscrollcommand=self.scroll_bar.set, wrap='none')
        self.t1.pack()
        self.scroll_bar.config(command=self.t1.yview)

        # Buttons
        self.b1 = Button(text='Load DICOM File', command=self.load_dicom_file, width=50)
        self.b1.grid(row=1, column=0, pady = 2)

        self.b2 = Button(text='3D View', width=50)
        self.b2.grid(row=2, column=0, pady = 2)

        self.b3 = Button(text='Segmentation', width=50)
        self.b3.grid(row=3, column=0, pady = 2)

    def load_dicom_file(self):
        # Clear any previous info in the textbox
        self.t1.delete(1.0, END)

        # Get directory path 
        file_path = filedialog.askdirectory()
        print(file_path)
        
        # Get patient's info
        self.info = ldf.load_dcm_info(file_path, self.var1.get())
        for item in self.info:
            self.t1.insert(1.0, f'{item[0]:25} : {item[1]} \n')

        # Display slices
        # self.display_sclice(file_path+'/1.dcm')
        print(file_path+'/1.dcm')

    def display_sclice(self, path):
        dicom_data = pydicom.dcmread(path)
        image = dicom_data.pixel_array

        # Convert the image to a PIL Image
        pil_image = Image.fromarray(image)

        # Convert the PIL Image to a PhotoImage
        tk_image = ImageTk.PhotoImage(pil_image)

        label = Label(self.f3, image=tk_image)
        label.pack()


         
        







if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()