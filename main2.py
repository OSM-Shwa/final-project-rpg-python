import os
from map import map
from biomes import biomes

run = True
menu = True
play = False

# all game stats
# stats = {
#     "name": "",
#     "HP": 50,
#     "HPMAX": 50,
#     "ATK": 3,
#     "POT": 1,
#     "ELIXIR": 0,
#     "GOLD": 0,
#     "x": 0,
#     "y": 0,
#     "key": 0,
# }

# game variables
HP = 50
HPMAX = HP
ATK = 3
pot = 1
elix = 0
gold = 0
x = 0  # col
y = 0  # row
key = 0

# game options
OPTIONS = ["NEW GAME", "LOAD GAME", "RULES", "QUIT GAME"]

return_to_menu = "Press [enter] to return to menu: "

# stuff for map
y_len = len(map) - 1
x_len = len(map[0]) - 1
current_tile = map[y][x]
name_of_tile = biomes[current_tile]["t"]
enemy_tile = biomes[current_tile]["e"]


# clear the screen
def clear():
    os.system("clear")


# the game rules
def rules():
    clear()
    draw()

    draw()
    input(return_to_menu)


# draw lines above the code
def draw():
    print("xX-------------------------Xx")


# load a previous game
def load_game():
    global menu, play, HP, ATK, pot, elix, gold, x, y, key

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
            key = int(load_list[8][:-1])
            clear()
            print(f"Welcome back, {name}!")
            input("Press [enter] to continue: ")
            menu = False
            play = True
        else:
            print("\nCorrupt save file!")
            input(return_to_menu)


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
def main():
    global run, menu, play, x_len, y_len, stats, x, y, name
    while run:
        while menu:
            clear()
            draw()
            # print the options to the screen
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
                    load_game()
                except OSError:
                    print("\nNo loadable save file!")
                    input(return_to_menu)

            elif choice == "3":
                choice = ""
                rules(rules)
            elif choice == "4":
                quit()

        while play:
            save_game()  # autosave

            print()
            draw()
            print(f"LOCATION: {biomes[map[y][x]]['t']}")
            draw()
            print(f"NAME: {name}")
            print(f"HP: {HP}/{HPMAX}")
            print(f"ATK: {ATK}")
            print(f"POTIONS: {pot}")
            print(f"ELIXIRS: {elix}")
            print(f"GOLD: {gold}")
            print(f"COORDS: {x},{y}")
            draw()
            print("0 - SAVE AND QUIT")
            if y > 0:
                print("1 - NORTH")
            if x < x_len:
                print("2 - EAST")
            if y < y_len:
                print("3 - SOUTH")
            if x > 0:
                print("4 - WEST")
            draw()

            dest = input("# ")
            if dest == "0":  # get back to main menu
                play = False
                menu = True
                save_game()
            elif dest == "1":
                if y > 0:
                    y -= 1
            elif dest == "2":
                if x < x_len:
                    x += 1
            elif dest == "3":
                if y < y_len:
                    y += 1
            elif dest == "4":
                if x > 0:
                    x -= 1


if __name__ == "__main__":
    main()
