from tkinter import *
from tkinter import messagebox
import inspect as i

import sys
sys.path.insert(0, '../fanalysis/generatedata')


def foo():
    print("hello")
    a='(random stuff hahaha) '
    freq="days"
    print('How many {} would you like to {} generate? '.format(freq, a))
    str =  "p = print('How many {} would you like to {} generate? '.format(freq, a))"


def retrieve_prints(fn):
    function_string = i.getsourcelines(fn)
    for line in function_string:
        if "print(" in function_string[line]:
            string = input_to_string(fn)
    return string



form_fields = 'field 1', 'field 2'

class app_main:
    
    def __init__(self, master):
        self.master = master
        master.title("Print Gui Tool")

        self.text = "hello"
        self.label_text = StringVar()
        self.label_text.set(self.text)
        self.label = Label(master, textvariable=self.label_text)
        self.label.pack()

        def makeform(root, form_fields):
            entries = []
            for field in form_fields:
                row = Frame(root)
                lab = Label(row, width=15, text=field, anchor='w')
                ent = Entry(row)
                row.pack(side=TOP, fill=X, padx=5, pady=5)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries.append((field, ent))
            return entries
        





if __name__ == '__main__':
    root = Tk()
    #root.protocol("WM_DELETE_WINDOW", callback_cancel)
    
    my_gui = app_main(root)

    # create a menu
    menu = Menu(root)
    root.config(menu=menu)  
    filemenu = Menu(menu)
  

    root.mainloop()
