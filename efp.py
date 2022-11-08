import yaml
import os
import platform

# Class that allows me to create colored text output
class bcolors:
    PINK = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

# Global Variables
with open("Rooms.yaml", "r") as file:
    rooms = yaml.safe_load(file)

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

# Checks if the conditions for winning are met or not and takes action based on that
# This is the centerpoint of most functions, as this usually ends up getting called in those functions
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

# Displays the player's inventory if it is not empty, if it is empty, it displays a message saying that
def inventory():
    if playerInventory != []:
        print(bcolors.BLUE + "This is your inventory:" + bcolors.ENDC)
        for item in playerInventory:
            print(bcolors.CYAN + item + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There is nothing in your inventory." + bcolors.ENDC)
    turn()

# Moves the player through whichever door corresponds to the direction they said in their command
# Displays different messages based on whether the player is able to go that direction or not
# Some rooms in my alphanumeric grid don't exist in the story, so I have to check if the room that the player wants to go to is empty or not
# Some rooms in this are locked, so I have to check that as well
def go(action):
    global currentRoom
    if action == "go north":
        nextRoom = rooms[currentRoom]["northDoor"]
        if rooms[currentRoom]["northDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["northDoor"]
            displayTitleDescription()
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
            displayTitleDescription()
            turn()
        elif rooms[currentRoom]["southDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            displayTitleDescription()
            print(lockedMessage)
            choice()
        else:
            displayTitleDescription()
            print(blockedMessage)
            choice()
    elif action == "go east":
        nextRoom = rooms[currentRoom]["eastDoor"]
        if rooms[currentRoom]["eastDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["eastDoor"]
            displayTitleDescription()
            turn()
        elif rooms[currentRoom]["eastDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            displayTitleDescription()
            print(lockedMessage)
            choice()
        else:
            displayTitleDescription()
            print(blockedMessage)
            choice()
    elif action == "go west":
        nextRoom = rooms[currentRoom]["westDoor"]
        if rooms[currentRoom]["westDoor"] != "Empty" and rooms[nextRoom]["locked"] == "false":
            currentRoom = rooms[currentRoom]["westDoor"]
            displayTitleDescription()
            turn()
        elif rooms[currentRoom]["westDoor"] != "Empty" and rooms[nextRoom]["locked"] == "true":
            displayTitleDescription()
            print(lockedMessage)
            choice()
        else:
            displayTitleDescription()
            print(blockedMessage)
            choice()
    else:
        displayTitleDescription()
        print(wrongMessage)
        turn()

# Gives the player a prompt to see what they want to do, then based on that prompt it calls the corresponding function(s)
# If the player inputs an invalid prompt, it displays a message saying that
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
        displayTitleDescription()
        turn()
    elif action[0:2] == "ac":
        access(action)
    else:
        print(wrongMessage)
        turn()

# Displays the details of the room
def look():
    global currentRoom
    roomTitle()
    print(bcolors.CYAN + rooms[currentRoom]["details"] + bcolors.ENDC)
    turn()

# Tests if any of the 4 adjacent rooms to the current room are not empty and are locked
# Then makes a list based off of what adjacent rooms pass that test
# Then checks if the item that the player specified in their command is usable on those rooms
# If the item matches a room, it gets unlocked
# Displays a message based on whether or not the item was usable
# Displays various messages depending on what the player put in their command
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
            if lockedRooms == []:
                print(bcolors.YELLOW + "You cannot use that here" + bcolors.ENDC)
            for room in lockedRooms:
                if loweredItem != rooms[room]["keyItem"].lower(): 
                    continue
                elif loweredItem == rooms[room]["keyItem"].lower():
                    print(bcolors.CYAN + "You use the " + rooms[room]["keyItem"] + " on the " + rooms[room]["name"] + bcolors.ENDC)
                    rooms[room]["locked"] = "false"
                    break
                else:
                    print(bcolors.YELLOW + "That item can't be used here." + bcolors.ENDC)
        else:
            print(bcolors.YELLOW + "That item is not in your inventory." + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There is nothing to use." + bcolors.ENDC)
    turn()

# Tests if the current room has an item in it
# Then tests if the item the player specified in their command is the item in the room
# If it is, it adds the item to the player's inventory, displays a message, and removes the item from the room
# Displays messages based on if either of those tests fail
def get(playerInventory, action):
    global currentRoom
    if rooms[currentRoom]["item"] != "Empty":
        if rooms[currentRoom]["item"].lower() in action:
            playerInventory.append(rooms[currentRoom]["item"])
            print(bcolors.CYAN + "You got the " + rooms[currentRoom]["item"] + bcolors.ENDC)
            rooms[currentRoom]["item"] = "Empty"
        else:
            print(bcolors.YELLOW + "There is no " + action[4:] + " here." + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There are no items to get in this room." + bcolors.ENDC)
    turn()

# Displays the title of the current room
# Accounts for even and odd amounts of characters
def roomTitle():
    global currentRoom
    print(bcolors.BLUE + "*"*50)
    if len(rooms[currentRoom]["name"]) % 2 == 0:
        print("***" + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 3) + rooms[currentRoom]["name"] + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 3) + "***")
    else:
        print("***" + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 3) + rooms[currentRoom]["name"] + " "*(25 - int(len(rooms[currentRoom]["name"])/2) - 4) + "***")
    print("*"*50 + bcolors.ENDC)

# Clears the screen
# Accounts for the player's operating system
def clearScreen():
    if platform.system() == "Windows":
        clear = lambda: os.system("cls")
    else:
        clear = lambda: os.system("clear")
    clear()

# Starts the game
# Reads in the intro text files and displays them
# Then displays the starting room's title and description
def start():
    with open("title.txt") as titleFile:
        title = titleFile.read()
    with open("ship.txt") as shipFile:
        ship = shipFile.read()
    with open("wakeUp.txt") as wakeUpFile:
        wakeUp = wakeUpFile.read()
    print(bcolors.YELLOW)
    print(title)
    titleFile.close()
    print(bcolors.RED)
    print(ship)
    shipFile.close()
    print(bcolors.ENDC)
    input(" "*36 + "Press enter to continue")
    help()
    print(bcolors.CYAN)
    clearScreen()
    print(wakeUp)
    wakeUpFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    clearScreen()
    displayTitleDescription()
    turn()

# Exits the program
def exitFunction():
    exit()

# Reads in the text files for the game instructions and displays them one by one
def help():
    with open("backstory.txt") as backstoryFile:
        backstory = backstoryFile.read()
    with open("listOfCommands.txt") as listOfCommandsFile:
        listOfCommands = listOfCommandsFile.read()
    with open("commandInstructions.txt") as commandInstructionsFile:
        commandInstructions = commandInstructionsFile.read()
    with open("loneCommands.txt") as loneCommandsFile:
        loneCommands = loneCommandsFile.read()
    with open("addonCommands.txt") as addonCommandsFile:
        addonCommands = addonCommandsFile.read()
    with open("reminder.txt") as reminderFile:
        reminder = reminderFile.read()
    print(bcolors.CYAN)
    clearScreen()
    print(backstory)
    backstoryFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    print(bcolors.CYAN)
    clearScreen()
    print(commandInstructions)
    commandInstructionsFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    print(bcolors.CYAN)
    clearScreen()
    print(listOfCommands)
    listOfCommandsFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    print(bcolors.CYAN)
    clearScreen()
    print(loneCommands)
    loneCommandsFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    print(bcolors.CYAN)
    clearScreen()
    print(addonCommands)
    addonCommandsFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    print(bcolors.CYAN)
    clearScreen()
    print(reminder)
    reminderFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    clearScreen()

# Reads in the ending text files and displays them, then exits the game
def win():
    with open("escape.txt") as escapeFile:
        escape = escapeFile.read()
    with open("destroyedShip.txt") as destroyedShipFile:
        destroyedShip = destroyedShipFile.read()
    with open("congratulations.txt") as congratulationsFile:
        congratulations = congratulationsFile.read()
    with open("escapePod.txt") as escapePodFile:
        escapePod = escapePodFile.read()
    clearScreen()
    print(bcolors.CYAN)
    print(escape)
    escapeFile.close()
    print(bcolors.RED)
    print(destroyedShip)
    destroyedShipFile.close()
    print(bcolors.ENDC)
    input("Press enter to continue")
    clearScreen()
    print(bcolors.YELLOW)
    print(congratulations)
    congratulationsFile.close()
    print(bcolors.RED)
    print(escapePod)
    escapePodFile.close()
    print(bcolors.ENDC)
    input("Press enter to exit the game")
    exitFunction()

# Tests if the current room has an accessible object in it
# Then tests if the object the player specified in their command is the object in the room
# If it is, it marks the object as accessed and displays a message
# Displays messages based on if either of those tests fail
def access(action):
    if rooms[currentRoom]["accessObject"] != "Empty":
        if rooms[currentRoom]["accessObject"].lower() in action:
            print(bcolors.CYAN + "You accessed the " + rooms[currentRoom]["accessObject"] + bcolors.ENDC)
            rooms[currentRoom]["accessed"] = "true"
        else:
            print(bcolors.YELLOW + "There is no " + action[4:] + " to access here." + bcolors.ENDC)
    else:
        print(bcolors.YELLOW + "There are no objects to access in this room." + bcolors.ENDC)
    turn()

def displayTitleDescription():
    global currentRoom
    roomTitle()
    print(bcolors.CYAN + rooms[currentRoom]["description"] + bcolors.ENDC)

# Called to start the game
start()