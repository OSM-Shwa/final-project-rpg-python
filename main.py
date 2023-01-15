run = True
menu = True
play = False
rules = False

HP = 50
ATK = 3


def load_game():
    with open("load.txt", "r") as f:
        load_list = f.readlines()
        name = load_list[0].strip("\n")
        HP = load_list[1].strip("\n")
        ATK = load_list[2].strip("\n")
        print(name, HP, ATK)


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
        print("1. NEW GAME")
        print("2. LOAD GAME")
        print("3. RULES")
        print("4. QUIT GAME")

        if rules:
            print("I'm the creator of this game and these are the rules!")
            rules = False
            choice = ""
            input("> ")
        else:
            choice = input("# ")

        if choice == "1":
            name = input("What's your name, hero? ")
            menu = False
            play = True
        elif choice == "2":
            load_game()
        elif choice == "3":
            rules = True
        elif choice == "4":
            quit()

    while play:
        save_game()  # autosave

        print(name)

        dest = input("# ")
        if dest == "0":  # get back to main menu
            play = False
            menu = True
            save_game()
