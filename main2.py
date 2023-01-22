import os
import random
from typing import List

from biomes import biomes
from map import map

run = True
menu = True
play = False
key = False
standing = True
fight = False

# game options
OPTIONS = ["NEW GAME", "LOAD GAME", "RULES", "QUIT GAME"]

return_to_menu = "Press [enter] to return to menu: "

# stuff for map
y_len = len(map) - 1
x_len = len(map[0]) - 1


def draw():
    print("xX-------------------------Xx")


# the player
class Player:

    # sets all the player variables/stats
    def __init__(
        self,
        name="",
        HP=50,
        HPMAX=50,
        ATK=3,
        pot=1,
        elix=0,
        gold=0,
        x=0,
        y=0,
        key=False,
    ):
        self.name = name
        self.HP = HP
        self.HPMAX = HPMAX
        self.ATK = ATK
        self.pot = pot
        self.elix = elix
        self.gold = gold
        self.x = x
        self.y = y
        self.key = False

    # sets the player's name
    def set_name(self):
        self.name = input("# What's your name, hero? ").strip()


# creates some enemies
class Enemy:
    def __init__(self, name: str, hp: int, atk: int, gold: int) -> None:
        self.name = name
        self.hp = hp
        self.atk = atk
        self.gold = gold


# this is the boss class which has all the same variables as a regular enemy
class Boss(Enemy):
    def __init__(self, name: str, hp: int, atk: int, gold: int):
        super().__init__(name, hp, atk, gold)


# handles displaying things
class UI:
    def __init__(self, player: Player):
        self.player = player

    # clear the screen
    def clear():
        os.system("clear")

    # draw lines above the code
    @classmethod
    def display_rules(self):
        with open("rules.txt", "r") as f:
            draw()
            for line in f:
                print(line.strip("\n"))
            draw()
        input(return_to_menu)

    def display_game_info(player):
        print()
        draw()
        print(f"LOCATION: {biomes[map[player.y][player.x]]['t']}")
        draw()
        print(f"NAME: {player.name}")
        print(f"HP: {player.HP}/{player.HPMAX}")
        print(f"ATK: {player.ATK}")
        print(f"POTIONS: {player.pot}")
        print(f"ELIXIRS: {player.elix}")
        print(f"GOLD: {player.gold}")
        print(f"COORDS: {player.x},{player.y}")
        draw()
        print("0 - SAVE AND QUIT")
        if player.y > 0:
            print("1 - NORTH")
        if player.x < x_len:
            print("2 - EAST")
        if player.y < y_len:
            print("3 - SOUTH")
        if player.x > 0:
            print("4 - WEST")
        draw()


# the main game
class Game:

    enemies = {}

    # creates an enemy with these stats
    def create_enemy(self, name: str, hp: int, atk: int, gold: int):
        self.enemies.append(Enemy(name, hp, atk, gold))

    # when you start the game, create some enemies
    def __init__(self, ui: UI, player: Player):
        self.create_enemy("Goblin", 15, 3, 8)
        self.create_enemy("Ogre", 35, 5, 18)
        self.create_enemy("Slime", 30, 2, 12)
        self.ui = ui
        self.player = player
        # boss = Boss("Dragon", 100, 8, 100)

    # saves the player's data to a file
    def save(self):
        list = [
            self.player.name,
            str(self.player.HP),
            str(self.player.ATK),
            str(self.player.pot),
            str(self.player.elix),
            str(self.player.gold),
            str(self.player.x),
            str(self.player.y),
            bool(self.player.key),
        ]

        with open("load.txt", "w") as f:
            for item in list:
                f.write(f"{item} \n")

    # retrieves the player's data and uses that to load the game
    def load(self) -> Player:
        global menu, play
        # load a previous game

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
                self.ui.clear()
                print(f"Welcome back, {name}!")
                input("Press [enter] to continue: ")
                menu = False
                play = True
                return self.player.__init__(name, HP, ATK, pot, elix, gold, x, y, key)
            else:
                print("\nCorrupt save file!")
                input(return_to_menu)

    def battle(self):
        pass

    def move_locations(self, dest):
        if dest == "1":
            if self.player.y > 0:
                self.player.y -= 1
                standing = False
        elif dest == "2":
            if self.player.x < x_len:
                self.player.x += 1
                standing = False
        elif dest == "3":
            if self.player.y < y_len:
                self.player.y += 1
                standing = False
        elif dest == "4":
            if self.player.x > 0:
                self.player.x -= 1
                standing = False

    def run(self):
        global menu, run, play
        while run:
            while menu:
                self.ui.clear()
                draw()
                # print the options to the screen
                for idx, option in enumerate(OPTIONS, start=1):
                    print(f"{idx}. {option}")
                draw()
                choice = input("# ")

                if choice == "1":
                    self.ui.clear()
                    self.player.set_name()
                    menu = False
                    play = True
                elif choice == "2":
                    try:
                        self.player = self.load()
                        print(player)
                    except OSError:
                        print("\nNo loadable save file!")
                        input(return_to_menu)

                elif choice == "3":
                    choice = ""
                    self.ui.display_rules()
                elif choice == "4":
                    quit()

            while play:
                self.save()  # autosave

                if not standing:
                    if biomes[map[player.y][player.x]]["e"]:
                        if random.randint(1, 100) <= 30:
                            fight = True
                            self.battle()

                self.ui.display_game_info(player)
                dest = input("# ")
                if dest == "0":  # get back to main menu
                    play = False
                    menu = True
                    self.save()
                self.move_locations(dest)


if __name__ == "__main__":
    player = Player()
    ui = UI(player)
    game = Game(UI, player)
    game.run()
