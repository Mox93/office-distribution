

class Map(list):
    def __init__(self, w, h):
        super(Map, self).__init__()
        self.w = w
        self.h = h
        self.cost = {"#": float("inf"), "~": 800, "*": 200, "+": 150, "X": 120, "_": 100, "H": 70, "T": 50}
        self.symbolic = ""

    def add_row(self, row):
        row2list = [x for x in row[0]]
        self.append([self.cost[x] for x in row2list])
        self.symbolic += " ".join(row2list) + "\n"

    def __repr__(self):
        out_str = ""
        for row in self:
            for elm in row:
                elm = str(elm)
                if len(elm) == 2:
                    elm = " " + elm
                out_str += elm + " "
            out_str += "\b\n"

        return out_str


class Customer(list):
    def __init__(self, prop):
        super(Customer, self).__init__()
        self.x = prop[0]
        self.y = prop[1]
        self.reward = prop[2]
        self.extend(prop)

    def distance(self, other, manhattan=False):
        if manhattan:
            return abs(self.x - other.x) + abs(self.y - other.y)
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __repr__(self):
        return str([self.x, self.y, self.reward])


class Office(list):
    def __init__(self, x, y):
        super(Office, self).__init__()
        self.x = x
        self.y = y
        self.extend((x, y))

    def distance(self, other, manhattan=False):
        if manhattan:
            return abs(self.x - other.x) + abs(self.y - other.y)
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __repr__(self):
        return str([self.x, self.y])


