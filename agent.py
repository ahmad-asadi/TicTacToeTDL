import numpy as np
import math
from matplotlib import pyplot as plt


def get_random_action(board):
    action_space = board.get_empty_spaces()
    a = np.random.randint(0, len(action_space))
    action = action_space[a]
    return action


class Agent:

    def __init__(self, _id, board_size=9):
        self.id = _id
        self.action_space = board_size
        self.draws = 0
        self.loses = 0
        self.wins = 0
        self.report = []

    def action(self, board):
        action = get_random_action(board)
        board.update_state(player=self.id, action=action)

    def lose(self):
        self.loses += 1
        self.report.append(-1)

    def win(self):
        self.wins += 1
        self.report.append(1)

    def draw(self):
        self.draws += 1
        self.report.append(0)

    def analyze(self):
        plt.scatter(range(len(self.report)), self.report)
        plt.title("Player: " + self.id)
        plt.show()


def get_state_id(state):
    state_id = 0
    for i in range(len(state)):
        s = state[i]
        if s == -1:
            s = 2
        state_id += s * (3**i)
    return int(state_id)


class RLAgent(Agent):

    def __init__(self, _id, lr = 0.1, board_size=9, initial_winning_prob=0.5, exploration_ratio=0.1, learning_rate_decrease_rate=0.9, warm_up_with_exploratory_moves=20000):
        super().__init__(_id, board_size)
        self.warm_up_with_exploratory_moves = warm_up_with_exploratory_moves
        self.action_count = 0
        self.first_time_learning_rate = lr
        self.learning_rate_decrease_rate = learning_rate_decrease_rate
        self.learning_rate = lr
        self.value_function = np.zeros(shape=3**board_size) + initial_winning_prob
        self.history = []
        self.exploration_ratio = exploration_ratio

    def action(self, board):
        backup_state = True
        if np.random.rand() < self.exploration_ratio:
            action = get_random_action(board)
            backup_state = False
            if self.action_count < self.warm_up_with_exploratory_moves :
                backup_state = True
            self.action_count += 1
        else:
            action = self.get_action(board)
        current_state = get_state_id(board.state)
        board.update_state(player=self.id, action=action)
        next_state = get_state_id(board.state)
        if backup_state:
            self.backup_state(current_state, next_state)

    def lose(self):
        super().lose()
        self.update_value_function(reward=0)

    def win(self):
        super().win()
        self.update_value_function(reward=1)

    def draw(self):
        super().draw()
        self.update_value_function(reward=0.5)

    def get_action(self, board):
        action_space = board.get_empty_spaces()
        state = np.copy(board.state)
        max_value = -math.inf
        best_action = -1
        for action in action_space:
            state[action] = 1
            next_state_id = get_state_id(state)
            state[action] = 0
            if  max_value < self.value_function[next_state_id]:
                max_value = self.value_function[next_state_id]
                best_action = action
        return best_action

    def backup_state(self, current_state, next_state):
        self.history.append([current_state, next_state])

    def update_value_function(self, reward):
        # print("update value function")
        if len(self.history) == 0:
            print("no history found (all of the steps were exploratory!)")
            return
        last_state = self.history[-1][1]
        self.value_function[last_state] += self.learning_rate * (reward-self.value_function[last_state])
        for i in range(len(self.history), 0, -1):
            s = self.history[i-1][0]
            s_prime = self.history[i-1][1]
            self.value_function[s] += self.learning_rate * (self.value_function[s_prime] - self.value_function[s])
        self.history = []
        # self.learning_rate *= self.learning_rate_decrease_rate
        # print(self.learning_rate)

    def another_opponent(self):
        self.loses = 0
        self.wins = 0
        self.report = []
        # self.learning_rate = self.first_time_learning_rate

