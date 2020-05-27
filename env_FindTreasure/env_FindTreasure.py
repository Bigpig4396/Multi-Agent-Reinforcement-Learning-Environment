import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2

class EnvFindTreasure(object):
    def __init__(self, map_size):
        self.map_size = map_size
        if map_size<7:
            self.map_size = 7

        self.half_pos = int((self.map_size - 1)/2)

        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0, i] = 1
            self.occupancy[i, 0] = 1
            self.occupancy[i, self.map_size - 1] = 1
            self.occupancy[self.map_size - 1, i] = 1
            self.occupancy[self.half_pos, i] = 1

        self.lever_pos = [self.map_size - 2, self.map_size - 2]

        # initialize agent 1
        self.agt1_pos = [self.half_pos+1, 1]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        # initialize agent 2
        self.agt2_pos = [self.map_size-2, 1]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        # initialize treasure
        self.treasure_pos = [1, self.map_size - 2]
        # self.treasure_pos = [self.half_pos - 1, self.half_pos]

        # sub pos = [self.map_size - 2, self.map_size - 2]
        self.sub_pos = [self.map_size - 3, self.map_size - 2]

    def get_s1_index(self):
        return self.agt1_pos[0]*7+self.agt1_pos[1]

    def get_s2_index(self):
        return self.agt2_pos[0]*7+self.agt2_pos[1]

    @property
    def n_agent(self):
        return 2

    @property
    def obs_size(self):
        return 2

    @property
    def n_action(self):
        return 5

    def get_env_info(self):
        return 4

    def reset(self):
        self.occupancy = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            self.occupancy[0, i] = 1
            self.occupancy[i, 0] = 1
            self.occupancy[i, self.map_size - 1] = 1
            self.occupancy[self.map_size - 1, i] = 1
            self.occupancy[self.half_pos, i] = 1

        self.lever_pos = [self.map_size - 2, self.map_size - 2]

        # initialize agent 1
        self.agt1_pos = [self.half_pos + 1, 1]
        self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1

        # initialize agent 2
        self.agt2_pos = [self.map_size - 2, 1]
        self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1

        # initialize treasure
        self.treasure_pos = [1, self.map_size - 2]
        # self.treasure_pos = [self.half_pos - 1, self.half_pos]

        # sub pos = [self.map_size - 2, self.map_size - 2]
        self.sub_pos = [self.map_size - 3, self.map_size - 2]
        return [self.get_state1(), self.get_state2()]

    def step(self, action_list):
        reward = 0
        # agent1 move
        if action_list[0] == 0:  # move up
            if self.occupancy[self.agt1_pos[0]-1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] - 1
                self.occupancy[self.agt1_pos[0]+1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward = reward - 0.1
        elif action_list[0] == 1:  # move down
            if self.occupancy[self.agt1_pos[0]+1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0]+1
                self.occupancy[self.agt1_pos[0]-1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward = reward - 0.1
        elif action_list[0] == 2:  # move left
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]-1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] - 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]+1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward = reward - 0.1
        elif action_list[0] == 3:  # move right
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]+1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] + 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]-1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward = reward - 0.1

        # agent2 move
        if action_list[1] == 0:  # move up
            if self.occupancy[self.agt2_pos[0]-1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] - 1
                self.occupancy[self.agt2_pos[0]+1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward = reward - 0.1
        elif action_list[1] == 1:  # move down
            if self.occupancy[self.agt2_pos[0]+1][self.agt2_pos[1]] != 1:  # if can move
                self.agt2_pos[0] = self.agt2_pos[0] + 1
                self.occupancy[self.agt2_pos[0]-1][self.agt2_pos[1]] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward = reward - 0.1
        elif action_list[1] == 2:  # move left
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]-1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] - 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]+1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward = reward - 0.1
        elif action_list[1] == 3:  # move right
            if self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]+1] != 1:  # if can move
                self.agt2_pos[1] = self.agt2_pos[1] + 1
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]-1] = 0
                self.occupancy[self.agt2_pos[0]][self.agt2_pos[1]] = 1
            else:
                reward = reward - 0.1

        # check lever
        if self.agt1_pos == self.lever_pos or self.agt2_pos == self.lever_pos:
            self.occupancy[self.half_pos][self.half_pos] = 0  # open secret door
            self.occupancy[self.half_pos][self.half_pos-1] = 0  # open secret door
            self.occupancy[self.half_pos][self.half_pos+1] = 0  # open secret door
        else:
            self.occupancy[self.half_pos][self.half_pos] = 1  # open secret door
            self.occupancy[self.half_pos][self.half_pos - 1] = 1  # open secret door
            self.occupancy[self.half_pos][self.half_pos + 1] = 1  # open secret door

        # check treasure
        if self.agt1_pos == self.treasure_pos or self.agt2_pos == self.treasure_pos:
            reward = reward + 100

        if (self.agt1_pos == self.sub_pos and self.agt2_pos == self.lever_pos) or (self.agt1_pos == self.lever_pos and self.agt2_pos == self.sub_pos):
            reward = reward + 3

        done = False
        if reward > 0:
            done = True

        return [self.get_state1(), self.get_state2()], reward, done, []

    def get_global_obs(self):
        obs = np.zeros((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.occupancy[i][j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
        obs[self.lever_pos[0], self.lever_pos[1], 0] = 1.0
        obs[self.lever_pos[0], self.lever_pos[1], 1] = 1.0
        obs[self.lever_pos[0], self.lever_pos[1], 2] = 0.0
        obs[self.treasure_pos[0], self.treasure_pos[1], 0] = 0.0
        obs[self.treasure_pos[0], self.treasure_pos[1], 1] = 1.0
        obs[self.treasure_pos[0], self.treasure_pos[1], 2] = 0.0
        obs[self.agt1_pos[0], self.agt1_pos[1], 0] = 1.0
        obs[self.agt1_pos[0], self.agt1_pos[1], 1] = 0.0
        obs[self.agt1_pos[0], self.agt1_pos[1], 2] = 0.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 0] = 0.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 1] = 0.0
        obs[self.agt2_pos[0], self.agt2_pos[1], 2] = 1.0
        obs[self.sub_pos[0], self.sub_pos[1], 0] = 1.0
        obs[self.sub_pos[0], self.sub_pos[1], 1] = 0.0
        obs[self.sub_pos[0], self.sub_pos[1], 2] = 1.0
        return obs

    def get_agt1_obs(self):
        obs = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                if self.occupancy[self.agt1_pos[0]-1+i][self.agt1_pos[1]-1+j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
                d_x = self.lever_pos[0] - self.agt1_pos[0]
                d_y = self.lever_pos[1] - self.agt1_pos[1]
                if d_x>=-1 and d_x<=1 and d_y>=-1 and d_y<=1:
                    obs[1+d_x, 1+d_y, 0] = 1.0
                    obs[1+d_x, 1+d_y, 1] = 1.0
                    obs[1+d_x, 1+d_y, 2] = 0.0
                d_x = self.treasure_pos[0] - self.agt1_pos[0]
                d_y = self.treasure_pos[1] - self.agt1_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1+d_x, 1+d_y, 0] = 0.0
                    obs[1+d_x, 1+d_y, 1] = 1.0
                    obs[1+d_x, 1+d_y, 2] = 0.0
                d_x = self.agt2_pos[0] - self.agt1_pos[0]
                d_y = self.agt2_pos[1] - self.agt1_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1 + d_x, 1 + d_y, 0] = 0.0
                    obs[1 + d_x, 1 + d_y, 1] = 0.0
                    obs[1 + d_x, 1 + d_y, 2] = 1.0
        obs[1, 1, 0] = 1.0
        obs[1, 1, 1] = 0.0
        obs[1, 1, 2] = 0.0
        return obs

    def get_agt2_obs(self):
        obs = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                if self.occupancy[self.agt2_pos[0]-1+i][self.agt2_pos[1]-1+j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
                d_x = self.lever_pos[0] - self.agt2_pos[0]
                d_y = self.lever_pos[1] - self.agt2_pos[1]
                if d_x>=-1 and d_x<=1 and d_y>=-1 and d_y<=1:
                    obs[1+d_x, 1+d_y, 0] = 1.0
                    obs[1+d_x, 1+d_y, 1] = 1.0
                    obs[1+d_x, 1+d_y, 2] = 0.0
                d_x = self.treasure_pos[0] - self.agt2_pos[0]
                d_y = self.treasure_pos[1] - self.agt2_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1+d_x, 1+d_y, 0] = 0.0
                    obs[1+d_x, 1+d_y, 1] = 1.0
                    obs[1+d_x, 1+d_y, 2] = 0.0
                d_x = self.agt1_pos[0] - self.agt2_pos[0]
                d_y = self.agt1_pos[1] - self.agt2_pos[1]
                if d_x >= -1 and d_x <= 1 and d_y >= -1 and d_y <= 1:
                    obs[1 + d_x, 1 + d_y, 0] = 1.0
                    obs[1 + d_x, 1 + d_y, 1] = 0.0
                    obs[1 + d_x, 1 + d_y, 2] = 0.0
        obs[1, 1, 0] = 0.0
        obs[1, 1, 1] = 0.0
        obs[1, 1, 2] = 1.0
        return obs

    def get_obs(self):
        return [self.get_agt1_obs(), self.get_agt2_obs()]

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

        ax1.imshow(self.get_global_obs())
        ax2.imshow(self.get_agt1_obs())
        ax3.imshow(self.get_agt2_obs())

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
                if obs[i][j][0] == 1.0 and obs[i][j][1] == 1.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (0, 255, 255), -1)
                if obs[i][j][0] == 1.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 1.0:
                    cv2.rectangle(new_obs, (j * enlarge, i * enlarge), (j * enlarge + enlarge, i * enlarge + enlarge), (255, 0, 255), -1)
        cv2.imshow('image', new_obs)
        cv2.waitKey(100)
