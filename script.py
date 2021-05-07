from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class sign_in_window():
    def __init__(self):
        self.sign_in_window = Toplevel()
        self.sign_in_window.configure(bg='#210039')
        self.sign_in_window.resizable(False,False)
        self.sign_in_window.title("SIGN IN")
        
        Label(self.sign_in_window,text="SIGN IN",font="Helvetica, 18",fg='white',bg='#210039').grid(row=0,column=1,sticky=W+E,pady=10)
        Label(self.sign_in_window,text="Username: ",font="Helvetica, 14",fg='white',bg='#210039').grid(row=1,column=0)
        Label(self.sign_in_window,text="Password: ",font="Helvetica, 14",fg='white',bg='#210039').grid(row=2,column=0)

        self.username = Entry(self.sign_in_window,font="Helvetica, 12",fg='#210039').grid(row=1,column=1)
        self.password = Entry(self.sign_in_window,font="Helvetica, 12",fg='#210039', show='*').grid(row=2,column=1)

        self.bt_in = Button(self.sign_in_window,text="Sign in",font="Helvetica, 16",fg='white',bg='#210039')
        self.bt_in.grid(row=1,column=2,rowspan=2,padx=20,pady=(0,20))

        self.sign_in_window.mainloop()

class sign_up_window():
    def __init__(self):
        self.register_window = Toplevel()
        self.register_window.configure(bg='#210039')
        self.register_window.resizable(False,False)
        self.register_window.title("Users Register")

        self.username_label = Label(self.register_window,text="Username:",font="Helvetica, 14",fg='white',bg='#210039')
        self.username_label.grid(row=0,column=0,sticky=W,padx=10,pady=10)

        self.username_entry = ttk.Entry(self.register_window,font="Helvetica, 12",foreground='#210039')
        self.username_entry.grid(row=0,column=1,columnspan=2,pady=10,sticky=W+E)

        self.password_label = Label(self.register_window,text="Password:",font="Helvetica, 14",fg='white',bg='#210039')
        self.password_label.grid(row=1,column=0,sticky=W,padx=10,pady=10)

        self.password_entry = ttk.Entry(self.register_window,font="Helvetica, 12",foreground='#210039')
        self.password_entry.grid(row=1,column=1,columnspan=2,pady=10,sticky=W+E)

        self.submit_button = ttk.Button(self.register_window,text="SUBMIT")
        self.submit_button.grid(row=0,column=3,padx=9,sticky=W+E)

        self.delete_button = ttk.Button(self.register_window,text="DELETE")
        self.delete_button.grid(row=1,column=3,padx=9,sticky=W+E)

        self.tree = ttk.Treeview(self.register_window,selectmode="browse",column=("column1","column2"),show='headings')
        self.tree.column("column1",width=250,minwidth=250,stretch=NO)
        self.tree.heading("#1",text="Username")
        self.tree.column("column2",width=250,minwidth=250,stretch=NO)
        self.tree.heading("#2",text="Password")
        self.tree.grid(row=2,column=1,pady=9,sticky=W+E)

        self.register_window.mainloop()

class mainwindow():
    def sign_in(self):
        try:
            sign_in_window()
        except:
            raise Exception("AN ERROR OCCURRED")

    def sign_up(self):
        try:
            sign_up_window()
        except:
            raise Exception("AN ERROR OCCURRED")

    def quit_window(self):
        if messagebox.askokcancel("Do you really want to leave?", "Do you really want to leave?"):
            self.root.destroy()

    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='#210039')
        self.root.resizable(False,False)
        self.root.protocol("WM_DELETE_WINDOW",self.quit_window)
        self.root.title("Users Register")

        Label(self.root,text="USERS REGISTER",font="Helvetica, 20",fg='white',bg='#210039').grid(row=0,column=0)
        Label(self.root,text="(If you don't have account,\nplease click in sign up)",font="Helvetica, 14",fg='red2',bg='#210039').grid(row=1,column=0)

        self.bt = Button(self.root,text="Sign up",font="Helvetica, 16",command=self.sign_up)
        self.bt.configure(width=18,height=2,fg='white',bg='#210039')
        self.bt.grid(row=5,column=0,columnspan=2,sticky=W+E)

        self.bt = Button(self.root,text="Sign in",font="Helvetica, 16",command=self.sign_in)
        self.bt.configure(width=18,height=2,fg='white',bg='#210039')
        self.bt.grid(row=6,column=0,columnspan=2,sticky=W+E)

        self.bt = Button(self.root,text="Quit",font="Helvetica, 16",command=self.quit_window)
        self.bt.configure(width=18,height=2,fg='white',bg='#210039')
        self.bt.grid(row=7,column=0,columnspan=2,sticky=W+E)

        self.root.mainloop()
try:
    mainwindow()
except:
    raise Exception("AN ERROR OCCURRED")