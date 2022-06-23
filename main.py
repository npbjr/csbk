import uuid


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
        self.items = Item()
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

    def set_attack(self, value):
        self.attack = value

    def set_defence(self, value):
        self.defence = value


class Board:
    def __init__(self):
        self.cell_data = []
        self.players = []

        '#generate data'

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

    def save_final_player_data(self, players):
        self.players = players
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
                break

    def update_player_id_position(self, old_player_data, new_player_data):
        for i, item in enumerate(self.cell_data):
            pos = item.get_position()
            item_data = item.items
            # update correct player cell
            if new_player_data.position == pos:
                self.cell_data[i].player_id = new_player_data.id
                # check cell item and update player
                if item_data is not None and item_data.position == pos:
                    old_player_data.item = item_data

                    # remove item in cell since player got it
                    self.cell_data[i].items = None
            # remove player in cell
            if old_player_data.position == pos:
                self.cell_data[i].player_id = None

    def move_south(self, player):

        old_player_data = player
        player.position.y += 1
        new_player_data = player

        if player.position.y > 7:
            player.position.x = -1
            player.position.y = -1
            return
        self.update_player_id_position(old_player_data, new_player_data)

    def move_north(self, player):
        old_player_data = player
        player.position.y -= 1
        new_player_data = player
        if player.position.y < 0:
            player.position.x = -1
            player.position.y = -1
            return

        self.update_player_id_position(old_player_data, new_player_data)

    def move_east(self, player):
        old_player_data = player
        player.position.x += 1
        new_player_data = player
        if player.position.x > 7:
            player.position.x = -1
            player.position.y = -1
            return

        self.update_player_id_position(old_player_data, new_player_data)

    def move_west(self, player):
        old_player_data = player
        player.position.x -= 1
        new_player_data = player
        if player.position.x < 0:
            player.position.x = -1
            player.position.y = -1
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

    def get_item(self):
        if self.item is None:
            return "null"
        else:
            return self.item

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

axe = Item(2, 2, "Axe")
axe.set_attack(2)

dagger = Item(2, 5, "Dagger")
dagger.set_attack(1)

helmet = Item(5, 5, "Helmet")
helmet.set_defence(1)

majicstaff = Item(5, 2, "MajicStaff")
majicstaff.set_defence(1)
majicstaff.set_attack(1)

# insert each items per location
items = [axe, dagger, helmet, majicstaff]
for t in items:
    b.add_item_position(t)


# create player
red = Player("red", 0, 0)
blue = Player("blue", 7, 0)
green = Player("green", 7, 7)
yellow = Player("yellow", 0, 7)

print("initial position ", red.position, " item ", red.item)
print("initial position ", blue.position, " item ", blue.item)
print("initial position ", green.position, " item ", green.item)
print("initial position ", yellow.position, " item ", yellow.item)

b.add_player_position(red)
b.add_player_position(blue)
b.add_player_position(green)
b.add_player_position(yellow)

b.move_south(red)
b.move_south(red)
b.move_east(blue)
b.move_north(green)
b.move_north(yellow)

players = [red,blue, green, yellow]

print("current position red ", red.position, " item ", red.item)
print("current position blue ", blue.position, " item ", blue.item)
print("current position green ", green.position, " item ", green.item)
print("current position yellow ", yellow.position, " item ", yellow.item)

# create player result data
d = dict()

for i, p in enumerate(players):
    d[p.player_name] = [list(p.position.values()), p.get_status(), p.get_item(), p.attack, p.defence]

# create item result data
for i, p in enumerate(items):
    d[p.item_name] = [list(p.position.values()), "false"]


print(d)
