import requests
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import requests

tehapi = '7336DFF16E6BEB8021C01674DA8AC4DE'
tehuid = '76561198959203651'  # This is to retrieve your friends list. Your profile needs to be set to public for this to work.
tehuri = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=' + tehapi + '&steamid=' + tehuid + '&relationship=friend'


friendlist = requests.get(tehuri).json()['friendslist']['friends']

steamidlist = []
for i in range(len(friendlist)):
    steamidlist.append(friendlist[i]['steamid'])

joinedsids = ','.join(steamidlist)


def printFriendInfo(ids):
    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + tehapi + '&steamids=' + ids
    userget = requests.get(useruri).json()['response']
    for i in range(len(userget['players'])):
        print(userget['players'][i])


def printOnlineFriends(ids):
    useruri = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' + tehapi + '&steamids=' + ids
    userget = requests.get(useruri).json()['response']

    onlineDict = {}
    global maxnamelen
    maxnamelen = 0
    for i in range(len(userget['players'])):
        tonli = userget['players'][i]['personastate']
        if tonli == 1:
            if 'gameextrainfo' in userget['players'][i]:
                sname = userget['players'][i]['personaname']
                sgame = userget['players'][i]['gameextrainfo']
                onlineDict.update({sname: sgame})
                if len(sname) > maxnamelen:
                    maxnamelen = int(len(sname))
        else:
            continue
    list = []
    for i in sorted(onlineDict.keys()):
        tspaces = ""
        lennamediff = (maxnamelen - len(i)) + 2
        for x in range(lennamediff):
            tspaces += ' '
        naam = i + tspaces, onlineDict[i]
        list.append(naam)
    return list


def open_jsonfile():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    r = requests.get(url)
    fileData = r.json()
    return fileData

def tkinter():
    dataList = sorted_data()
    gameList = dataList[0]
    priceList = dataList[1]
    releaseList = dataList[2]
    genreList = dataList[3]
    steam = printOnlineFriends(joinedsids)
    root = tk.Tk()
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=my_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    second_frame = Frame(canvas)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")
    mystring = StringVar(second_frame)
    wrapper1 = LabelFrame(second_frame)
    wrapper2 = LabelFrame(second_frame)
    wrapper1.pack(fill="both", expand="yes", padx=40, pady=30)
    wrapper2.pack(fill="both", expand="yes", padx=20, pady=40)
    trv = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4), show="headings", height="25", selectmode="browse")
    trv.pack()
    trv1 = ttk.Treeview(wrapper2, columns=(1, 2), show="headings", height="25", selectmode="browse")
    trv1.pack()
    scrollbar = ttk.Scrollbar(second_frame, orient="vertical", command=trv.yview)
    scrollbar.place(x=930, y=60, height=500)
    trv.configure(yscrollcommand=scrollbar.set)
    trv.heading(1, text="Game naam")
    trv.column(1, width=300, minwidth=50)
    trv.heading(2, text='Prijs')
    trv.heading(3, text='Release datum')
    trv.heading(4, text="Genres")
    trv1.heading(1, text="Online vrienden")
    trv1.heading(2, text="Game")
    ent = Entry(wrapper1, textvariable=mystring)
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
            if query == '':
                pass
            else:
                messagebox.showerror('Foutmelding', 'Game niet gevonden!')
    btn = Button(wrapper1, text="Zoeken", command=zoek)
    btn.pack(side=tk.LEFT, padx=6)
    for (game, gameprijs, gamerelease, genre) in zip(gameList, priceList, releaseList, genreList):
        trv.insert("", tk.END, values=(game, gameprijs, gamerelease, genre))
    for (naam, game) in steam:
        trv1.insert("", tk.END, values=(naam, game))
    def update():
        steam = printOnlineFriends(joinedsids)
        count = 0
        for row in trv1.get_children():
            count += 1
            trv1.delete(row)
        for (naam, game) in steam:
            trv1.insert("", tk.END, values=(naam, game))
        messagebox.showinfo('Steam melding', 'De lijst is geupdate!')
        if count >= 1:

    btn2 = Button(wrapper2, text="Update", command=update)
    btn2.pack(side=tk.RIGHT)
    string = StringVar(root)
    string.set("A-Z")
    w = OptionMenu(wrapper1, string, "A-Z", "Datum van Release", "Prijs Laag - Hoog", "Genres")
    w.pack()
    s = ttk.Style()
    s.theme_use("clam")
    second_frame.configure(background="#264055")
    root.geometry("1000x1500")
    root.title('Steam Dashboard')
    root.mainloop()


def first_game():
    fileData = open_jsonfile()
    data = fileData[0]
    name = data["name"]
    return name


def sorted_data():
    gameList = []
    prijsdata = []
    release = []
    genres = []
    fileData = open_jsonfile()
    for data in fileData:
        name = data["name"]
        prijs = data["price"]
        datum = data["release_date"]
        genre = data["genres"]
        gameList.append(name)
        prijsdata.append(prijs)
        release.append(datum)
        genres.append(genre)
    return gameList, prijsdata, release, genres


open_jsonfile()
tkinter()
