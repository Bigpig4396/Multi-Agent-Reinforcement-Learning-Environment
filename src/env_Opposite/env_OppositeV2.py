import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random
import cv2

class EnvOppositeV2(object):
    def __init__(self, size):
        self.map_size = size
        self.raw_occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.raw_occupancy[0][i] = 1
            self.raw_occupancy[self.map_size - 1][i] = 1
            self.raw_occupancy[i][0] = 1
            self.raw_occupancy[i][self.map_size - 1] = 1

        for i in range(2, self.map_size - 2, 2):
            for j in range(2, self.map_size - 2, 2):
                self.raw_occupancy[i][j] = 1

        self.occupancy = self.raw_occupancy.copy()

        self.agt1_pos = [1, 1]
        self.goal1_pos = [self.map_size - 2, self.map_size - 2]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt2_pos = [self.map_size - 2, self.map_size - 2]
        self.goal2_pos = [1, 1]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt3_pos = [self.map_size - 2, 1]
        self.goal3_pos = [1, self.map_size - 2]
        self.occupancy[self.agt3_pos[0]][self.agt3_pos[1]] = 1

        self.agt4_pos = [1, self.map_size - 2]
        self.goal4_pos = [self.map_size - 2, 1]
        self.occupancy[self.agt4_pos[0]][self.agt4_pos[1]] = 1

    def reset(self):
        self.occupancy = self.raw_occupancy.copy()

        self.agt1_pos = [1, 1]
        self.goal1_pos = [self.map_size - 2, self.map_size - 2]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        self.agt2_pos = [self.map_size - 2, self.map_size - 2]
        self.goal2_pos = [1, 1]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        self.agt3_pos = [self.map_size - 2, 1]
        self.goal3_pos = [1, self.map_size - 2]
        self.occupancy[self.agt3_pos[0]][self.agt3_pos[1]] = 1

        self.agt4_pos = [1, self.map_size - 2]
        self.goal4_pos = [self.map_size - 2, 1]
        self.occupancy[self.agt4_pos[0]][self.agt4_pos[1]] = 1

    def get_state(self):
        state = np.zeros((1, 8))
        state[0, 0] = self.agt1_pos[0] / self.map_size
        state[0, 1] = self.agt1_pos[1] / self.map_size
        state[0, 2] = self.agt2_pos[0] / self.map_size
        state[0, 3] = self.agt2_pos[1] / self.map_size
        state[0, 4] = self.agt3_pos[0] / self.map_size
        state[0, 5] = self.agt3_pos[1] / self.map_size
        state[0, 6] = self.agt4_pos[0] / self.map_size
        state[0, 7] = self.agt4_pos[1] / self.map_size
        return state

    def step(self, action_list):
        reward = 0
        # agent1 move
        if action_list[0] == 0:  # move up
            if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] - 1
                self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
        elif action_list[0] == 1:  # move down
            if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] + 1
                self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
        elif action_list[0] == 2:  # move left
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] - 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
        elif action_list[0] == 3:  # move right
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] + 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        if self.agt1_pos == self.goal1_pos:
            reward = reward + 5

        if action_list[1] == 0:  # move up
            if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] - 1
                self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
        elif action_list[1] == 1:  # move down
            if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] + 1
                self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
        elif action_list[1] == 2:  # move left
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] - 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
        elif action_list[1] == 3:  # move right
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] + 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        if self.agt2_pos == self.goal2_pos:
            reward = reward + 5

        if action_list[2] == 0:  # move up
            if self.occupancy[self.agt3_pos[0] - 1][self.agt3_pos[1]] != 1:  # if can move
                self.agt3_pos[0] = self.agt3_pos[0] - 1
                self.occupancy[self.agt3_pos[0] + 1][self.agt3_pos[1]] = 0
                self.occupancy[self.agt3_pos[0]][self.agt3_pos[1]] = 1
        elif action_list[2] == 1:  # move down
            if self.occupancy[self.agt3_pos[0] + 1][self.agt3_pos[1]] != 1:  # if can move
                self.agt3_pos[0] = self.agt3_pos[0] + 1
                self.occupancy[self.agt3_pos[0] - 1][self.agt3_pos[1]] = 0
                self.occupancy[self.agt3_pos[0]][self.agt3_pos[1]] = 1
        elif action_list[2] == 2:  # move left
            if self.occupancy[self.agt3_pos[0]][self.agt3_pos[1] - 1] != 1:  # if can move
                self.agt3_pos[1] = self.agt3_pos[1] - 1
                self.occupancy[self.agt3_pos[0]][self.agt3_pos[1] + 1] = 0
                self.occupancy[self.agt3_pos[0]][self.agt3_pos[1]] = 1
        elif action_list[2] == 3:  # move right
            if self.occupancy[self.agt3_pos[0]][self.agt3_pos[1] + 1] != 1:  # if can move
                self.agt3_pos[1] = self.agt3_pos[1] + 1
                self.occupancy[self.agt3_pos[0]][self.agt3_pos[1] - 1] = 0
                self.occupancy[self.agt3_pos[0]][self.agt3_pos[1]] = 1

        if self.agt3_pos == self.goal3_pos:
            reward = reward + 5

        if action_list[3] == 0:  # move up
            if self.occupancy[self.agt4_pos[0] - 1][self.agt4_pos[1]] != 1:  # if can move
                self.agt4_pos[0] = self.agt4_pos[0] - 1
                self.occupancy[self.agt4_pos[0] + 1][self.agt4_pos[1]] = 0
                self.occupancy[self.agt4_pos[0]][self.agt4_pos[1]] = 1
        elif action_list[3] == 1:  # move down
            if self.occupancy[self.agt4_pos[0] + 1][self.agt4_pos[1]] != 1:  # if can move
                self.agt4_pos[0] = self.agt4_pos[0] + 1
                self.occupancy[self.agt4_pos[0] - 1][self.agt4_pos[1]] = 0
                self.occupancy[self.agt4_pos[0]][self.agt4_pos[1]] = 1
        elif action_list[3] == 2:  # move left
            if self.occupancy[self.agt4_pos[0]][self.agt4_pos[1] - 1] != 1:  # if can move
                self.agt4_pos[1] = self.agt4_pos[1] - 1
                self.occupancy[self.agt4_pos[0]][self.agt4_pos[1] + 1] = 0
                self.occupancy[self.agt4_pos[0]][self.agt4_pos[1]] = 1
        elif action_list[3] == 3:  # move right
            if self.occupancy[self.agt4_pos[0]][self.agt4_pos[1] + 1] != 1:  # if can move
                self.agt4_pos[1] = self.agt4_pos[1] + 1
                self.occupancy[self.agt4_pos[0]][self.agt4_pos[1] - 1] = 0
                self.occupancy[self.agt4_pos[0]][self.agt4_pos[1]] = 1

        if self.agt4_pos == self.goal4_pos:
            reward = reward + 5

        done = False
        if reward == 20:
            done = True
        return reward, done

    def get_global_obs(self):
        obs = np.zeros((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.occupancy[i][j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
        obs[self.agt1_pos[0], self.agt1_pos[1], 0] = 1.0
        obs[self.agt1_pos[0], self.agt1_pos[1], 1] = 0.0
        obs[self.agt1_pos[0], self.agt1_pos[1], 2] = 0.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 0] = 0.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 1] = 1.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 2] = 0.0
        obs[self.agt3_pos[0], self.agt3_pos[1], 0] = 1.0
        obs[self.agt3_pos[0], self.agt3_pos[1], 1] = 1.0
        obs[self.agt3_pos[0], self.agt3_pos[1], 2] = 0.0
        obs[self.agt4_pos[0], self.agt4_pos[1], 0] = 0.0
        obs[self.agt4_pos[0], self.agt4_pos[1], 1] = 1.0
        obs[self.agt4_pos[0], self.agt4_pos[1], 2] = 1.0
        return obs

    def render(self):
        obs = self.get_global_obs()
        enlarge = 30
        new_obs = np.ones((self.map_size*enlarge, self.map_size*enlarge, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):

                if obs[i][j][0] == 0.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (0, 0, 0), -1)
                if obs[i][j][0] == 1.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (0, 0, 255), -1)
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 1.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (0, 255, 0), -1)
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 1.0 and obs[i][j][2] == 1.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (255, 255, 0), -1)
                if obs[i][j][0] == 1.0 and obs[i][j][1] == 1.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (0, 255, 255), -1)
        cv2.imshow('image', new_obs)
        cv2.waitKey(100)
