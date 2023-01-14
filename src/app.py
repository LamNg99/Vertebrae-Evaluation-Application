import tkinter as tk
from tkinter import BOTTOM, LEFT, Button, filedialog
import loaddicomfile as ldf

class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1350x700+0+0")
        self.root.title("Veterbrae Evaluation Software")
        self.root.config(bg="skyblue")

        # Load dicom files button 
        self.b1 = Button(text='Load DICOM File', command=self.load_dicom_file)
        self.b1.pack(ipadx=20, ipady=10, side=LEFT, expand=True)

        # Segmentation button
        self.b2 = Button(text='Segmentation')
        self.b2.pack(ipadx=20, ipady=10, side=LEFT, expand=True)

    def load_dicom_file(self):
        # Get directory path 
        file_path = filedialog.askdirectory()
        print(file_path)





if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()