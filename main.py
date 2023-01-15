import os

run = True
menu = True
play = False
rules = False

# player stats
HP = 50
ATK = 3

# clear the screen
def clear():
    os.system("clear")


def rules(rules):
    clear()
    draw()
    print("I'm the creator of this game and these are the rules!")
    draw()
    input("Press [enter] to return to menu: ")
    return False


# draw lines above the code
def draw():
    print("xX-------------------------Xx")


OPTIONS = ["NEW GAME", "LOAD GAME", "RULES", "QUIT GAME"]

# load a previous game
def load_game():
    with open("load.txt", "r") as f:
        load_list = [n.strip("\n") for n in f.readlines()]
        print(load_list)
        # name = load_list[0].strip("\n")
        # HP = load_list[1].strip("\n")
        # ATK = load_list[2].strip("\n")
        clear()
        print(f"Welcome back, {load_list[0]}")

    return load_list


# save the game to the load.txt file
def save_game():
    list = [
        name,
        str(HP),
        str(ATK),
    ]

    with open("load.txt", "w") as f:
        for item in list:
            f.write(item + "\n")


# main game loop
while run:
    while menu:
        clear()
        draw()
        for idx, option in enumerate(OPTIONS, start=1):
            print(f"{idx}. {option}")
        draw()

        choice = input("# ")

        if choice == "1":
            clear()
            name = input("# What's your name, hero? ")
            menu = False
            play = True
        elif choice == "2":
            name, HP, ATK = load_game()
            input("Press [enter] to continue: ")
            menu = False
            play = True
        elif choice == "3":
            choice = ""
            rules(rules)
        elif choice == "4":
            quit()

    while play:
        save_game()  # autosave

        clear()
        draw()
        print("0 - SAVE AND QUIT")
        draw()

        dest = input("# ")
        if dest == "0":  # get back to main menu
            play = False
            menu = True
            save_game()
