import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2

class EnvMoveBox(object):
    def __init__(self):
        self.raw_occupancy = np.zeros((15, 15))
        for i in range(15):
            self.raw_occupancy[0, i] = 1
            self.raw_occupancy[i, 0] = 1
            self.raw_occupancy[14, i] = 1
            self.raw_occupancy[i, 14] = 1
            self.raw_occupancy[1, i] = 1
            self.raw_occupancy[5, i] = 1
            self.raw_occupancy[6, i] = 1
        self.raw_occupancy[1, 6] = 0
        self.raw_occupancy[1, 7] = 0
        self.raw_occupancy[1, 8] = 0
        self.raw_occupancy[5, 1] = 0
        self.raw_occupancy[5, 2] = 0
        self.raw_occupancy[5, 3] = 0
        self.raw_occupancy[5, 4] = 0
        self.raw_occupancy[6, 1] = 0
        self.raw_occupancy[6, 2] = 0
        self.raw_occupancy[6, 3] = 0
        self.raw_occupancy[6, 4] = 0
        self.raw_occupancy[6, 6] = 0
        self.raw_occupancy[6, 7] = 0
        self.raw_occupancy[6, 8] = 0
        self.raw_occupancy[11, 6] = 1
        self.raw_occupancy[11, 7] = 1
        self.raw_occupancy[11, 8] = 1
        self.raw_occupancy[12, 6] = 1
        self.raw_occupancy[12, 7] = 1
        self.raw_occupancy[12, 8] = 1
        self.raw_occupancy[13, 6] = 1
        self.raw_occupancy[13, 7] = 1
        self.raw_occupancy[13, 8] = 1

        self.occupancy = self.raw_occupancy.copy()

        self.agt1_pos = [13, 1]
        self.occupancy[self.agt1_pos[0], self.agt1_pos[1]] = 1
        self.agt2_pos = [13, 13]
        self.occupancy[self.agt2_pos[0], self.agt2_pos[1]] = 1

        self.box_pos = [10, 7]
        self.occupancy[self.box_pos[0], self.box_pos[1]] = 1

        self.is_1_catch_box = False
        self.is_2_catch_box = False

    @property
    def n_agent(self):
        return 2

    @property
    def obs_size(self):
        return 15*15

    @property
    def n_action(self):
        return 4

    def get_env_info(self):
        return 15*15

    def reset(self):
        self.occupancy = self.raw_occupancy.copy()

        self.agt1_pos = [13, 1]
        self.occupancy[self.agt1_pos[0], self.agt1_pos[1]] = 1
        self.agt2_pos = [13, 13]
        self.occupancy[self.agt2_pos[0], self.agt2_pos[1]] = 1

        self.box_pos = [10, 7]
        self.occupancy[self.box_pos[0], self.box_pos[1]] = 1

        self.is_1_catch_box = False
        self.is_2_catch_box = False
        return [self.get_state1(), self.get_state2()]

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

        done = False
        reward = 0
        if self.box_pos == [6, 7]:
            reward = 10
            done = True
            self.reset()
        if self.box_pos == [1, 7]:
            reward = 100
            done = True
            self.reset()
        return [self.get_state1(), self.get_state2()], reward, done, []

    def get_global_obs(self):
        obs = np.ones((15, 15, 3))
        for i in range(15):
            for j in range(15):
                if self.raw_occupancy[i, j] == 1:
                    obs[i, j, 0] = 0.0
                    obs[i, j, 1] = 0.0
                    obs[i, j, 2] = 0.0
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
        obs = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                if self.raw_occupancy[self.agt1_pos[0] - 1 + i][self.agt1_pos[1] - 1 + j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
                d_x = self.agt2_pos[0] - self.agt1_pos[0]
                d_y = self.agt2_pos[1] - self.agt1_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1 + d_x, 1 + d_y, 0] = 0.0
                    obs[1 + d_x, 1 + d_y, 1] = 0.0
                    obs[1 + d_x, 1 + d_y, 2] = 1.0
                d_x = self.box_pos[0] - self.agt1_pos[0]
                d_y = self.box_pos[1] - self.agt1_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1 + d_x, 1 + d_y, 0] = 0.0
                    obs[1 + d_x, 1 + d_y, 1] = 1.0
                    obs[1 + d_x, 1 + d_y, 2] = 0.0
        obs[1, 1, 0] = 1.0
        obs[1, 1, 1] = 0.0
        obs[1, 1, 2] = 0.0
        return obs

    def get_agt2_obs(self):
        obs = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                if self.raw_occupancy[self.agt2_pos[0] - 1 + i][self.agt2_pos[1] - 1 + j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
                d_x = self.agt1_pos[0] - self.agt2_pos[0]
                d_y = self.agt1_pos[1] - self.agt2_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1 + d_x, 1 + d_y, 0] = 1.0
                    obs[1 + d_x, 1 + d_y, 1] = 0.0
                    obs[1 + d_x, 1 + d_y, 2] = 0.0
                d_x = self.box_pos[0] - self.agt2_pos[0]
                d_y = self.box_pos[1] - self.agt2_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1 + d_x, 1 + d_y, 0] = 0.0
                    obs[1 + d_x, 1 + d_y, 1] = 1.0
                    obs[1 + d_x, 1 + d_y, 2] = 0.0
        obs[1, 1, 0] = 0.0
        obs[1, 1, 1] = 0.0
        obs[1, 1, 2] = 1.0
        return obs

    def get_state(self):
        haha = np.zeros((15, 15))
        haha[self.agt1_pos[0], self.agt1_pos[1]] = 1
        haha[self.agt2_pos[0], self.agt2_pos[1]] = -1
        haha = haha.reshape((15*15, ))
        return haha

    def get_state1(self):
        haha = np.zeros((15, 15))
        haha[self.agt1_pos[0], self.agt1_pos[1]] = 1
        haha = haha.reshape((15*15, ))
        return haha

    def get_state1(self):
        haha = np.zeros((15, 15))
        haha[self.agt2_pos[0], self.agt2_pos[1]] = 1
        haha = haha.reshape((15*15, ))
        return haha

    def plot_scene(self):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(2, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])
        ax4 = fig.add_subplot(gs[0, 1])
        ax1.imshow(self.get_global_obs())
        plt.xticks([])
        plt.yticks([])
        ax2.imshow(self.get_agt1_obs())
        plt.xticks([])
        plt.yticks([])
        ax3.imshow(self.get_agt2_obs())
        plt.xticks([])
        plt.yticks([])
        ax4.imshow(self.occupancy)
        plt.xticks([])
        plt.yticks([])
        plt.show()

    def render(self):
        obs = np.ones((15 * 20, 15 * 20, 3))
        for i in range(15):
            for j in range(15):
                if self.raw_occupancy[i, j] == 1:
                    cv2.rectangle(obs, (j*20, i*20), (j*20+20, i*20+20), (0, 0, 0), -1)
        cv2.rectangle(obs, (self.agt1_pos[1] * 20, self.agt1_pos[0] * 20), (self.agt1_pos[1] * 20 + 20, self.agt1_pos[0] * 20 + 20), (0, 0, 255), -1)
        cv2.rectangle(obs, (self.agt2_pos[1] * 20, self.agt2_pos[0] * 20), (self.agt2_pos[1] * 20 + 20, self.agt2_pos[0] * 20 + 20), (255, 0, 0), -1)
        cv2.rectangle(obs, (self.box_pos[1] * 20, self.box_pos[0] * 20),
                      (self.box_pos[1] * 20 + 20, self.box_pos[0] * 20 + 20), (0, 255, 0), -1)
        cv2.imshow('image', obs)
        cv2.waitKey(100)
