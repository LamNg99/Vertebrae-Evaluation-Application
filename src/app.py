import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import utils as utils
import pydicom
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np
import csv
from PIL import Image, ImageTk
from splash import SplashScreen
from view3d import View3D
from viewsegmentation import ViewSegmentation


class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1100x600+0+0")
        self.root.title("Veterbrae Evaluation Software")
        self.root.resizable(False, False)
        self.photo = PhotoImage(file = '../icon/bone.png')
        self.root.iconphoto(False, self.photo)
        #self.root.config(bg="skyblue")

        self.dir_path = None
        self.image = None
        self.dicom_slices = None
        self.hu_slices = None

        # Frames
        self.f1 = Frame(self.root)
        self.f1.grid(row=1, column=5, columnspan=4, rowspan=2)

        # Sliders
        self.x = IntVar()
        self.y = IntVar()
        self.z = IntVar()

        self.v1 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, variable=self.x, command=self.update_x)
        self.v1.grid(row=5, column=0)

        self.h1 = ttk.Scale(self.root, orient='horizontal', length=400, from_=0, to=400, variable=self.y, command=self.update_y)
        self.h1.grid(row=4, column=1, columnspan=2)

        self.v2 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, variable=self.z, command=self.update_z)
        self.v2.grid(row=5, column=3)

        self.h2 = ttk.Scale(self.root, orient='horizontal', length=300, from_=0, to=400, variable=self.x, command=self.update_x)
        self.h2.grid(row=4, column=4, columnspan=2)

        self.v3 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, variable=self.z, command=self.update_z)
        self.v3.grid(row=5, column=6)

        self.h3 = ttk.Scale(self.root, orient='horizontal', length=300, from_=0, to=400, variable=self.y, command=self.update_y)
        self.h3.grid(row=4, column=7, columnspan=2)

        # Scroll bar
        self.scroll_bar = Scrollbar(self.f1, width=10)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        # Labels
        self.l1 = Label(self.root, text='DICOM info', font=('Arial', 10))
        self.l1.grid(row=0, column=5)

        self.l2  = Label(self.root, text='Axial')
        self.l2.grid(row=6, column=1, columnspan=2)

        self.l3  = Label(self.root, text='Saggital')
        self.l3.grid(row=6, column=4, columnspan=2)

        self.l4  = Label(self.root, text='Coronal')
        self.l4.grid(row=6, column=7, columnspan=2)

        # Checkboxes
        self.var1 = tk.BooleanVar()
        self.cb1 = Checkbutton(self.root, text='Protected Display', font=('Arial',10), variable=self.var1, onvalue='True', offvalue='False')
        self.cb1.grid(row=0, column=8, pady=2)

        # Text Boxes
        self.tb1 = Text(self.f1, height=5, yscrollcommand=self.scroll_bar.set, wrap='none', state='disabled')
        self.tb1.pack(fill='both')
        self.scroll_bar.config(command=self.tb1.yview)

        # Buttons
        self.b1 = Button(self.root, text='Load DICOM File', width=40, command=self.load_dicom_file)
        self.b1.grid(row=1, column=1, pady = 2, columnspan=4)

        self.b2 = Button(self.root, text='3D View', width=40, command= lambda: self.view_3d(View3D, self.hu_slices, self.dicom_slices))
        self.b2.grid(row=2, column=1, pady = 2, columnspan=4)

        self.b3 = Button(self.root, text='Segmentation', width=40, command= lambda: self.view_segmentation(ViewSegmentation, self.hu_slices, self.dicom_slices))
        self.b3.grid(row=3, column=1, pady = 2, columnspan=4)

        # Canvas
        self.cv1 = Canvas(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.cv1.grid(row=5, column=1, columnspan=2)

        self.cv2 = Canvas(self.root, highlightbackground='black', highlightthickness=1, width=300, height=400, bd= 0)
        self.cv2.grid(row=5, column=4, columnspan=2)

        self.cv3 = Canvas(self.root, highlightbackground='black', highlightthickness=1, width=300, height=400, bd= 0)
        self.cv3.grid(row=5, column=7, columnspan=2)

    def get_directory(self):
        file_path = tk.filedialog.askdirectory()
        return file_path

    def load_dicom_file(self):
        # Clear any previous info in the textbox
        self.tb1.delete(1.0, END)

        # Get directory path 
        self.dir_path = self.get_directory()
        if self.dir_path == None or self.dir_path == '':
            tk.messagebox.showinfo('Info', 'No folder selected.')
            return None
        else:
            for file in os.listdir(self.dir_path):
                if not file.endswith('.dcm'):
                    tk.messagebox.showinfo('Info', 'Please select a folder that contains all \'.dcm\' files.')
                    return None
        
        # Get patient's info
        self.info = utils.load_dcm_info(self.dir_path, self.var1.get())
        self.tb1.config(state='normal')
        for item in self.info:
            self.tb1.insert(1.0, f'{item[0]:25} : {item[1]} \n')
        self.tb1.config(state='disable')

        # Load all the slices
        self.dicom_slices = utils.load_slices(self.dir_path)

        # Transform all slices to HU
        self.hu_slices = utils.transform_all_to_hu(self.dicom_slices)

        # Change path to temporary folder
        base = os.path.basename(self.dir_path)
        path = os.path.dirname(self.dir_path) + '/temp_' + base
        if not os.path.exists(path):
            os.makedirs(path)
        
        os.chdir(path)

        # Create csv file 
        field = ['Vertebral Label', 'Axial Area', 'Vertebral Height', 'Volume', 'Estimated BMC', 'aBMD', 'vBMD', 'Elastic Modulus']
        if not os.path.exists('result.csv'):
            with open('result.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(field)

        self.display_plane()

        cur_x = self.dicom_slices[0].pixel_array.shape[0]//2
        cur_y = self.dicom_slices[0].pixel_array.shape[1]//2
        cur_z = len(self.dicom_slices)//2

        # Update sliders
        self.v1.config(from_=0, to=self.dicom_slices[0].pixel_array.shape[0]-1)
        self.v1.set(cur_x)

        self.h1.config(from_=0, to=self.dicom_slices[0].pixel_array.shape[1]-1)
        self.h1.set(cur_y)

        self.v2.config(from_=0, to=len(self.dicom_slices)-1)
        self.v2.set(cur_z)

        self.h2.config(from_=0, to=self.dicom_slices[0].pixel_array.shape[0]-1)
        self.h2.set(cur_x)

        self.v3.config(from_=0, to=len(self.dicom_slices)-1)
        self.v3.set(cur_z)

        self.h3.config(from_=0, to=self.dicom_slices[0].pixel_array.shape[1]-1)
        self.h3.set(cur_y)

        # Get imagees
        self.plot_axial(z=cur_z)
        self.plot_coronal(x=cur_x)
        self.plot_saggital(y=cur_y)

        self.display_axial()
        self.display_saggital()
        self.display_coronal()

    def display_plane(self):
        ds = self.dicom_slices
        pixel_spacing = ds[0].PixelSpacing
        slice_thickness = ds[0].SliceThickness
        self.axial_aspect = pixel_spacing[1] / pixel_spacing[0]
        self.saggital_aspect = pixel_spacing[1] / slice_thickness
        self.coronal_aspect = slice_thickness / pixel_spacing[0]
        img_shape = list(ds[0].pixel_array.shape)
        img_shape.append(len(ds))
        self.img3d = np.zeros(img_shape)

        for i, s in enumerate(ds):
            self.img3d[:, :, i] = s.pixel_array

        # Create a figure of specific size
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.img3d[:, img_shape[1]//2, :], cmap='gray')
        plot.set_aspect(self.saggital_aspect)
        plot.axis('off')
        plot.figure.savefig('saggital_mid.png', transparent=True)

    def plot_axial(self, z):
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.img3d[:, :, len(self.dicom_slices)-z-1], cmap='gray')
        # plot.set_aspect(self.axial_aspect)
        plot.axis('off')
        plot.figure.savefig('axial.png', transparent=True)

    def plot_saggital(self, y):
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.img3d[:, y, :], cmap='gray')
        # plot.set_aspect(self.saggital_aspect)
        plot.axis('off')
        plot.figure.savefig('saggital.png', transparent=True)

    def plot_coronal(self, x):       
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.img3d[x, :, :].T, cmap='gray')
        # plot.set_aspect(self.coronal_aspect)
        plot.axis('off')
        plot.figure.savefig('coronal.png', transparent=True)

    def display_axial(self):
        self.axial = ImageTk.PhotoImage(Image.open('axial.png').resize((400,400)))
        self.cv1.create_image(0, 0, anchor=NW, image=self.axial)
        cur_x = self.x.get()
        cur_y = self.y.get()
        cur_v1 = cur_x*400/self.dicom_slices[0].pixel_array.shape[0]
        cur_h1 = cur_y*400/self.dicom_slices[0].pixel_array.shape[1]
        self.cv1.delete('v1')
        self.cv1.delete('h1')
        self.cv1.create_line(0, cur_v1, 400, cur_v1, tag='v1', fill='red')
        self.cv1.create_line(cur_h1, 0, cur_h1, 400, tag='h1', fill='red')

    def display_saggital(self):
        self.saggital = ImageTk.PhotoImage(Image.open('saggital.png').rotate(90).resize((300,400)))
        self.cv2.create_image(0, 0, anchor=NW, image=self.saggital)
        cur_z = self.z.get()
        cur_x = self.x.get()
        cur_v2 = cur_z*400/len(self.dicom_slices)
        cur_h2 = cur_x*300/self.dicom_slices[0].pixel_array.shape[0]
        self.cv2.delete('v2')
        self.cv2.delete('h2')
        self.cv2.create_line(0, cur_v2, 300, cur_v2, tag='v2', fill='red')
        self.cv2.create_line(cur_h2, 0, cur_h2, 400, tag='h2', fill='red')

    def display_coronal(self):
        self.coronal = ImageTk.PhotoImage(Image.open('coronal.png').rotate(180).resize((300,400)))
        self.cv3.create_image(0, 0, anchor=NW, image=self.coronal)
        cur_z = self.z.get()
        cur_y = self.y.get()
        cur_v3 = cur_z*400/len(self.dicom_slices)
        cur_h3 = cur_y*300/self.dicom_slices[0].pixel_array.shape[1]
        self.cv3.delete('v3')
        self.cv3.delete('h3')
        self.cv3.create_line(0, cur_v3, 300, cur_v3, tag='v3', fill='red')
        self.cv3.create_line(cur_h3, 0, cur_h3, 400, tag='h3', fill='red')

    def update_x(self, event):
        cur_x = self.x.get()
        cur_v1 = cur_x*400/self.dicom_slices[0].pixel_array.shape[0]
        cur_h2 = cur_x*300/self.dicom_slices[0].pixel_array.shape[0]
        self.cv1.delete('v1')
        self.cv2.delete('h2')
        self.cv1.create_line(0, cur_v1, 400, cur_v1, tag='v1', fill='red')
        self.cv2.create_line(cur_h2, 0, cur_h2, 400, tag='h2', fill='red')
        self.plot_coronal(x=cur_x)
        self.display_coronal()

    def update_y(self, event):
        cur_y = self.y.get()
        cur_h1 = cur_y*400/self.dicom_slices[0].pixel_array.shape[1]
        cur_h3 = cur_y*300/self.dicom_slices[0].pixel_array.shape[1]
        self.cv1.delete('h1')
        self.cv3.delete('h3')
        self.cv1.create_line(cur_h1, 0, cur_h1, 400, tag='h1', fill='red')
        self.cv3.create_line(cur_h3, 0, cur_h3, 400, tag='h3', fill='red')
        self.plot_saggital(y=cur_y)
        self.display_saggital()

    def update_z(self, event):
        cur_z = self.z.get()
        cur_v2 = cur_z*400/len(self.dicom_slices)
        cur_v3 = cur_z*400/len(self.dicom_slices)
        self.cv2.delete('v2')
        self.cv3.delete('v3')
        self.cv2.create_line(0, cur_v2, 300, cur_v2, tag='v2', fill='red')
        self.cv3.create_line(0, cur_v3, 300, cur_v3, tag='v3', fill='red')
        self.plot_axial(z=cur_z)
        self.display_axial()

    def view_3d(self, _class, image, scan):
        if self.dir_path == None or self.dir_path == '':
            tk.messagebox.showinfo('Info', 'Please load the DICOM files first.')
        else:
            try:
                if self.new.state() == "normal":
                    self.new.focus()
            except:
                self.new = tk.Toplevel(self.root)
                _class(self.new, image, scan)

    def view_segmentation(self, _class, hu_slices, dicom_slices):
        if self.dir_path == None or self.dir_path == '':
            tk.messagebox.showinfo('Info', 'Please load the DICOM files first.')
        else:
            try:
                if self.new.state() == "normal":
                    self.new.focus()
            except:
                self.new = tk.Toplevel(self.root)
                _class(self.new, hu_slices, dicom_slices)

        

if __name__ == '__main__':
    root = tk.Tk()
    # root.withdraw()
    # win = tk.Toplevel()
    # splash = SplashScreen(win)
    # root.deiconify()
    # win.destroy()
    app = MainApp(root)
    root.mainloop()