import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2

class EnvMoveBox(object):
    def __init__(self):
        self.raw_occupancy = np.zeros((17, 17))
        for i in range(17):
            self.raw_occupancy[0, i] = 1
            self.raw_occupancy[i, 0] = 1
            self.raw_occupancy[16, i] = 1
            self.raw_occupancy[i, 16] = 1
            self.raw_occupancy[14, i] = 1
        self.raw_occupancy[10, 5] = 1
        self.raw_occupancy[10, 6] = 1
        self.raw_occupancy[10, 7] = 1
        self.raw_occupancy[10, 8] = 1
        self.raw_occupancy[10, 9] = 1
        self.raw_occupancy[10, 10] = 1
        self.raw_occupancy[10, 11] = 1
        self.raw_occupancy[0, 7] = 0
        self.raw_occupancy[0, 8] = 0
        self.raw_occupancy[0, 9] = 0
        self.raw_occupancy[14, 8] = 0

        self.occupancy = self.raw_occupancy.copy()

        self.agt1_pos = [15, 1]
        self.occupancy[self.agt1_pos[0], self.agt1_pos[1]] = 1
        self.agt2_pos = [15, 15]
        self.occupancy[self.agt2_pos[0], self.agt2_pos[1]] = 1

        self.box_pos = [11, 8]
        self.occupancy[self.box_pos[0], self.box_pos[1]] = 1

        self.is_1_catch_box = False
        self.is_2_catch_box = False

    def reset(self):
        self.occupancy = self.raw_occupancy.copy()

        self.agt1_pos = [15, 1]
        self.occupancy[self.agt1_pos[0], self.agt1_pos[1]] = 1
        self.agt2_pos = [15, 15]
        self.occupancy[self.agt2_pos[0], self.agt2_pos[1]] = 1

        self.box_pos = [11, 8]
        self.occupancy[self.box_pos[0], self.box_pos[1]] = 1

        self.is_caught_by_1 = False
        self.is_caught_by_2 = False
        self.is_1_catch_box = False
        self.is_2_catch_box = False

    def step(self, action_list):
        if self.is_1_catch_box == False:
            if action_list[0] == 0: # up
                if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                    self.agt1_pos[0] = self.agt1_pos[0] - 1
                    self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            if action_list[0] == 1:   # down
                if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                    self.agt1_pos[0] = self.agt1_pos[0] + 1
                    self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            if action_list[0] == 2:   # left
                if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                    self.agt1_pos[1] = self.agt1_pos[1] - 1
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            if action_list[0] == 3:  # right
                if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
                    self.agt1_pos[1] = self.agt1_pos[1] + 1
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                    self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        if self.is_2_catch_box == False:
            if action_list[1] == 0: # up
                if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                    self.agt2_pos[0] = self.agt2_pos[0] - 1
                    self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            if action_list[1] == 1:   # down
                if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                    self.agt2_pos[0] = self.agt2_pos[0] + 1
                    self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            if action_list[1] == 2:   # left
                if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                    self.agt2_pos[1] = self.agt2_pos[1] - 1
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            if action_list[1] == 3:  # right
                if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
                    self.agt2_pos[1] = self.agt2_pos[1] + 1
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] = 0
                    self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        if self.is_1_catch_box and self.is_2_catch_box:
            if action_list[0] == 0 and action_list[1] == 0: # up
                if self.occupancy[self.box_pos[0] - 1,self.box_pos[1]] == 0 and self.occupancy[self.box_pos[0] - 1,self.box_pos[1] - 1] == 0 and self.occupancy[self.box_pos[0] - 1,self.box_pos[1] + 1] == 0:
                    self.box_pos[0] = self.box_pos[0] - 1
                    self.agt1_pos[0] = self.agt1_pos[0] - 1
                    self.agt2_pos[0] = self.agt2_pos[0] - 1
                    self.occupancy[self.box_pos[0] + 1, self.box_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0] + 1, self.agt1_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0] + 1, self.agt2_pos[1]] = 0
                    self.occupancy[self.box_pos[0], self.box_pos[1]] = 1
                    self.occupancy[self.agt1_pos[0], self.agt1_pos[1]] = 1
                    self.occupancy[self.agt2_pos[0], self.agt2_pos[1]] = 1
            if action_list[0] == 1 and action_list[1] == 1:  # down
                if self.occupancy[self.box_pos[0] + 1,self.box_pos[1]] == 0 and self.occupancy[self.box_pos[0] + 1,self.box_pos[1] - 1] == 0 and self.occupancy[self.box_pos[0] + 1,self.box_pos[1] + 1] == 0:
                    self.box_pos[0] = self.box_pos[0] + 1
                    self.agt1_pos[0] = self.agt1_pos[0] + 1
                    self.agt2_pos[0] = self.agt2_pos[0] + 1
                    self.occupancy[self.box_pos[0] - 1, self.box_pos[1]] = 0
                    self.occupancy[self.agt1_pos[0] - 1, self.agt1_pos[1]] = 0
                    self.occupancy[self.agt2_pos[0] - 1, self.agt2_pos[1]] = 0
                    self.occupancy[self.box_pos[0], self.box_pos[1]] = 1
                    self.occupancy[self.agt1_pos[0], self.agt1_pos[1]] = 1
                    self.occupancy[self.agt2_pos[0], self.agt2_pos[1]] = 1
            if action_list[0] == 2 and action_list[1] == 2:  # left
                if self.occupancy[self.box_pos[0], self.box_pos[1] - 2] == 0:
                    self.box_pos[1] = self.box_pos[1] - 1
                    self.agt1_pos[1] = self.agt1_pos[1] - 1
                    self.agt2_pos[1] = self.agt2_pos[1] - 1
                    self.occupancy[self.box_pos[0], self.box_pos[1] - 1] = 1
                    self.occupancy[self.box_pos[0], self.box_pos[1] + 2] = 0
            if action_list[0] == 3 and action_list[1] == 3:  # right
                if self.occupancy[self.box_pos[0], self.box_pos[1] + 2] == 0:
                    self.box_pos[1] = self.box_pos[1] + 1
                    self.agt1_pos[1] = self.agt1_pos[1] + 1
                    self.agt2_pos[1] = self.agt2_pos[1] + 1
                    self.occupancy[self.box_pos[0], self.box_pos[1] + 1] = 1
                    self.occupancy[self.box_pos[0], self.box_pos[1] - 2] = 0

        if self.agt1_pos[0] == self.box_pos[0] and abs(self.agt1_pos[1] - self.box_pos[1]) == 1:
            self.is_1_catch_box = True

        if self.agt2_pos[0] == self.box_pos[0] and abs(self.agt2_pos[1] - self.box_pos[1]) == 1:
            self.is_2_catch_box = True

        reward_list = [0, 0]
        if self.box_pos == [0, 8]:
            reward_list = [100, 100]
            self.reset()
        return reward_list

    def get_global_obs(self):
        obs = np.ones((17, 17, 3))
        for i in range(17):
            obs[0, i, 0] = 0
            obs[i, 0, 0] = 0
            obs[16, i, 0] = 0
            obs[i, 16, 0] = 0
            obs[14, i, 0] = 0
            obs[0, i, 1] = 0
            obs[i, 0, 1] = 0
            obs[16, i, 1] = 0
            obs[i, 16, 1] = 0
            obs[14, i, 1] = 0
            obs[0, i, 2] = 0
            obs[i, 0, 2] = 0
            obs[16, i, 2] = 0
            obs[i, 16, 2] = 0
            obs[14, i, 2] = 0
        obs[10, 5, 0] = 0
        obs[10, 6, 0] = 0
        obs[10, 7, 0] = 0
        obs[10, 8, 0] = 0
        obs[10, 9, 0] = 0
        obs[10, 10, 0] = 0
        obs[10, 11, 0] = 0
        obs[0, 7, 0] = 1
        obs[0, 8, 0] = 1
        obs[0, 9, 0] = 1
        obs[14, 8, 0] = 1
        obs[10, 5, 1] = 0
        obs[10, 6, 1] = 0
        obs[10, 7, 1] = 0
        obs[10, 8, 1] = 0
        obs[10, 9, 1] = 0
        obs[10, 10, 1] = 0
        obs[10, 11, 1] = 0
        obs[0, 7, 1] = 1
        obs[0, 8, 1] = 1
        obs[0, 9, 1] = 1
        obs[14, 8, 1] = 1
        obs[10, 5, 2] = 0
        obs[10, 6, 2] = 0
        obs[10, 7, 2] = 0
        obs[10, 8, 2] = 0
        obs[10, 9, 2] = 0
        obs[10, 10, 2] = 0
        obs[10, 11, 2] = 0
        obs[0, 7, 2] = 1
        obs[0, 8, 2] = 1
        obs[0, 9, 2] = 1
        obs[14, 8, 2] = 1
        obs[0, 8, 2] = 1
        obs[0, 9, 2] = 1
        obs[14, 8, 2] = 1

        obs[self.agt1_pos[0], self.agt1_pos[1], 0] = 1
        obs[self.agt1_pos[0], self.agt1_pos[1], 1] = 0
        obs[self.agt1_pos[0], self.agt1_pos[1], 2] = 0

        obs[self.agt2_pos[0], self.agt2_pos[1], 0] = 0
        obs[self.agt2_pos[0], self.agt2_pos[1], 1] = 0
        obs[self.agt2_pos[0], self.agt2_pos[1], 2] = 1

        obs[self.box_pos[0], self.box_pos[1], 0] = 0
        obs[self.box_pos[0], self.box_pos[1], 1] = 1
        obs[self.box_pos[0], self.box_pos[1], 2] = 0
        return obs

    def get_agt1_obs(self):
        obs = np.ones((17, 17, 3))
        for i in range(17):
            obs[0, i, 0] = 0
            obs[i, 0, 0] = 0
            obs[16, i, 0] = 0
            obs[i, 16, 0] = 0
            obs[14, i, 0] = 0
            obs[0, i, 1] = 0
            obs[i, 0, 1] = 0
            obs[16, i, 1] = 0
            obs[i, 16, 1] = 0
            obs[14, i, 1] = 0
            obs[0, i, 2] = 0
            obs[i, 0, 2] = 0
            obs[16, i, 2] = 0
            obs[i, 16, 2] = 0
            obs[14, i, 2] = 0
        obs[10, 5, 0] = 0
        obs[10, 6, 0] = 0
        obs[10, 7, 0] = 0
        obs[10, 8, 0] = 0
        obs[10, 9, 0] = 0
        obs[10, 10, 0] = 0
        obs[10, 11, 0] = 0
        obs[0, 7, 0] = 1
        obs[0, 8, 0] = 1
        obs[0, 9, 0] = 1
        obs[14, 8, 0] = 1
        obs[10, 5, 1] = 0
        obs[10, 6, 1] = 0
        obs[10, 7, 1] = 0
        obs[10, 8, 1] = 0
        obs[10, 9, 1] = 0
        obs[10, 10, 1] = 0
        obs[10, 11, 1] = 0
        obs[0, 7, 1] = 1
        obs[0, 8, 1] = 1
        obs[0, 9, 1] = 1
        obs[14, 8, 1] = 1
        obs[10, 5, 2] = 0
        obs[10, 6, 2] = 0
        obs[10, 7, 2] = 0
        obs[10, 8, 2] = 0
        obs[10, 9, 2] = 0
        obs[10, 10, 2] = 0
        obs[10, 11, 2] = 0
        obs[0, 7, 2] = 1
        obs[0, 8, 2] = 1
        obs[0, 9, 2] = 1
        obs[14, 8, 2] = 1
        obs[0, 8, 2] = 1
        obs[0, 9, 2] = 1
        obs[14, 8, 2] = 1

        obs[self.agt1_pos[0], self.agt1_pos[1], 0] = 1
        obs[self.agt1_pos[0], self.agt1_pos[1], 1] = 0
        obs[self.agt1_pos[0], self.agt1_pos[1], 2] = 0

        obs[self.box_pos[0], self.box_pos[1], 0] = 0
        obs[self.box_pos[0], self.box_pos[1], 1] = 1
        obs[self.box_pos[0], self.box_pos[1], 2] = 0
        return obs

    def get_agt2_obs(self):
        obs = np.ones((17, 17, 3))
        for i in range(17):
            obs[0, i, 0] = 0
            obs[i, 0, 0] = 0
            obs[16, i, 0] = 0
            obs[i, 16, 0] = 0
            obs[14, i, 0] = 0
            obs[0, i, 1] = 0
            obs[i, 0, 1] = 0
            obs[16, i, 1] = 0
            obs[i, 16, 1] = 0
            obs[14, i, 1] = 0
            obs[0, i, 2] = 0
            obs[i, 0, 2] = 0
            obs[16, i, 2] = 0
            obs[i, 16, 2] = 0
            obs[14, i, 2] = 0
        obs[10, 5, 0] = 0
        obs[10, 6, 0] = 0
        obs[10, 7, 0] = 0
        obs[10, 8, 0] = 0
        obs[10, 9, 0] = 0
        obs[10, 10, 0] = 0
        obs[10, 11, 0] = 0
        obs[0, 7, 0] = 1
        obs[0, 8, 0] = 1
        obs[0, 9, 0] = 1
        obs[14, 8, 0] = 1
        obs[10, 5, 1] = 0
        obs[10, 6, 1] = 0
        obs[10, 7, 1] = 0
        obs[10, 8, 1] = 0
        obs[10, 9, 1] = 0
        obs[10, 10, 1] = 0
        obs[10, 11, 1] = 0
        obs[0, 7, 1] = 1
        obs[0, 8, 1] = 1
        obs[0, 9, 1] = 1
        obs[14, 8, 1] = 1
        obs[10, 5, 2] = 0
        obs[10, 6, 2] = 0
        obs[10, 7, 2] = 0
        obs[10, 8, 2] = 0
        obs[10, 9, 2] = 0
        obs[10, 10, 2] = 0
        obs[10, 11, 2] = 0
        obs[0, 7, 2] = 1
        obs[0, 8, 2] = 1
        obs[0, 9, 2] = 1
        obs[14, 8, 2] = 1
        obs[0, 8, 2] = 1
        obs[0, 9, 2] = 1
        obs[14, 8, 2] = 1

        obs[self.agt2_pos[0], self.agt2_pos[1], 0] = 0
        obs[self.agt2_pos[0], self.agt2_pos[1], 1] = 0
        obs[self.agt2_pos[0], self.agt2_pos[1], 2] = 1

        obs[self.box_pos[0], self.box_pos[1], 0] = 0
        obs[self.box_pos[0], self.box_pos[1], 1] = 1
        obs[self.box_pos[0], self.box_pos[1], 2] = 0
        return obs

    def get_obs(self):
        return [self.get_agt1_obs(), self.get_agt2_obs()]

    def plot_scene(self):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(2, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])
        ax4 = fig.add_subplot(gs[0, 1])
        ax1.imshow(self.get_global_obs())
        ax2.imshow(self.get_agt1_obs())
        ax3.imshow(self.get_agt2_obs())
        ax4.imshow(self.occupancy)
        plt.show()

    def render(self):
        obs = np.ones((17 * 20, 17 * 20, 3))
        for i in range(17):
            for j in range(17):
                if self.raw_occupancy[i, j] == 1:
                    cv2.rectangle(obs, (j*20, i*20), (j*20+20, i*20+20), (0, 0, 0), -1)
        cv2.rectangle(obs, (self.agt1_pos[1] * 20, self.agt1_pos[0] * 20), (self.agt1_pos[1] * 20 + 20, self.agt1_pos[0] * 20 + 20), (0, 0, 255), -1)
        cv2.rectangle(obs, (self.agt2_pos[1] * 20, self.agt2_pos[0] * 20), (self.agt2_pos[1] * 20 + 20, self.agt2_pos[0] * 20 + 20), (255, 0, 0), -1)
        cv2.rectangle(obs, (self.box_pos[1] * 20, self.box_pos[0] * 20),
                      (self.box_pos[1] * 20 + 20, self.box_pos[0] * 20 + 20), (0, 255, 0), -1)
        cv2.imshow('image', obs)
        cv2.waitKey(50)