import os
import random


from biomes import biomes
from map import map

players = dict()
        
# stuff for map
y_len = len(map) - 1
x_len = len(map[0]) - 1

def read_int(prompt: str, min_value: int = 0, max_value: int = 5) -> int:
    """Read an integer between a min and max value."""
    
    while True:
        line = input(prompt)
        try:
            value = int(line)
            if value < min_value:
                print(f"The minimum value is {min_value}. Try again.")
            elif value > max_value:
                print(f"The maximum value is {max_value}. Try again.")
            else:
                return value
        except ValueError:
            print("That's not a number! Try again.")


def invalid():
    print("Invalid option")
    input("> ")
    
    
def draw() -> None:
    """draw lines above the code """
    
    print("xX-------------------------Xx")

def display_rules() -> None:
    with open("rules.txt", "r") as f:
        draw()
        for line in f:
            print(line.strip("\n"))
        draw()
    input("> ")

def clear():
    """clear the screen"""
    os.system("clear")


def get_player_name():
    clear()
    while True:
        name = input("# What's your name, hero? ").strip()
        if name == "":
            print("Invalid input. Try again.")
            continue
        return name


# the player
class Player:

    # sets all the player variables/stats
    def __init__(
        self,
        name="",
        hp=50,
        atk=3,
        pot=6,
        elix=3,
        gold=50,
        x=0,
        y=0,
        key=0,
    ):
        self.name = name
        self.hp = hp
        self.HPMAX = 200
        self.atk = atk
        self.pot = pot
        self.elix = elix
        self.gold = gold
        self.x = x
        self.y = y
        self.key = key

    def __repr__(self):
        return f"Player: {self.name}"

# creates some enemies
class Enemy:
    def __init__(self, name: str, hp: int, atk: int, gold: int) -> None:
        self.name = name
        self.hp = hp
        self.atk = atk
        self.gold = gold

