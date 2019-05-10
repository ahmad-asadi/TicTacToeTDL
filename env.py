import numpy as np


class Board:

    def __init__(self, print_map=True, size=3):
        self.size = size
        self.print_map=print_map
        self.state = np.zeros(self.size**2)

    def get_empty_spaces(self):
        empty_spaces = []
        for i in range(len(self.state)):
            if self.state[i] == 0:
                empty_spaces.append(i)
        return empty_spaces

    def update_state(self, player, action):
        if player == "X":
            marker = 1
        else:
            marker = -1

        self.state[action]=marker

        return self.check()

    def print(self):
        if not self.print_map:
            return
        print("Board state:")
        printable = ["X" if self.state[i] == 1 else ("O" if self.state[i] == -1 else "-") for i in range(self.size**2)]
        for i in range(1, self.size+1):
            print(printable[(i-1)*self.size:i*self.size])

    def check(self):
        if not list(self.state).__contains__(0):
            return 0

        s = np.sum(self.state[0] + self.state[4] + self.state[8])
        if s == 3:
            return 1
        elif s == -3:
            return -1

        s = np.sum(self.state[2] + self.state[4] + self.state[6])
        if s == 3:
            return 1
        elif s == -3:
            return -1

        for i in range(self.size):
            s = np.sum(self.state[(i - 1) * self.size:i * self.size])
            if s == 3:
                return 1
            elif s == -3:
                return -1

            s = np.sum([self.state[j*3 +i] for j in range(self.size)])
            if s == 3:
                return 1
            elif s == -3:
                return -1
        return 2

    def reset(self):
        self.state = np.zeros(self.size**2)
