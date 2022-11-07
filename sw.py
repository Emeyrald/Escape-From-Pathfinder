import yaml
import os
import platform

class bcolors:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

with open('Rooms.yaml', 'r') as file:
    rooms = yaml.safe_load(file)

##### Examples of code
#print(type(rooms))
#print(rooms)
#print(rooms["A1"]["name"])
#print(type(rooms["A1"]))
#print(rooms["B4"]["item"])
#print(bcolors.OKGREEN + "Testing" + bcolors.ENDC)
#input = input("testInput: ")
#inventory.append(rooms[currentRoom]["item"])

startingRoom = "B4"
currentRoom = startingRoom
playerInventory = []
nextRoom = ""
directions = ["northDoor", "southDoor", "eastDoor", "westDoor"]
lockedRooms = []
loweredPlayerInventory = []

lockedMessage = bcolors.YELLOW + bcolors.BOLD + "THAT ROOM IS LOCKED." + bcolors.ENDC
blockedMessage = bcolors.YELLOW + bcolors.BOLD + "You can't go that way!" + bcolors.ENDC
wrongMessage = bcolors.RED + bcolors.BOLD + "Please enter a command that is formatted properly." + bcolors.ENDC

def turn():
    global currentRoom
    if rooms[currentRoom]["winningRoom"] == "false" and rooms[currentRoom]["accessed"] == "false":
        lockedRooms = []
        choice()
    elif rooms[currentRoom]["winningRoom"] == "true" and rooms[currentRoom]["accessed"] == "false":
        lockedRooms = []
        choice()
    elif rooms[currentRoom]["winningRoom"] == "false" and rooms[currentRoom]["accessed"] == "true":
        lockedRooms = []
        choice()
    elif rooms[currentRoom]["winningRoom"] == "true" and rooms[currentRoom]["accessed"] == "true":
        win()

