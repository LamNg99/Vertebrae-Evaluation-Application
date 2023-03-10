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
from splash import SplashScreen
from view3d import View3D
from viewsegmentation import ViewSegmentation


class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1100x800+0+0")
        self.root.title("VertScan")
        self.root.resizable(False, False)
        self.photo = PhotoImage(file = '../icon/bone.png')
        self.root.iconphoto(False, self.photo)
        #self.root.config(bg="skyblue")

        self.dir_path = None
        self.image = None
        self.window = None
        self.plane = None
        self.dicom_slices = None
        self.hu_slices = None

        # Frames
        self.f1 = Frame(self.root)
        self.f1.grid(row=1, column=1, columnspan=2, rowspan=2)

        self.f2 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=500, height=500, bd= 0)
        self.f2.grid(row=5, column=0, padx=20, pady=20)

        self.f3 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=500, height=500, bd= 0)
        self.f3.grid(row=5, column=1, padx=20, pady=20, columnspan=2)

        # Scroll bar
        self.scroll_bar = Scrollbar(self.f1, width=10)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        # Labels
        self.l1 = Label(self.root, text='DICOM info', font=('Arial', 10))
        self.l1.grid(row=0, column=1)

        # Checkboxes
        self.var1 = tk.BooleanVar()
        self.cb1 = Checkbutton(self.root, text='Protected Display', font=('Arial',10), variable=self.var1, onvalue='True', offvalue='False')
        self.cb1.grid(row=0, column=2, pady=2)

        # Text Boxes
        self.tb1 = Text(self.f1, height=5, width=50, yscrollcommand=self.scroll_bar.set, wrap='none')
        self.tb1.pack(fill='both')
        self.scroll_bar.config(command=self.tb1.yview)

        # Buttons
        self.b1 = Button(self.root, text='Load DICOM File', command=self.load_dicom_file, width=50)
        self.b1.grid(row=1, column=0, pady = 2)

        self.b2 = Button(self.root, text='3D View', width=50, command= lambda: self.view_3d(View3D, self.hu_slices, self.dicom_slices))
        self.b2.grid(row=2, column=0, pady = 2)

        self.b3 = Button(self.root, text='Segmentation', width=50, command= lambda: self.view_segmentation(ViewSegmentation, self.hu_slices, self.dicom_slices))
        self.b3.grid(row=3, column=0, pady = 2)

        # Combo boxes
        self.plane_options = [
            'Saggital',
            'Axial',
            'Coronal'
        ]
        self.cbb1 = ttk.Combobox(self.root, value=self.plane_options)
        self.option = self.cbb1.current(0)
        self.cbb1.bind('<<ComboboxSelected>>', self.plane_image)
        self.cbb1.grid(row=4, column=0, pady = 20)

        self.window_options = [
            'Original',
            'Soft Tissue',
            'Bone',
            'Mediastinum'
        ]
        self.cbb2 = ttk.Combobox(self.root, value=self.window_options)
        self.option = self.cbb2.current(0)
        self.cbb2.bind('<<ComboboxSelected>>', self.window_image)
        self.cbb2.grid(row=4, column=1, pady = 20)

    def get_directory(self):
        file_path = tk.filedialog.askdirectory()
        return file_path

    def get_dicom_image(self, index):
        dicom_data = self.dicom_slices[index]
        self.image = utils.transform_to_hu(dicom_data)
        return self.image

    def load_dicom_file(self):
        # Clear any previous info in the textbox
        self.tb1.delete(1.0, END)

        # Get directory path 
        self.dir_path = self.get_directory()
        if self.dir_path == None or self.dir_path == '':
            tk.messagebox.showwarning('Error', 'No folder selected.')
            return None
        else:
            for file in os.listdir(self.dir_path):
                if not file.endswith('.dcm'):
                    tk.messagebox.showwarning('Error', 'Please select a folder that contains all \'.dcm\' files.')
                    return None
        
        # Get patient's info
        self.info = utils.load_dcm_info(self.dir_path, self.var1.get())
        for item in self.info:
            self.tb1.insert(1.0, f'{item[0]:25} : {item[1]} \n')

        # Load all the slices
        self.dicom_slices = utils.load_slices(self.dir_path)

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

        # Transform all slices to HU
        self.hu_slices = utils.transform_all_to_hu(self.dicom_slices)

        # Get DICOM image
        self.get_dicom_image(0)

        # Display axial plane
        self.display_plane()

        # Display first slice
        self.display_sclice()

        # Slider
        self.current_value = tk.IntVar()
        self.s1 = ttk.Scale(self.root, orient='horizontal', length=400, from_=0, to=len(self.dicom_slices)-1, command=self.update_image, variable=self.current_value)
        self.s1.grid(row=6, column=1, columnspan=2)

    def display_sclice(self):
        slice = self.image
        if self.window ==  'Original':
            slice = self.image
        elif self.window == 'Soft Tissue':
            slice = utils.apply_window(self.image, 40, 80)
        elif self.window == 'Bone':
            slice = utils.apply_window(self.image, 400, 1000)
        elif self.window == 'Mediastinum':
            slice = utils.apply_window(self.image, 50, 350)

        # Create a figure of specific size
        figure = Figure(figsize=(5,5), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(slice, cmap='gray')
        plot.axis('off')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=5, column=1, padx=20, pady=20, columnspan=2)

    def display_plane(self):
        ds = self.dicom_slices
        pixel_spacing = ds[0].PixelSpacing
        slice_thickness = ds[0].SliceThickness
        axial_aspect = pixel_spacing[1] / pixel_spacing[0]
        saggital_aspect = pixel_spacing[1] / slice_thickness
        coronal_aspect = slice_thickness / pixel_spacing[0]
        img_shape = list(ds[0].pixel_array.shape)
        img_shape.append(len(ds))
        img3d = np.zeros(img_shape)

        for i, s in enumerate(ds):
            img2d = s.pixel_array
            img3d[:, :, i] = img2d
        
        # Create a figure of specific size
        figure = Figure(figsize=(5,5), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(img3d[:, img_shape[1]//2, :], cmap='gray')
        plot.set_aspect(saggital_aspect)
        plot.axis('off')

        plot.figure.savefig('saggital.png')

        if self.plane == 'Axial':
            plot.imshow(img3d[:, :, img_shape[2]//2], cmap='gray')
            plot.set_aspect(axial_aspect)
            plot.axis('off')
        elif self.plane == 'Saggital':
            plot.imshow(img3d[:, img_shape[1]//2, :], cmap='gray')
            plot.set_aspect(saggital_aspect)
            plot.axis('off')
        elif self.plane == 'Coronal':
            plot.imshow(img3d[img_shape[0]//2, :, :].T, cmap='gray')
            plot.set_aspect(coronal_aspect)
            plot.axis('off')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=5, column=0, padx=20, pady=20)

    def update_image(self, event):
        self.image = self.get_dicom_image(self.current_value.get())
        self.display_sclice()

    def window_image(self, event):
        self.window = self.cbb2.get()
        self.display_sclice()

    def plane_image(self, event):
        self.plane = self.cbb1.get()
        self.display_plane()

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
    root.withdraw()
    win = tk.Toplevel()
    splash = SplashScreen(win)
    root.deiconify()
    win.destroy()
    app = MainApp(root)
    root.mainloop()