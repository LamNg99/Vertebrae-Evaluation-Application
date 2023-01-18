import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Button, Checkbutton, Frame, Label, Scrollbar, filedialog, Text
from tkinter import END, RIGHT, Y, BOTTOM, LEFT, W
import loaddicomfile as ldf
import pydicom
import cv2
from PIL import ImageTk, Image


class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1200x800+0+0")
        self.root.title("Veterbrae Evaluation Software")
        #self.root.config(bg="skyblue")
        self.dir_path = ''

        # Frames
        self.f1 = Frame(self.root)
        self.f1.grid(row=1, column=1, columnspan=2, rowspan=2)

        self.f2 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=550, height=550, bd= 0)
        self.f2.grid(row=4, column=0, padx=20, pady=20)

        self.f3 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=550, height=550, bd= 0)
        self.f3.grid(row=4, column=1, padx=20, pady=20, columnspan=2)

        # Scroll bar
        self.scroll_bar = Scrollbar(self.f1, width=10)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        # Labels
        self.l1 = Label(self.root, text='DICOM info', font=('Arial', 10))
        self.l1.grid(row=0, column=1)

        self.l2 = Label(self.root)
        self.l2.grid(row=4, column=1, padx=20, pady=20, columnspan=2)

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

        # Slider
        self.current_value = tk.IntVar()
        self.s1 = ttk.Scale(self.root, orient='horizontal', length=400, from_=1, to=100, command=self.update_image, variable=self.current_value)
        self.s1.grid(row=5, column=1, columnspan=2)
    
    def get_directory(self):
        file_path = filedialog.askdirectory()
        print(file_path)
        return file_path

    def load_dicom_file(self):
        # Clear any previous info in the textbox
        self.t1.delete(1.0, END)

        # Get directory path 
        self.dir_path = self.get_directory()
        
        # Get patient's info
        self.info = ldf.load_dcm_info(self.dir_path, self.var1.get())
        for item in self.info:
            self.t1.insert(1.0, f'{item[0]:25} : {item[1]} \n')

        # Display slices
        self.display_sclice(self.dir_path+'/1.dcm')

    def display_sclice(self, path):
        dicom_data = pydicom.dcmread(path)
        image = dicom_data.pixel_array

        # Convert the image to a PIL Image
        image = Image.fromarray(image)

        # Resize the image 
        image = image.resize((550, 550), Image.ANTIALIAS)

        # Convert the PIL Image to a PhotoImage
        image = ImageTk.PhotoImage(image)

        self.l2.configure(image=image)
        self.l2.image = image

    def update_image(self, even):
        # file_path = self.get_directory()
        self.display_sclice(self.dir_path + '/' + str(self.current_value.get()) + '.dcm')
        


         
        







if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()