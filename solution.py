from parser import *
import random


def cost(p1, p2):
    global map_

    distance = abs(p1.x - p2.x) + abs(p1.y - p2.y)
    weight = np.mean(map_[min(p1.x, p2.x): max(p1.x, p2.x), min(p1.y, p2.y): max(p1.y, p2.y)])

    # for x in range(min(p1.x, p2.x), max(p1.x, p2.x)):
    #     for y in range(min(p1.y, p2.y), max(p1.y, p2.y)):
    #         weight += map_[min(y, map_.h - 1)][min(x, map_.w - 1)]

    return distance * weight


def center(zone):
    if np.any(zone):
        mask = zone[:, 2] > 0
        coordinates = np.sum(zone[mask], axis=0)
        x = int(coordinates[0] / np.sum(mask))
        y = int(coordinates[1] / np.sum(mask))

        if x > map_.shape[0]:
            x = map_.shape[0] - 1

        if y > map_.shape[1]:
            y = map_.shape[1] - 1

        # for customer in zone:
        #     x += customer.x
        #     y += customer.y
        #
        # x = min(int(x / len(zone)), map_.w)
        # y = min(int(y / len(zone)), map_.h)

        if map_[x, y] > 200:
            move = min(map_.shape) // 5

            for dx in range(1, move):

                for dy in range(1, move):

                    for d in [-1, 1]:
                        nx = x + d * dx
                        nx = min(nx, map_.shape[0] - 1)
                        nx = max(nx, 0 - 1)
                        ny = y + d * dy
                        ny = min(ny, map_.shape[1] - 1)
                        ny = max(ny, 0 - 1)

                        if map_[nx, ny] < 800:
                            return Office(nx, ny)

        return Office(x, y)
    return Office(random.randint(0, map_.shape[0] - 1), random.randint(0, map_.shape[1] - 1))


inputs = ["1_victoria_lake.txt", "2_himalayas.txt", "3_budapest.txt", "4_manhattan.txt", "5_oceania.txt"]

for file_name in inputs:
    path = "inputs/{}".format(file_name)

    global map_

    p = Parser(path)

    map_ = np.array(p.map_)

    print(map_.shape)

    office_list = [Office(random.randint(0, p.m - 1), random.randint(0, p.n - 1)) for _ in range(p.r)]

    while any([map_[office.x, office.y] > 200 for office in office_list]):
        for o in range(p.r):
            if map_[office_list[o][0], office_list[o][1]] > 200:
                office_list[o] = Office(random.randint(0, p.m - 1), random.randint(0, p.n - 1))

    zone_list = [np.zeros((p.c, 3), dtype=int) for _ in range(p.r)]  # [[] for _ in range(p.r)]

    print()

    for _ in range(100):

        count = 0

        for c, customer in enumerate(p.customers):
            min_cost = float("inf")
            best_zone = 0

            for o, office in enumerate(office_list):

                count += 1

                print("\r{}".format(count), end="")

                office_cost = cost(customer, office)

                if office_cost < min_cost:
                    min_cost = office_cost
                    best_zone = o

            zone_list[best_zone][c, 0] = customer.x
            zone_list[best_zone][c, 1] = customer.y
            zone_list[best_zone][c, 2] = customer.reward  # .append(customer)

        for o, zone in enumerate(zone_list):

            office_list[o] = center(zone)

    outputs = []

    for o in range(p.r):

        customers = zone_list[o]

        direction = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
        opposite = {"U":"D", "D":"U", "L":"R", "R":"L"}

        office = office_list[o]
        print(office, map_[office.x, office.y])

        for customer in customers:

            if customer[2] == 0:
                continue

            # print(customer)
            start = [office.x, office.y]
            end = [customer[0], customer[1]]

            steps = []
            path_score = 0
            me_now = start
            been_there = []

            while me_now != end:
                me_next = []
                next_move = []
                me_next_score = []

                for d in direction.keys():
                    # if steps and opposite[d] == steps[-1]:
                    #     continue

                    move = direction[d]
                    next_loc = [me_now[0] + move[0], me_now[1] + move[1]]


                    if str(next_loc) in been_there:
                        continue

                    if 0 <= next_loc[0] < map_.shape[0] and 0 <= next_loc[1]  < map_.shape[1]:

                        if map_[next_loc[0], next_loc[1]] > 800:
                            continue

                        move_score = path_score + map_[next_loc[0], next_loc[1]] + \
                                     ((next_loc[0] - end[0]) ** 2 + (next_loc[1] - end[1]) ** 2) ** 0.5

                        me_next.append(next_loc)
                        next_move.append(d)
                        me_next_score.append(move_score)

                try:
                    best_move = me_next_score.index(min(me_next_score))
                except:
                    break
                me_now = me_next[best_move]
                steps.append(next_move[best_move])
                path_score = me_next_score[best_move] - map_[me_now[0], me_now[1]] + \
                             ((me_now[0] - end[0]) ** 2 + (me_now[1] - end[1]) ** 2) ** 0.5

                been_there.append(str(me_now))

            outputs.append([])
            outputs[-1].extend(office)
            outputs[-1].extend(steps)

            #     print("\r{}".format(me_now), end="")
            #
            # print()

    path = "outputs/{}".format(file_name)

    with open(path, "w") as output_file:
        out_str = ""
        for row in outputs:
            out_str += "{} {} ".format(row[0], row[1])
            for x in row[2:]:
                out_str += x
            out_str += "\n"

        output_file.write(out_str)

    # for zone in zone_list:
    #     print(zone)

    print("=" * 50)





