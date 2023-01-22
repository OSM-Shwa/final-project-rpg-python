import os
import random
from typing import List

from biomes import biomes
from map import map

# game options
OPTIONS = ["NEW GAME", "LOAD GAME", "RULES", "QUIT GAME"]

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
        hp=50,
        atk=3,
        pot=10,
        elix=3,
        gold=100,
        x=0,
        y=0,
        key=False,
    ):
        self.name = name
        self.hp = hp
        self.HPMAX = 500
        self.atk = atk
        self.pot = pot
        self.elix = elix
        self.gold = gold
        self.x = x
        self.y = y
        self.key = key

    # sets the player's name
    def set_name(self):
        while True:
            self.name = input("# What's your name, hero? ").strip()
            if self.name == "":
                print("Invalid input. Try again.")
                continue
            break


# creates some enemies
class Enemy:
    def __init__(self, name: str, hp: int, atk: int, gold: int) -> None:
        self.name = name
        self.hp = hp
        self.atk = atk
        self.gold = gold

    def __str__(self):
        return self.name


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
    def display_rules(self):
        with open("rules.txt", "r") as f:
            draw()
            for line in f:
                print(line.strip("\n"))
            draw()
        input("> ")

    def display_game_info(player):
        draw()
        print(f"LOCATION: {biomes[map[player.y][player.x]]['t']}")
        draw()
        print(f"NAME: {player.name}")
        print(f"HP: {player.hp}/{player.HPMAX}")
        print(f"ATK: {player.atk}")
        print(f"POTIONS: {player.pot}")
        print(f"ELIXIR: {player.elix}")
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
        if player.hp < player.HPMAX:
            if player.pot > 0:
                print("5 - USE POTION (30HP)")
            if player.elix > 0:
                print("6 - USE ELIXIR (50HP)")
        if map[player.y][player.x] in ["shop", "mayor", "cave"]:
            print("7 - ENTER")
        draw()


