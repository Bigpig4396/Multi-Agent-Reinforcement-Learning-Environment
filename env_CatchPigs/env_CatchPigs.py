import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
import random


class EnvCatchPigs(object):
    def __init__(self):
        self.occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1]]

        self.raw_occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 0, 1, 0, 1, 0, 1, 0, 1],
                   [1, 0, 0, 0, 0, 0, 0, 0, 1],
                   [1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # initialize agent 1
        self.agt1_pos = [random.randint(1, 7), random.randint(1, 7)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1:
            self.agt1_pos = [random.randint(1, 7), random.randint(1, 7)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt1_ori = random.randint(0, 3)

        # initialize agent 2
        self.agt2_pos = [random.randint(1, 7), random.randint(1, 7)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1:
            self.agt2_pos = [random.randint(1, 7), random.randint(1, 7)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt2_ori = random.randint(0, 3)

        # initialize pig
        self.pig_pos = [random.randint(1, 7), random.randint(1, 7)]
        while self.occupancy[self.pig_pos[0]][self.pig_pos[1]] == 1:
            self.pig_pos = [random.randint(1, 7), random.randint(1, 7)]
        self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1

        self.pig_ori = random.randint(0, 3)

        self.if_agt1_catches = False
        self.if_agt2_catches = False

        self.action1_list = []
        self.action2_list = []
        self.action_pig_list = []
        self.agt1_pos_list = []
        self.agt2_pos_list = []
        self.pig_pos_list = []
        self.agt1_ori_list = []
        self.agt2_ori_list = []
        self.pig_ori_list = []
        self.obs1_list = []
        self.obs2_list = []
        self.obs_pig_list = []

        self.fig = plt.figure(figsize=(8, 8))
        self.gs = GridSpec(3, 3, figure=self.fig)
        self.ax1 = self.fig.add_subplot(self.gs[0:2, 0:2])
        self.ax2 = self.fig.add_subplot(self.gs[2, 0:1])
        self.ax3 = self.fig.add_subplot(self.gs[2, 1:2])
        self.ax4 = self.fig.add_subplot(self.gs[2, 2:3])

    def reset(self):
        self.occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 1],
                          [1, 0, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # initialize agent 1
        self.agt1_pos = [random.randint(1, 7), random.randint(1, 7)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1:
            self.agt1_pos = [random.randint(1, 7), random.randint(1, 7)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt1_ori = random.randint(0, 3)

        # initialize agent 2
        self.agt2_pos = [random.randint(1, 7), random.randint(1, 7)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1:
            self.agt2_pos = [random.randint(1, 7), random.randint(1, 7)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt2_ori = random.randint(0, 3)

        # initialize pig
        self.pig_pos = [random.randint(1, 7), random.randint(1, 7)]
        while self.occupancy[self.pig_pos[0]][self.pig_pos[1]] == 1:
            self.pig_pos = [random.randint(1, 7), random.randint(1, 7)]
        self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1

        self.pig_ori = random.randint(0, 3)

        self.if_agt1_catches = False
        self.if_agt2_catches = False

    def get_agt1_obs(self):
        obs = np.zeros((9, 9))
        for i in range(9):
            for j in range(9):
                obs[i][j] = 4

        x = self.agt1_pos[0]
        y = self.agt1_pos[1]

        if self.agt1_ori == 0:  # if agent is facing west
            for i in range(0, x+1):
                for j in range(max(0, y-x+i), min(8, y+x-i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt1_ori == 1:    # if agent is facing north
            for j in range(y, 9):
                for i in range(max(0, x+y-j), min(8, x-y+j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt1_ori == 2:    # if agent is facing east
            for i in range(x, 9):
                for j in range(max(0, y+x-i), min(8, y-x+i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt1_ori == 3:    # if agent is facing south
            for j in range(0, y+1):
                for i in range(max(0, x-y+j), min(8, x+y-j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        return obs

    def get_agt2_obs(self):
        obs = np.zeros((9, 9))
        for i in range(9):
            for j in range(9):
                obs[i][j] = 4

        x = self.agt2_pos[0]
        y = self.agt2_pos[1]

        if self.agt2_ori == 0:  # if agent is facing west
            for i in range(0, x + 1):
                for j in range(max(0, y - x + i), min(8, y + x - i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt2_ori == 1:  # if agent is facing north
            for j in range(y, 9):
                for i in range(max(0, x + y - j), min(8, x - y + j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt2_ori == 2:  # if agent is facing east
            for i in range(x, 9):
                for j in range(max(0, y + x - i), min(8, y - x + i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt2_ori == 3:  # if agent is facing south
            for j in range(0, y + 1):
                for i in range(max(0, x - y + j), min(8, x + y - j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        return obs

    def get_pig_obs(self):
        obs = np.zeros((9, 9))
        for i in range(9):
            for j in range(9):
                obs[i][j] = 4

        x = self.pig_pos[0]
        y = self.pig_pos[1]

        if self.pig_ori == 0:  # if agent is facing west
            for i in range(0, x + 1):
                for j in range(max(0, y - x + i), min(8, y + x - i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.pig_ori == 1:  # if agent is facing north
            for j in range(y, 9):
                for i in range(max(0, x + y - j), min(8, x - y + j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.pig_ori == 2:  # if agent is facing east
            for i in range(x, 9):
                for j in range(max(0, y + x - i), min(8, y - x + i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.pig_ori == 3:  # if agent is facing south
            for j in range(0, y + 1):
                for i in range(max(0, x - y + j), min(8, x + y - j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        return obs

    def step(self, action1, action2, action_pig):
        reward_1 = 0
        reward_2 = 0
        reward_pig = 0

        # agent1 move
        if action1 == 0:    # turn left
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                self.agt1_ori = 3
            elif self.agt1_ori == 1:
                self.agt1_ori = 0
            elif self.agt1_ori == 2:
                self.agt1_ori = 1
            elif self.agt1_ori == 3:
                self.agt1_ori = 2

        elif action1 == 1:  # turn right
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                self.agt1_ori = 1
            elif self.agt1_ori == 1:
                self.agt1_ori = 2
            elif self.agt1_ori == 2:
                self.agt1_ori = 3
            elif self.agt1_ori == 3:
                self.agt1_ori = 0

        elif action1 == 2:  # move
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                    self.agt1_pos[0] = self.agt1_pos[0] - 1
                    self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            elif self.agt1_ori == 1:
                if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
                    self.agt1_pos[1] = self.agt1_pos[1] + 1
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            elif self.agt1_ori == 2:
                if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                    self.agt1_pos[0] = self.agt1_pos[0] + 1
                    self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            elif self.agt1_ori == 3:
                if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                    self.agt1_pos[1] = self.agt1_pos[1] - 1
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        elif action1 == 3:  # catch
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                if self.pig_pos[0] == self.agt1_pos[0]-1:
                    if self.pig_pos[1] == self.agt1_pos[1]:
                        self.if_agt1_catches = True
            elif self.agt1_ori == 1:
                if self.pig_pos[1] == self.agt1_pos[1]+1:
                    if self.pig_pos[0] == self.agt1_pos[0]:
                        self.if_agt1_catches = True
            elif self.agt1_ori == 2:
                if self.pig_pos[0] == self.agt1_pos[0]+1:
                    if self.pig_pos[1] == self.agt1_pos[1]:
                        self.if_agt1_catches = True
            elif self.agt1_ori == 3:
                if self.pig_pos[1] == self.agt1_pos[1]-1:
                    if self.pig_pos[0] == self.agt1_pos[0]:
                        self.if_agt1_catches = True

        # agent2 move
        if action2 == 0:    # turn left
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                self.agt2_ori = 3
            elif self.agt2_ori == 1:
                self.agt2_ori = 0
            elif self.agt2_ori == 2:
                self.agt2_ori = 1
            elif self.agt2_ori == 3:
                self.agt2_ori = 2

        elif action2 == 1:  # turn right
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                self.agt2_ori = 1
            elif self.agt2_ori == 1:
                self.agt2_ori = 2
            elif self.agt2_ori == 2:
                self.agt2_ori = 3
            elif self.agt2_ori == 3:
                self.agt2_ori = 0

        elif action2 == 2:  # move
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                    self.agt2_pos[0] = self.agt2_pos[0] - 1
                    self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            elif self.agt2_ori == 1:
                if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
                    self.agt2_pos[1] = self.agt2_pos[1] + 1
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            elif self.agt2_ori == 2:
                if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                    self.agt2_pos[0] = self.agt2_pos[0] + 1
                    self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            elif self.agt2_ori == 3:
                if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                    self.agt2_pos[1] = self.agt2_pos[1] - 1
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        elif action2 == 3:  # catch
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                if self.pig_pos[0] == self.agt2_pos[0]-1:
                    if self.pig_pos[1] == self.agt2_pos[1]:
                        self.if_agt2_catches = True
            elif self.agt2_ori == 1:
                if self.pig_pos[1] == self.agt2_pos[1]+1:
                    if self.pig_pos[0] == self.agt2_pos[0]:
                        self.if_agt2_catches = True
            elif self.agt2_ori == 2:
                if self.pig_pos[0] == self.agt2_pos[0]+1:
                    if self.pig_pos[1] == self.agt2_pos[1]:
                        self.if_agt2_catches = True
            elif self.agt2_ori == 3:
                if self.pig_pos[1] == self.agt2_pos[1]-1:
                    if self.pig_pos[0] == self.agt2_pos[0]:
                        self.if_agt2_catches = True

        # pig move
        if action_pig == 0:  # turn left
            reward_pig = reward_pig - 1
            if self.pig_ori == 0:
                self.pig_ori = 3
            elif self.pig_ori == 1:
                self.pig_ori = 0
            elif self.pig_ori == 2:
                self.pig_ori = 1
            elif self.pig_ori == 3:
                self.pig_ori = 2

        elif action_pig == 1:  # turn right
            reward_pig = reward_pig - 1
            if self.pig_ori == 0:
                self.pig_ori = 1
            elif self.pig_ori == 1:
                self.pig_ori = 2
            elif self.pig_ori == 2:
                self.pig_ori = 3
            elif self.pig_ori == 3:
                self.pig_ori = 0

        elif action_pig == 2:  # move
            reward_pig = reward_pig - 1
            if self.pig_ori == 0:
                if self.occupancy[self.pig_pos[0] - 1][self.pig_pos[1]] != 1:  # if can move
                    self.pig_pos[0] = self.pig_pos[0] - 1
                    self.occupancy[self.pig_pos[0] + 1][self.pig_pos[1]] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False
            elif self.pig_ori == 1:
                if self.occupancy[self.pig_pos[0]][self.pig_pos[1] + 1] != 1:  # if can move
                    self.pig_pos[1] = self.pig_pos[1] + 1
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1] - 1] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False
            elif self.pig_ori == 2:
                if self.occupancy[self.pig_pos[0] + 1][self.pig_pos[1]] != 1:  # if can move
                    self.pig_pos[0] = self.pig_pos[0] + 1
                    self.occupancy[self.pig_pos[0] - 1][self.pig_pos[1]] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False
            elif self.pig_ori == 3:
                if self.occupancy[self.pig_pos[0]][self.pig_pos[1] - 1] != 1:  # if can move
                    self.pig_pos[1] = self.pig_pos[1] - 1
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1] + 1] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False

        # check if caught
        if self.if_agt1_catches == True:
            if self.if_agt2_catches == True:
                reward_1 = reward_1 + 50
                reward_2 = reward_2 + 50
                reward_pig = reward_pig - 50
                self.reset()

        obs_1 = self.get_agt1_obs()
        obs_2 = self.get_agt2_obs()
        obs_pig = self.get_pig_obs()
        return reward_1, reward_2, reward_pig, obs_1, obs_2, obs_pig

    def test(self, action1_list, action2_list, action_pig_list, max_iter, interval, if_plot):
        self.reset()
        if if_plot:
            self.action1_list = action1_list
            self.action2_list = action2_list
            self.action_pig_list = action_pig_list
            self.agt1_pos_list = self.agt1_pos
            self.agt2_pos_list = self.agt2_pos
            self.pig_pos_list = self.pig_pos
            self.agt1_ori_list = self.agt1_ori
            self.agt2_ori_list = self.agt2_ori
            self.pig_ori_list = self.pig_ori
            self.obs1_list = self.get_agt1_obs()
            self.obs2_list = self.get_agt2_obs()
            self.obs_pig_list = self.get_pig_obs()
            for i in range(max_iter):
                reward_1, reward_2, reward_pig, obs_1, obs_2, obs_pig = self.step(action1_list[0][i], action2_list[0][i], action_pig_list[0][i])
                self.agt1_pos_list = np.vstack((self.agt1_pos_list, self.agt1_pos))
                self.agt2_pos_list = np.vstack((self.agt2_pos_list, self.agt2_pos))
                self.pig_pos_list = np.vstack((self.pig_pos_list, self.pig_pos))
                self.agt1_ori_list = np.vstack((self.agt1_ori_list, self.agt1_ori))
                self.agt2_ori_list = np.vstack((self.agt2_ori_list, self.agt2_ori))
                self.pig_ori_list = np.vstack((self.pig_ori_list, self.pig_ori))
                self.obs1_list = np.vstack((self.obs1_list, obs_1))
                self.obs2_list = np.vstack((self.obs2_list, obs_2))
                self.obs_pig_list = np.vstack((self.obs_pig_list, obs_pig))


            # plot
            anim1 = FuncAnimation(self.fig, self.update_1, frames=np.arange(0, max_iter + 1), interval=interval)
            anim2 = FuncAnimation(self.fig, self.update_2, frames=np.arange(0, max_iter + 1), interval=interval)
            anim3 = FuncAnimation(self.fig, self.update_3, frames=np.arange(0, max_iter + 1), interval=interval)
            anim4 = FuncAnimation(self.fig, self.update_4, frames=np.arange(0, max_iter + 1), interval=interval)
            plt.show()

        else:
            reward_1 = np.zeros((1, max_iter))
            reward_2 = np.zeros((1, max_iter))
            reward_pig = np.zeros((1, max_iter))
            for iter in range(max_iter):
                step_reward_1, step_reward_2, step_reward_pig, obs_1, obs_2, obs_pig = self.step(self, self.action1_list[iter], self.action2_list[iter], self.action_pig_list[iter])
                reward_1[0, iter] = step_reward_1
                reward_2[0, iter] = step_reward_2
                reward_pig[0, iter] = step_reward_pig
                print("iter= ", iter)
                print("agent 1 action= ", action1_list[iter])
                print("agent 2 action= ", action2_list[iter])
                print("pig action= ", action2_list[iter])
                print("agent 1 reward= ", step_reward_1)
                print("agent 2 reward= ", step_reward_2)
                print("pig reward= ", step_reward_pig)
                print("accumulated joint reward= ", np.sum(reward_1) + np.sum(reward_2))
                print("accumulated pig reward= ", np.sum(reward_pig))
                print("agent 1 position= ", self.agt1_pos)
                print("agent 2 position= ", self.agt2_pos)
                print("pig position= ", self.pig_pos)
                print("agent 1 oritation=", self.agt1_ori)
                print("agent 2 oritation=", self.agt2_ori)
                print("pig oritation=", self.pig_ori)
                print("")

    def update_1(self, i):
        self.ax1.cla()
        label = 'timestep {0}'.format(i)
        self.ax1.set_xlabel(label)

        # plot grid
        for k in range(9):
            for j in range(9):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax1.add_patch(rect)

        # plot block
        for k in range(9):
            for j in range(9):
                if self.raw_occupancy[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax1.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos_list[i][0], self.agt1_pos_list[i][1]), 1, 1, color='r')
        self.ax1.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos_list[i][0], self.agt2_pos_list[i][1]), 1, 1, color='b')
        self.ax1.add_patch(rect)

        # plot pig
        rect = plt.Rectangle((self.pig_pos_list[i][0], self.pig_pos_list[i][1]), 1, 1, color='g')
        self.ax1.add_patch(rect)

        self.ax1.set_xlim([-1, 10])
        self.ax1.set_ylim([-1, 10])
        return self.ax1

    def update_2(self, i):
        self.ax2.cla()
        label = 'timestep {0}'.format(i)
        self.ax2.set_xlabel(label)
        for k in range(9):
            for j in range(9):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax2.add_patch(rect)

        obs_1 = self.obs1_list[9*i:9*i+9, :]

        # plot obs 1
        for k in range(9):
            for j in range(9):
                if obs_1[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    self.ax2.add_patch(rect)
                elif obs_1[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax2.add_patch(rect)
                elif obs_1[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    self.ax2.add_patch(rect)
                elif obs_1[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    self.ax2.add_patch(rect)

        self.ax2.set_xlim([-1, 10])
        self.ax2.set_ylim([-1, 10])
        return self.ax2

    def update_3(self, i):
        self.ax3.cla()
        label = 'timestep {0}'.format(i)
        self.ax3.set_xlabel(label)
        for k in range(9):
            for j in range(9):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax3.add_patch(rect)

        obs_2 = self.obs2_list[9 * i:9 * i + 9, :]

        # plot obs 1
        for k in range(9):
            for j in range(9):
                if obs_2[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    self.ax3.add_patch(rect)
                elif obs_2[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax3.add_patch(rect)
                elif obs_2[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    self.ax3.add_patch(rect)
                elif obs_2[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    self.ax3.add_patch(rect)

        self.ax3.set_xlim([-1, 10])
        self.ax3.set_ylim([-1, 10])
        return self.ax3

    def update_4(self, i):
        self.ax4.cla()
        label = 'timestep {0}'.format(i)
        self.ax4.set_xlabel(label)
        for k in range(9):
            for j in range(9):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax4.add_patch(rect)

        obs_pig = self.obs_pig_list[9 * i:9 * i + 9, :]

        # plot obs pig
        for k in range(9):
            for j in range(9):
                if obs_pig[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    self.ax4.add_patch(rect)
                elif obs_pig[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax4.add_patch(rect)
                elif obs_pig[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    self.ax4.add_patch(rect)
                elif obs_pig[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    self.ax4.add_patch(rect)

        self.ax4.set_xlim([-1, 10])
        self.ax4.set_ylim([-1, 10])
        return self.ax4

