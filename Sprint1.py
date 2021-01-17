import requests
from tkinter import ttk
from tkinter import *
import tkinter as tk

def open_jsonfile():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    r = requests.get(url)
    fileData = r.json()
    return fileData


def tkinter():
    gameList = sorted_data()
    root = tk.Tk()
    root.resizable(width=1, height=1)
    treeView = ttk.Treeview(root, selectmode='browse')
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=treeView.yview)
    treeView.pack(side='top')
    scrollbar.pack(side='right', fill='x')
    treeView.configure(xscrollcommand=scrollbar.set)
    treeView["columns"] = "1"
    treeView['show'] = 'headings'
    treeView.column("1", width=250)
    treeView.heading("1", text="Game Naam:")
    for games in gameList:
        if "\"" not in games:
            games = "\"" + games + "\""
        treeView.insert("", 'end', text="Game", values=games)
    root.geometry("750x750")
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
    return sorted(gameList)


print(first_game())
open_jsonfile()
tkinter()
