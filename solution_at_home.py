from parser import *
import random
import numpy as np
import matplotlib.pyplot as plt


# random.seed(1)


def focus(a, b):
    p1 = min(a, b, key=lambda p: p.x)
    p2 = a if p1 != a else b
    # print("p1 = {}, p2 = {}".format(p1, p2))

    dx = p2.x - p1.x
    dy = p2.y - p1.y

    if dx == 0:
        grid = np.ones((abs(dy) + 1, 1))
        # print("grid = {}".format(grid.shape))
        return grid
    if dy == 0:
        grid = np.ones((1, abs(dx) + 1))
        # print("grid = {}".format(grid.shape))
        return grid

    m = dy / dx
    c = p1.y - m * p1.x

    # z = 1 - (sin d^2)^2;      d = [-1.25:1.25]
    f_d = lambda d: np.cos(d) ** 2
    f_x = lambda x: m * x + c
    f_y = lambda y: (y - c) / m

    grid = np.zeros((abs(dy) + 1, abs(dx) + 1))
    # print("grid = {}".format(grid.shape))

    min_d = 10

    max_d = max(abs(dx), min_d) * max(abs(dy), min_d) / (max(abs(dx), min_d) ** 2 + max(abs(dy), min_d) ** 2) ** 0.5

    # print("max distance = {}".format(max_d))

    stretch = 1.55

    for i in range(abs(dx) + 1):
        x = p1.x + i
        for j in range(abs(dy) + 1):
            y = min(p1.y, p2.y) + j

            h = abs(x - f_y(y))
            v = abs(y - f_x(x))
            t = (h ** 2 + v ** 2) ** 0.5
            intensity = f_d(stretch * (h * v / t) / max_d) if t else f_d(0)

            grid[j, i] = intensity

    return grid


'''
line = focus(Office(1, 50), Office(60, 5))
# line = focus(Office(1, 2), Office(10, 20))
print(np.round(line, 2))
print(np.sum(line))
fig, axes = plt.subplots(subplot_kw={'xticks': [], 'yticks': []})

axes.imshow(line, interpolation="bicubic", cmap='Greys')  # "bicubic"

plt.show()
'''


def shift(x, y):
    """
    takes a (x, y) coordinates and moves then one step in any of the 4 main directions,
    following certain constraint:
        * the new location is inside the map.
        * the cost of the new location isn't way more expensive than old one.
    :param x: int
    :param y: int
    :return: tuple
    """

    ox, oy = x, y  # saves the old coordinates for reference
    current_cost = map_[y, x]  # gets the cost of the current location for checking against later
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    random.shuffle(directions)

    for move in directions:  # tries out each direction

        if 0 <= x + move[0] < map_.shape[1] and 0 <= y + move[1] < map_.shape[0]:  # checks that we're still in the map
            x += move[0]  # applies the shift to the x coordinate
            y += move[1]  # applies the shift to the y coordinate

        if map_[y, x] <= current_cost * 2:  # stops trying if it finds a location that satisfies the constraints
            break

        x, y = ox, oy  # resets the x and y to their old values for the next try

    return x, y


def rand_loc(dist_check=True):
    """
    gives a random office location that's next to one of the customers and,
    has a minimum distance from other offices (optional).
    :param dist_check: bool
    :return: tuple
    """
    customer = random.choice(customers)  # randomly picks a customer to place the office next to
    x = customer.x  # sets the x coordinate to the chosen customer's x location
    y = customer.y  # sets the y coordinate to the chosen customer's y location

    if dist_check:  # whether or not to check for distance between other offices
        # if there were offices added previously, it checks if it's close to any of them.
        while offices and any([customer.distance(office) < sum(map_.shape) / (p.r * 1.5) for office in offices]):
            # in case it's close to any offices then it repeat the random customer selection and location assignment
            customer = random.choice(customers)
            x = customer.x
            y = customer.y

    while x == customer.x and y == customer.y or map_[y, x] == np.inf:
        # keeps shifting the location till it's not in the same location as the customer or in the mountains
        x, y = shift(x, y)

    return x, y


def cost(a, b, manhattan=True):
    """
    calculates an approximation of the cost to move between point a and point b
    :param a:
    :param b:
    :param manhattan:
    :return:
    """
    box = map_[min(a.y, b.y):max(a.y, b.y) + 1, min(a.x, b.x):max(a.x, b.x) + 1]

    if not box.size:
        return 0

    mask = box == np.inf
    num_mountains = int(np.sum(mask))
    if num_mountains:
        box[mask] = num_mountains ** 5 / box.size
    # print("box = {}".format(box.shape))
    # box *= focus(a, b)

    weight = np.mean(box)
    distance = a.distance(b, manhattan=manhattan)

    box[mask] = np.inf

    return distance * weight