# the main game
class Game:

    enemies = []

    # creates an enemy with these stats
    def create_enemy(self, name: str, hp: int, atk: int, gold: int):
        self.enemies.append(Enemy(name, hp, atk, gold))

    # when you start the game, create some enemies
    def __init__(self, ui: UI, player: Player):
        self.ui = ui
        self.player = player
        self.running = True
        self.menu = True
        self.play = False
        self.standing = True
        self.fight = False
        self.buy = False
        self.speak = False
        self.boss = False
        self.create_enemy("Goblin", 15, 3, 8)
        self.create_enemy("Ogre", 35, 5, 18)
        self.create_enemy("Slime", 30, 2, 12)
        self.boss = Boss("Dragon", 100, 8, 100)

    # saves the player's data to a file
    def save(self):
        list = [
            str(self.player.name),
            str(self.player.hp),
            str(self.player.atk),
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
    def load(self):
        # load a previous game

        with open("load.txt", "r") as f:
            load_list = f.readlines()
            if len(load_list) == 9:
                name = str(load_list[0][:-1].strip())
                hp = int(load_list[1][:-1])
                atk = int(load_list[2][:-1])
                pot = int(load_list[3][:-1])
                elix = int(load_list[4][:-1])
                gold = int(load_list[5][:-1])
                x = int(load_list[6][:-1])
                y = int(load_list[7][:-1])
                key = bool(load_list[8][:-1])
                self.ui.clear()
                print(f"Welcome back, {name}!")
                input("> ")
                self.menu = False
                self.play = True
                return self.player.__init__(
                    name=name,
                    hp=hp,
                    atk=atk,
                    pot=pot,
                    elix=elix,
                    gold=gold,
                    x=x,
                    y=y,
                    key=key,
                )
            else:
                print("\nCorrupt save file!")
                input("> ")

    def heal(self, amount):
        if self.player.hp + amount < self.player.HPMAX:
            self.player.hp += amount
        else:
            self.player.hp = self.player.HPMAX
        print(f"{self.player.name}'s HP refilled to {self.player.hp}!")

    def battle(self):
        enemy = random.choice(self.enemies)
        hp = enemy.hp
        hpmax = hp
        atk = enemy.atk
        gold = enemy.gold

        while self.fight:
            self.ui.clear()
            draw()
            print(f"Defeat the {enemy.name}!")
            draw()
            print(f"{enemy.name}'s HP: {hp}/{hpmax}")
            print(f"{self.player.name}'s HP: {self.player.hp}/{self.player.HPMAX}")
            print(f"POTIONS: {self.player.pot}")
            print(f"ELIXIR: {self.player.elix}")
            draw()
            print("1 - ATTACK")
            if self.player.pot > 0:
                print("2 - USE POTION (30HP)")
            if self.player.elix > 0:
                print("3 - USE ELIXIR (50HP)")
            draw()

            choice = input("# ")
            if choice == "1":
                hp -= self.player.atk
                print(f"You dealt {self.player.atk} damage to the {enemy.name}!")
                if hp > 0:
                    self.player.hp -= atk
                    print(f"{enemy.name} dealt {atk} damage to the you!")
                input("> ")
            elif choice == "2":
                if self.player.pot > 0:
                    self.player.pot -= 1
                    self.heal(30)
                    self.player.hp -= atk
                    print(f"{enemy.name} dealt {atk} damage to the you!")
                else:
                    print("No potions!")
                input("> ")
            elif choice == "3":
                if self.player.elix > 0:
                    self.player.elix -= 1
                    self.heal(50)
                    self.player.hp -= atk
                    print(f"{enemy.name} dealt {atk} damage to the you!")
                else:
                    print("No potions!")
                input("> ")

            if self.player.hp <= 0:
                print(f"{enemy.name} has defeated {self.player.name}...")
                draw()
                self.fight = False
                self.running = False
                self.play = False
                print("GAME OVER")
                input("> ")

            if hp <= 0:
                print(f"{self.player.name} has defeated the {enemy.name}!")
                draw()
                self.fight = False
                self.player.gold += gold
                print(f"You've found {gold} gold!")
                if random.randint(0, 100) < 30:
                    self.player.pot += 1
                    print("You've found a potion!")
                self.standing = True
                input("> ")

    def mayor(self):
        while self.speak:
            self.ui.clear()
            draw()
            print(f"Hello there, {self.player.name}!")
            if self.player.atk < 10:
                print(
                    "You are not strong enough to face the dragon yet. Keep practicing and come back later!"
                )
                self.player.key = False
            else:
                print(
                    "You might want to take on the dragon now! Take this key but be careful with the beast..."
                )
                self.player.key = True

            draw()
            print("1 - LEAVE")
            draw()

            choice = input("# ")
            if choice == "1":
                self.speak = False

    def shop(self):

        while self.buy:
            self.save()
            self.ui.clear()
            draw()
            print("Welcome to the shop!")
            draw()
            print(f"GOLD: {self.player.gold}")
            print(f"POTIONS: {self.player.pot}")
            print(f"ELIXIR: {self.player.elix}")
            print(f"ATK: {self.player.atk}")
            draw()
            print("1 - BUY POTION (30HP) - 5 GOLD")
            print("2 - BUY ELIXIR (50HP) - 8 GOLD")
            print("3 - UPGRADE WEAPON (+2ATK) - 10 GOLD")
            print("4 - LEAVE")
            draw()

            choice = input("# ")
            if choice == "1":
                if self.player.gold >= 5:
                    self.player.pot += 1
                    self.player.gold -= 5
                    print("You've bought a potion!")
                else:
                    print("You don't have enough gold for this item...")
                input("> ")
            elif choice == "2":
                if self.player.gold >= 8:
                    self.player.elix += 1
                    self.player.gold -= 8
                    print("You've bought an elixir!")
                else:
                    print("You don't have enough gold for this item...")
                input("> ")
            elif choice == "3":
                if self.player.gold >= 10:
                    self.player.atk += 2
                    self.player.gold -= 10
                    print("You've upgraded your weapon!")
                else:
                    print("You don't have enough gold for this item...")
                input("> ")
            elif choice == "4":
                self.buy = False

    def cave(self):
        while self.boss:
            self.ui.clear()
            draw()
            print(f"Here lies the cave of the {self.boss.name}. What will you do?")
            draw()

            if self.player.key:
                print("1 - USE KEY")
            print("2 - TURN BACK")

    def action(self, dest):
        if dest == "0":  # get back to main menu
            self.play = False
            self.menu = True
            self.save()
        if dest == "1":
            if self.player.y > 0:
                self.player.y -= 1
                self.standing = False
        elif dest == "2":
            if self.player.x < x_len:
                self.player.x += 1
                self.standing = False
        elif dest == "3":
            if self.player.y < y_len:
                self.player.y += 1
                self.standing = False
        elif dest == "4":
            if self.player.x > 0:
                self.player.x -= 1
                self.standing = False
        elif dest == "5":
            if self.player.hp == self.player.HPMAX:
                print("Health is already full!")
            elif self.player.pot > 0:
                self.player.pot -= 1
                self.heal(40)
            else:
                print("No potions!")
            input("> ")
        elif dest == "6":
            if self.player.hp == self.player.HPMAX:
                print("Health is already full!")
            elif self.player.elix > 0:
                self.player.elix -= 1
                self.heal(50)
            else:
                print("No elixir!")
            input("> ")
        elif dest == "7":
            if map[self.player.y][self.player.x] == "shop":
                self.buy = True
                self.shop()
            elif map[self.player.y][self.player.x] == "mayor":
                self.speak = True
                self.mayor()
            elif map[self.player.y][self.player.x] == "cave":
                self.boss = True
        else:
            self.standing = True

    def run(self):
        while self.running:
            while self.menu:
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
                    self.menu = False
                    self.play = True
                elif choice == "2":
                    try:
                        self.load()
                    except OSError:
                        print("\nNo loadable save file!")
                        input("> ")

                elif choice == "3":
                    choice = ""
                    self.ui.display_rules()
                elif choice == "4":
                    quit()

            while self.play:
                self.save()  # autosave

                if not self.standing:
                    if biomes[map[player.y][player.x]]["e"]:
                        if random.randint(0, 100) < 0:
                            self.fight = True
                            self.battle()

                self.ui.clear()

                if self.play:
                    self.ui.display_game_info(player)
                    action = input("# ")
                    self.action(action)


if __name__ == "__main__":
    player = Player()
    ui = UI(player)
    game = Game(UI, player)
    game.run()
