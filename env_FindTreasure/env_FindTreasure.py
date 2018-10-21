import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random


class EnvFindTreasure(object):
    def __init__(self):
        self.occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.raw_occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # initialize lever
        self.lever_pos = [6, 3]

        # initialize agent 1
        self.agt1_pos = [random.randint(1, 8), random.randint(1, 5)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1 or self.agt1_pos == self.lever_pos:
            self.agt1_pos = [random.randint(1, 8), random.randint(1, 5)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        # initialize agent 2
        self.agt2_pos = [random.randint(1, 8), random.randint(1, 5)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1 or self.agt2_pos == self.lever_pos:
            self.agt2_pos = [random.randint(1, 8), random.randint(1, 5)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        # initialize treasure
        self.treasure_pos = [8, 8]

    def reset(self):
        self.occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # initialize lever
        self.lever_pos = [6, 3]

        # initialize agent 1
        self.agt1_pos = [random.randint(1, 8), random.randint(1, 5)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1 or self.agt1_pos == self.lever_pos:
            self.agt1_pos = [random.randint(1, 8), random.randint(1, 5)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        # initialize agent 2
        self.agt2_pos = [random.randint(1, 8), random.randint(1, 5)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1 or self.agt2_pos == self.lever_pos:
            self.agt2_pos = [random.randint(1, 8), random.randint(1, 5)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        # initialize treasure
        self.treasure_pos = [8, 8]
        self.occupancy[8][8] = 1

    def step(self, action1, action2):
        reward = 0

        # agent1 move
        if action1 == 0:  # move up
            reward = reward - 1
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
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
        if action2 == 0:  # move up
            reward = reward - 1
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
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

        # check lever
        if self.agt1_pos == self.lever_pos or self.agt2_pos == self.lever_pos:
            self.occupancy[4][6] = 0    # open secret door
        else:
            self.occupancy[4][6] = 1    # close secret door

        # check treasure
        if self.agt1_pos == self.treasure_pos or self.agt2_pos == self.treasure_pos:
            reward = reward + 100
            self.reset()

        obs_1 = self.get_agt1_obs()
        obs_2 = self.get_agt2_obs()
        return reward, obs_1, obs_2, self.occupancy

    def get_agt1_obs(self):
        obs_1 = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                obs_1[i][j] = 4

        x = self.agt1_pos[0]
        y = self.agt1_pos[1]
        for i in range(10):
            for j in range(10):
                if [i, j] != self.agt1_pos:
                    # for all intermedia points
                    is_observed = True
                    for k in range(min(i, x), max(i, x)+1):
                        for l in range(min(j, y), max(j, y) + 1):
                            # check the distance to line
                            if [k, l] != [i, j] and [k, l] != [x, y]:
                                s = np.abs(i*(y-l)+x*(l-j)+k*(j-y))
                                dab = np.sqrt((i-x)*(i-x)+(j-y)*(j-y))
                                dis = s/dab
                                if dis < 0.5 and self.occupancy[k][l] == 1:     # has an obstacle
                                    is_observed = False
                    if is_observed:
                        obs_1[i][j] = self.occupancy[i][j]
                        if [i, j] == self.agt1_pos:
                            obs_1[i][j] = 2
                        if [i, j] == self.agt2_pos:
                            obs_1[i][j] = 2
                        if [i, j] == self.lever_pos:
                            obs_1[i][j] = 3
                        if [i, j] == self.treasure_pos:
                            obs_1[i][j] = 5
        obs_1[x][y] = 2
        return obs_1

    def get_agt2_obs(self):
        obs_2 = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                obs_2[i][j] = 4

        x = self.agt2_pos[0]
        y = self.agt2_pos[1]
        for i in range(10):
            for j in range(10):
                if [i, j] != self.agt2_pos:
                    # for all intermedia points
                    is_observed = True
                    for k in range(min(i, x), max(i, x)+1):
                        for l in range(min(j, y), max(j, y) + 1):
                            # check the distance to line
                            if [k, l] != [i, j] and [k, l] != [x, y]:
                                s = np.abs(i*(y-l)+x*(l-j)+k*(j-y))
                                dab = np.sqrt((i-x)*(i-x)+(j-y)*(j-y))
                                dis = s/dab
                                if dis < 0.5 and self.occupancy[k][l] == 1:     # has an obstacle
                                    is_observed = False
                    if is_observed:
                        obs_2[i][j] = self.occupancy[i][j]
                        if [i, j] == self.agt1_pos:
                            obs_2[i][j] = 2
                        if [i, j] == self.agt2_pos:
                            obs_2[i][j] = 2
                        if [i, j] == self.lever_pos:
                            obs_2[i][j] = 3
                        if [i, j] == self.treasure_pos:
                            obs_2[i][j] = 5
        obs_2[x][y] = 2
        return obs_2

    def plot_scene(self):
        fig = plt.figure(figsize=(8, 8))
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        ax2 = fig.add_subplot(gs[2, 0:1])
        ax3 = fig.add_subplot(gs[2, 1:2])

        # plot grid
        for k in range(10):
            for j in range(10):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax1.add_patch(rect)

        # plot block
        for k in range(10):
            for j in range(10):
                    if self.occupancy[k][j] == 1:
                        rect = plt.Rectangle((k, j), 1, 1, color='k')
                        ax1.add_patch(rect)

        # plot lever
        rect = plt.Rectangle((self.lever_pos[0], self.lever_pos[1]), 1, 1, color='y')
        ax1.add_patch(rect)

        # plot treasure
        rect = plt.Rectangle((self.treasure_pos[0], self.treasure_pos[1]), 1, 1, color='r')
        ax1.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos[0], self.agt1_pos[1]), 1, 1, color='g')
        ax1.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos[0], self.agt2_pos[1]), 1, 1, color='g')
        ax1.add_patch(rect)

        ax1.set_xlim([-1, 12])
        ax1.set_ylim([-1, 12])

        # plot grid
        for k in range(10):
            for j in range(10):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax2.add_patch(rect)

        obs_1 = self.get_agt1_obs()
        for k in range(10):
            for j in range(10):
                if obs_1[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='y')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 5:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    ax2.add_patch(rect)

        ax2.set_xlim([-1, 12])
        ax2.set_ylim([-1, 12])

        # plot grid
        for k in range(10):
            for j in range(10):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax3.add_patch(rect)

        obs_2 = self.get_agt2_obs()
        for k in range(10):
            for j in range(10):
                if obs_2[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='y')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 5:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    ax3.add_patch(rect)

        ax3.set_xlim([-1, 12])
        ax3.set_ylim([-1, 12])

        plt.show()

    def print_info(self):
        print("agent 1 is at", self.agt1_pos)
        print("agent 2 is at", self.agt2_pos)
        print(" ")