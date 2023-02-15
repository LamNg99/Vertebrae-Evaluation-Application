import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from turtle import width
import segmentation as seg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from PIL import Image, ImageTk
from RangeSlider.RangeSlider import RangeSliderV

class ViewSegmentation:
    def __init__(self, root, hu_slices):
        self.root = root 
        self.root.geometry("1500x800+0+0")
        self.root.title("Segmentation")
        self.root.resizable(False, False)

        self.hu_slices = hu_slices
        self.saggital_image = ImageTk.PhotoImage(Image.open('saggital.png').rotate(90).resize((400,400)))
        self.increment= 400/len(self.hu_slices)
        self.index = 0
        self.option = None
        self.image = None

        # Labels
        self.l1 = Label(self.root, text='Threshold', font=('Arial', 15))
        self.l1.grid(row=0, column=2, pady=2)

        self.l2 = Label(self.root, text='Area Threshold', font=('Arial', 15))
        self.l2.grid(row=1, column=2, pady=2)

        self.l3 = Label(self.root, text='Saggital View', font=('Arial',15))
        self.l3.grid(row=4, column=2, columnspan=2, sticky='S')

        self.l4 = Label(self.root, text='Corresponding Slice', font=('Arial',15))
        self.l4.grid(row=4, column=4, columnspan=2, sticky='S')

        # Buttons
        self.b1 = Button(self.root, text='Extract Slice', width=40, command=self.extract_slice)
        self.b1.grid(row=2, column=2, pady = 2, columnspan=2)

        self.b2 = Button(self.root, text='Extract Properties', width=40, command=self.extract_properties)
        self.b2.grid(row=3, column=2, pady = 2, columnspan=2)

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
        self.spin1.grid(row=4, column=0)
        self.s1 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, command=self.on_slider1, variable=self.val1)
        self.s1.grid(row=5, column=0)
        

        self.val2 = tk.DoubleVar()
        self.spin2 = ttk.Spinbox(self.root, textvariable=self.val2, wrap=True, width=4, from_=0, to=400, increment=self.increment, command=self.update_slider2)
        self.spin2.grid(row=4, column=1)
        self.s2 = ttk.Scale(self.root, orient='vertical', length=400, from_=0, to=400, command=self.on_slider2, variable=self.val2)
        self.s2.grid(row=5, column=1)

        # Frames
        self.f1 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.f1.grid(row=5, column=4, padx=20, pady=20, columnspan=2)

        self.f2 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=400, height=400, bd= 0)
        self.f2.grid(row=5, column=6, padx=20, pady=20, columnspan=2)
        
        self.f3 = Frame(self.root)
        self.f3.grid(row=1, column=4, columnspan=4, rowspan=3)

        # Combo boxes
        self.image_options = [
            'Binary Image',
            'Mask',
            'Segmented Image'
        ]
        self.cbb1 = ttk.Combobox(self.root, value=self.image_options)
        self.option = self.cbb1.current(0)
        self.cbb1.bind('<<ComboboxSelected>>', self.display_options)
        self.cbb1.grid(row=4, column=6, pady = 20, columnspan=2, sticky='S')

        # Canvas
        self.canvas = Canvas(self.root, width=400, height=400)
        self.canvas.grid(row=5, column=2, columnspan=2)
        self.canvas.create_image(0, 0, anchor=NW, image=self.saggital_image)
        self.canvas.create_line(0, self.val1.get(), 400, self.val1.get(), tag="top_line", fill='red')
        self.canvas.create_line(0, self.val2.get(), 400, self.val2.get(), tag="top_line", fill='red')

        # Tree 
        self.tree = self.create_tree_widget()

    def create_tree_widget(self):
        # Create scrollbars
        y_scroll_bar = Scrollbar(self.f3, width=10)
        y_scroll_bar.pack(side=RIGHT, fill=Y)

        x_scroll_bar = Scrollbar(self.f3, width=10, orient=HORIZONTAL)
        x_scroll_bar.pack(side=BOTTOM, fill=X)

        columns = ('vertebral_label', 'axial_area', 'volume', 'area_bmd', 'volume_bmd', 'elastic_modulus')
        tree = ttk.Treeview(self.f3, columns=columns, height=5, show='headings', xscrollcommand=x_scroll_bar.set, yscrollcommand=y_scroll_bar.set)
        tree.pack(fill=BOTH, expand=TRUE)
        y_scroll_bar.config(command=tree.yview)
        x_scroll_bar.config(command=tree.xview)

        # Define headings
        tree.heading('vertebral_label', text='Vertebral Label')
        tree.heading('axial_area', text='Axial Area')
        tree.heading('volume', text='Volume')
        tree.heading('area_bmd', text='aBMD')
        tree.heading('volume_bmd', text='vBMD')
        tree.heading('elastic_modulus', text='Elastic Modulus')

        tree.column('vertebral_label', anchor=CENTER, stretch=NO, width=100)
        tree.column('axial_area', anchor=CENTER, stretch=NO, width=100)
        tree.column('volume', anchor=CENTER, stretch=NO, width=100)
        tree.column('area_bmd', anchor=CENTER, stretch=NO, width=100)
        tree.column('volume_bmd', anchor=CENTER, stretch=NO, width=100)
        tree.column('elastic_modulus', anchor=CENTER, stretch=NO, width=100)

        contacts = []
        for n in range(1, 10):
            contacts.append((f'L{n}', n, n+2, n/10, n**2, n))

        # add data to the treeview
        for contact in contacts:
            tree.insert('', tk.END, values=contact)

        return tree

    def on_slider1(self, event):
        self.canvas.delete("top_line")
        self.canvas.create_line(0, self.val1.get(), 400, self.val1.get(), tag="top_line", fill='red')

    def on_slider2(self, event):
        self.canvas.delete("bottom_line")
        self.canvas.create_line(0, self.val2.get(), 400, self.val2.get(), tag="bottom_line", fill='red')

    def update_slider1(self):
        self.s1.set(self.val1.get())

    def update_slider2(self):
        self.s2.set(self.val2.get())

    def extract_slice(self):
        # Get mid slide
        self.get_mid_slice()

        # Get binary image
        self.get_binary()

        self.option = self.cbb1.current(0)

        # Segmentation
        seg.get_segmentation(area_theshold=float(self.e2.get()))

    def get_mid_slice(self):
        self.index = int((self.val1.get() + self.val2.get())*(len(self.hu_slices)-1)/(400*2))

        # Create a figure of specific size
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.hu_slices[-self.index-1], cmap='gray')
        plot.axis('off')

        plot.figure.savefig('original.png')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=5, column=4, padx=20, pady=20, columnspan=2)

    def get_binary(self):
        threshold = float(self.e1.get())
        self.binary_image = self.hu_slices[-self.index-1] > threshold

        # Create a figure of specific size
        figure = Figure(figsize=(4,4), dpi=100)
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)
        plot.imshow(self.binary_image, cmap='gray')
        plot.axis('off')

        plot.figure.savefig('binary.png')

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=5, column=6, padx=20, pady=20, columnspan=2)
         
        

    def extract_properties(self):
        pass

    def handle_options(self):
        if self.option == 'Binary Image':
            self.image = ImageTk.PhotoImage(Image.open('binary.png').resize((400,400)))
        elif self.option == 'Mask':
            self.image = ImageTk.PhotoImage(Image.open('mask.png').resize((400,400)))
        elif self.option == 'Segmented Image':
            self.image = ImageTk.PhotoImage(Image.open('segmentedimage.png').resize((400,400)))

        temp_canvas = Canvas(self.root, width=400, height=400)
        temp_canvas.grid(row=5, column=6, columnspan=2)
        temp_canvas.create_image(0, 0, anchor=NW, image=self.image)

    def display_options(self, event):
        self.option = self.cbb1.get()
        self.handle_options()

        
