import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


class EnvFindGoals(object):
    """docstring for Hotel"""
    def __init__(self):
        self.start1 = [3, 1]
        self.start2 = [6, 1]
        self.dest1 = [8, 2]
        self.dest2 = [1, 2]
        self.agt1_pos = [3, 1]
        self.agt2_pos = [6, 1]
        self.occupancy = [[1, 1, 1, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 1, 1]]

    def list_add(self, a, b):
        c = [a[i] + b[i] for i in range(min(len(a), len(b)))]
        return c

    def get_agt1_obs(self):
        vec = np.zeros((1, 8))

        # detect block
        if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1] + 1] == 1:
            vec[0, 0] = 1
        if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] == 1:
            vec[0, 1] = 1
        if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1] + 1] == 1:
            vec[0, 2] = 1
        if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] == 1:
            vec[0, 3] = 1
        if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] == 1:
            vec[0, 4] = 1
        if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1] - 1] == 1:
            vec[0, 5] = 1
        if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] == 1:
            vec[0, 6] = 1
        if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1] - 1] == 1:
            vec[0, 7] = 1

        # detect agent2
        if self.agt2_pos == self.list_add(self.agt1_pos, [-1, 1]):
            vec[0, 0] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [0, 1]):
            vec[0, 1] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [1, 1]):
            vec[0, 2] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [-1, 0]):
            vec[0, 3] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [1, 0]):
            vec[0, 4] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [-1, -1]):
            vec[0, 5] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [0, -1]):
            vec[0, 6] = 2
        if self.agt2_pos == self.list_add(self.agt1_pos, [1, -1]):
            vec[0, 7] = 2
        return vec

    def get_agt2_obs(self):
        vec = np.zeros((1, 8))

        # detect block
        if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1] + 1] == 1:
            vec[0, 0] = 1
        if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] == 1:
            vec[0, 1] = 1
        if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1] + 1] == 1:
            vec[0, 2] = 1
        if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] == 1:
            vec[0, 3] = 1
        if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] == 1:
            vec[0, 4] = 1
        if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1] - 1] == 1:
            vec[0, 5] = 1
        if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] == 1:
            vec[0, 6] = 1
        if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1] - 1] == 1:
            vec[0, 7] = 1

        # detect agent1
        if self.agt1_pos == self.list_add(self.agt2_pos, [-1, 1]):
            vec[0, 0] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [0, 1]):
            vec[0, 1] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [1, 1]):
            vec[0, 2] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [-1, 0]):
            vec[0, 3] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [1, 0]):
            vec[0, 4] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [-1, -1]):
            vec[0, 5] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [0, -1]):
            vec[0, 6] = 2
        if self.agt1_pos == self.list_add(self.agt2_pos, [1, -1]):
            vec[0, 7] = 2
        return vec

    def step(self, action1, action2):
        reward = 0
        self.start1 = [3, 1]
        self.start2 = [6, 1]
        # agent1 move
        if action1 == 0:    # move up
            reward = reward - 1
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:     # if can move
                self.agt1_pos[1] = self.agt1_pos[1] + 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
        elif action1 == 1:  # move down
            reward = reward - 1
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] - 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
        elif action1 == 2:  # move left
            reward = reward - 1
            if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] - 1
                self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
        elif action1 == 3:  # move right
            reward = reward - 1
            if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] + 1
                self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        # agent2 move
        if action2 == 0:    # move up
            reward = reward - 1
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:     # if can move
                self.agt2_pos[1] = self.agt2_pos[1] + 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
        elif action2 == 1:  # move down
            reward = reward - 1
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] - 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
        elif action2 == 2:  # move left
            reward = reward - 1
            if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] - 1
                self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
        elif action2 == 3:  # move right
            reward = reward - 1
            if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] + 1
                self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        if self.agt1_pos == self.dest1:
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 0
            self.agt1_pos = self.start1
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            reward = reward + 100

        if self.agt2_pos == self.dest2:
            self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 0
            self.agt2_pos = self.start2
            self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            reward = reward + 100

        obs_1 = self.get_agt1_obs()
        obs_2 = self.get_agt2_obs()
        return reward, obs_1, obs_2

    def reset(self):
        self.agt1_pos = [3, 1]
        self.agt2_pos = [6, 1]
        self.occupancy = [[1, 1, 1, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 1, 1]]

    def plot_scene(self):
        fig = plt.figure(figsize=(8, 8))
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        ax2 = fig.add_subplot(gs[2, 0:1])
        ax3 = fig.add_subplot(gs[2, 1:2])

        # plot grid
        for k in range(10):
            for j in range(4):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax1.add_patch(rect)

        # plot block
        for k in range(10):
            for j in range(4):
                    if self.occupancy[k][j] == 1:
                        rect = plt.Rectangle((k, j), 1, 1, color='k')
                        ax1.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos[0], self.agt1_pos[1]), 1, 1, color='r')
        ax1.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos[0], self.agt2_pos[1]), 1, 1, color='b')
        ax1.add_patch(rect)

        ax1.set_xlim([-1, 12])
        ax1.set_ylim([-1, 6])

        # plot grid
        for k in range(10):
            for j in range(4):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax2.add_patch(rect)

        # plot block
        for k in range(10):
            for j in range(4):
                if self.occupancy[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax2.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos[0], self.agt1_pos[1]), 1, 1, color='r')
        ax2.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos[0], self.agt2_pos[1]), 1, 1, color='b')
        ax2.add_patch(rect)

        # plot fog
        x = self.agt1_pos[0]
        y = self.agt1_pos[1]
        for k in range(10):
            for j in range(4):
                if np.abs(k - x) > 1 or np.abs(j - y) > 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax2.add_patch(rect)

        ax2.set_xlim([-1, 12])
        ax2.set_ylim([-1, 6])

        # plot grid
        for k in range(10):
            for j in range(4):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax3.add_patch(rect)

        # plot block
        for k in range(10):
            for j in range(4):
                if self.occupancy[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax3.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos[0], self.agt1_pos[1]), 1, 1, color='r')
        ax3.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos[0], self.agt2_pos[1]), 1, 1, color='b')
        ax3.add_patch(rect)

        # plot fog
        x = self.agt2_pos[0]
        y = self.agt2_pos[1]
        for k in range(10):
            for j in range(4):
                if np.abs(k - x) > 1 or np.abs(j - y) > 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax3.add_patch(rect)

        ax3.set_xlim([-1, 12])
        ax3.set_ylim([-1, 6])

        plt.show()

    def print_info(self):
        print("agent 1 is at", self.agt1_pos)
        print("agent 2 is at", self.agt2_pos)
        print(" ")
