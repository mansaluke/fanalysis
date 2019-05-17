from tkinter import *
from tkinter import messagebox
import sys
sys.path.insert(0, '../fanalysis/generatedata')


form_fields = 'field 1', 'field 2'

class app_main:
    
    def __init__(self, master):
        self.master = master
        master.title("test app")

        self.button = Button(master, text="createdata", command=self.createdata)
        self.button.pack()

        self.text = "hello"
        self.label_text = StringVar()
        self.label_text.set(self.text)
        self.label = Label(master, textvariable=self.label_text)
        self.label.pack()

        #entry with data validation
        #vcmd = master.register(self.validate) # we have to wrap the command
        #self.entry = Entry(master, text = "entry 1", validate="key", validatecommand=(vcmd, '%P'))
        #self.entry.pack()

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
        
        def fetch(entries):
            for entry in entries:
                field = entry[0]
                text  = entry[1].get()
                print('%s: "%s"' % (field, text)) 

        self.ents = makeform(root, form_fields)
        root.bind('<Return>', (lambda event, e=self.ents: fetch(e)))   
        #layout
        #self.label.grid(row=0, column=0, sticky=W)
        #self.button.grid(row=2, column=0)
        #self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

    def createdata(self):
        self.text = "you have clicked me!"
        self.label_text.set(self.text)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            return False
        else:
            return True
    



    
def callback_cancel():
    if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()

def callback_new():
    print("called the callback_new!")

def callback_open():
    print("called the callback_open!")

def callback_exit():
    print("called the callback_exit!")

def callback_about():
    print("called the callback_about!")



if __name__ == '__main__':
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", callback_cancel)
    
    my_gui = app_main(root)

    # create a menu
    menu = Menu(root)
    root.config(menu=menu)
    
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=callback_new)
    filemenu.add_command(label="Open...", command=callback_open)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=callback_exit)
    
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=callback_about)
    

    root.mainloop()



