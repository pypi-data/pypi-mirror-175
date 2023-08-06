from termcolor import colored
from art import *
import os
import time
import json
import platform



sys = platform.system()

    


commands = {"Windows": ["cls", "exit"], "Linux":["clear", """
        osascript -e 'tell application "Terminal" to close first window' && exit
        """], "Darwin": ["clear", """
        osascript -e 'tell application "Terminal" to close first window' && exit
        """] }



sys = platform.system()

class variables():
    def __init__(self):
        self.colors = ['blue', 'green', 'red', 'yellow','cyan', 'grey']
        self.title = ["Morpion", ""]
        self.scheme = ["debug", colored("1", 'green'), colored("2", 'green'), colored("3", 'green'), colored("4", 'green'), colored("5", 'green'), colored("6", 'green'), colored("7", 'green'), colored("8", 'green'), colored("9", 'green')]
        self.cases = self.scheme

def loadFormat(x, base=2) -> int:
    return base * round(x/base)

def loading(currentVersion, path, SavePath, lang, l):
    

    os.system(commands[sys][0])
    tprint("morpion")
    fill = colored('■', "blue")
    percent = 0


    for progress in range(0, 1010):
        progress = progress/10
        percent = progress
        bar = f"{lang[l][17]}  [---------------------------------------------------] {percent} %" #11
        progress = loadFormat(progress)
        if progress!= 0:
                
                
            progress = int(progress/2)
            bar = bar.replace('-', fill, progress)
            print(f"{bar}", end="\r")
        else:
            print(f"{bar}", end='\r')
        time.sleep(3/1010)
    percent = 100
    bar = f"{lang[l][17]}  [{fill*50}] 100 %        "

    print(bar)


    time.sleep(1)
    os.system(commands[sys][0])

global cases
cases = []

def setGrid(turn, case, value, lang, l) ->list:
    global cases
    vars = variables()
    if turn == 1:
        cases = vars.cases
    else:
        cases[case] = value
    global grid1
    global grid2
    global grid3
    global grid4
    global grid5
    grid1 = f"           {cases[1]} | {cases[2]} | {cases[3]}"
    grid2 = "           --+---+--"
    grid3 = f"           {cases[4]} | {cases[5]} | {cases[6]}       {lang[l][18]} {turn}"        
    grid4 = "           --+---+--"
    grid5 = f"           {cases[7]} | {cases[8]} | {cases[9]}"
    return [grid1, grid2, grid3, grid4, grid5]

def getPlayers(path, lang, l) -> dict:
    with open(f'{path}/save.json', 'r') as save:
        players = {}
        #récupérer les données des joueurs précédents
        players = json.load(save)
        #j1
        p1 = input(f'{lang[l][18]} 1, {lang[l][19]} ?\n')
        if players.get(p1):
            print(f'{lang[l][20]} {p1} !')
        else:
            players[p1] = [0, 0, 0]
            print(f'{lang[l][21]} {p1} !')
        #j2
        #os.system('clear')
        def P2(p1) -> str:
            p2 = input(f'{lang[l][18]}, {lang[l][19]} ?\n')
            if p2 == p1:
                print(f'{lang[l][22]}')
                return P2(p1)
            else:
                return p2

        p2 = P2(p1)
        if players.get(p2):
            print(f'{lang[l][20]} {p2} !')
        else:
            players[p2] = [0, 0, 0]
            print(f'{lang[l][21]} {p2} !')
    players['currentPlayers'] = [p1, p2]
    #print(players)
    time.sleep(1.0)
    return players

def notDone(turn) -> bool:
    
    global cases
    if cases[1] == cases[2] == cases[3] == cases[4] == cases[5] == cases[6] == cases[7] == cases[8] == cases[9]:
        return True
    elif turn == 10:
        return False
    elif cases[1] == cases[2] == cases[3]:
        return False
    elif cases[4] == cases[5] == cases[6]:
        return False
    elif cases[7] == cases[8] == cases[9]:
        return False
    elif cases[1] == cases[4] == cases[7]:
        return False
    elif cases[2] == cases[5] == cases[8]:
        return False
    elif cases[3] == cases[6] == cases[9]:
        return False
    elif cases[1] == cases[5] == cases[9]:
        return False
    elif cases[3] == cases[5] == cases[7]:
        return False
    else:
        return True

def isWinner() -> bool:
    if cases[1] == cases[2] == cases[3]:
        return False
    elif cases[4] == cases[5] == cases[6]:
        return False
    elif cases[7] == cases[8] == cases[9]:
        return False
    elif cases[1] == cases[4] == cases[7]:
        return False
    elif cases[2] == cases[5] == cases[8]:
        return False
    elif cases[3] == cases[6] == cases[9]:
        return False
    elif cases[1] == cases[5] == cases[9]:
        return False
    elif cases[3] == cases[5] == cases[7]:
        return False
    else:
        return True



