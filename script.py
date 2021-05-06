from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class sign_in_window():
    def __init__(self):
        self.sign_in_window = Toplevel()
        self.sign_in_window.title("SIGN IN")
        self.sign_in_window.resizable(False,False)
        
        Label(self.sign_in_window,text="SIGN IN",font="Helvetica").grid(row=0,column=0,sticky=W,pady=10)
        Label(self.sign_in_window,text="Username: ",font="Helvetica, 12").grid(row=1,column=0)
        Label(self.sign_in_window,text="Password: ",font="Helvetica, 12").grid(row=2,column=0)

        self.username = Entry(self.sign_in_window,font="Helvetica, 10").grid(row=1,column=1)
        self.password = Entry(self.sign_in_window,font="Helvetica, 10", show='*').grid(row=2,column=1,pady=(0,20))

        self.bt_in = Button(self.sign_in_window,text="Sign in",font="Helvetica, 16",bg='white')
        self.bt_in.grid(row=1,column=2,rowspan=2,padx=20,pady=(0,20))

        self.sign_in_window.mainloop()

class sign_up_window():
    def __init__(self):
        self.sign_in_window = Toplevel()
        self.sign_in_window.title("SIGN UP")
        self.sign_in_window.resizable(False,False)
        
        Label(self.sign_in_window,text="SIGN UP",font="Helvetica").grid(row=0,column=0,sticky=W,pady=10)
        Label(self.sign_in_window,text="Username: ",font="Helvetica, 12").grid(row=1,column=0)
        Label(self.sign_in_window,text="Password: ",font="Helvetica, 12").grid(row=2,column=0)

        Entry(self.sign_in_window,font="Helvetica, 10").grid(row=1,column=1)
        Entry(self.sign_in_window,font="Helvetica, 10").grid(row=2,column=1)

        self.bt_up = Button(self.sign_in_window,text="Sign up",font="Helvetica, 16")
        self.bt_up.grid(row=1,column=2,rowspan=2,pady=20)

        self.sign_up_window.mainloop()

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
        self.root=Tk()
        self.root.resizable(False,False)
        self.root.protocol("WM_DELETE_WINDOW",self.quit_window)
        self.root.title("Users Register")

        Label(self.root,text="Users Register",font="Helvetica, 20",fg='blue').grid(row=0,column=0,sticky=W+E)
        Label(self.root,text="If you don't have account, please click in sign up",font="Helvetica, 18",fg='red4').grid(row=1,column=0,sticky=W)

        self.bt = Button(self.root,text="Sign up",font="Helvetica, 16",command=self.sign_up)
        self.bt.configure(width=18,height=2,fg='white',bg='orange4')
        self.bt.grid(row=5,column=0,columnspan=2,sticky='N',pady=30)

        self.bt = Button(self.root,text="Sign in",font="Helvetica, 16",command=self.sign_in)
        self.bt.configure(width=18,height=2,fg='white',bg='orange4')
        self.bt.grid(row=5,column=2,columnspan=2,sticky='N',pady=30)

        self.bt = Button(self.root,text="Quit",font="Helvetica, 16",command=self.quit_window)
        self.bt.configure(width=18,height=2,fg='white',bg='orange4')
        self.bt.grid(row=6,column=1,columnspan=2,sticky='N',pady=30)

        self.root.mainloop()
try:
    mainwindow()
except:
    raise Exception("AN ERROR OCCURRED")