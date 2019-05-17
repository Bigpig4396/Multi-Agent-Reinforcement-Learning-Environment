import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random
import cv2

class EnvCatchPigs(object):
    def __init__(self, size, if_PO):
        assert self.check_size(size)
        self.if_PO = if_PO
        self.map_size = size
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0][i] = 1
            self.occupancy[1][i] = 1
            self.occupancy[self.map_size - 2][i] = 1
            self.occupancy[self.map_size - 1][i] = 1
            self.occupancy[i][0] = 1
            self.occupancy[i][1] = 1
            self.occupancy[i][self.map_size - 2] = 1
            self.occupancy[i][self.map_size - 1] = 1

        for i in range(3, self.map_size - 3, 2):
            for j in range(3, self.map_size - 3, 2):
                self.occupancy[i][j] = 1

        self.raw_occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.raw_occupancy[0][i] = 1
            self.raw_occupancy[1][i] = 1
            self.raw_occupancy[self.map_size - 2][i] = 1
            self.raw_occupancy[self.map_size - 1][i] = 1
            self.raw_occupancy[i][0] = 1
            self.raw_occupancy[i][1] = 1
            self.raw_occupancy[i][self.map_size - 2] = 1
            self.raw_occupancy[i][self.map_size - 1] = 1

        for i in range(3, self.map_size - 3, 2):
            for j in range(3, self.map_size - 3, 2):
                self.raw_occupancy[i][j] = 1

        # initialize agent 1
        self.agt1_pos = [random.randint(2, self.map_size - 3), random.randint(2, self.map_size - 3)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1:
            self.agt1_pos = [random.randint(2, self.map_size - 3), random.randint(2, self.map_size - 3)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt1_ori = random.randint(0, 3)

        # initialize agent 2
        self.agt2_pos = [random.randint(2, self.map_size - 3), random.randint(2, self.map_size - 3)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1:
            self.agt2_pos = [random.randint(2, self.map_size - 3), random.randint(2, self.map_size - 3)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt2_ori = random.randint(0, 3)

        # initialize pig
        self.pig_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        while self.occupancy[self.pig_pos[0]][self.pig_pos[1]] == 1:
            self.pig_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1

        self.pig_ori = random.randint(0, 3)

        self.if_agt1_catches = False
        self.if_agt2_catches = False

    def check_size(self, size):
        print("size of map should be an odd integer no smaller than 7")
        if (size % 2) == 1 and size >= 7:
            return True
        else:
            return False

    def reset(self):
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0][i] = 1
            self.occupancy[1][i] = 1
            self.occupancy[self.map_size - 2][i] = 1
            self.occupancy[self.map_size - 1][i] = 1
            self.occupancy[i][0] = 1
            self.occupancy[i][1] = 1
            self.occupancy[i][self.map_size - 2] = 1
            self.occupancy[i][self.map_size - 1] = 1

        for i in range(3, self.map_size - 3, 2):
            for j in range(3, self.map_size - 3, 2):
                self.occupancy[i][j] = 1

        # initialize agent 1
        self.agt1_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        while self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] == 1:
            self.agt1_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt1_ori = random.randint(0, 3)

        # initialize agent 2
        self.agt2_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        while self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] == 1:
            self.agt2_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt2_ori = random.randint(0, 3)

        # initialize pig
        self.pig_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        while self.occupancy[self.pig_pos[0]][self.pig_pos[1]] == 1:
            self.pig_pos = [random.randint(2, self.map_size-3), random.randint(2, self.map_size-3)]
        self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1

        self.pig_ori = random.randint(0, 3)

        self.if_agt1_catches = False
        self.if_agt2_catches = False

    def list_add(self, a, b):
        c = [a[i] + b[i] for i in range(min(len(a), len(b)))]
        return c

    def paint_block(self, obs, i, j):
        new_obs = obs
        for row in range(3):
            for col in range(3):
                new_obs[i * 3 + row, j * 3 + col, 0] = 0.0
                new_obs[i * 3 + row, j * 3 + col, 1] = 0.0
                new_obs[i * 3 + row, j * 3 + col, 2] = 0.0
        return new_obs

    def paint_agt1(self, obs, i, j, ori):
        new_obs = obs
        if ori == 0:
            new_obs[i * 3, j * 3, 0] = 1.0
            new_obs[i * 3, j * 3, 1] = 0.0
            new_obs[i * 3, j * 3, 2] = 0.0
            new_obs[i * 3 + 1, j * 3, 0] = 1.0
            new_obs[i * 3 + 1, j * 3, 1] = 0.0
            new_obs[i * 3 + 1, j * 3, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 0] = 1.0
            new_obs[i * 3 + 1, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 2, j * 3, 0] = 1.0
            new_obs[i * 3 + 2, j * 3, 1] = 0.0
            new_obs[i * 3 + 2, j * 3, 2] = 0.0
        elif ori == 1:
            new_obs[i * 3, j * 3, 0] = 1.0
            new_obs[i * 3, j * 3, 1] = 0.0
            new_obs[i * 3, j * 3, 2] = 0.0
            new_obs[i * 3, j * 3 + 1, 0] = 1.0
            new_obs[i * 3, j * 3 + 1, 1] = 0.0
            new_obs[i * 3, j * 3 + 1, 2] = 0.0
            new_obs[i * 3, j * 3 + 2, 0] = 1.0
            new_obs[i * 3, j * 3 + 2, 1] = 0.0
            new_obs[i * 3, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 0] = 1.0
            new_obs[i * 3 + 2, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 2] = 0.0
        elif ori == 2:
            new_obs[i * 3, j * 3 + 2, 0] = 1.0
            new_obs[i * 3, j * 3 + 2, 1] = 0.0
            new_obs[i * 3, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 1, j * 3, 0] = 1.0
            new_obs[i * 3 + 1, j * 3, 1] = 0.0
            new_obs[i * 3 + 1, j * 3, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 0] = 1.0
            new_obs[i * 3 + 1, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 0] = 1.0
            new_obs[i * 3 + 2, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 2] = 0.0
        elif ori == 3:
            new_obs[i * 3, j * 3 + 1, 0] = 1.0
            new_obs[i * 3, j * 3 + 1, 1] = 0.0
            new_obs[i * 3, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 2, j * 3, 0] = 1.0
            new_obs[i * 3 + 2, j * 3, 1] = 0.0
            new_obs[i * 3 + 2, j * 3, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 0] = 1.0
            new_obs[i * 3 + 2, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 0] = 1.0
            new_obs[i * 3 + 2, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 2] = 0.0
        return new_obs

    def paint_agt2(self, obs, i, j, ori):
        new_obs = obs
        if ori == 0:
            new_obs[i * 3, j * 3, 0] = 0.0
            new_obs[i * 3, j * 3, 1] = 0.0
            new_obs[i * 3, j * 3, 2] = 1.0
            new_obs[i * 3 + 1, j * 3, 0] = 0.0
            new_obs[i * 3 + 1, j * 3, 1] = 0.0
            new_obs[i * 3 + 1, j * 3, 2] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 1.0
            new_obs[i * 3 + 1, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 2] = 1.0
            new_obs[i * 3 + 2, j * 3, 0] = 0.0
            new_obs[i * 3 + 2, j * 3, 1] = 0.0
            new_obs[i * 3 + 2, j * 3, 2] = 1.0
        elif ori == 1:
            new_obs[i * 3, j * 3, 0] = 0.0
            new_obs[i * 3, j * 3, 1] = 0.0
            new_obs[i * 3, j * 3, 2] = 1.0
            new_obs[i * 3, j * 3 + 1, 0] = 0.0
            new_obs[i * 3, j * 3 + 1, 1] = 0.0
            new_obs[i * 3, j * 3 + 1, 2] = 1.0
            new_obs[i * 3, j * 3 + 2, 0] = 0.0
            new_obs[i * 3, j * 3 + 2, 1] = 0.0
            new_obs[i * 3, j * 3 + 2, 2] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 1.0
            new_obs[i * 3 + 2, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 2] = 1.0
        elif ori == 2:
            new_obs[i * 3, j * 3 + 2, 0] = 0.0
            new_obs[i * 3, j * 3 + 2, 1] = 0.0
            new_obs[i * 3, j * 3 + 2, 2] = 1.0
            new_obs[i * 3 + 1, j * 3, 0] = 0.0
            new_obs[i * 3 + 1, j * 3, 1] = 0.0
            new_obs[i * 3 + 1, j * 3, 2] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 1.0
            new_obs[i * 3 + 1, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 2] = 1.0
            new_obs[i * 3 + 2, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 2] = 1.0
        elif ori == 3:
            new_obs[i * 3, j * 3 + 1, 0] = 0.0
            new_obs[i * 3, j * 3 + 1, 1] = 0.0
            new_obs[i * 3, j * 3 + 1, 2] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 1.0
            new_obs[i * 3 + 2, j * 3, 0] = 0.0
            new_obs[i * 3 + 2, j * 3, 1] = 0.0
            new_obs[i * 3 + 2, j * 3, 2] = 1.0
            new_obs[i * 3 + 2, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 2] = 1.0
            new_obs[i * 3 + 2, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 1] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 2] = 1.0
        return new_obs

    def paint_pig(self, obs, i, j, ori):
        new_obs = obs
        if ori == 0:
            new_obs[i * 3, j * 3, 0] = 0.0
            new_obs[i * 3, j * 3, 1] = 1.0
            new_obs[i * 3, j * 3, 2] = 0.0
            new_obs[i * 3 + 1, j * 3, 0] = 0.0
            new_obs[i * 3 + 1, j * 3, 1] = 1.0
            new_obs[i * 3 + 1, j * 3, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 1] = 1.0
            new_obs[i * 3 + 1, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 2, j * 3, 0] = 0.0
            new_obs[i * 3 + 2, j * 3, 1] = 1.0
            new_obs[i * 3 + 2, j * 3, 2] = 0.0
        elif ori == 1:
            new_obs[i * 3, j * 3, 0] = 0.0
            new_obs[i * 3, j * 3, 1] = 1.0
            new_obs[i * 3, j * 3, 2] = 0.0
            new_obs[i * 3, j * 3 + 1, 0] = 0.0
            new_obs[i * 3, j * 3 + 1, 1] = 1.0
            new_obs[i * 3, j * 3 + 1, 2] = 0.0
            new_obs[i * 3, j * 3 + 2, 0] = 0.0
            new_obs[i * 3, j * 3 + 2, 1] = 1.0
            new_obs[i * 3, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 1] = 1.0
            new_obs[i * 3 + 2, j * 3 + 1, 2] = 0.0
        elif ori == 2:
            new_obs[i * 3, j * 3 + 2, 0] = 0.0
            new_obs[i * 3, j * 3 + 2, 1] = 1.0
            new_obs[i * 3, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 1, j * 3, 0] = 0.0
            new_obs[i * 3 + 1, j * 3, 1] = 1.0
            new_obs[i * 3 + 1, j * 3, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 2, 1] = 1.0
            new_obs[i * 3 + 1, j * 3 + 2, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 1] = 1.0
            new_obs[i * 3 + 2, j * 3 + 2, 2] = 0.0
        elif ori == 3:
            new_obs[i * 3, j * 3 + 1, 0] = 0.0
            new_obs[i * 3, j * 3 + 1, 1] = 1.0
            new_obs[i * 3, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 1, j * 3 + 1, 1] = 1.0
            new_obs[i * 3 + 1, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 2, j * 3, 0] = 0.0
            new_obs[i * 3 + 2, j * 3, 1] = 1.0
            new_obs[i * 3 + 2, j * 3, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 1, 1] = 1.0
            new_obs[i * 3 + 2, j * 3 + 1, 2] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 0] = 0.0
            new_obs[i * 3 + 2, j * 3 + 2, 1] = 1.0
            new_obs[i * 3 + 2, j * 3 + 2, 2] = 0.0
        return new_obs

    def get_agt1_obs(self):
        obs = []
        if self.if_PO == False:
            obs = self.get_global_obs()
        else:
            obs = np.zeros((5*3, 5*3, 3))
            for i in range(5*3):
                for j in range(5*3):
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
            for k in range(5):
                if self.raw_occupancy[self.agt1_pos[0] - 2][self.agt1_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 0)
                if self.raw_occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 1)
                if self.raw_occupancy[self.agt1_pos[0]][self.agt1_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 2)
                if self.raw_occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 3)
                if self.raw_occupancy[self.agt1_pos[0] + 2][self.agt1_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 4)

            # detect self
            self.paint_agt1(obs, 2, 2, self.agt1_ori)

            # detect agent2
            for k in range(5):
                if self.agt2_pos == self.list_add(self.agt1_pos, [-2 + k, 2]):
                    self.paint_agt2(obs, 0, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.agt1_pos, [-2 + k, 1]):
                    self.paint_agt2(obs, 1, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.agt1_pos, [-2 + k, 0]):
                    self.paint_agt2(obs, 2, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.agt1_pos, [-2 + k, -1]):
                    self.paint_agt2(obs, 3, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.agt1_pos, [-2 + k, -2]):
                    self.paint_agt2(obs, 4, k, self.agt2_ori)

            # detect pig
            for k in range(5):
                if self.pig_pos == self.list_add(self.agt1_pos, [-2 + k, 2]):
                    self.paint_pig(obs, 0, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt1_pos, [-2 + k, 1]):
                    self.paint_pig(obs, 1, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt1_pos, [-2 + k, 0]):
                    self.paint_pig(obs, 2, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt1_pos, [-2 + k, -1]):
                    self.paint_pig(obs, 3, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt1_pos, [-2 + k, -2]):
                    self.paint_pig(obs, 4, k, self.pig_ori)

            # add fog
            if self.agt1_ori == 0:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[i, 14-j, 0] = 0.5
                        obs[i, 14-j, 1] = 0.5
                        obs[i, 14-j, 2] = 0.5
            if self.agt1_ori == 1:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[14-j, i, 0] = 0.5
                        obs[14-j, i, 1] = 0.5
                        obs[14-j, i, 2] = 0.5
            if self.agt1_ori == 2:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[i, j, 0] = 0.5
                        obs[i, j, 1] = 0.5
                        obs[i, j, 2] = 0.5
            if self.agt1_ori == 3:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[j, i, 0] = 0.5
                        obs[j, i, 1] = 0.5
                        obs[j, i, 2] = 0.5

        return obs

    def get_agt2_obs(self):
        obs = []
        if self.if_PO == False:
            obs = self.get_global_obs()
        else:
            obs = np.zeros((5*3, 5*3, 3))
            for i in range(5*3):
                for j in range(5*3):
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
            for k in range(5):
                if self.raw_occupancy[self.agt2_pos[0] - 2][self.agt2_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 0)
                if self.raw_occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 1)
                if self.raw_occupancy[self.agt2_pos[0]][self.agt2_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 2)
                if self.raw_occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 3)
                if self.raw_occupancy[self.agt2_pos[0] + 2][self.agt2_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4-k, 4)

            # detect self
            self.paint_agt2(obs, 2, 2, self.agt2_ori)

            # detect agent1
            for k in range(5):
                if self.agt1_pos == self.list_add(self.agt2_pos, [-2 + k, 2]):
                    self.paint_agt1(obs, 0, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.agt2_pos, [-2 + k, 1]):
                    self.paint_agt1(obs, 1, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.agt2_pos, [-2 + k, 0]):
                    self.paint_agt1(obs, 2, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.agt2_pos, [-2 + k, -1]):
                    self.paint_agt1(obs, 3, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.agt2_pos, [-2 + k, -2]):
                    self.paint_agt1(obs, 4, k, self.agt1_ori)

            # detect pig
            for k in range(5):
                if self.pig_pos == self.list_add(self.agt2_pos, [-2 + k, 2]):
                    self.paint_pig(obs, 0, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt2_pos, [-2 + k, 1]):
                    self.paint_pig(obs, 1, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt2_pos, [-2 + k, 0]):
                    self.paint_pig(obs, 2, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt2_pos, [-2 + k, -1]):
                    self.paint_pig(obs, 3, k, self.pig_ori)
                if self.pig_pos == self.list_add(self.agt2_pos, [-2 + k, -2]):
                    self.paint_pig(obs, 4, k, self.pig_ori)

            # add fog
            if self.agt2_ori == 0:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[i, 14-j, 0] = 0.5
                        obs[i, 14-j, 1] = 0.5
                        obs[i, 14-j, 2] = 0.5
            if self.agt2_ori == 1:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[14-j, i, 0] = 0.5
                        obs[14-j, i, 1] = 0.5
                        obs[14-j, i, 2] = 0.5
            if self.agt2_ori == 2:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[i, j, 0] = 0.5
                        obs[i, j, 1] = 0.5
                        obs[i, j, 2] = 0.5
            if self.agt2_ori == 3:
                for i in range(5*3):
                    for j in range(2*3):
                        obs[j, i, 0] = 0.5
                        obs[j, i, 1] = 0.5
                        obs[j, i, 2] = 0.5

        return obs

    def get_pig_obs(self):
        obs = []
        if self.if_PO == False:
            obs = self.get_global_obs()
        else:
            obs = np.zeros((5 * 3, 5 * 3, 3))
            for i in range(5 * 3):
                for j in range(5 * 3):
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
            for k in range(5):
                if self.raw_occupancy[self.pig_pos[0] - 2][self.pig_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4 - k, 0)
                if self.raw_occupancy[self.pig_pos[0] - 1][self.pig_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4 - k, 1)
                if self.raw_occupancy[self.pig_pos[0]][self.pig_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4 - k, 2)
                if self.raw_occupancy[self.pig_pos[0] + 1][self.pig_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4 - k, 3)
                if self.raw_occupancy[self.pig_pos[0] + 2][self.pig_pos[1] + k - 2] == 1:
                    self.paint_block(obs, 4 - k, 4)

            # detect self
            self.paint_pig(obs, 2, 2, self.pig_ori)

            # detect agent1
            for k in range(5):
                if self.agt1_pos == self.list_add(self.pig_pos, [-2 + k, 2]):
                    self.paint_agt1(obs, 0, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.pig_pos, [-2 + k, 1]):
                    self.paint_agt1(obs, 1, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.pig_pos, [-2 + k, 0]):
                    self.paint_agt1(obs, 2, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.pig_pos, [-2 + k, -1]):
                    self.paint_agt1(obs, 3, k, self.agt1_ori)
                if self.agt1_pos == self.list_add(self.pig_pos, [-2 + k, -2]):
                    self.paint_agt1(obs, 4, k, self.agt1_ori)


            # detect agent2
            for k in range(5):
                if self.agt2_pos == self.list_add(self.pig_pos, [-2 + k, 2]):
                    self.paint_agt2(obs, 0, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.pig_pos, [-2 + k, 1]):
                    self.paint_agt2(obs, 1, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.pig_pos, [-2 + k, 0]):
                    self.paint_agt2(obs, 2, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.pig_pos, [-2 + k, -1]):
                    self.paint_agt2(obs, 3, k, self.agt2_ori)
                if self.agt2_pos == self.list_add(self.pig_pos, [-2 + k, -2]):
                    self.paint_agt2(obs, 4, k, self.agt2_ori)

            # add fog
            if self.pig_ori == 0:
                for i in range(5 * 3):
                    for j in range(2 * 3):
                        obs[i, 14 - j, 0] = 0.5
                        obs[i, 14 - j, 1] = 0.5
                        obs[i, 14 - j, 2] = 0.5
            if self.pig_ori == 1:
                for i in range(5 * 3):
                    for j in range(2 * 3):
                        obs[14 - j, i, 0] = 0.5
                        obs[14 - j, i, 1] = 0.5
                        obs[14 - j, i, 2] = 0.5
            if self.pig_ori == 2:
                for i in range(5 * 3):
                    for j in range(2 * 3):
                        obs[i, j, 0] = 0.5
                        obs[i, j, 1] = 0.5
                        obs[i, j, 2] = 0.5
            if self.pig_ori == 3:
                for i in range(5 * 3):
                    for j in range(2 * 3):
                        obs[j, i, 0] = 0.5
                        obs[j, i, 1] = 0.5
                        obs[j, i, 2] = 0.5

        return obs

    def get_obs(self):
        return [self.get_agt1_obs(), self.get_agt2_obs()]

    def get_full_obs(self):
        obs = np.zeros((self.map_size*3, self.map_size*3, 3))
        for i in range(self.map_size*3):
            for j in range(self.map_size*3):
                obs[i, j, 0] = 1.0
                obs[i, j, 1] = 1.0
                obs[i, j, 2] = 1.0
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.raw_occupancy[i][j] == 1:
                    self.paint_block(obs, i, j)
        self.paint_agt1(obs, self.map_size - self.agt1_pos[1] - 1, self.agt1_pos[0], self.agt1_ori)
        self.paint_agt2(obs, self.map_size - self.agt2_pos[1] - 1, self.agt2_pos[0], self.agt2_ori)
        self.paint_pig(obs, self.map_size - self.pig_pos[1] - 1, self.pig_pos[0], self.pig_ori)
        return obs

    def step(self, action_list):
        reward_1 = 0
        reward_2 = 0
        reward_pig = 0

        # agent1 move
        if action_list[0] == 0:    # turn left
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                self.agt1_ori = 3
            elif self.agt1_ori == 1:
                self.agt1_ori = 0
            elif self.agt1_ori == 2:
                self.agt1_ori = 1
            elif self.agt1_ori == 3:
                self.agt1_ori = 2

        elif action_list[0] == 1:  # turn right
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                self.agt1_ori = 1
            elif self.agt1_ori == 1:
                self.agt1_ori = 2
            elif self.agt1_ori == 2:
                self.agt1_ori = 3
            elif self.agt1_ori == 3:
                self.agt1_ori = 0

        elif action_list[0] == 2:  # move
            reward_1 = reward_1 - 1
            if self.agt1_ori == 0:
                if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                    self.agt1_pos[0] = self.agt1_pos[0] - 1
                    self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
                else:
                    reward_1 = reward_1 - 20
            elif self.agt1_ori == 1:
                if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
                    self.agt1_pos[1] = self.agt1_pos[1] + 1
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
                else:
                    reward_1 = reward_1 - 20
            elif self.agt1_ori == 2:
                if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                    self.agt1_pos[0] = self.agt1_pos[0] + 1
                    self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
                else:
                    reward_1 = reward_1 - 20
            elif self.agt1_ori == 3:
                if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                    self.agt1_pos[1] = self.agt1_pos[1] - 1
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
                else:
                    reward_1 = reward_1 - 20

        elif action_list[0] == 3:  # catch
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
        if action_list[1] == 0:    # turn left
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                self.agt2_ori = 3
            elif self.agt2_ori == 1:
                self.agt2_ori = 0
            elif self.agt2_ori == 2:
                self.agt2_ori = 1
            elif self.agt2_ori == 3:
                self.agt2_ori = 2

        elif action_list[1] == 1:  # turn right
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                self.agt2_ori = 1
            elif self.agt2_ori == 1:
                self.agt2_ori = 2
            elif self.agt2_ori == 2:
                self.agt2_ori = 3
            elif self.agt2_ori == 3:
                self.agt2_ori = 0

        elif action_list[1] == 2:  # move
            reward_2 = reward_2 - 1
            if self.agt2_ori == 0:
                if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                    self.agt2_pos[0] = self.agt2_pos[0] - 1
                    self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
                else:
                    reward_2 = reward_2 - 20
            elif self.agt2_ori == 1:
                if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
                    self.agt2_pos[1] = self.agt2_pos[1] + 1
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
                else:
                    reward_2 = reward_2 - 20
            elif self.agt2_ori == 2:
                if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                    self.agt2_pos[0] = self.agt2_pos[0] + 1
                    self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
                else:
                    reward_2 = reward_2 - 20
            elif self.agt2_ori == 3:
                if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                    self.agt2_pos[1] = self.agt2_pos[1] - 1
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
                else:
                    reward_2 = reward_2 - 20

        elif action_list[1] == 3:  # catch
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
        action_pig = random.randint(0,3)
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
                else:
                    reward_pig = reward_pig - 20
            elif self.pig_ori == 1:
                if self.occupancy[self.pig_pos[0]][self.pig_pos[1] + 1] != 1:  # if can move
                    self.pig_pos[1] = self.pig_pos[1] + 1
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1] - 1] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False
                else:
                    reward_pig = reward_pig - 20
            elif self.pig_ori == 2:
                if self.occupancy[self.pig_pos[0] + 1][self.pig_pos[1]] != 1:  # if can move
                    self.pig_pos[0] = self.pig_pos[0] + 1
                    self.occupancy[self.pig_pos[0] - 1][self.pig_pos[1]] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False
                else:
                    reward_pig = reward_pig - 20
            elif self.pig_ori == 3:
                if self.occupancy[self.pig_pos[0]][self.pig_pos[1] - 1] != 1:  # if can move
                    self.pig_pos[1] = self.pig_pos[1] - 1
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1] + 1] = 0
                    self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
                    self.if_agt1_catches = False
                    self.if_agt2_catches = False
                else:
                    reward_pig = reward_pig - 20

        # check if caught
        if (self.if_agt1_catches == True) and (self.if_agt2_catches == True):
            reward_1 = reward_1 + 500
            reward_2 = reward_2 + 500
            reward_pig = reward_pig - 500
            self.reset()
        else:
            if action_list[1] == 3:
                reward_2 = reward_2 - 50
            if action_list[0] == 3:
                reward_1 = reward_1 - 50

        self.if_agt1_catches = False
        self.if_agt2_catches = False
        done = False
        if reward_1>0:
            done = True
        return [reward_1, reward_2], done

    def plot_scene(self):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(3, 3, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:3])
        plt.xticks([])
        plt.yticks([])
        ax2 = fig.add_subplot(gs[2, 0:1])
        plt.xticks([])
        plt.yticks([])
        ax3 = fig.add_subplot(gs[2, 1:2])
        plt.xticks([])
        plt.yticks([])
        ax4 = fig.add_subplot(gs[2, 2:3])
        plt.xticks([])
        plt.yticks([])

        ax1.imshow(self.get_full_obs())
        ax2.imshow(self.get_agt1_obs())
        ax3.imshow(self.get_agt2_obs())
        ax4.imshow(self.get_pig_obs())

        plt.show()

    def set_agt1_at(self, tgt_pos, tgt_ori):
        if self.occupancy[tgt_pos[0]][tgt_pos[1]] == 0:     # free space
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 0
            self.agt1_pos = tgt_pos
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            self.agt1_ori = tgt_ori

    def set_agt2_at(self, tgt_pos, tgt_ori):
        if self.occupancy[tgt_pos[0]][tgt_pos[1]] == 0:     # free space
            self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 0
            self.agt2_pos = tgt_pos
            self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            self.agt2_ori = tgt_ori

    def set_pig_at(self, tgt_pos, tgt_ori):
        if self.occupancy[tgt_pos[0]][tgt_pos[1]] == 0:     # free space
            self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 0
            self.pig_pos = tgt_pos
            self.occupancy[self.pig_pos[0]][self.pig_pos[1]] = 1
            self.pig_ori = tgt_ori

    def render(self):
        obs = np.ones((self.map_size*21, self.map_size*21, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.raw_occupancy[i, j] == 1:
                    cv2.rectangle(obs, (i*21, j*21), (i*21+21, j*21+21), (0, 0, 0), -1)
        # plot agent1
        temp_x = self.agt1_pos[0]
        temp_y = self.map_size - self.agt1_pos[1] - 1
        if self.agt1_ori == 0:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21), (temp_x * 21 + 7, temp_y * 21 + 21), (0, 0, 255), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21 + 7), (temp_x * 21 + 21, temp_y * 21 + 14), (0, 0, 255),
                          -1)
        elif self.agt1_ori==1:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21), (temp_x * 21 + 21, temp_y * 21 + 7), (0, 0, 255), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21 + 7), (temp_x * 21 + 14, temp_y * 21 + 21), (0, 0, 255),
                          -1)
        elif self.agt1_ori == 2:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21 + 7), (temp_x * 21 + 14, temp_y * 21 + 14), (0, 0, 255), -1)
            cv2.rectangle(obs, (temp_x * 21 + 14, temp_y * 21), (temp_x * 21 + 21, temp_y * 21 + 21), (0, 0, 255), -1)
        else:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21 + 14), (temp_x * 21 + 21, temp_y * 21 + 21), (0, 0, 255), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21), (temp_x * 21 + 14, temp_y * 21 + 14), (0, 0, 255), -1)

        # plot agent2
        temp_x = self.agt2_pos[0]
        temp_y = self.map_size - self.agt2_pos[1] - 1
        if self.agt2_ori == 0:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21), (temp_x * 21 + 7, temp_y * 21 + 21), (255, 0, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21 + 7), (temp_x * 21 + 21, temp_y * 21 + 14), (255, 0, 0),
                          -1)
        elif self.agt2_ori==1:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21), (temp_x * 21 + 21, temp_y * 21 + 7), (255, 0, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21 + 7), (temp_x * 21 + 14, temp_y * 21 + 21), (255, 0, 0),
                          -1)
        elif self.agt2_ori == 2:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21 + 7), (temp_x * 21 + 14, temp_y * 21 + 14), (255, 0, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 14, temp_y * 21), (temp_x * 21 + 21, temp_y * 21 + 21), (255, 0, 0), -1)
        else:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21 + 14), (temp_x * 21 + 21, temp_y * 21 + 21), (255, 0, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21), (temp_x * 21 + 14, temp_y * 21 + 14), (255, 0, 0), -1)

        # plot pig
        temp_x = self.pig_pos[0]
        temp_y = self.map_size - self.pig_pos[1] - 1
        if self.pig_ori == 0:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21), (temp_x * 21 + 7, temp_y * 21 + 21), (0, 255, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21 + 7), (temp_x * 21 + 21, temp_y * 21 + 14), (0, 255, 0),
                          -1)
        elif self.pig_ori == 1:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21), (temp_x * 21 + 21, temp_y * 21 + 7), (0, 255, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21 + 7), (temp_x * 21 + 14, temp_y * 21 + 21), (0, 255, 0),
                          -1)
        elif self.pig_ori == 2:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21 + 7), (temp_x * 21 + 14, temp_y * 21 + 14), (0, 255, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 14, temp_y * 21), (temp_x * 21 + 21, temp_y * 21 + 21), (0, 255, 0), -1)
        else:
            cv2.rectangle(obs, (temp_x * 21, temp_y * 21 + 14), (temp_x * 21 + 21, temp_y * 21 + 21), (0, 255, 0), -1)
            cv2.rectangle(obs, (temp_x * 21 + 7, temp_y * 21), (temp_x * 21 + 14, temp_y * 21 + 14), (0, 255, 0), -1)
        cv2.imshow('image', obs)
        cv2.waitKey(50)