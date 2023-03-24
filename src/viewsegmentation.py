import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import segmentation as seg
import calculation as cal
from popup import PopUp
import os
import cv2
import csv
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk


class ViewSegmentation:
    def __init__(self, root, hu_slices, dicom_slices):
        self.root = root
        self.width_of_window = 1450
        self.height_of_window = 800
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.pos_x = (self.screen_width//2)-(self.width_of_window//2)
        self.pos_y = (self.screen_height//2)-(self.height_of_window//2)
        self.root.geometry(f'{self.width_of_window}x{self.height_of_window}+{self.pos_x}+{self.pos_y}') 
        self.root.title("Segmentation")
        self.root.resizable(False, False)

        self.hu_slices = hu_slices
        self.dicom_slices = dicom_slices
        self.saggital_image = ImageTk.PhotoImage(Image.open('saggital_mid.png').rotate(90).resize((400,400)))
        self.increment= 400/len(self.hu_slices)
        self.index = 0
        self.top_index = 0
        self.bottom_index = 0
        self.current_index = 0
        self.option = None
        self.image = None
        self.position = None
        self.properties = []
        self.label = None 

        # Labels
        self.l1 = Label(self.root, text='HU Threshold', font=('Arial', 15))
        self.l1.grid(row=0, column=2, pady=2)

        self.l2 = Label(self.root, text='Area Threshold', font=('Arial', 15))
        self.l2.grid(row=1, column=2, pady=2)

        self.l3 = Label(self.root, text='Saggital View', font=('Arial',15))
        self.l3.grid(row=7, column=2, columnspan=2, sticky=S)

        self.l4 = Label(self.root, text='Corresponding Slice', font=('Arial',15))
        self.l4.grid(row=7, column=4, columnspan=2, sticky=S)

        self.l5 = Label(self.root, text='Segmentation Result', font=('Arial',15))
        self.l5.grid(row=7, column=6, columnspan=2, sticky=S)

        # Buttons
        self.b1 = Button(self.root, text='Extract Slice', width=40, command=self.extract_slice)
        self.b1.grid(row=2, column=2, pady = 2, columnspan=2)

        self.b2 = Button(self.root, text='Extract Properties', width=40, 
                        command= lambda: self.click_extract_properties(PopUp, self.properties, self.tree))
        self.b2.grid(row=3, column=2, pady = 2, columnspan=2)

        self.b3 = Button(self.root, text='Delete data', width=15, command=self.delete_data)
        self.b3.grid(row=4, column=6, padx=2, pady=2)

        self.b4 = Button(self.root, text='Save data', width=15, command=self.save_data)
        self.b4.grid(row=4, column=7, padx=2, pady=2)

        # Entry widgetValuess
        self.e1 = Entry(self.root, justify=CENTER)
        self.e1.insert(0, '200')
        self.e1.grid(row=0, column=3, pady=2)

        self.e2 = Entry(self.root, justify=CENTER)
        self.e2.insert(0, '200')
        self.e2.grid(row=1, column=3, pady=2)

        # Sliders and Spin Boxes 
        self.val1 = tk.DoubleVar()
        self.spin1 = ttk.Spinbox(self.root, textvariable=self.val1, wrap=True, width=4, from_=0, to=400, increment=self.increment, command=self.update_slider1)
        self.spin1.grid(row=5, column=0)
        self.s1 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, command=self.on_slider1, variable=self.val1)
        self.s1.grid(row=6, column=0)
        

        self.val2 = tk.DoubleVar()
        self.spin2 = ttk.Spinbox(self.root, textvariable=self.val2, wrap=True, width=4, from_=0, to=400, increment=self.increment, command=self.update_slider2)
        self.spin2.grid(row=5, column=1)
        self.s2 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, command=self.on_slider2, variable=self.val2)
        self.s2.grid(row=6, column=1)

        # Frames
        self.f1 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.f1.grid(row=6, column=4, padx=20, pady=20, columnspan=2)

        self.f2 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.f2.grid(row=6, column=6, padx=20, pady=20, columnspan=2)
        
        self.f3 = Frame(self.root)
        self.f3.grid(row=1, column=4, columnspan=4, rowspan=3)

        # Combo boxes
        self.slice_options = [
            'Top Slice',
            'Middle Slice',
            'Bottom Slice'
        ]
        self.cbb1 = ttk.Combobox(self.root, value=self.slice_options)
        self.position = self.cbb1.current(1)
        self.cbb1.bind('<<ComboboxSelected>>', self.choose_slice)
        self.cbb1.grid(row=5, column=4, pady = 20, columnspan=2, sticky=S)

        self.image_options = [
            'Binary Image',
            'Mask',
            'Segmented Image'
        ]
        self.cbb2 = ttk.Combobox(self.root, value=self.image_options)
        self.option = self.cbb2.current(0)
        self.cbb2.bind('<<ComboboxSelected>>', self.display_options)
        self.cbb2.grid(row=5, column=6, pady = 20, columnspan=2, sticky=S)

        # Canvas
        self.canvas = Canvas(self.root, width=400, height=400)
        self.canvas.grid(row=6, column=2, columnspan=2)
        self.canvas.create_image(0, 0, anchor=NW, image=self.saggital_image)
        self.canvas.create_line(0, self.val1.get(), 400, self.val1.get(), tag='top_line', fill='red')
        self.canvas.create_line(0, self.val2.get(), 400, self.val2.get(), tag='bottom_line', fill='red')

        # Tree 
        self.tree = self.create_tree_widget()

    def create_tree_widget(self):
        # Create scrollbars
        y_scroll_bar = Scrollbar(self.f3, width=10)
        y_scroll_bar.pack(side=RIGHT, fill=Y)

        x_scroll_bar = Scrollbar(self.f3, width=10, orient=HORIZONTAL)
        x_scroll_bar.pack(side=BOTTOM, fill=X)

        columns = ('vertebral_label', 'axial_area', 'height', 'volume', 'bmc', 'area_bmd', 'volume_bmd', 'elastic_modulus')
        tree = ttk.Treeview(self.f3, columns=columns, height=5, show='headings', xscrollcommand=x_scroll_bar.set, yscrollcommand=y_scroll_bar.set)
        tree.pack(fill=BOTH, expand=TRUE)
        y_scroll_bar.config(command=tree.yview)
        x_scroll_bar.config(command=tree.xview)

        # Define headings
        tree.heading('vertebral_label', text='Vertebral Label')
        tree.heading('axial_area', text='Axial Area')
        tree.heading('height', text='Vertebral Height')
        tree.heading('volume', text='Volume')
        tree.heading('bmc', text='Estimated BMC')
        tree.heading('area_bmd', text='aBMD')
        tree.heading('volume_bmd', text='vBMD')
        tree.heading('elastic_modulus', text='Elastic Modulus')

        tree.column('vertebral_label', anchor=CENTER, stretch=NO, width=100)
        tree.column('axial_area', anchor=CENTER, stretch=NO, width=100)
        tree.column('height', anchor=CENTER, stretch=NO, width=100)
        tree.column('volume', anchor=CENTER, stretch=NO, width=100)
        tree.column('bmc', anchor=CENTER, stretch=NO, width=100)
        tree.column('area_bmd', anchor=CENTER, stretch=NO, width=100)
        tree.column('volume_bmd', anchor=CENTER, stretch=NO, width=100)
        tree.column('elastic_modulus', anchor=CENTER, stretch=NO, width=100)

        with open('result.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                vertebral_label = row['Vertebral Label']
                axial_area = row['Axial Area']
                height = row['Vertebral Height']
                volume = row['Volume']
                bmc = row['Estimated BMC']
                area_bmd = row['aBMD']
                volume_bmd = row['vBMD']
                elastic_modulus = row['Elastic Modulus']
                tree.insert('', 0, values=[vertebral_label, axial_area, height, volume, bmc, area_bmd, volume_bmd, elastic_modulus])

        return tree

    def on_slider1(self, event):
        self.canvas.delete('top_line')
        self.canvas.create_line(0, self.val1.get(), 400, self.val1.get(), tag='top_line', fill='red')

    def on_slider2(self, event):
        self.canvas.delete('bottom_line')
        self.canvas.create_line(0, self.val2.get(), 400, self.val2.get(), tag='bottom_line', fill='red')

    def update_slider1(self):
        self.s1.set(self.val1.get())

    def update_slider2(self):
        self.s2.set(self.val2.get())

    def extract_slice(self):
        # Get mid slide
        self.position = self.cbb1.get()
        self.get_corresponding_slice()

        # Get binary image
        self.get_binary()

        self.option = self.cbb2.current(0)

        # Segmentation
        seg.get_segmentation(area_theshold=float(self.e2.get()))

        # Extract properties
        self.extract_properties()

    def get_corresponding_slice(self):
        self.index = int((self.val1.get() + self.val2.get())*(len(self.hu_slices)-1)/(400*2))
        if self.val1.get() > self.val2.get():
            self.top_index = int(self.val2.get()*(len(self.hu_slices)-1)/400)
            self.bottom_index = int(self.val1.get()*(len(self.hu_slices)-1)/400)
        else:
            self.top_index = int(self.val1.get()*(len(self.hu_slices)-1)/400)
            self.bottom_index = int(self.val2.get()*(len(self.hu_slices)-1)/400)
        # Create a figure of specific size
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        
        if self.position == 'Top Slice':
            plot.imshow(self.hu_slices[-self.top_index-1], cmap='gray')
            plot.axis('off')
            self.current_index = self.top_index
        elif self.position == 'Middle Slice':
            plot.imshow(self.hu_slices[-self.index-1], cmap='gray')
            plot.axis('off')
            self.current_index = self.index
        elif self.position == 'Bottom Slice':
            plot.imshow(self.hu_slices[-self.bottom_index-1], cmap='gray')
            plot.axis('off')
            self.current_index = self.bottom_index
        
        plot.figure.savefig('original.png')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=6, column=4, padx=20, pady=20, columnspan=2)

    def get_binary(self):
        threshold = float(self.e1.get())
        self.binary_image = self.hu_slices[-self.current_index-1] > threshold

        # Create a figure of specific size
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.binary_image, cmap='gray')
        plot.axis('off')

        plot.figure.savefig('binary.png')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=6, column=6, padx=20, pady=20, columnspan=2)
         
    def choose_slice(self, event):
        self.extract_slice()

    def handle_options(self):
        if self.option == 'Binary Image':
            self.image = ImageTk.PhotoImage(Image.open('binary.png').resize((400,400)))
        elif self.option == 'Mask':
            self.image = ImageTk.PhotoImage(Image.open('mask.png').resize((400,400)))
        elif self.option == 'Segmented Image':
            self.image = ImageTk.PhotoImage(Image.open('segmentedimage.png').resize((400,400)))

        temp_canvas = Canvas(self.root, width=400, height=400)
        temp_canvas.grid(row=6, column=6, columnspan=2)
        temp_canvas.create_image(0, 0, anchor=NW, image=self.image)

    def display_options(self, event):
        self.option = self.cbb2.get()
        self.handle_options()

    def extract_properties(self):
        # DICOM data
        pixel_spacing = self.dicom_slices[0].PixelSpacing
        slice_thickness = self.dicom_slices[0].SliceThickness
        dicom_shape = self.dicom_slices[0].pixel_array.shape
        num_slices = abs(self.val1.get() - self.val2.get())*(len(self.hu_slices)-1)/400
        
        # Get image to extract properties
        image = cv2.imread('segmentedimage.png')
        img_shape = image.shape

        # Get contour area 
        pixel_area = cal.contour_area(image)

        # Get area in cm^2
        area = cal.get_area(pixel_area, img_shape, dicom_shape, pixel_spacing)

        # Get height in cm 
        height = cal.get_height(num_slices, slice_thickness)

        # Get volumns in cm^3
        volume = cal.get_volume(area, height)

        # Get bcm in g 
        bmc = cal.get_bmc(image)

        # Get aBMD in g/cm^2
        aBMD = cal.get_aBMD(bmc, area)

        # Get vBMD in g/cm^3
        vBMD = cal.get_vBMD(bmc, volume)

        # Get Elastic Modulus
        em = cal.get_elastic_modulus(vBMD)

        self.properties = [round(num, 2) for num in [area, height, volume, bmc, aBMD, vBMD, em]]

        return self.properties

    def click_extract_properties(self, _class, properties, tree):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = tk.Toplevel(self.root)
            _class(self.new, properties, tree)

    def delete_data(self):
        selected_item = self.tree.selection()[0]
        self.tree.delete(selected_item)

    def save_data(self):
        field = ['Vertebral Label', 'Axial Area', 'Vertebral Height', 'Volume', 'Estimated BMC', 'aBMD', 'vBMD', 'Elastic Modulus']
        with open('result.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field)
            
            for row_id in self.tree.get_children():
                row = self.tree.item(row_id)['values']
                writer.writerow(row)
        
        tk.messagebox.showinfo('Info', 'Saved!')


    
        
