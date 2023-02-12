import json
import time

# the player
class Player:

    # sets all the player variables/stats
    def __init__(
        self,
        name="",
        hp=100,
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

def save_player(player: dict, players: dict) -> None:
    players[player['name']] = player
    with open('players.json', 'w') as myfile:
        json.dump(players, myfile, indent=2)



def read():
    # read file
    while True:
        try:
            with open('players.json', 'r') as myfile:
                data = myfile.read()
                assert isinstance(data, str), "Empty file..."
                # parse file
                obj = json.loads(data)
                return obj
        # if the file doesn't exist
        except FileNotFoundError:
            with open('players.json', 'w') as myfile:
                myfile.write("{}")
        

while True:
    name = input('Enter player name: ').title()
    if len(name) >= 1: break
    
players = read()
if name == players.get(name,{}).get('name'):
    print(f'Player "{name}" was found in the file. Loading player now...')
    time.sleep(3)
    player = players[name]
else:
    print(f'Player "{name}" is not found in the file. Creating a new player...')
    new_player = Player()
    new_player.name = name 
    time.sleep(3)
    player = vars(new_player)

# player['hp'] = player.get('hp') + 10000
save_player(player, players)
players = read()