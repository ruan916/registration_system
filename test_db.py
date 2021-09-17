from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class admin_window:
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def update_tree(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT * FROM users")
            self.rows = self.theCursor.fetchall()
            i=0
            for row in self.rows:
                if(i%2==0):
                    self.tree.insert("",END, values=row,tag='1')
                else:
                    self.tree.insert("",END, values=row,tag='2')
                i=i+1
        except:
            raise print("IT WAS NOT POSSIBLE UPDATE DATABASE")

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('users.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print("IT WAS NOT POSSIBLE TO CREATE A DATABASE CONNECTION")
        try:
            self.theCursor.execute("CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);")
        except:
            print("THE TABLE CANNOT BE CREATED")
        finally:
            self.sqlite_var.commit()
            self.update_tree()

    def clear_entries(self):
        self.username_entry.delete(0,"end")
        self.password_entry.delete(0,"end")

    def update_database(self):
        self.update_tree()
        self.clear_entries()
        print("UPDATE DATABASE")

    def search_record(self):
        try:
            self.tree.delete(*self.tree.get_children())
            self.theCursor.execute("SELECT * FROM users WHERE username like ? or password like ?",('%'+self.search_vl.get()+'%','%'+self.search_vl.get()+'%'))
            self.result = self.theCursor.fetchall()
            length = str(len(self.result))
            if(length==0):
                messagebox.showinfo("ERROR","NO RESULTS COULD BE FOUND")
            if(length!='0'):
                i=0
                for row in self.result:
                    if(i%2==0):
                        self.tree.insert("",END, values=row,tag='1')
                    else:
                        self.tree.insert("",END, values=row,tag='2')
                    i=i+1
        except:
            raise messagebox.showerror("IT WAS NOT POSSIBLE FIND THIS DATA")

    def reset_db(self):
        yesno=messagebox.askquestion("RESET DB","ALL DATA IN DATABASE WILL BE LOST, CONTINUE?")
        if(yesno=='yes'):
            self.theCursor.execute("DROP TABLE users")
            messagebox.showinfo("REDEFINED DATABASE","REDEFINED DATABASE")
            self.setup_db()
            self.update_tree()

    def delete_record(self):
        try:
            self.theCursor.execute("DELETE FROM users WHERE ID=?",(self.curItem['values'][0],))
            print("DELETED")
        except:
            print("ERROR","DELETED FAILED!")
        finally:
            self.curItem=0
            self.clear_entries()
            self.update_tree()
            self.sqlite_var.commit()

    def selectItem(self,event):
        self.curItem = self.tree.item(self.tree.focus())
        print(self.curItem)
        self.username_vl.set(self.curItem['values'][1])
        self.password_vl.set(self.curItem['values'][2])

    def write_record(self):
        if(self.username_vl.get()!="" and self.password_vl.get()!=""):
            try:
                self.theCursor.execute("""INSERT INTO users (username, password) VALUES (?,?)""",(self.username_vl.get(),self.password_vl.get()))
                self.sqlite_var.commit()
                self.theCursor.execute("SELECT *,max(ID) FROM users")
                self.rows=self.theCursor.fetchall()
                print("{username: ",self.rows[0][1],"| password: ",self.rows[0][2],"} WAS ADDED")
                self.clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror("ERROR","THIS USER HAS BEEN REGISTERED IN DATABASE")
            except:
                messagebox.showerror("ERROR","DATA WRITING FAILED")
            finally:
                self.update_tree()
        else:
            messagebox.showwarning("WARNING","PLEASE, FILL IN ALL FIELDS")

    def __init__(self):
        self.admin_window=Tk()
        self.admin_window.config(bg='light green')
        self.admin_window.resizable(False,False)
        self.admin_window.title("ADM CONTROL OF USERS DATABASE")

        self.username_lbl = Label(self.admin_window,text="USERNAME: ",font="Helvetica, 16",bg='light green',fg='#001a00')
        self.username_lbl.grid(row=0,column=0,pady=2,sticky=E)

        self.username_vl = StringVar(self.admin_window,value="")
        self.username_entry = ttk.Entry(self.admin_window,width=10,font="Helvetica, 14",background='light green',textvariable=self.username_vl)
        self.username_entry.grid(row=0,column=1,columnspan=2,padx=5,pady=5,sticky=W+E)

        self.password_lbl = Label(self.admin_window,text="PASSWORD: ",font="Helvetica, 16",bg='light green',fg='#001a00')
        self.password_lbl.grid(row=2,column=0,pady=2,sticky=E)

        self.password_vl = StringVar(self.admin_window,value="")
        self.password_entry = ttk.Entry(self.admin_window,width=10,font="Helvetica, 14",background='light green',textvariable=self.password_vl)
        self.password_entry.grid(row=2,column=1,columnspan=2,padx=5,pady=5,sticky=W+E)

        self.bt_adm_register = Button(self.admin_window,text="REGISTER",font="Helvetica, 16",command=self.write_record)
        self.bt_adm_register.configure(bg='#001a00',fg='white')
        self.bt_adm_register.grid(row=0,column=3,padx=2,pady=2,sticky=W+E)

        self.bt_adm_delete = Button(self.admin_window,text="DELETE",font="Helvetica, 16",command=self.delete_record)
        self.bt_adm_delete.configure(bg='#001a00',fg='white')
        self.bt_adm_delete.grid(row=2,column=3,padx=2,sticky=W+E)

        self.tree = ttk.Treeview(self.admin_window,selectmode="browse",column=("column1","column2","column3"),show='headings')
        self.tree.column("column1",width=50,minwidth=50,stretch=NO)
        self.tree.heading("#1",text="ID")
        self.tree.column("column2",width=350,minwidth=350,stretch=NO)
        self.tree.heading("#2",text="USERNAME")
        self.tree.column("column3",width=350,minwidth=350,stretch=NO)
        self.tree.heading("#3",text="PASSWORD")
        self.tree.bind("<ButtonRelease-1>",self.selectItem)
        self.tree.bind("<space>",self.selectItem)
        self.tree.tag_configure('1')
        self.tree.tag_configure('2')
        self.tree.grid(row=4,column=0,columnspan=4,sticky=W+E,padx=2,pady=2)

        Label(self.admin_window,text="SEARCH BY USERNAME: ",font="Helvetica, 16",bg='light green',fg='#001a00').grid(row=5,column=0,columnspan=2,pady=5,sticky=E)
        
        self.search_vl = StringVar(self.admin_window,value="")
        Entry(self.admin_window,font="Helvetica, 14",textvariable=self.search_vl).grid(row=5,column=2,pady=5,padx=5,sticky=W+E)

        self.bt_adm_search = Button(self.admin_window,text="SEARCH",font="Helvetica, 16",command=self.search_record)
        self.bt_adm_search.configure(bg='#001a00',fg='white')
        self.bt_adm_search.grid(row=5,column=3,padx=5,pady=5,sticky=W+E)

        self.bt_adm_update_database = Button(self.admin_window,text="UPDATE",font="Helvetica, 16",command=self.update_database)
        self.bt_adm_update_database.configure(bg='#001a00',fg='white')
        self.bt_adm_update_database.grid(row=6,column=0,columnspan=3,padx=5,pady=5,sticky=W+E)

        self.bt_adm_reset = Button(self.admin_window,text="RESET DATABASE",font="Helvetica, 16",command=self.reset_db)
        self.bt_adm_reset.configure(bg='#001a00',fg='white')
        self.bt_adm_reset.grid(row=6,column=3,padx=5,pady=5,sticky=W+E)

        self.setup_db()
        self.admin_window.mainloop()

class register_window:
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('users.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print("IT WAS NOT POSSIBLE TO CREATE A DATABASE CONNECTION")
        try:
            self.theCursor.execute("CREATE TABLE if not exists users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);")
        except:
            print("THE DATABASE CANNOT BE CREATED")
        finally:
            self.sqlite_var.commit()

    def new_user(self):
        try:
            if(self.username_text.get()!="" and self.password_text.get()!=""):
                self.theCursor.execute("INSERT INTO users (username,password) VALUES(?,?)",(self.username_text.get(),self.password_text.get()))
                self.register_window.destroy()
                messagebox.showinfo("SUCCESS","SUCCESSFUL REGISTRATION!\nNOW MAKE THE LOGIN")
            else:
                messagebox.showwarning("WARNING","PLEASE, FILL IN ALL FIELDS")
        except sqlite3.IntegrityError:
            messagebox.showerror("ERROR","THIS USER HAS BEEN REGISTERED IN DATABASE")
        except:
            messagebox.showerror("ERROR","IT WAS NOT POSSIBLE REGISTERED THIS DATA")
        finally:
            self.sqlite_var.commit()
            self.theCursor.execute("SELECT * FROM users")
            res = self.theCursor.fetchall()
            self.username_text.set("")
            self.password_text.set("")

    def __init__(self):
        self.register_window = Toplevel()
        self.register_window.config(bg='light green')
        self.register_window.title("USER REGISTER")
        self.register_window.resizable(False,False)
        
        self.password_text = StringVar()
        self.username_text = StringVar()

        Label(self.register_window,text="REGISTER",font="Helvetica, 20",bg='light green',fg='#001a00').grid(row=0,column=0,columnspan=3,padx=10,pady=10,sticky=W+E)
        Label(self.register_window,text="USERNAME: ",font="Helvetica, 16",bg='light green',fg='#001a00').grid(row=1,column=0,sticky=E)
        Label(self.register_window,text="PASSWORD: ",font="Helvetica, 16",bg='light green',fg='#001a00').grid(row=2,column=0,sticky=E)

        Entry(self.register_window,font="Helvetica, 14",textvariable=self.username_text).grid(row=1,column=1)
        Entry(self.register_window,font="Helvetica, 14",textvariable=self.password_text).grid(row=2,column=1,pady=5)

        bt_add_user = Button(self.register_window,font="Helvetica, 16",text="REGISTER",command=self.new_user)
        bt_add_user.configure(bg='#001a00',fg='white')
        bt_add_user.grid(row=1,column=2,rowspan=2,padx=10)
        
        self.setup_db()
        self.register_window.mainloop()

class login_window:
    sqlite_var = 0
    theCursor = 0
    curItem = 0

    def setup_db(self):
        try:
            self.sqlite_var = sqlite3.connect('users.db')
            self.theCursor = self.sqlite_var.cursor()
        except:
            print("IT WAS NOT POSSIBLE TO CREATE A DATABASE CONNECTION")
        try:
            self.theCursor.execute("CREATE TABLE if not exists users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);")
        except:
            print("THE TABLE CANNOT BE CREATED")
        finally:
            self.sqlite_var.commit()

    def log(self):
        try:
            self.theCursor.execute("SELECT * FROM users")
            res = self.theCursor.fetchall()
            flag = 0
            for x in res:
                if(self.var.get()==1 and self.username_text.get()==x[1] and self.password_text.get()==x[2]):
                    self.login_window.destroy()
                    
                    flag = 1
            if(self.var.get()==2 and self.username_text.get()=="admin" and self.password_text.get()=="aps"):
                self.login_window.destroy()
                admin_window()
                flag = 1
            if(flag==0):
                messagebox.showinfo("ERROR","INVALID USERNAME OR PASSWORD")
        except:
            messagebox.showerror("ERROR","IT WAS NOT POSSIBLE TO BE LOGIN")
        finally:
            self.password_text.set("")
            self.username_text.set("")

    def __init__(self):
        self.login_window = Tk()
        self.login_window.config(bg='light green')
        self.login_window.title("LOGIN")
        self.login_window.resizable(False,False)

        self.password_text = StringVar(self.login_window)
        self.username_text = StringVar(self.login_window)
        self.var = IntVar(self.login_window)

        Label(self.login_window,text="LOGIN",font="Helvetica, 20",bg='light green',fg='#001a00').grid(row=0,column=0,columnspan=3,padx=10,pady=10,sticky=W+E)
        Label(self.login_window,text="USERNAME: ",font="Helvetica, 16",bg='light green',fg='#001a00').grid(row=1,column=0,sticky=E)
        Label(self.login_window,text="PASSWORD: ",font="Helvetica, 16",bg='light green',fg='#001a00').grid(row=2,column=0,sticky=E)
        self.username_entry = Entry(self.login_window,font="Helvetica, 14",textvariable=self.username_text).grid(row=1,column=1)
        self.password_entry = Entry(self.login_window,font="Helvetica, 14",textvariable=self.password_text,show='*').grid(row=2,column=1)

        self.bt_login = Button(self.login_window,text="LOGIN",font="Helvetica, 16",command=self.log)
        self.bt_login.configure(bg='#001a00',fg='white')
        self.bt_login.grid(row=1,column=2,rowspan=2,padx=10)

        self.var.set(1)

        Radiobutton(self.login_window,text="USER",bg='light green',fg='#001a00',variable=self.var,value=1).grid(row=3,column=0,pady=5)
        Radiobutton(self.login_window,text="ADM (ONLY FOR AUTHORIZED)",bg='light green',fg='#001a00',variable=self.var,value=2).grid(row=3,column=1)

        self.setup_db()
        self.login_window.mainloop()

class main_window:
    def login(self):
        try:
            self.root.destroy()
            login_window()
        except:
            raise Exception("THE LOGIN WINDOW CANNOT WORK")

    def register(self):
        try:
            register_window()
        except:
            raise Exception("THE REGISTER WINDOW CANNOT WORK")

    def main_quit(self):
        if messagebox.askokcancel("Do you really want to leave?", "Do you really want to leave?"):
            self.root.destroy()

    def __init__(self):
        self.root = Tk()
        self.root.config(bg='light green')
        self.root.resizable(False,False)
        self.root.protocol("WM_DELETE_WINDOW",self.main_quit)
        self.root.title("HOME")

        Label(self.root,text="IF YOU DON'T HAVE A LOGIN,\n PLEASE, SIGN UP\n",font="Helvetica, 22",bg='light green',fg='#001a00').grid(row=0,column=0,padx=20,sticky=W+E)

        self.bt_main_login = Button(self.root,text="LOGIN",font="Helvetica, 16",command=self.login)
        self.bt_main_login.configure(width=18,height=2,bg='#001a00',fg='white')
        self.bt_main_login.grid(row=1,column=0,padx=5,pady=5,sticky=W+E)

        self.bt_main_register = Button(self.root,text="REGISTER",font="Helvetica, 16",command=self.register)
        self.bt_main_register.configure(width=18,height=2,bg='#001a00',fg='white')
        self.bt_main_register.grid(row=2,column=0,padx=5,pady=5,sticky=W+E)

        self.bt_main_quit = Button(self.root,text="QUIT",font="Helvetica, 16",command=self.main_quit)
        self.bt_main_quit.configure(width=18,height=2,bg='#001a00',fg='white')
        self.bt_main_quit.grid(row=3,column=0,padx=5,pady=5,sticky=W+E)

        self.root.mainloop()
try:
    main_window()
except:
    raise Exception("AN ERROR OCCURRED")