import os

run = True
menu = True
play = False
rules = False

HP = 50
ATK = 3


def clear():
    os.system("clear")


def draw():
    print("xX-------------------------xX")


def load_game():
    with open("load.txt", "r") as f:
        load_list = f.readlines()
        name = load_list[0].strip("\n")
        HP = load_list[1].strip("\n")
        ATK = load_list[2].strip("\n")
        clear()
        print(f"Welcome back, {name}")

    return [name, HP, ATK]


def save_game():
    list = [
        name,
        str(HP),
        str(ATK),
    ]

    with open("load.txt", "w") as f:
        for item in list:
            f.write(item + "\n")


while run:
    while menu:
        clear()
        draw()
        print("1. NEW GAME")
        print("2. LOAD GAME")
        print("3. RULES")
        print("4. QUIT GAME")
        draw()

        if rules:
            print("I'm the creator of this game and these are the rules!")
            rules = False
            choice = ""
            input("> ")
        else:
            choice = input("# ")

        if choice == "1":
            clear()
            name = input("What's your name, hero? ")
            menu = False
            play = True
        elif choice == "2":
            name, HP, ATK = load_game()
            input(">")
            menu = False
            play = True
        elif choice == "3":
            rules = True
        elif choice == "4":
            quit()

    while play:
        save_game()  # autosave

        draw()
        print("0 - SAVE AND QUIT")
        draw()

        dest = input("# ")
        if dest == "0":  # get back to main menu
            play = False
            menu = True
            save_game()
