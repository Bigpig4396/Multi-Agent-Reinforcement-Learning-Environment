import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random


class EnvCatchPigs(object):
    def __init__(self, size):
        assert self.check_size(size)
        self.map_size = size
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0][i] = 1
            self.occupancy[self.map_size-1][i] = 1
            self.occupancy[i][0] = 1
            self.occupancy[i][self.map_size-1] = 1

        for i in range(2, self.map_size - 2, 2):
            for j in range(2, self.map_size - 2, 2):
                self.occupancy[i][j] = 1

        self.raw_occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.raw_occupancy[0][i] = 1
            self.raw_occupancy[self.map_size - 1][i] = 1
            self.raw_occupancy[i][0] = 1
            self.raw_occupancy[i][self.map_size - 1] = 1

        for i in range(2, self.map_size - 2, 2):
            for j in range(2, self.map_size - 2, 2):
                self.raw_occupancy[i][j] = 1

        # initialize agent 1
        self.agt1_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1:
            self.agt1_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt1_ori = random.randint(0, 3)

        # initialize agent 2
        self.agt2_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1:
            self.agt2_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt2_ori = random.randint(0, 3)

        # initialize pig
        self.pig_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        while self.occupancy[self.pig_pos[0]][self.pig_pos[1]] == 1:
            self.pig_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1

        self.pig_ori = random.randint(0, 3)

        self.if_agt1_catches = False
        self.if_agt2_catches = False

    def check_size(self, size):
        print("size of map should be an odd integer no smaller than 5")
        if (size % 2) == 1 and size >= 5:
            return True
        else:
            return False

    def reset(self):
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0][i] = 1
            self.occupancy[self.map_size - 1][i] = 1
            self.occupancy[i][0] = 1
            self.occupancy[i][self.map_size - 1] = 1

        for i in range(2, self.map_size - 2, 2):
            for j in range(2, self.map_size - 2, 2):
                self.occupancy[i][j] = 1

        # initialize agent 1
        self.agt1_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1:
            self.agt1_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt1_ori = random.randint(0, 3)

        # initialize agent 2
        self.agt2_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1:
            self.agt2_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt2_ori = random.randint(0, 3)

        # initialize pig
        self.pig_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        while self.occupancy[self.pig_pos[0]][self.pig_pos[1]] == 1:
            self.pig_pos = [random.randint(1, self.map_size-2), random.randint(1, self.map_size-2)]
        self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1

        self.pig_ori = random.randint(0, 3)

        self.if_agt1_catches = False
        self.if_agt2_catches = False

    def get_agt1_obs(self):
        obs = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            for j in range(self.map_size):
                obs[i][j] = 4

        x = self.agt1_pos[0]
        y = self.agt1_pos[1]

        if self.agt1_ori == 0:  # if agent is facing west
            for i in range(0, x+1):
                for j in range(max(0, y-x+i), min(self.map_size-1, y+x-i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt1_ori == 1:    # if agent is facing north
            for j in range(y, self.map_size):
                for i in range(max(0, x+y-j), min(self.map_size-1, x-y+j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt1_ori == 2:    # if agent is facing east
            for i in range(x, self.map_size):
                for j in range(max(0, y+x-i), min(self.map_size-1, y-x+i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt1_ori == 3:    # if agent is facing south
            for j in range(0, y+1):
                for i in range(max(0, x-y+j), min(self.map_size-1, x+y-j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        return obs

    def get_agt2_obs(self):
        obs = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            for j in range(self.map_size):
                obs[i][j] = 4

        x = self.agt2_pos[0]
        y = self.agt2_pos[1]

        if self.agt2_ori == 0:  # if agent is facing west
            for i in range(0, x + 1):
                for j in range(max(0, y - x + i), min(self.map_size-1, y + x - i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt2_ori == 1:  # if agent is facing north
            for j in range(y, self.map_size):
                for i in range(max(0, x + y - j), min(self.map_size-1, x - y + j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt2_ori == 2:  # if agent is facing east
            for i in range(x, self.map_size):
                for j in range(max(0, y + x - i), min(self.map_size-1, y - x + i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.agt2_ori == 3:  # if agent is facing south
            for j in range(0, y + 1):
                for i in range(max(0, x - y + j), min(self.map_size-1, x + y - j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        return obs

    def get_pig_obs(self):
        obs = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            for j in range(self.map_size):
                obs[i][j] = 4

        x = self.pig_pos[0]
        y = self.pig_pos[1]

        if self.pig_ori == 0:  # if agent is facing west
            for i in range(0, x + 1):
                for j in range(max(0, y - x + i), min(self.map_size-1, y + x - i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.pig_ori == 1:  # if agent is facing north
            for j in range(y, self.map_size):
                for i in range(max(0, x + y - j), min(self.map_size-1, x - y + j)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.pig_ori == 2:  # if agent is facing east
            for i in range(x, self.map_size):
                for j in range(max(0, y + x - i), min(self.map_size-1, y - x + i)+1):
                    obs[i][j] = self.raw_occupancy[i][j]
                    if [i, j] == self.agt1_pos:
                        obs[i][j] = 2
                    if [i, j] == self.agt2_pos:
                        obs[i][j] = 2
                    if [i, j] == self.pig_pos:
                        obs[i][j] = 3

        elif self.pig_ori == 3:  # if agent is facing south
            for j in range(0, y + 1):
                for i in range(max(0, x - y + j), min(self.map_size-1, x + y - j)+1):
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
            #reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                self.agt1_ori = 3
            elif self.agt1_ori == 1:
                self.agt1_ori = 0
            elif self.agt1_ori == 2:
                self.agt1_ori = 1
            elif self.agt1_ori == 3:
                self.agt1_ori = 2

        elif action1 == 1:  # turn right
            #reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                self.agt1_ori = 1
            elif self.agt1_ori == 1:
                self.agt1_ori = 2
            elif self.agt1_ori == 2:
                self.agt1_ori = 3
            elif self.agt1_ori == 3:
                self.agt1_ori = 0

        elif action1 == 2:  # move
            #reward_1 = reward_1 - 1
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
            #reward_1 = reward_1 - 1
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
            #reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                self.agt2_ori = 3
            elif self.agt2_ori == 1:
                self.agt2_ori = 0
            elif self.agt2_ori == 2:
                self.agt2_ori = 1
            elif self.agt2_ori == 3:
                self.agt2_ori = 2

        elif action2 == 1:  # turn right
            #reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                self.agt2_ori = 1
            elif self.agt2_ori == 1:
                self.agt2_ori = 2
            elif self.agt2_ori == 2:
                self.agt2_ori = 3
            elif self.agt2_ori == 3:
                self.agt2_ori = 0

        elif action2 == 2:  # move
            #reward_2 = reward_2 - 1
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
            #reward_2 = reward_2 - 1
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

    def plot_scene(self):
        fig = plt.figure(figsize=(8, 8))
        gs = GridSpec(3, 3, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:3])
        ax2 = fig.add_subplot(gs[2, 0:1])
        ax3 = fig.add_subplot(gs[2, 1:2])
        ax4 = fig.add_subplot(gs[2, 2:3])

        # plot grid
        for k in range(self.map_size):
            for j in range(self.map_size):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax1.add_patch(rect)

        # plot block
        for k in range(self.map_size):
            for j in range(self.map_size):
                    if self.occupancy[k][j] == 1:
                        rect = plt.Rectangle((k, j), 1, 1, color='k')
                        ax1.add_patch(rect)

        # plot pig
        rect = plt.Rectangle((self.pig_pos[0], self.pig_pos[1]), 1, 1, color='g')
        ax1.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos[0], self.agt1_pos[1]), 1, 1, color='r')
        ax1.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos[0], self.agt2_pos[1]), 1, 1, color='b')
        ax1.add_patch(rect)

        ax1.set_xlim([-1, self.map_size+2])
        ax1.set_ylim([-1, self.map_size+2])

        # plot grid
        for k in range(self.map_size):
            for j in range(self.map_size):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax2.add_patch(rect)

        obs_1 = self.get_agt1_obs()
        for k in range(self.map_size):
            for j in range(self.map_size):
                if obs_1[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    ax2.add_patch(rect)
                elif obs_1[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax2.add_patch(rect)


        ax2.set_xlim([-1, self.map_size+2])
        ax2.set_ylim([-1, self.map_size+2])

        # plot grid
        for k in range(self.map_size):
            for j in range(self.map_size):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax3.add_patch(rect)

        obs_2 = self.get_agt2_obs()
        for k in range(self.map_size):
            for j in range(self.map_size):
                if obs_2[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    ax3.add_patch(rect)
                elif obs_2[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax3.add_patch(rect)

        ax3.set_xlim([-1, self.map_size+2])
        ax3.set_ylim([-1, self.map_size+2])

        # plot grid
        for k in range(self.map_size):
            for j in range(self.map_size):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                ax4.add_patch(rect)

        obs_pig = self.get_pig_obs()
        for k in range(self.map_size):
            for j in range(self.map_size):
                if obs_pig[k][j] == 2:
                    rect = plt.Rectangle((k, j), 1, 1, color='r')
                    ax4.add_patch(rect)
                elif obs_pig[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    ax4.add_patch(rect)
                elif obs_pig[k][j] == 3:
                    rect = plt.Rectangle((k, j), 1, 1, color='g')
                    ax4.add_patch(rect)
                elif obs_pig[k][j] == 4:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    ax4.add_patch(rect)

        ax4.set_xlim([-1, self.map_size+2])
        ax4.set_ylim([-1, self.map_size+2])

        plt.show()

    def print_info(self):
        print("agent 1 is at", self.agt1_pos)
        print("agent 1 is looking at", self.agt1_ori)
        print("agent 2 is at", self.agt2_pos)
        print("agent 2 is looking at", self.agt2_ori)
        print("pig is at", self.pig_pos)
        print("pig is looking at", self.pig_ori)
        print(" ")
