import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import utils as utils
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class View3D:
    def __init__(self, root, image, scan):
        self.root = root 
        self.width_of_window = 800
        self.height_of_window = 700
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.pos_x = (self.screen_width//2)-(self.width_of_window//2)
        self.pos_y = (self.screen_height//2)-(self.height_of_window//2)
        self.root.geometry(f'{self.width_of_window}x{self.height_of_window}+{self.pos_x}+{self.pos_y}')
        self.root.title("3D View")
        self.root.resizable(False, False)

        self.image = image
        self.scan = scan

        # Frames
        self.f1 = Frame(self.root, highlightbackground='black', highlightthickness=1, width=750, height=550, bd= 0, background="white")
        self.f1.grid(row=4, column=0, padx=20, pady=20, columnspan=4)

        # Labels
        self.l1 = Label(self.root, text='Threshold', font=('Arial', 15))
        self.l1.grid(row=0, column=1, pady=2)

        self.l2 = Label(self.root, text='Step Size', font=('Arial', 15))
        self.l2.grid(row=1, column=1, pady=2)

        self.l3 = Label(self.root, text='Alpha', font=('Arial', 15))
        self.l3.grid(row=2, column=1, pady=2)

        # Entry widgets
        self.e1 = Entry(self.root, justify=CENTER)
        self.e1.insert(0, '800')
        self.e1.grid(row=0, column=2, pady=2, sticky=W)

        self.e2 = Entry(self.root, justify=CENTER)
        self.e2.insert(0, '1')
        self.e2.grid(row=1, column=2, pady=2, sticky=W)

        self.e3 = Entry(self.root, justify=CENTER)
        self.e3.insert(0, '0.7')
        self.e3.grid(row=2, column=2, pady=2, sticky=W)

        # Buttons
        self.b1 = Button(self.root, text='Apply', command=self.plot_3d)
        self.b1.grid(row=1, column=3, pady = 2, sticky=W)

        self.b2 = Button(self.root, text='Refresh', command=self.refresh)
        self.b2.grid(row=2, column=3, pady = 2, sticky=W)


    def plot_3d(self):
        threshold = float(self.e1.get())
        step_size = float(self.e2.get())
        alpha = float(self.e3.get())

        # Resample image
        image, spacing = utils.resample(self.image, self.scan)

        # Create mesh
        verts, faces, p = utils.make_mesh(image, threshold, step_size)

        figure = Figure(figsize=(6,5))
        figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
        plot = figure.add_subplot(111, projection='3d')

        mesh = Poly3DCollection(verts[faces], alpha=alpha)
        face_color = [0.45, 0.45, 0.75]
        mesh.set_facecolor(face_color)
        plot.add_collection3d(mesh)

        plot.set_xlim(0, p.shape[0])
        plot.set_ylim(0, p.shape[1])
        plot.set_zlim(0, p.shape[2])

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(row=4, column=1, padx=20, pady=20, columnspan=2)    
    
    def refresh(self):
        self.e1.delete(0, END)
        self.e1.insert(0, '800')

        self.e2.delete(0, END)
        self.e2.insert(0, '1')

        self.e3.delete(0, END)
        self.e3.insert(0, '0.7')











