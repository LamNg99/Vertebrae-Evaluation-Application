import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import segmentation as seg

class ViewSegmentation:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("800x700+0+0")
        self.root.title("Segmentation")