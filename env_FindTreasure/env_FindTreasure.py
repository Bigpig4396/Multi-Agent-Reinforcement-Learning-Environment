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

    def step(self, action_list):
        self.lever_pos = [6, 3]
        self.treasure_pos = [8, 8]
        reward_1 = 0
        reward_2 = 0
        # agent1 move
        if action_list[0] == 0:  # move up
            reward_1 = reward_1 - 1
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] + 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 20
        elif action_list[0] == 1:  # move down
            reward_1 = reward_1 - 1
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] - 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 20
        elif action_list[0] == 2:  # move left
            reward_1 = reward_1 - 1
            if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] - 1
                self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 20
        elif action_list[0] == 3:  # move right
            reward_1 = reward_1 - 1
            if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] + 1
                self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 20

        # agent2 move
        if action_list[1] == 0:  # move up
            reward_2 = reward_2 - 1
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] + 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward_2 = reward_2 - 20
        elif action_list[1] == 1:  # move down
            reward_2 = reward_2 - 1
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] - 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward_2 = reward_2 - 20
        elif action_list[1] == 2:  # move left
            reward_2 = reward_2 - 1
            if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] - 1
                self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward_2 = reward_2 - 20
        elif action_list[1] == 3:  # move right
            reward_2 = reward_2 - 1
            if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] + 1
                self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward_2 = reward_2 - 20

        # check lever
        if self.agt1_pos == self.lever_pos or self.agt2_pos == self.lever_pos:
            self.occupancy[4][6] = 0    # open secret door
        else:
            self.occupancy[4][6] = 1    # close secret door

        # check treasure
        if self.agt1_pos == self.treasure_pos or self.agt2_pos == self.treasure_pos:
            reward_1 = reward_1 + 100
            reward_2 = reward_2 + 100
            self.reset()

        done = False
        if reward_1 > 0:
            done = True

        return [reward_1, reward_2], done

    def get_agt1_obs(self):
        obs_1 = np.zeros((10, 10, 3))
        for i in range(10):
            for j in range(10):
                obs_1[i, j, 0] = 0.5
                obs_1[i, j, 1] = 0.5
                obs_1[i, j, 2] = 0.5

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
                        if self.occupancy[i][j] == 0:
                            obs_1[9 - j, i, 0] = 1
                            obs_1[9 - j, i, 1] = 1
                            obs_1[9 - j, i, 2] = 1
                        if self.occupancy[i][j] == 1:
                            obs_1[9 - j, i, 0] = 0
                            obs_1[9 - j, i, 1] = 0
                            obs_1[9 - j, i, 2] = 0
                        if [i, j] == self.lever_pos:
                            obs_1[9 - j, i, 0] = 1
                            obs_1[9 - j, i, 1] = 1
                            obs_1[9 - j, i, 2] = 0
                        if [i, j] == self.agt1_pos:
                            obs_1[9 - j, i, 0] = 1
                            obs_1[9 - j, i, 1] = 0
                            obs_1[9 - j, i, 2] = 0
                        if [i, j] == self.agt2_pos:
                            obs_1[9 - j, i, 0] = 0
                            obs_1[9 - j, i, 1] = 1
                            obs_1[9 - j, i, 2] = 0
                        if [i, j] == self.treasure_pos:
                            obs_1[9 - j, i, 0] = 0
                            obs_1[9 - j, i, 1] = 0
                            obs_1[9 - j, i, 2] = 1
        obs_1[9 - y, x, 0] = 1
        obs_1[9 - y, x, 1] = 0
        obs_1[9 - y, x, 2] = 0
        return obs_1

    def get_agt2_obs(self):
        obs_2 = np.zeros((10, 10, 3))
        for i in range(10):
            for j in range(10):
                obs_2[i, j, 0] = 0.5
                obs_2[i, j, 1] = 0.5
                obs_2[i, j, 2] = 0.5

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
                        if self.occupancy[i][j] == 0:
                            obs_2[9 - j, i, 0] = 1
                            obs_2[9 - j, i, 1] = 1
                            obs_2[9 - j, i, 2] = 1
                        if self.occupancy[i][j] == 1:
                            obs_2[9 - j, i, 0] = 0
                            obs_2[9 - j, i, 1] = 0
                            obs_2[9 - j, i, 2] = 0
                        if [i, j] == self.lever_pos:
                            obs_2[9 - j, i, 0] = 1
                            obs_2[9 - j, i, 1] = 1
                            obs_2[9 - j, i, 2] = 0
                        if [i, j] == self.agt1_pos:
                            obs_2[9 - j, i, 0] = 1
                            obs_2[9 - j, i, 1] = 0
                            obs_2[9 - j, i, 2] = 0
                        if [i, j] == self.agt2_pos:
                            obs_2[9 - j, i, 0] = 0
                            obs_2[9 - j, i, 1] = 1
                            obs_2[9 - j, i, 2] = 0
                        if [i, j] == self.treasure_pos:
                            obs_2[9 - j, i, 0] = 0
                            obs_2[9 - j, i, 1] = 0
                            obs_2[9 - j, i, 2] = 1
        obs_2[9 - y, x, 0] = 0
        obs_2[9 - y, x, 1] = 1
        obs_2[9 - y, x, 2] = 0
        return obs_2

    def get_obs(self):
        return [self.get_agt1_obs(), self.get_agt2_obs()]

    def get_full_obs(self):
        obs_2 = np.zeros((10, 10, 3))
        for i in range(10):
            for j in range(10):
                if self.occupancy[i][j] == 0:
                    obs_2[9 - j, i, 0] = 1
                    obs_2[9 - j, i, 1] = 1
                    obs_2[9 - j, i, 2] = 1
                if self.occupancy[i][j] == 1:
                    obs_2[9 - j, i, 0] = 0
                    obs_2[9 - j, i, 1] = 0
                    obs_2[9 - j, i, 2] = 0
                if [i, j] == self.lever_pos:
                    obs_2[9 - j, i, 0] = 1
                    obs_2[9 - j, i, 1] = 1
                    obs_2[9 - j, i, 2] = 0
                if [i, j] == self.agt1_pos:
                    obs_2[9 - j, i, 0] = 1
                    obs_2[9 - j, i, 1] = 0
                    obs_2[9 - j, i, 2] = 0
                if [i, j] == self.agt2_pos:
                    obs_2[9 - j, i, 0] = 0
                    obs_2[9 - j, i, 1] = 1
                    obs_2[9 - j, i, 2] = 0
                if [i, j] == self.treasure_pos:
                    obs_2[9 - j, i, 0] = 0
                    obs_2[9 - j, i, 1] = 0
                    obs_2[9 - j, i, 2] = 1
        return obs_2

    def plot_scene(self):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        plt.xticks([])
        plt.yticks([])
        ax2 = fig.add_subplot(gs[2, 0:1])
        plt.xticks([])
        plt.yticks([])
        ax3 = fig.add_subplot(gs[2, 1:2])
        plt.xticks([])
        plt.yticks([])

        ax1.imshow(self.get_full_obs())
        ax2.imshow(self.get_agt1_obs())
        ax3.imshow(self.get_agt2_obs())

        plt.show()

    def set_agt1_at(self, new_pos):
        if self.occupancy[new_pos[0]][new_pos[1]] == 0:
            self.occupancy[new_pos[0]][new_pos[1]] = 1
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 0
            self.agt1_pos = new_pos

    def set_agt2_at(self, new_pos):
        if self.occupancy[new_pos[0]][new_pos[1]] == 0:
            self.occupancy[new_pos[0]][new_pos[1]] = 1
            self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 0
            self.agt2_pos = new_pos