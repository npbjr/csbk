import uuid
from typing import cast


class MakeAttribute(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class CellObject:
    def __init__(self, y=0, x=0):
        pos = MakeAttribute()
        pos.y = y
        pos.x = x
        self.player_id = None
        self.items = None
        self.position = pos

    def get_position(self):
        return self.position

    def get_player_id(self):
        return self.player_id


class Item:
    def __init__(self, y=0, x=0, name=""):
        pos = MakeAttribute()
        pos.y = y
        pos.x = x
        self.position = pos
        self.item_name = name
        self.attack = 0
        self.defence = 0
        self.equiped = False

    def get_bonus(self):
        bonus = {
            "axe": {"attack": 2, "defence": 0},
            "dagger": {"attack": 1, "defence": 0},
            "helmet": {"attack": 0, "defence": 1},
            "majic_staff": {"attack": 1, "defence": 1},
        }
        bo = bonus[self.item_name]
        return bo

    def set_attack(self, value):
        self.attack = value

    def set_defence(self, value):
        self.defence = value


class Board:
    def __init__(self):
        self.cell_data = []
        self.players = []

        "#generate data"

        for i in range(0, 8):

            for r in range(0, 8):
                cell = CellObject()
                cell.position.y = r
                cell.position.x = i
                self.cell_data.append(cell)

            for r in range(0, 8):
                cell = CellObject()
                cell.position.y = i
                cell.position.x = r
                self.cell_data.append(cell)

    def save_final_player_data(self, p):
        self.players = p

    def add_item_position(self, item_data):
        for idx, item in enumerate(self.cell_data):
            pos = item.get_position()
            if item_data.position == pos:
                self.cell_data[idx].items = item_data
                break

    def add_player_position(self, player):
        for idx, item in enumerate(self.cell_data):
            pos = item.get_position()
            if player.position == pos:
                self.cell_data[idx].player_id = player.id
                # self.update_player_id_position(player, player)
                break

    def insert_player_if_not(self, player):

        if not (any(cast(Player, i).id == player.id for i in self.players)):
            self.players.append(player)

        print("players ", self.players)

    def update_player_id_position(self, old_player_data, new_player_data):
        self.insert_player_if_not(old_player_data)
        havewon = self.check_fight(new_player_data)
        if havewon:
            return
        for i, item in enumerate(self.cell_data):
            pos = item.get_position()
            item_data = item.items
            # update correct player cell
            if new_player_data.position == pos:
                print(" INSERTING NEW PLAYER ", new_player_data.player_name)
                self.cell_data[i].player_id = new_player_data.id
                # check cell item and update player
                if item_data is not None and item_data.position == pos:
                    item_data.equiped = True
                    bonus = item_data.get_bonus()

                    if bonus:
                        print(" BONUS FOUND for ", old_player_data.player_name, bonus)
                        old_player_data.defence = bonus["defence"]
                        old_player_data.attack = bonus["attack"]
                        print(
                            " ",
                            old_player_data.player_name,
                            " new power ",
                            " attack ,defence ",
                            old_player_data.attack,
                            old_player_data.defence,
                        )
                    old_player_data.item = item_data

                    # remove item in cell since player got it
                    self.cell_data[i].items = None
                break
            # remove player in cell
            if old_player_data.position == pos:
                self.cell_data[i].player_id = None

    def get_player_by_id(self, id):
        for i in self.players:
            pl = cast(Player, i)
            if pl.id == id:
                return pl

    def check_fight(self, new_player_data):

        pos = new_player_data.position
        for i, item in enumerate(self.cell_data):
            if (
                self.cell_data[i].position == pos
                and self.cell_data[i].player_id is not None
            ):
                # match fight
                defender = self.get_player_by_id(self.cell_data[i].player_id)
                attacker = new_player_data
                print(
                    " two players found in same location",
                    defender.player_name,
                    {defender.attack, defender.defence},
                    "vs ",
                    attacker.player_name,
                    {attacker.attack, attacker.defence},
                )
                win = self.handle_fight(attacker, defender)

                defender.status = "DEAD"

                self.cell_data[i].player_id = win.id
                print(
                    "cell ",
                    i,
                    " pos ",
                    self.cell_data[i].position,
                    " new player ",
                    self.cell_data[i].player_id,
                )
                return win

    def handle_fight(self, attacker, defender):
        attacker_score = attacker.attack
        attacker_score += float(0.5)  # special bonus for attacker
        defender_score = defender.defence
        print(attacker_score, defender_score)
        if attacker_score > defender_score:
            # attacker wins
            print("attacker {} wins ".format(attacker.player_name))
            print("defender {} defeated ".format(defender.player_name))
            print(
                "defender current item ",
                None if not defender.item else defender.item.item_name,
            )
            print(
                "attacker previous item ",
                None if not attacker.item else attacker.item.item_name,
            )

            if not None is defender.item:
                attacker.item = defender.item
                print("attacker new item ", attacker.item.item_name)

            print("removing defender {}".format(defender.player_name))
            return attacker

    def move_south(self, player):

        old_player_data = player
        player.position.y = 1
        new_player_data = player

        if player.position.y > 7:
            player.position.x = -1
            player.position.y = -1
            new_player_data.status = "DROWNED"
            return
        self.update_player_id_position(old_player_data, new_player_data)

    def move_north(self, player):
        old_player_data = player
        player.position.y -= 1
        new_player_data = player
        if player.position.y < 0:
            player.position.x = -1
            player.position.y = -1
            new_player_data.status = "DROWNED"
            return

        self.update_player_id_position(old_player_data, new_player_data)

    def move_east(self, player):
        old_player_data = player
        player.position.x = 1
        new_player_data = player
        if player.position.x > 7:
            player.position.x = -1
            player.position.y = -1
            new_player_data.status = "DROWNED"
            return

        self.update_player_id_position(old_player_data, new_player_data)

    def move_west(self, player):
        old_player_data = player
        player.position.x -= 1
        new_player_data = player
        if player.position.x < 0:
            player.position.x = -1
            player.position.y = -1
            new_player_data.status = "DROWNED"
            return

        self.update_player_id_position(old_player_data, new_player_data)


class Player:
    def __init__(self, name, y, x):
        pos = MakeAttribute()
        pos.y = y
        pos.x = x
        self.id = uuid.uuid1()
        self.player_name = name
        self.position = pos
        self.attack = 1
        self.defence = 1
        self.item = None
        self.status = "LIVE"

    def get_item_name(self):
        if self.item is None:
            return "null"
        else:
            return self.item.item_name

    def get_status(self):
        if self.position.y < 0 or self.position.x < 0:
            return "DROWNED"
        else:
            return "LIVE"

    def set_attack(self, value):
        self.attack = value

    def set_defence(self, value):
        self.defence = value


b = Board()

# initial item data

axe = Item(1, 0, "axe")
axe.set_attack(2)

dagger = Item(2, 5, "dagger")
dagger.set_attack(1)

helmet = Item(5, 5, "helmet")
helmet.set_defence(1)

majicstaff = Item(5, 2, "majic_staff")
majicstaff.set_defence(1)
majicstaff.set_attack(1)

# insert each items per location
items = [axe, dagger, helmet, majicstaff]
for t in items:
    b.add_item_position(t)


# b.move_south(blue)
# b.move_south(red)
# b.move_north(green)
# b.move_north(yellow)

# create player result data


sample_text_file_command = ["GAME-START", "R:S", "R:S", "B:E", "G:N", "Y:N", "GAME-END"]

if (
    "GAME-START" == sample_text_file_command[0]
    and "GAME-END" in sample_text_file_command
):
    last_index = sample_text_file_command.index("GAME-END")
    data = sample_text_file_command[1:last_index]

    # create player
    red = Player("red", 0, 0)
    blue = Player("blue", 7, 0)
    green = Player("green", 7, 7)
    yellow = Player("yellow", 0, 7)
    direction_map = {
        "S": b.move_south,
        "W": b.move_west,
        "E": b.move_east,
        "N": b.move_north,
    }
    player_map = {"R": red, "B": blue, "G": green, "Y": yellow}
    for c in data:
        com = c.split(":")
        if com[1] not in direction_map.keys():
            print("invalid direction")
            break
        elif com[0] not in player_map.keys():
            print("player not found")
            break

        f = direction_map[com[1]]
        f(player_map[com[0]])

    d = dict()
    for p in b.players:
        d[p.player_name] = [
            list(p.position.values()),
            p.status,
            p.get_item_name(),
            p.attack,
            p.defence,
        ]
    # create item result data
    for p in items:
        d[p.item_name] = [list(p.position.values()), p.equiped]

    print(d)

else:
    print("invalid commands")
