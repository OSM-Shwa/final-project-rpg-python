run = True
menu = True
play = False
rules = False

HP = 50
ATK = 3


def save():
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
            pass
        elif choice == "3":
            rules = True
        elif choice == "4":
            quit()

    while play:
        print(name)

        dest = input("# ")
        if dest == "0":  # get back to main menu
            play = False
            menu = True