# the main game
class Game:

    enemies = list()

    # creates an enemy with these stats
    def create_enemy(self, name: str, hp: int, atk: int, gold: int):
        self.enemies.append(Enemy(name, hp, atk, gold))

        
    def display_game_info(self):
        draw()
        print(f"LOCATION: {biomes[map[self.player.y][self.player.x]]['t']}")
        draw()
        print(f"NAME: {self.player.name}")
        print(f"HP: {self.player.hp}/{self.player.HPMAX}")
        print(f"ATK: {self.player.atk}")
        print(f"POTIONS: {self.player.pot}")
        print(f"ELIXIR: {self.player.elix}")
        print(f"GOLD: {self.player.gold}")
        print(f"COORDS: {self.player.x},{self.player.y}")
        draw()
        print("0 - SAVE AND QUIT")
        if self.player.y > 0:
            print("1 - NORTH")
        if self.player.x < x_len:
            print("2 - EAST")
        if self.player.y < y_len:
            print("3 - SOUTH")
        if self.player.x > 0:
            print("4 - WEST")
        if self.player.hp < self.player.HPMAX:
            if self.player.pot > 0:
                print("5 - USE POTION (30HP)")
            if self.player.elix > 0:
                print("6 - USE ELIXIR (50HP)")
        if map[self.player.y][self.player.x] in ["shop", "mayor", "cave"]:
            print("7 - ENTER")
        draw()
    
    # when you start the game, create some enemies
    def __init__(self):
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
        self.b = Enemy("Dragon", 100, 8, 100)
        self.GAME_OPTIONS = {
        "new game": self.new_game,
        "load game": self.load,
        "rules":self.rules,
        "quit":quit
        }

    # saves the player's data
    def save(self):
        players[self.player.name] = self.player

    # retrieves the player's data and uses that to load the game
    def load(self):
        # load a previous game
         while True:   
            name = get_player_name()
            self.player = players.get(name, None)
            if self.player is not None:
                print(f"Welcome back, {name}!")
                input("> ")
                self.menu = False
                self.play = True
                break
            else:
                choice = self.player_dne()
                if choice == 1:
                    break
                else:
                    continue
                
    @staticmethod
    def player_dne():
        print("Player does not exist.")
        input("> ")
        while True:
            draw()
            print("1 - Return to Main Menu")
            print("2 - Try again")
            draw()
            choice = input("# ")
            if choice == "1":
                return 1
            elif choice == "2":
                return 2
            else:
                print("Invalid choice. Try again.")

         
            
    def heal(self, amount):
        if self.player.hp + amount < self.player.HPMAX:
            self.player.hp += amount
        else:
            self.player.hp = self.player.HPMAX
        print(f"{self.player.name}'s HP refilled to {self.player.hp}!")

    def battle(self):
        if not self.boss:
            enemy = random.choice(self.enemies)
        else:
            enemy = self.b
        hp = enemy.hp
        hpmax = hp
        atk = enemy.atk
        gold = enemy.gold

        while self.fight:
            clear()
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

            choice = read_int("# ", max_value=3)
            if choice == 1:
                hp -= self.player.atk
                print(f"You dealt {self.player.atk} damage to the {enemy.name}!")
                if hp > 0:
                    self.player.hp -= atk
                    print(f"{enemy.name} dealt {atk} damage to the you!")
                input("> ")
            elif choice == 2:
                if self.player.pot > 0:
                    self.player.pot -= 1
                    self.heal(30)
                    self.player.hp -= atk
                    print(f"{enemy.name} dealt {atk} damage to the you!")
                else:
                    print("No potions!")
                input("> ")
            elif choice == 3:
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
                if enemy == self.b:
                    draw()
                    print("Congradulations, you have finished the game!")
                    self.boss = False
                    self.running = False
                    self.play = False

                self.save()
                input("> ")

    def mayor(self):
        while self.speak:
            clear()
            draw()
            print(f"Hello there, {self.player.name}!")
            if self.player.atk < 10:
                print(
                    "You are not strong enough to face the dragon yet. Keep practicing and come back later!"
                )
                self.player.key = 0
            else:
                print(
                    "You might want to take on the dragon now! Take this key but be careful with the beast..."
                )
                self.player.key = 1

            draw()
            print("1 - LEAVE")
            draw()

            choice = read_int("# ", max_value=1)
            if choice == 1:
                self.speak = False

    def shop(self):

        while self.buy:
            self.save()
            clear()
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

            choice = read_int("# ", max_value=4)
            if choice == 1:
                if self.player.gold >= 5:
                    self.player.pot += 1
                    self.player.gold -= 5
                    print("You've bought a potion!")
                else:
                    print("You don't have enough gold for this item...")
                input("> ")
            elif choice == 2:
                if self.player.gold >= 8:
                    self.player.elix += 1
                    self.player.gold -= 8
                    print("You've bought an elixir!")
                else:
                    print("You don't have enough gold for this item...")
                input("> ")
            elif choice == 3:
                if self.player.gold >= 10:
                    self.player.atk += 2
                    self.player.gold -= 10
                    print("You've upgraded your weapon!")
                else:
                    print("You don't have enough gold for this item...")
                input("> ")
            elif choice == 4:
                self.buy = False

    def cave(self):
        while self.boss:
            clear()
            draw()
            print(f"Here lies the cave of the {self.b.name}. What will you do?")
            draw()

            if self.player.key == 1:
                print("1 - USE KEY")
            print("2 - TURN BACK")

            choice = read_int("# ", max_value=2)
            if choice == 1:
                if self.player.key == 1:
                    self.fight = True
                    self.battle()
            elif choice == 2:
                self.boss = False

    def action(self, action):
        match action:
            case 0:
                self.play = False
                self.menu = True
                self.save()
            case 1:
                if self.player.y > 0:
                    self.player.y -= 1
                    self.standing = False
            case 2:
                if self.player.x < x_len:
                    self.player.x += 1
                    self.standing = False
            case 3:
                if self.player.y < y_len:
                    self.player.y += 1
                    self.standing = False
            case 4:
                if self.player.x > 0:
                    self.player.x -= 1
                    self.standing = False
            case 5:
                if self.player.hp == self.player.HPMAX:
                    print("Health is already full!")
                elif self.player.pot > 0:
                    self.player.pot -= 1
                    self.heal(40)
                else:
                    print("No potions!")
                input("> ")
            case 6:
                if self.player.hp == self.player.HPMAX:
                    print("Health is already full!")
                elif self.player.elix > 0:
                    self.player.elix -= 1
                    self.heal(50)
                else:
                    print("No elixir!")
                input("> ")
            case 7:
                if map[self.player.y][self.player.x] == "shop":
                    self.buy = True
                    self.shop()
                elif map[self.player.y][self.player.x] == "mayor":
                    self.speak = True
                    self.mayor()
                elif map[self.player.y][self.player.x] == "cave":
                    self.boss = True
                    self.cave()
            case other:
                self.standing = True
    
    def create_player(self, name: str):
        players[name] = Player(name=name)
        self.player = players[name]
    
    def new_game(self):
        self.create_player(name=get_player_name())
        self.menu = False
        self.play = True

    def rules(self):
        display_rules()
        return ""
        
    def start(self, option: str) -> str:
        return self.GAME_OPTIONS.get(option, invalid)()

    def display_game_options(self):
        for key in self.GAME_OPTIONS.keys():
            print(f"- {key}")
    
    def run(self):
        while self.running:
            while self.menu:
                clear()
                draw()
                
                # print the options to the screen
                self.display_game_options()
                draw()
                choice = input("")
                self.start(choice)
                

            while self.play:
                self.save()  # autosave

                if not self.standing:
                    if biomes[map[self.player.y][self.player.x]]["e"]:
                        if random.randint(0, 100) <= 30:
                            self.fight = True
                            self.battle()

                clear()
                if self.play:
                    self.display_game_info()
                    action = read_int("# ", max_value=7)
                    self.action(action)



def main() -> None:
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
