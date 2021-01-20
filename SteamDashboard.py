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


# Deel 1/2 van de Merge Sort die de lijst opsplists in kleinere lijsten
def mergeSort(lst, req):
    # Als een lijst 1 ding of niks bevat, is hij automatisch gesorteerd
    if len(lst) <= 1:
        return lst

    # Kopie van de lijst maken
    sortedList = lst

    # Twee lijsten maken en de originele lijst in twee splitsen.
    leftList = []
    rightList = []
    for i in range(len(sortedList)):
        # Alles links van het middenpunt in de lijst LeftList, de rest in rightList
        if i < (len(sortedList) / 2):
            x = sortedList[i]
            leftList.append(x)
        else:
            x = sortedList[i]
            rightList.append(x)

    # Recursief the linker en rechter lijst opsplitsen totdat de lijst 1 object bevat
    leftList = mergeSort(leftList, req)
    rightList = mergeSort(rightList, req)

    # Dit geeft aan waarop de sorteer functie moet sorteren, waar key (behalve bij median) de index is
    if req == "name":
        key = 0
    elif req == "price":
        key = 1
    elif req == "date":
        key = 2
    elif req == "genre":
        key = 3
    elif req == "median":
        key = 4

    # Roep sorteerfunctie aan
    return mergeLists(leftList, rightList, key)


# Deel 2/2 van de Merge Sort die de verschillende opgesplitste lijsten met elkaar sorteerd
def mergeLists(left, right, key):
    sortedSubList = []

    # Als de linker lijst en de rechter lijst beide niet leeg zijn
    while left and right:
        # Als we de median willen, hoeven we niet twee keer te indexen
        if key == 4:
            leftData = left[0]
            rightData = right[0]
        # Als we de op andere waarden willen sorteren
        else:
            leftGame = left[0]
            leftData = leftGame[key]
            rightGame = right[0]
            rightData = rightGame[key]

        # Voeg linker waarde aan gesorteerde lijst toe en haal linker waarde weg als links kleiner is dan rechts
        if leftData <= rightData:
            sortedSubList.append(left[0])
            del left[0]
        # Anders, voeg rechter waarde toe en haal rechter waarde weg
        else:
            sortedSubList.append(right[0])
            del right[0]

    # Als linker lijst nog vol is, maar rechter is leeg
    # Voeg dan alle resterende waarde van linker lijst toe aan gesorteerde lijst
    if left:
        sortedSubList.extend(left)
    # Anders voeg dan alle resterende waarde van rechter lijst toe aan gesorteerde lijst
    elif right:
        sortedSubList.extend(right)

    return sortedSubList


def open_jsonfile():
    url = "https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json"
    r = requests.get(url)
    fileData = r.json()
    return fileData


def median_price(lst):
    lstSorted = mergeSort(lst, "median")
    lenLst = len(lstSorted)
    isEven = False
    if (lenLst % 2) == 0:
        isEven = True
    if isEven:
        midpoint1 = (lenLst // 2)
        midpoint2 = (lenLst // 2) + 1
        median = float((lstSorted[midpoint1] + lstSorted[midpoint2]) / 2)
        return median
    else:
        midpoint = int((lenLst / 2) + 1)
        median = lstSorted[midpoint]
        return median


def tkinter():
    dataList = sorted_data()
    gesorteerde_naam = mergeSort(dataList, "name")
    gesorteerde_prijs = mergeSort(dataList, "price")
    gesorteerde_date = mergeSort(dataList, "date")
    gesorteerde_genre = mergeSort(dataList, "genre")
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
    meest_volkomende_genres = []
    for x in genreList:
        genres = x.split(';')
        for a in genres:
            meest_volkomende_genres.append(a)
    def meest_voorkomende(List):
        return max(set(List), key=List.count)
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
    string = StringVar(root)
    string.set("Select")
    def knopje_mediaan():
        messagebox.showinfo("Mediaan", 'De mediaan is: ' + str(median_price(priceList)))
    def knopje_genre():
        messagebox.showinfo("Meest volkomende Genre", "De meest volkomende genre is: " + str(meest_voorkomende(meest_volkomende_genres)))
    knopje = Button(wrapper1, text="Mediaan van de prijs", command=knopje_mediaan)
    knopje.pack(side=tk.RIGHT)
    knopje2 = Button(wrapper1, text="Meest voorkomende genre", command=knopje_genre)
    knopje2.pack(side=tk.RIGHT)
    btn2 = Button(wrapper2, text="Update", command=update)
    btn2.pack(side=tk.RIGHT)
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
