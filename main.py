import os
from map import map
from biomes import biomes

run = True
menu = True
play = False
rules = False
key = False


HP = 50
ATK = 3
pot = 1
elix = 0
gold = 0
row = 0
col = 0

return_to_menu = "Please [enter] to return to menu: "

row_len = len(map) - 1
col_len = len(map[0]) - 1

current_tile = map[row][col]
print(current_tile)
name_of_tile = biomes[current_tile]["t"]
print(name_of_tile)
enemy_tile = biomes[current_tile]["e"]
print(enemy_tile)

# clear the screen
def clear():
    os.system("clear")


def rules(rules):
    clear()
    draw()
    print("I'm the creator of this game and these are the rules!")
    draw()
    input(return_to_menu)
    return False


# draw lines above the code
def draw():
    print("xX-------------------------Xx")


OPTIONS = ["NEW GAME", "LOAD GAME", "RULES", "QUIT GAME"]

# load a previous game
def load_game():
    ...


# save the game to the load.txt file
def save_game():
    list = [
        name,
        str(HP),
        str(ATK),
        str(pot),
        str(elix),
        str(gold),
        str(x),
        str(y),
        str(key),
    ]
    with open("load.txt", "w") as f:
        for item in list:
            f.write(f"{item} \n")


# main game loop
while run:
    while menu:
        # clear()
        draw()
        for idx, option in enumerate(OPTIONS, start=1):
            print(f"{idx}. {option}")
        draw()
        choice = input("# ")

        if choice == "1":
            clear()
            name = input("# What's your name, hero? ").strip()
            menu = False
            play = True
        elif choice == "2":
            try:
                with open("load.txt", "r") as f:
                    load_list = f.readlines()
                    if len(load_list) == 9:
                        name = load_list[0][:-1].strip()
                        HP = int(load_list[1][:-1])
                        ATK = int(load_list[2][:-1])
                        pot = int(load_list[3][:-1])
                        elix = int(load_list[4][:-1])
                        gold = int(load_list[5][:-1])
                        x = int(load_list[6][:-1])
                        y = int(load_list[7][:-1])
                        key = bool(load_list[8][:-1])
                        clear()
                        print(f"Welcome back, {name}!")
                        input("Press [enter] to continue: ")
                        menu = False
                        play = True
                    else:
                        print("Corrupt save file!")
                        input(return_to_menu)
            except OSError:
                print("No loadable save file!")
                input(return_to_menu)

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
