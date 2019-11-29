from models import *


class Parser(object):
    def __init__(self, path):
        self.file = open(path, "r")

        self.n, self.m, self.c, self.r = self.next_row()

        self.customers = []

        for i in range(self.c):
            self.customers.append(Customer(self.next_row()))

        self.map_ = Map(self.n, self.m)

        for i in range(self.m):
            self.map_.add_row(self.next_row())

        self.file.close()

    @staticmethod
    def str2list(input_str):
        output = []
        to_list = input_str.strip().split(" ")
        for x in to_list:
            try:
                output.append(int(x))
            except ValueError:
                try:
                    output.append(float(x))
                except ValueError:
                    output.append(x)
        return output

    def next_row(self):
        return self.str2list(next(self.file))

    def __repr__(self):
        return str(self.__dict__) + "\n"


if __name__ == "__main__":
    path_list = ["inputs/1_victoria_lake.txt"]

    for path in path_list:
        data = Parser(path)
        print(data.map_.symbolic)
