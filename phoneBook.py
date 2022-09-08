from doctest import master
import psycopg2
import tkinter as tk
from tkinter import *
import re

window = tk.Tk()
window.title("Phone Book")
#window.geometry('675x75')


#title prompting user to enter contact's info
frm_title = tk.Frame(master = window)
lbl_title = tk.Label(master = frm_title, text = "Welcome to your phone book!  Enter in your contact's information:")
lbl_title.pack()


#entry to get contact_name
frm_name = tk.Frame(master = window,  borderwidth = 5)
lbl_name = tk.Label(master = frm_name, text = "Name:")
lbl_name.pack()
ent_name = tk.Entry(master = frm_name)
ent_name.pack()


#entry to get phone_number
frm_pnumb = tk.Frame(master = window, borderwidth = 5)
lbl_pnumb = tk.Label(
    master = frm_pnumb, 
    text = "Phone Number:"
)
lbl_pnumb.pack()
ent_pnumb = tk.Entry(master = frm_pnumb)
ent_pnumb.pack()


#button will initiate send to database
frm_send = tk.Frame(master = window, borderwidth = 5)
btn_send = tk.Button(
    master = frm_send,
    text = "Click to submit to phonebook"
)
btn_send.pack()


#button to access database
frm_db = tk.Frame(master = window, borderwidth = 5)
btn_db = tk.Button(
    master = frm_db,
    text = "Click to see contacts"
)
btn_db.pack()


#frame under the phone number entry frame to be used for error messages
frm_error = tk.Frame(master = window, borderwidth = 5)
lbl_error = tk.Label(master = frm_error, text = "")
lbl_error.pack()


#placing all of the frames in the grid accordingly
frm_title.grid(row = 0, column = 1, padx = 5, pady = 5)
frm_name.grid(row = 1, column = 0, padx = 5, pady = 5)
frm_pnumb.grid(row = 1, column = 1, padx = 5, pady = 5)
frm_send.grid(row = 1, column = 2, padx = 5, pady = 5)
frm_db.grid(row = 2, column = 0, padx = 5, pady = 5)
frm_error.grid(row = 2, column = 1, padx = 5, pady = 5)


#ensures the GUI adjusts as you resize the window
for i in range(3):
    window.columnconfigure(i, weight = 1)

for j in range(3):
    window.rowconfigure(j, weight = 1)


#function to upload to postgresql
def db_upload(val1, val2):
    values = "('" + val1 + "', '" + val2 + "')"
    with open('phonebook credentials.txt') as f:
        lines = f.read().splitlines()
    USER = str(lines[0])
    PASS = str(lines[1])
    conn = psycopg2.connect(
        dbname='phonebook',
        user=USER,
        password=PASS)
    point = conn.cursor()
    command = ("INSERT INTO contacts(contact_name, phone_number) VALUES" + values)
    point.execute(command)
    point.close()
    conn.commit()
    lbl_error["text"] = "Success, uploaded contact successfully"
    
    return


#function to read from postgresql database
def db_read():
    with open('phonebook credentials.txt') as f:
        lines = f.read().splitlines()
    USER = str(lines[0])
    PASS = str(lines[1])
    conn = psycopg2.connect(
        dbname='phonebook',
        user=USER,
        password=PASS)
    point = conn.cursor()
    command = ("SELECT * FROM contacts")
    point.execute(command)
    contacts = point.fetchall()
    point.close()

    return(contacts)


#function to show errors
def error_message():
    lbl_error["text"] = """Something is wrong try inputting
    a new Contact Name and Phone Number"""
    return


#function to check for valid inputs
def input_check(namecheck, phonecheck):
    valid = 0
    lbl_error["text"] = ""
    if len(namecheck) == 0 or len(phonecheck) == 0:
        error_message()
    elif namecheck.isspace():
        error_message()
    else:
        regex = '\d+'
        match = re.findall(regex, phonecheck)
        phonecheck = ""
        for x in match:
            phonecheck += x
        if len(phonecheck) == 11:
            if phonecheck[0] != '1':
                error_message()
            else:
                phonecheck = '+' + phonecheck
                valid = 1
        elif len(phonecheck) == 10:
            phonecheck = '+1' + phonecheck
            valid = 1
        else:
            error_message()

    return namecheck, phonecheck, valid


#function to handle button press
def handle_send(event):
    name = str(ent_name.get())
    phonenum = str(ent_pnumb.get())
    name, phonenum, check = input_check(name, phonenum)
    if check == 1:
        db_upload(name, phonenum)

    return   


#function to open pop up window
def popup(event):
    top = Toplevel(window)
    top.title("Contacts")
    
    frm_id = tk.Frame(master = top, borderwidth = 5)
    tk.Label(master = frm_id, text = "Contact ID").pack()

    frm_conName = tk.Frame(master = top, borderwidth = 5)
    tk.Label(master = frm_conName, text = "Name").pack()

    frm_phone = tk.Frame(master = top, borderwidth = 5)
    tk.Label(master = frm_phone, text = "Phone Number").pack()

    frm_delete = tk.Frame(master = top, borderwidth = 5)
    tk.Label(master = frm_delete, text = "Enter Contact ID to delete").pack()
    ent_delete = tk.Entry(master = frm_delete)
    ent_delete.pack()
    lbl_delete = tk.Label(master = frm_delete, text = "")
    btn_delete = tk.Button(master = frm_delete, text = "Delete", command = lambda: db_delete(ent_delete.get(), lbl_delete))
    btn_delete.pack()
    lbl_delete.pack()
    
    frm_id.grid(row = 0, column = 0, padx = 5, pady = 5)
    frm_conName.grid(row = 0, column = 1, padx = 5, pady = 5)
    frm_phone.grid(row = 0, column = 2, padx = 5, pady = 5)
    frm_delete.grid(row = 0, column = 4, padx = 5, pady = 5)

    db_id = tk.Text(frm_id, width = 5)
    db_id.pack()
    db_name = tk.Text(frm_conName, width = 50)
    db_name.pack()
    db_phone = tk.Text(frm_phone, width =20)
    db_phone.pack()
    
    text = db_read()
    for x in text:
        db_id.insert(tk.END, x[0])
        db_id.insert(tk.END, '\n')
        db_name.insert(tk.END, x[1])
        db_name.insert(tk.END, '\n')
        db_phone.insert(tk.END, x[2])
        db_phone.insert(tk.END, '\n')

    return


#function to delete entries in the database
def db_delete(target, lbl):
    with open('phonebook credentials.txt') as f:
        lines = f.read().splitlines()
    USER = str(lines[0])
    PASS = str(lines[1])
    conn = psycopg2.connect(
        dbname='phonebook',
        user=USER,
        password=PASS)
    point = conn.cursor()
    command = ("DELETE FROM contacts WHERE contact_id=" + str(target))
    point.execute(command)
    point.close()
    conn.commit()
    lbl["text"] = "Successfully deleted close and reopen database to see changes"
    return





#binding the buttons to their respective functions
btn_send.bind("<Button-1>", handle_send)
btn_db.bind("<Button-1>", popup)



window.mainloop()








