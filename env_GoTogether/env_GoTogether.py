import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random
import cv2

class EnvGoTogether(object):
    def __init__(self, size):
        self.map_size = size
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0][i] = 1
            self.occupancy[self.map_size - 1][i] = 1
            self.occupancy[i][0] = 1
            self.occupancy[i][self.map_size - 1] = 1
        self.agt1_pos = [self.map_size - 3, 1]
        self.agt2_pos = [self.map_size - 2, 2]
        self.goal_pos = [1, self.map_size - 2]

    def reset(self):
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0][i] = 1
            self.occupancy[self.map_size - 1][i] = 1
            self.occupancy[i][0] = 1
            self.occupancy[i][self.map_size - 1] = 1
        self.agt1_pos = [self.map_size - 3, 1]
        self.agt2_pos = [self.map_size - 2, 2]
        self.goal_pos = [1, self.map_size - 2]
        return [self.get_state1(), self.get_state2()]

    @property
    def n_agent(self):
        return 2

    @property
    def obs_size(self):
        return 2

    @property
    def n_action(self):
        return 4

    def get_env_info(self):
        return 4

    def get_state(self):
        state = np.zeros((1, 4))
        state[0, 0] = self.agt1_pos[0] / self.map_size
        state[0, 1] = self.agt1_pos[1] / self.map_size
        state[0, 2] = self.agt2_pos[0] / self.map_size
        state[0, 3] = self.agt2_pos[1] / self.map_size
        return state.reshape((4, ))

    def get_state1(self):
        state = np.zeros((1, 2))
        state[0, 0] = self.agt1_pos[0] / self.map_size
        state[0, 1] = self.agt1_pos[1] / self.map_size
        return state.reshape((2, ))

    def get_state2(self):
        state = np.zeros((1, 2))
        state[0, 0] = self.agt2_pos[0] / self.map_size
        state[0, 1] = self.agt2_pos[1] / self.map_size
        return state.reshape((2, ))

    def step(self, action_list):
        reward = 0
        # agent1 move
        if action_list[0] == 0:  # move up
            if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] - 1
        elif action_list[0] == 1:  # move down
            if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] + 1
        elif action_list[0] == 2:  # move left
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] - 1
        elif action_list[0] == 3:  # move right
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] + 1

        # agent2 move
        if action_list[1] == 0:  # move up
            if self.occupancy[self.agt2_pos[0] - 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] - 1
        elif action_list[1] == 1:  # move down
            if self.occupancy[self.agt2_pos[0] + 1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] + 1
        elif action_list[1] == 2:  # move left
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] - 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] - 1
        elif action_list[1] == 3:  # move right
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1] + 1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] + 1

        if self.agt1_pos == self.goal_pos and self.agt2_pos == self.goal_pos:
            reward = reward + 10

        if self.sqr_dist(self.agt1_pos, self.agt2_pos)<=1 or self.sqr_dist(self.agt1_pos, self.agt2_pos)>9:
            reward = reward - 0.5
        done = False
        if reward > 0:
            done = True
        return [self.get_state1(), self.get_state2()], reward, done, []

    def sqr_dist(self, pos1, pos2):
        return (pos1[0]-pos2[0])*(pos1[0]-pos2[0])+(pos1[1]-pos2[1])*(pos1[1]-pos2[1])

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
        obs[self.agt2_pos[0], self.agt2_pos[1], 1] = 0.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 2] = 1.0
        obs[self.goal_pos[0], self.goal_pos[1], 0] = 0.0
        obs[self.goal_pos[0], self.goal_pos[1], 1] = 1.0
        obs[self.goal_pos[0], self.goal_pos[1], 2] = 0.0
        return obs

    def plot_scene(self):
        plt.figure(figsize=(5, 5))
        plt.imshow(self.get_global_obs())
        plt.xticks([])
        plt.yticks([])
        plt.show()

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
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 1.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (255, 0, 0), -1)
        cv2.imshow('image', new_obs)
        cv2.waitKey(100)
