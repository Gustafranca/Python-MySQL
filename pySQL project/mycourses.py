#GUI - graphical user interface
# Tkinter - Built-in Python module used to creat GUI'S
#ttk - Themed Tk Widget Library

from tkinter import Tk, Button, Label, Scrollbar, Listbox,StringVar, Entry, W, E,N,S, END
from tkinter import ttk
from tkinter import messagebox
from mysql_config import dbConfig
import mysql.connector as pyo


con = pyo.connect(**dbConfig)

cursor = con.cursor()

 
class Coursedb:
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("You have connected to the DataBase")
        print(con)
    
    def __del__(self):
        self.con.close()
    
    def view(self):
        self.cursor.execute("SELECT * FROM courses")
        rows = self.cursor.fetchall()
        return rows

    def insert(self,title,institute,subjective):
        sql= ("INSERT INTO courses(title, institute, subjective) VALUES (%s,%s,%s)")
        values = [title,institute,subjective]
        self.cursor.execute(sql,values)
        self.con.commit()
        messagebox.showinfo(title="Course Database", message="New course added to database")

    def update(self,id,title,institute,subjective):
        tsql = "UPDATE courses SET title = %s, institute = %s, subjective = %s WHERE id=%s"
        self.cursor.execute(tsql, [title,institute,subjective,id])
        self.con.commit()
        messagebox.showinfo(title='Course Database', message="Course Update")

    def delete(self, id):
        delquery = "DELETE FROM courses WHERE id=%s"
        self.cursor.execute(delquery,[id])
        self.con.commit()
        messagebox.showinfo(title="Course Database", message="Course deleted")

db = Coursedb()

def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_tuple[1])
    institute_entry.delete(0, 'end')
    institute_entry.insert('end', selected_tuple[2])
    subjective_entry.delete(0, 'end')
    subjective_entry.insert('end', selected_tuple[3])

def view_records():
    list_bx.delete(0,"end")
    for row in db.view():
        list_bx.insert('end', row)

def add_course():
    db.insert(title_text.get(), institute_text.get(),subjective_text.get())
    list_bx.insert('end',(title_text.get(), institute_text.get(), subjective_text.get()))
    db.con.commit()
    title_entry.delete(0, "end") # Clears input after inserting
    institute_entry.delete(0, "end")
    subjective_entry.delete(0, "end")

def delete_records():
    db.delete(selected_tuple[0])
    db.con.commit()

def clear_screen():
    list_bx.delete(0,"end")
    title_entry.delete(0,"end")
    institute_entry.delete(0,"end")
    subjective_entry.delete(0,"end")

def update_records():
    db.update(selected_tuple[0], title_text.get(), institute_text.get(), subjective_text.get())
    title_entry.delete(0,"end")
    institute_entry.delete(0,"end")
    subjective_entry.delete(0,"end")
    db.con.commit()

def on_closing():
    dd = db
    if messagebox.askokcancel("Quit","Do you want to quit?"):
        root.destroy()
        del dd





root = Tk() # creats application window

#front-end part
root.title("Mybooks DataBase Application")
root.configure(background="light blue")
#root.geometry("850x500")
#root.resizable(width=False,height=False)
title_label = ttk.Label(root,text="Title", background="light blue", font=("TkDefaultFont", 16))
title_label.grid(row=0, column= 0, sticky=W) #position label
title_text = StringVar()
title_entry = ttk.Entry(root, width=24, textvariable=title_text)
title_entry.grid(row=0, column=1,sticky=W)

institute_label = ttk.Label(root,text="Institute", background="light blue", font=("TkDefaultFont", 16))
institute_label.grid(row=0, column= 2, sticky=W) #position label
institute_text = StringVar()
institute_entry = ttk.Entry(root, width=24, textvariable=institute_text)
institute_entry.grid(row=0, column=3,sticky=W)

subjective_label = ttk.Label(root,text="Subjective", background="light blue", font=("TkDefaultFont", 14))
subjective_label.grid(row=0, column= 4, sticky=W) #position label
subjective_text = StringVar()
subjective_entry = ttk.Entry(root, width=24, textvariable=subjective_text)
subjective_entry.grid(row=0, column=5,sticky=W) 


list_bx = Listbox(root, height=16, width=40, font="helvetica 13", bg="light green")
list_bx.grid(row=3, column=1,columnspan=14, sticky=W + E, pady=40,padx= 15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=8, rowspan=14,stick=W)

list_bx.configure(yscrollcommand=scroll_bar.set) # Enables vetical scrolling
scroll_bar.configure(command=list_bx.yview)


add_btn = Button(root, text="Add in list", bg="blue", fg="white", font="helvetica 10 bold", command=add_course)
add_btn.grid(row=0, column=7, sticky=W)

exit_btn = Button(root, text="exit", bg="blue", fg="white", font="helvetica 10 bold", command=on_closing)
exit_btn.grid(row=15, column=5)

modify_btn = Button(root, text="modify", bg="blue", fg="white", font="helvetica 10 bold", command=update_records)
modify_btn.grid(row=15, column=2)


view_btn = Button(root, text="view", bg="blue", fg="white", font="helvetica 10 bold", command=view_records)
view_btn.grid(row=15, column=1)

clear_btn = Button(root, text="clear", bg="blue", fg="white", font="helvetica 10 bold", command=clear_screen)
clear_btn.grid(row=15, column=3)

delete_btn = Button(root, text="delete", bg="blue", fg="white", font="helvetica 10 bold", command=delete_records)
delete_btn.grid(row=15, column=4)

#SQL PART






root.mainloop() #runs the application until exit

