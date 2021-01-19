import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import requests
import RPi.GPIO as GPIO

tehapi = '7336DFF16E6BEB8021C01674DA8AC4DE'
tehuid = '76561198959203651'
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

def copyList(lst):
    lst_copy = lst
    return lst_copy


def mergeSort(lst, req):
    if len(lst) <= 1:
        return lst

    sortedList = copyList(lst)

    leftList = []
    rightList = []
    for i in range(len(sortedList)):
        if i < (len(sortedList) / 2):
            x = sortedList[i]
            leftList.append(x)
        else:
            x = sortedList[i]
            rightList.append(x)

    leftList = mergeSort(leftList, req)
    rightList = mergeSort(rightList, req)

    if req == 1:   #name
        key = 0
    elif req == 2:   #price
        key = 1
    elif req == 3:      #date
        key = 2
    elif req == 4:      #genre
        key = 3

    return mergeLists(leftList, rightList, key)


def mergeLists(left, right, key):
    sortedSubList = []
    while left and right:
        leftGame = left[0]
        leftData = leftGame[key]
        rightGame = right[0]
        rightData = rightGame[key]
        if leftData <= rightData:
            sortedSubList.append(left[0])
            del left[0]
        else:
            sortedSubList.append(right[0])
            del right[0]
    if left:
        sortedSubList.extend(left)
    elif right:
        sortedSubList.extend(right)
    return sortedSubList

def open_jsonfile():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    r = requests.get(url)
    fileData = r.json()
    return fileData

def tkinter():
    dataList = sorted_data()
    gesorteerde_naam = mergeSort(dataList, 1)
    gesorteerde_prijs = mergeSort(dataList, 2)
    gesorteerde_date = mergeSort(dataList, 3)
    gesorteerde_genre = mergeSort(dataList, 4)
    nameList = []
    priceList = []
    dateList = []
    genreList = []
    for data in dataList:
        name = data[0]
        price = data[1]
        date = data[2]
        genre = data[3]
        nameList.append(name)
        priceList.append(price)
        dateList.append(date)
        genreList.append(genre)
    def naam():
        nameList = []
        priceList = []
        dateList = []
        genreList = []
        for row in trv.get_children():
            trv.delete(row)
        for data in gesorteerde_naam:
            name = data[0]
            price = data[1]
            date = data[2]
            genre = data[3]
            nameList.append(name)
            priceList.append(price)
            dateList.append(date)
            genreList.append(genre)
        for (game, gameprijs, gamerelease, genre) in zip(nameList, priceList, dateList, genreList):
            trv.insert("", tk.END, values=(game, gameprijs, gamerelease, genre))
    def prijs():
        nameList = []
        priceList = []
        dateList = []
        genreList = []
        for row in trv.get_children():
            trv.delete(row)
        for data in gesorteerde_prijs:
            name = data[0]
            price = data[1]
            date = data[2]
            genre = data[3]
            nameList.append(name)
            priceList.append(price)
            dateList.append(date)
            genreList.append(genre)
        for (game, gameprijs, gamerelease, genre) in zip(nameList, priceList, dateList, genreList):
            trv.insert("", tk.END, values=(game, gameprijs, gamerelease, genre))
    def date():
        nameList = []
        priceList = []
        dateList = []
        genreList = []
        for row in trv.get_children():
            trv.delete(row)
        for data in gesorteerde_date:
            name = data[0]
            price = data[1]
            date = data[2]
            genre = data[3]
            nameList.append(name)
            priceList.append(price)
            dateList.append(date)
            genreList.append(genre)
        for (game, gameprijs, gamerelease, genre) in zip(nameList, priceList, dateList, genreList):
            trv.insert("", tk.END, values=(game, gameprijs, gamerelease, genre))
    def genre():
        nameList = []
        priceList = []
        dateList = []
        genreList = []
        for row in trv.get_children():
            trv.delete(row)
        for data in gesorteerde_genre:
            name = data[0]
            price = data[1]
            date = data[2]
            genre = data[3]
            nameList.append(name)
            priceList.append(price)
            dateList.append(date)
            genreList.append(genre)
        for (game, gameprijs, gamerelease, genre) in zip(nameList, priceList, dateList, genreList):
            trv.insert("", tk.END, values=(game, gameprijs, gamerelease, genre))
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
    trv.heading(1, text="Game naam", command=naam)
    trv.column(1, width=300, minwidth=50)
    trv.heading(2, text='Prijs', command=prijs)
    trv.heading(3, text='Release datum', command=date)
    trv.heading(4, text="Genres", command=genre)
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
    for (game, gameprijs, gamerelease, genre) in zip(nameList, priceList, dateList, genreList):
        trv.insert("", tk.END, values=(game, gameprijs, gamerelease, genre))
    for (naam, game) in steam:
        trv1.insert("", tk.END, values=(naam, game))
    def update():
        steam = printOnlineFriends(joinedsids)
        count = 0
        for row in trv1.get_children():
            count += 1
            trv1.delete(row)
        count2 = 0
        for (naam, game) in steam:
            count2 += 1
            trv1.insert("", tk.END, values=(naam, game))
        messagebox.showinfo('Steam melding', 'De lijst is geupdate!')
        if count >= count2:
            pass
        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(0)
            GPIO.setup(18, GPIO.OUT)
            while True:
                GPIO.output(18, GPIO.HIGH)
                time.sleep(2.0)
                GPIO.output(18, GPIO.LOW)
                time.sleep(2.0)
    btn2 = Button(wrapper2, text="Update", command=update)
    btn2.pack(side=tk.RIGHT)
    string = StringVar(root)
    string.set("Select")
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
    fileData = open_jsonfile()
    for data in fileData:
        name = data["name"]
        price = data["price"]
        date = data["release_date"]
        genre = data["genres"]
        dataList = [name, price, date, genre]
        gameList.append(dataList)
    return gameList

tkinter()
