from env import Board
from agent import RLAgent, Agent
import numpy as np



def train(board, rl_agent, opponent):
    experiments = 2000000
    for game in range(experiments):
        if game % 10000 == 0:
            print(game)
        done = 2
        board.reset()
        while done == 2:
            rl_agent.action(board)
            done = board.check()
            if done != 2:
                if done == 1:
                    # print("Victory")
                    rl_agent.win()
                else:
                    # print("Draw!")
                    rl_agent.draw()
                break

            opponent.action(board)
            done = board.check()
            if done != 2:
                if done == -1:
                    # print("Game Over!")
                    rl_agent.lose()
                elif done == 0:
                    # print("Draw!")
                    rl_agent.draw()

                break

            board.print()
        board.print()
    rl_agent.analyze()
    print("V: ", rl_agent.wins, ", L: ", rl_agent.loses," D: ", experiments-rl_agent.loses-rl_agent.wins)


def test(board, rl_agent):
    board.print_map=True
    experiments = 100
    for game in range(experiments):
        done = 2
        board.reset()
        while done == 2:
            rl_agent.action(board)
            done = board.check()
            if done != 2:
                if done == 1:
                    # print("Victory")
                    rl_agent.win()
                else:
                    # print("Draw!")
                    rl_agent.lose()
                break

            board.print()

            action = int(input())-1
            board.update_state(player="O", action=action)
            done = board.check()
            if done != 2:
                # if done == -1:
                #     print("Game Over!")
                # elif done == 0:
                #     print("Draw!")
                rl_agent.lose()
                break

            board.print()
        board.print()
    print("V: ", rl_agent.wins, ", L: ", rl_agent.loses," D: ", experiments-rl_agent.loses-rl_agent.wins)

board = Board(print_map=False)
rl_agent = RLAgent(_id = "X")
opponent = Agent(_id = "O")

train(board, rl_agent, opponent)
rl_agent.another_opponent()
test(board, rl_agent)