def inventory():
    if playerInventory != []:
        print(bcolors.GREEN + "This is your inventory:" + bcolors.ENDC)
        for item in playerInventory:
            print(bcolors.CYAN + item + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There is nothing in your inventory." + bcolors.ENDC)
    turn()

def go(action):
    global currentRoom
    if action == "go north":
        nextRoom = rooms[currentRoom]["northDoor"]
        if rooms[currentRoom]["northDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["northDoor"]
            roomTitle()
            print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
            turn()
        elif rooms[currentRoom]["northDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            print(lockedMessage)
            choice()
        else:
            print(blockedMessage)
            choice()
    elif action == "go south":
        nextRoom = rooms[currentRoom]["southDoor"]
        if rooms[currentRoom]["southDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["southDoor"]
            roomTitle()
            print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
            turn()
        elif rooms[currentRoom]["southDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            print(lockedMessage)
            choice()
        else:
            print(blockedMessage)
            choice()
    elif action == "go east":
        nextRoom = rooms[currentRoom]["eastDoor"]
        if rooms[currentRoom]["eastDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["eastDoor"]
            roomTitle()
            print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
            turn()
        elif rooms[currentRoom]["eastDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            print(lockedMessage)
            choice()
        else:
            print(blockedMessage)
            choice()
    elif action == "go west":
        nextRoom = rooms[currentRoom]["westDoor"]
        if rooms[currentRoom]["westDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["westDoor"]
            roomTitle()
            print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
            turn()
        elif rooms[currentRoom]["westDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            print(lockedMessage)
            choice()
        else:
            print(blockedMessage)
            choice()
    else:
        print(wrongMessage)
        turn()

def choice():
    global currentRoom
    action = input("What do you want to do? " + bcolors.GREEN).lower()
    print(bcolors.ENDC)
    if action[0:2] == "lo":
        clearScreen()
        look()
    elif action[0:2] == "go":
        clearScreen()
        go(action)
    elif action[0:2] == "us":
        use(playerInventory, action)
    elif action[0:2] == "ge":
        get(playerInventory, action)
    elif action[0:2] == "in":
        inventory()
    elif action[0:2] == "ex":
        clearScreen()
        exitFunction()
    elif action[0:2] == "he":
        clearScreen()
        help()
    elif action[0:2] == "ac":
        access()
    else:
        print(wrongMessage)
        turn()

def look():
    global currentRoom
    roomTitle()
    print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
    turn()

def use(playerInventory, action):
    global currentRoom
    for direction in directions:
        if rooms[currentRoom][direction] != "Empty" and rooms[rooms[currentRoom][direction]]["locked"] == "true":
            lockedRooms.append(rooms[currentRoom][direction])
    if playerInventory != []:
        loweredItem = action[4:].lower()
        for item in playerInventory:
            loweredPlayerInventory.append(item.lower())
        if loweredItem in loweredPlayerInventory:
            for room in lockedRooms:
                if loweredItem != rooms[room]["keyItem"].lower():
                    continue
                elif loweredItem == rooms[room]["keyItem"].lower():
                    print("You use the " + rooms[room]["keyItem"] + " on the " + rooms[room]["name"])
                    rooms[room]["locked"] = "false"
                    break
                else:
                    print("That item can't be used here.")
        else:
            print("That item is not in your inventory.")
    else:
        print("There is nothing to use.")
    turn()

def get(playerInventory, action):
    global currentRoom
    if rooms[currentRoom]["item"] != "Empty":
        if rooms[currentRoom]["item"].lower() in action:
            playerInventory.append(rooms[currentRoom]["item"])
            print("You got the " + rooms[currentRoom]["item"])
            rooms[currentRoom]["item"] = "Empty"
        else:
            print(bcolors.YELLOW + "There is no " + action[4:] + " here." + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There are no items to get in this room." + bcolors.ENDC)
    turn()

def roomTitle():
    global currentRoom
    print(bcolors.BLUE + "*"*50)
    if len(rooms[currentRoom]["name"]) % 2 == 0:
        print("***" + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 3) + rooms[currentRoom]["name"] + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 3) + "***")
    else:
        print("***" + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 3) + rooms[currentRoom]["name"] + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 4) + "***")
    print("*"*50 + bcolors.ENDC)

def clearScreen():
    if platform.system() == "Windows":
        clear = lambda: os.system('cls')
    else:
        clear = lambda: os.system("clear")
    clear()

def start():
    title = open('title.txt', 'r').read()
    ship = open("ship.txt", "r").read()
    print(bcolors.YELLOW)
    print(title)
    print(bcolors.RED)
    print(ship)
    print(bcolors.ENDC)
    input(" "*36 + "Press enter to continue")
    roomTitle()
    print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
    turn()

def exitFunction():
    exit()

def help():
    helpFile = open('help.txt', 'r').read()
    print(helpFile)
    input("Press enter to continue")
    clearScreen()
    roomTitle()
    print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)
    turn()

def win():
    print("Congratulations!")
    exit()

def textTest():
    for room in rooms:
        if rooms[room]["name"] != "Empty":
            print(bcolors.GREEN + "*"*50)
            if len(rooms[room]["name"]) % 2 == 0:
                print("***" + " "*(25 - int(len(rooms[room]["name"])/2) - 3) + rooms[room]["name"] + " "*(25 - int(len(rooms[room]["name"])/2) - 3) + "***")
            else:
                print("***" + " "*(25 - int(len(rooms[room]["name"])/2) - 3) + rooms[room]["name"] + " "*(25 - int(len(rooms[room]["name"])/2) - 4) + "***")
            print("*"*50 + bcolors.ENDC)
            print(rooms[room]["description"])
            print(rooms[room]["details"])

def access(action):
    if rooms[currentRoom]["accessObject"] != "Empty":
        if rooms[currentRoom]["accessObject"].lower() in action:
            print("You accessed the " + rooms[currentRoom]["accessObject"])
            rooms[currentRoom]["accessed"] = "true"
        else:
            print(bcolors.YELLOW + "There is no " + action[4:] + " to access here." + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There are no objects to access in this room." + bcolors.ENDC)
    turn()

#textTest()
start()