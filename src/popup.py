import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from urllib import response

class PopUp:
    def __init__(self, root, properties, tree):
        self.root = root
        self.root = root 
        self.root.geometry("350x300+0+0")
        self.root.title("Preview Vertebral Properties")
        self.root.resizable(False, False)
        
        self.properties = properties
        self.tree = tree
        self.label = None

        # Labels
        self.l1 = Label(self.root, text='Area:', font=('Arial', 15))
        self.l1.grid(row=0, column=0, pady=2)
        self.l11 = Label(self.root, text=f'{self.properties[0]} cm^2', font=('Arial', 15))
        self.l11.grid(row=0, column=1, pady=2)

        self.l2 = Label(self.root, text='Vertebral Height:', font=('Arial', 15))
        self.l2.grid(row=1, column=0, pady=2)
        self.l22 = Label(self.root, text=f'{self.properties[1]} cm', font=('Arial', 15))
        self.l22.grid(row=1, column=1, pady=2)

        self.l3 = Label(self.root, text='Volume:', font=('Arial',15))
        self.l3.grid(row=2, column=0, pady=2)
        self.l33 = Label(self.root, text=f'{self.properties[2]} cm^3', font=('Arial', 15))
        self.l33.grid(row=2, column=1, pady=2)

        self.l4 = Label(self.root, text='BMC:', font=('Arial',15))
        self.l4.grid(row=3, column=0, pady=2)
        self.l44 = Label(self.root, text=f'{self.properties[3]} g', font=('Arial', 15))
        self.l44.grid(row=3, column=1, pady=2)

        self.l5 = Label(self.root, text='aBMD:', font=('Arial',15))
        self.l5.grid(row=4, column=0, pady=2)
        self.l55 = Label(self.root, text=f'{self.properties[4]} g/cm^2', font=('Arial', 15))
        self.l55.grid(row=4, column=1, pady=2)

        self.l6 = Label(self.root, text='vBMD:', font=('Arial',15))
        self.l6.grid(row=5, column=0, pady=2)
        self.l66 = Label(self.root, text=f'{self.properties[5]} g/cm^3', font=('Arial', 15))
        self.l66.grid(row=5, column=1, pady=2)

        self.l7 = Label(self.root, text='Elastic Modulus:', font=('Arial',15))
        self.l7.grid(row=6, column=0, pady=2)
        self.l77 = Label(self.root, text=f'{self.properties[6]}', font=('Arial', 15))
        self.l77.grid(row=6, column=1, pady=2)

        self.l8 = Label(self.root, text='Vertebral Label:', font=('Arial',15))
        self.l8.grid(row=7, column=0, pady=2)


        # Entry widget
        self.e1 = Entry(self.root, justify=CENTER)
        self.e1.insert(0, '')
        self.e1.grid(row=7, column=1, pady=2)

        # Buttons
        self.b1 = Button(self.root, text='Add data', width=10, command=self.add_data)
        self.b1.grid(row=8, column=0, pady = 2)

        self.b2 = Button(self.root, text='Cancel', width=10, command=self.cancel)
        self.b2.grid(row=8, column=1, pady = 2)

    def add_data(self):
        self.label = self.e1.get().strip().upper()
        if not self.label or self.label.isspace():
            tk.messagebox.showinfo('Invalid Label', 'Please label the vertebra before adding to the record')
        else:
            data = [self.label] + self.properties
            children = self.tree.get_children('')
            duplicate = None
            response = 'no'
            for child in children:
                values = self.tree.item(child, 'values')
                if self.label == values[0]:
                    response = tk.messagebox.askquestion('Existed Label', 'The label is already existed. Do you want to overwrite this data?')
                    duplicate = child
            if response == 'yes':
                self.tree.delete(duplicate)
                self.tree.insert('', END, values=data)
                self.root.destroy()
            elif response == 'no' and duplicate is None:
                self.tree.insert('', END, values=data)
                self.root.destroy()
            else:
                return None
            
    def cancel(self):
        response = tk.messagebox.askquestion('Form', 'Data have not been added yet. Continue?')
        if response == 'yes':
            self.root.destroy()

