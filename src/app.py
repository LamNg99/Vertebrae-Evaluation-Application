import tkinter as tk
from tkinter import Button, Checkbutton, Frame, Label, Scrollbar, filedialog, Text
from tkinter import END, RIGHT, Y
import loaddicomfile as ldf

class MainApp:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1000x700+0+0")
        self.root.title("Veterbrae Evaluation Software")
        #self.root.config(bg="skyblue")

        # Labels
        self.l1 = Label(text='DICOM info', font=('Arial', 10))
        self.l1.grid(row=0, column=1)

        # Checkboxes
        self.var = tk.BooleanVar()
        self.c1 = Checkbutton(text='Protected Display', font=('Arial',10), variable=self.var, onvalue='True', offvalue='False')
        self.c1.grid(row=0, column=3)

        # Buttons
        self.b1 = Button(text='Load DICOM File', command=self.load_dicom_file, width=50)
        self.b1.grid(row=1, column=0, pady = 2)

        self.b2 = Button(text='Segmentation', width=50)
        self.b2.grid(row=2, column=0, pady = 2)

        # Frame
        self.f1 = Frame(self.root)
        self.f1.grid(row=1, column=1, columnspan = 3, rowspan = 2, padx = 2, pady = 2)

        # Scroll bar
        self.scroll_bar = Scrollbar(self.f1, width=10)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        # Text Boxes
        self.t1 = Text(self.f1, height=5, width=50, yscrollcommand=self.scroll_bar.set, wrap='none')
        self.t1.pack()
        self.scroll_bar.config(command=self.t1.yview)

    def load_dicom_file(self):
        # Clear any previous info in the textbox
        self.t1.delete(1.0, END)

        # Get directory path 
        file_path = filedialog.askdirectory()
        print(file_path)
        
        # Get patient's info
        self.info = ldf.load_dcm_info(file_path, self.var.get())
        for item in self.info:
            self.t1.insert(1.0, f'{item[0]:25} : {item[1]} \n')







if __name__ == '__main__':
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()