def center(zone):
    if not zone:
        x, y = rand_loc(dist_check=False)
        return Office(x, y)

    np_zone = np.array(zone)
    coordinates = np.rint(np.mean(np_zone[:, :2], axis=0))

    # np_zone[:, :2] *= np_zone[:, 2:]
    #
    # weight = np.mean(np_zone[:, 2:])
    # coordinates = np.rint(np.mean(np_zone[:, :2], axis=0) / weight)

    x = int(coordinates[0])
    y = int(round(coordinates[1]))

    for customer in zone:

        while x == customer.x and y == customer.y or map_[y, x] == np.inf:
            x, y = shift(x, y)

    if map_[y, x] == np.inf:
        x, y = rand_loc(dist_check=False)
        return Office(x, y)

    return Office(x, y)


inputs = ["1_victoria_lake.txt", "2_himalayas.txt", "3_budapest.txt", "4_manhattan.txt", "5_oceania.txt"]

plot_scalar = [5, 1000, 1000, 1000, 1000]

for file_name in inputs:
    print("=" * 50, file_name, "=" * 50)

    path = "inputs/{}".format(file_name)

    p = Parser(path)

    p_scale = plot_scalar[inputs.index(file_name)]

    solution = []

    global map_, customers, offices

    map_ = np.array(p.map_)

    customers = p.customers

    # ========================================================================== #
    # choosing random customer locations as initialization for office locations. #
    # ========================================================================== #

    offices = []

    for _ in range(p.r):
        x, y = rand_loc()
        offices.append(Office(x, y))

    # =================================== #
    # populating the zones using K-means. #
    # =================================== #

    zones = [[] for _ in range(p.r)]

    for _ in range(50):

        for c, customer in enumerate(customers):
            zone_score = np.empty(p.r, dtype=float)

            for o, office in enumerate(offices):
                zone_score[o] = cost(customer, office)

            z_i = int(np.argmin(zone_score))
            zones[z_i].append(customer)

        for z, zone in enumerate(zones):
            offices[z] = center(zone)

            # print(zone)

        zones = [[] for _ in range(p.r)]

    # ===================================================== #
    # assigning each customer to as many zones as possible. #
    # ===================================================== #

    for c, customer in enumerate(customers):
        zone_score = np.empty(p.r, dtype=float)

        for o, office in enumerate(offices):
            zone_score[o] = cost(customer, office, manhattan=False)

        z_i = int(np.argmin(zone_score))
        zones[z_i].append(customer)

        z_i_s = np.nonzero(zone_score < customer.reward)[0]

        if len(z_i_s) > 1:
            print(customer[:2], len(z_i_s))

        for i in z_i_s:
            if i != z_i:
                zones[i].append(customer)

    print("office location difficulty = {}".format([map_[office.y, office.x] for office in offices]))

    # =============================== #
    # writing the solution to a file. #
    # =============================== #

    path = "outputs/{}".format(file_name)

    with open(path, "w") as output_file:
        out_str = ""
        for row in solution:
            out_str += "{} {} ".format(row[0], row[1])
            for x in row[2:]:
                out_str += x
            out_str += "\n"

        output_file.write(out_str)

    map_list = [elm.split(" ") for elm in p.map_.symbolic.strip().split("\n")]
    color_map = np.empty((p.map_.h, p.map_.w), dtype=int)

    colors = {"#": 1, "~": 2, "*": 3, "+": 4, "X": 5, "_": 6, "H": 7, "T": 8}

    for x in range(p.map_.w):
        for y in range(p.map_.h):
            color_map[y, x] = colors[map_list[y][x]]

    fig, axes = plt.subplots(figsize=(10, 6), subplot_kw={'xticks': [], 'yticks': []})

    axes.imshow(color_map, interpolation=None, cmap='Set1')
    axes.set_title(file_name)

    for customer in customers:
        axes.scatter(customer.x, customer.y, s=customer.reward / p_scale, c="orange", alpha=0.75)

    for office in offices:
        axes.scatter(office.x, office.y, marker='*', c="lime")

    for z, zone in enumerate(zones):
        for customer in zone:
            axes.plot([offices[z].x, customer.x], [offices[z].y, customer.y], c="lightcyan")

plt.show()




