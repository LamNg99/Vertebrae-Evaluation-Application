import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import segmentation as seg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ViewSegmentation:
    def __init__(self, root, saggital_view, slices):
        self.root = root 
        self.root.geometry("800x700+0+0")
        self.root.title("Segmentation")

        self.saggital_view = saggital_view
        self.slices = slices

        self.canvas = FigureCanvasTkAgg(self.saggital_view, self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

        # Slider
        self.val1 = tk.IntVar()
        self.s1 = ttk.Scale(self.root, orient='horizontal', length=400, from_=1, to=len(self.slices), command=self.on_slider1, variable=self.val1)
        self.s1.grid(row=1, column=0)

        self.val2 = tk.IntVar()
        self.s2 = ttk.Scale(self.root, orient='horizontal', length=400, from_=1, to=len(self.slices), command=self.on_slider2, variable=self.val2)
        self.s2.grid(row=2, column=0)

        self.canvas.create_line(self.val1, 0, self.val1, 400, tag="left_line", fill='')
        self.canvas.create_line(self.val2, 0, self.val2, 400, tag="right_line", fill='red')

    def on_slider1(self, event):
        self.canvas.delete("left_line")
        self.canvas.create_line(self.val1.get(), 0, self.left.get(), 400, tag="left_line", fill='green')

    def on_slider2(self, event):
        self.canvas.delete("right_line")
        self.canvas.create_line(self.val2.get(), 0, self.right.get(), 400, tag="right_line", fill='red')
