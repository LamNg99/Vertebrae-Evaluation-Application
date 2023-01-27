import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Button, Checkbutton, Frame, Label, Scrollbar, filedialog, Text
from tkinter import END, RIGHT, Y, BOTTOM, LEFT, W
import utils as utils
import pydicom
import cv2
from PIL import ImageTk, Image
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1200x800+0+0")
        self.root.title("Veterbrae Evaluation Software")
        #self.root.config(bg="skyblue")

        self.dir_path = None
        self.image = None

        # Frames
        self.f1 = Frame(self.root)
        self.f1.grid(row=1, column=1, columnspan=2, rowspan=2)

        self.f2 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=500, height=500, bd= 0)
        self.f2.grid(row=4, column=0, padx=20, pady=20)

        self.f3 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=500, height=500, bd= 0)
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
        self.cb1 = Checkbutton(text='Protected Display', font=('Arial',10), variable=self.var1, onvalue='True', offvalue='False')
        self.cb1.grid(row=0, column=2, pady=2)

        # Text Boxes
        self.tb1 = Text(self.f1, height=5, width=50, yscrollcommand=self.scroll_bar.set, wrap='none')
        self.tb1.pack()
        self.scroll_bar.config(command=self.tb1.yview)

        # Buttons
        self.b1 = Button(text='Load DICOM File', command=self.load_dicom_file, width=50)
        self.b1.grid(row=1, column=0, pady = 2)

        self.b2 = Button(text='3D View', width=50)
        self.b2.grid(row=2, column=0, pady = 2)

        self.b3 = Button(text='Segmentation', width=50)
        self.b3.grid(row=3, column=0, pady = 2)

        # Combo boxes
        self.window_options = [
            'Original',
            'Soft Tissue',
            'Bone',
            'Mediastinum'
        ]
        self.cbb1 = ttk.Combobox(self.root, value=self.window_options)
        self.option = self.cbb1.current(0)
        self.cbb1.bind('<<ComboboxSelected>>', self.window_image)
        self.cbb1.grid(row=3, column=1)

    def get_directory(self):
        file_path = filedialog.askdirectory()
        return file_path

    def get_dicom_image(self, path):
        dicom_data = pydicom.dcmread(path)
        self.image = utils.transform_to_hu(dicom_data)
        return self.image

    def load_dicom_file(self):
        # Clear any previous info in the textbox
        self.tb1.delete(1.0, END)

        # Get directory path 
        self.dir_path = self.get_directory()
        
        # Get patient's info
        self.info = utils.load_dcm_info(self.dir_path, self.var1.get())
        for item in self.info:
            self.tb1.insert(1.0, f'{item[0]:25} : {item[1]} \n')

        # Get DICOM image
        self.get_dicom_image(self.dir_path+'/1.dcm')

        # Display first slice
        self.display_sclice()

        count = 0
        # Iterate directory
        for path in os.listdir(self.dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(self.dir_path, path)):
                count += 1

        # Slider
        self.current_value = tk.IntVar()
        self.s1 = ttk.Scale(self.root, orient='horizontal', length=400, from_=1, to=count, command=self.update_image, variable=self.current_value)
        self.s1.grid(row=5, column=1, columnspan=2)

    def display_sclice(self):
        slice = self.image
        if self.option ==  'Original':
            slice = self.image
        elif self.option == 'Soft Tissue':
            slice = utils.apply_window(self.image, 40, 80)
        elif self.option == 'Bone':
            slice = utils.apply_window(self.image, 400, 1000)
        elif self.option == 'Mediastinum':
            slice = utils.apply_window(self.image, 50, 350)

        # Create a figure of specific size
        figure = Figure(figsize=(5,5), dpi=100)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(slice, cmap='gray')
        plot.axis('off')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=4, column=1, padx=20, pady=20, columnspan=2)

    def update_image(self, event):
        self.image = self.get_dicom_image(self.dir_path + '/' + str(self.current_value.get()) + '.dcm')
        self.display_sclice()

    def window_image(self, event):
        self.option = self.cbb1.get()
        self.display_sclice()
        


         
        







if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()