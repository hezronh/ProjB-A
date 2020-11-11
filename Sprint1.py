import json
from tkinter import *
import requests
from tkinter import ttk
import tkinter as tk

def json_file_openen():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    r = requests.get(url)
    filedata = r.json()
    return filedata


def tkinter():
    game = first_game()
    root = tk.Tk()
    root.resizable(width=1, height=1)
    treev = ttk.Treeview(root, selectmode='browse')
    treev.pack(side='top')
    scrollbar = ttk.Scrollbar(root,
                              orient="vertical",
                              command=treev.yview)
    scrollbar.pack(side='right', fill='x')
    treev.configure(xscrollcommand=scrollbar.set)
    treev["columns"] = ("1")
    treev['show'] = 'headings'
    treev.column("1", width=90, anchor='w')
    treev.heading("1", text="Game Naam")
    treev.insert("", 'end', text='Game',
                 values=game)
    root.geometry("750x750")
    root.mainloop()

def first_game():
    filedata = json_file_openen()
    data = filedata[0]
    name = data["name"]
    return name

def gesorteerde_data():
    list = []
    filedate = json_file_openen()
    num = 0
    for data in filedate:
        data = filedate[num]
        namen = data["name"]
        num += 1
        list.append(namen)
    gesorteerde = sorted(list)

    return gesorteerde
tkinter()
print(first_game())
json_file_openen()
print(gesorteerde_data())