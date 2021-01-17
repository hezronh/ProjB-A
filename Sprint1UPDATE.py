import requests
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox


def open_jsonfile():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    r = requests.get(url)
    fileData = r.json()
    return fileData

def tkinter():
    gameList = sorted_data()
    price = prijs()
    datum = release_date()
    root = tk.Tk()
    mystring = StringVar(root)
    wrapper1 = LabelFrame(root, text="Games")
    wrapper2 = LabelFrame(root, text="Zoeken")
    wrapper1.pack(fill="both", expand="yes", padx=40, pady=30)
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
    trv = ttk.Treeview(wrapper1, columns=(1, 2, 3), show="headings", height="25", selectmode="browse")
    trv.pack()
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=trv.yview)
    scrollbar.place(x=695, y=75, height=500)
    trv.configure(yscrollcommand=scrollbar.set)
    trv.heading(1, text="Game naam")
    trv.column(1, width=300, minwidth=50)
    trv.heading(2, text='Prijs')
    trv.heading(3, text='Release datum')
    ent = Entry(wrapper2, textvariable=mystring)
    ent.pack(side=tk.LEFT, padx=6)
    def zoek():
        query = ent.get()
        selections = []
        for child in trv.get_children():
            if query in trv.item(child)['values']:
                selections.append(child)
        trv.selection_set(selections)
        try:
            trv.see(selections[0])
        except IndexError:
            messagebox.showerror('Foutmelding', 'Game niet gevonden!')
            pass
    btn = Button(wrapper2, text="Zoeken", command=zoek)
    btn.pack(side=tk.LEFT, padx=6)
    for (game, gameprijs, gamerelease) in zip(gameList, price, datum):
        trv.insert("", tk.END, values=(game, gameprijs, gamerelease))
    string = StringVar(root)
    string.set("A-Z")
    w = OptionMenu(root, string, "A-Z", "Datum van Release", "Prijs Laag - Hoog")
    w.pack()
    s = ttk.Style()
    s.theme_use("clam")
    root.configure(background="#264055")
    root.geometry("750x750")
    root.title('Steam Dashboard')
    root.mainloop()


def first_game():
    fileData = open_jsonfile()
    data = fileData[0]
    name = data["name"]
    return name


def sorted_data():
    gameList = []
    fileData = open_jsonfile()
    for data in fileData:
        name = data["name"]
        gameList.append(name)
    return gameList

def prijs():
    prijsdata = []
    filedata = open_jsonfile()
    for data in filedata:
        prijs = data["price"]
        prijsdata.append(prijs)
    return prijsdata

def release_date():
    release = []
    filedata = open_jsonfile()
    for data in filedata:
        datum = data["release_date"]
        release.append(datum)
    return release

open_jsonfile()
tkinter()
