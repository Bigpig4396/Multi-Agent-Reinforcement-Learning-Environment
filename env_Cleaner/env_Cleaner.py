import numpy as np
import maze
import random
import cv2

class EnvCleaner(object):
    def __init__(self, N_agent, map_size, seed):
        self.map_size = map_size
        self.seed = seed
        self.occupancy = self.generate_maze(seed)
        self.N_agent = N_agent
        self.agt_pos_list = []
        for i in range(self.N_agent):
            self.agt_pos_list.append([1, 1])

    def generate_maze(self, seed):
        symbols = {
            # default symbols
            'start': 'S',
            'end': 'X',
            'wall_v': '|',
            'wall_h': '-',
            'wall_c': '+',
            'head': '#',
            'tail': 'o',
            'empty': ' '
        }
        maze_obj = maze.Maze(int((self.map_size - 1) / 2), int((self.map_size - 1) / 2), seed, symbols, 1)
        grid_map = maze_obj.to_np()
        for i in range(self.map_size):
            for j in range(self.map_size):
                if grid_map[i][j] == 0:
                    grid_map[i][j] = 2
        return grid_map

    @property
    def n_agent(self):
        return self.N_agent

    @property
    def obs_size(self):
        return self.map_size*self.map_size

    @property
    def n_action(self):
        return 4

    def get_env_info(self):
        return self.map_size*self.map_size

    def step(self, action_list):
        reward = 0
        for i in range(len(action_list)):
            if action_list[i] == 0:     # up
                if self.occupancy[self.agt_pos_list[i][0] - 1][self.agt_pos_list[i][1]] != 1:  # if can move
                    self.agt_pos_list[i][0] = self.agt_pos_list[i][0] - 1
            if action_list[i] == 1:     # down
                if self.occupancy[self.agt_pos_list[i][0] + 1][self.agt_pos_list[i][1]] != 1:  # if can move
                    self.agt_pos_list[i][0] = self.agt_pos_list[i][0] + 1
            if action_list[i] == 2:     # left
                if self.occupancy[self.agt_pos_list[i][0]][self.agt_pos_list[i][1] - 1] != 1:  # if can move
                    self.agt_pos_list[i][1] = self.agt_pos_list[i][1] - 1
            if action_list[i] == 3:     # right
                if self.occupancy[self.agt_pos_list[i][0]][self.agt_pos_list[i][1] + 1] != 1:  # if can move
                    self.agt_pos_list[i][1] = self.agt_pos_list[i][1] + 1
            if self.occupancy[self.agt_pos_list[i][0]][self.agt_pos_list[i][1]] == 2:   # if the spot is dirty
                self.occupancy[self.agt_pos_list[i][0]][self.agt_pos_list[i][1]] = 0
                reward = reward + 1
        return [self.get_state1(), self.get_state2()], reward, False, []

    def get_global_obs(self):
        obs = np.zeros((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.occupancy[i, j] == 0:
                    obs[i, j, 0] = 1.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 1.0
                if self.occupancy[i, j] == 2:
                    obs[i, j, 0] = 0.0
                    obs[i, j, 1] = 1.0
                    obs[i, j, 2] = 0.0
        for i in range(self.N_agent):
            obs[self.agt_pos_list[i][0], self.agt_pos_list[i][1], 0] = 1.0
            obs[self.agt_pos_list[i][0], self.agt_pos_list[i][1], 1] = 0.0
            obs[self.agt_pos_list[i][0], self.agt_pos_list[i][1], 2] = 0.0
        return obs

    def reset(self):
        self.occupancy = self.generate_maze(self.seed)
        self.agt_pos_list = []
        for i in range(self.N_agent):
            self.agt_pos_list.append([1, 1])
        return [self.get_state1(), self.get_state2()]

    def render(self):
        obs = self.get_global_obs()
        enlarge = 5
        new_obs = np.ones((self.map_size*enlarge, self.map_size*enlarge, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge), (0, 0, 0), -1)
                if obs[i][j][0] == 1.0 and obs[i][j][1] == 0.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge), (0, 0, 255), -1)
                if obs[i][j][0] == 0.0 and obs[i][j][1] == 1.0 and obs[i][j][2] == 0.0:
                    cv2.rectangle(new_obs, (i * enlarge, j * enlarge), (i * enlarge + enlarge, j * enlarge + enlarge), (0, 255, 0), -1)
        cv2.imshow('image', new_obs)
        cv2.waitKey(10)

    def plot_scene(self):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(3, 3, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        plt.xticks([])
        plt.yticks([])
        ax2 = fig.add_subplot(gs[2, 0])
        plt.xticks([])
        plt.yticks([])
        ax3 = fig.add_subplot(gs[2, 1])
        plt.xticks([])
        plt.yticks([])
        ax1.imshow(self.get_global_obs())
        ax2.imshow(self.get_obs(0))
        ax3.imshow(self.get_obs(1))
        plt.show()

    def save_map(self):
        np.save("map.npy", self.occupancy)

    def load_map(self):
        self.occupancy = np.load("map.npy")

    def get_state(self):
        obs = self.occupancy.copy()
        obs[self.agt_pos_list[0][0], self.agt_pos_list[0][1]] = 3
        obs[self.agt_pos_list[1][0], self.agt_pos_list[1][1]] = 4
        obs = obs / 4
        return obs.reshape((self.map_size*self.map_size, ))

    def get_state1(self):
        obs = self.occupancy.copy()
        obs[self.agt_pos_list[0][0], self.agt_pos_list[0][1]] = 4
        obs = obs / 4
        return obs.reshape((self.map_size*self.map_size, ))

    def get_state2(self):
        obs = self.occupancy.copy()
        obs[self.agt_pos_list[1][0], self.agt_pos_list[1][1]] = 4
        obs = obs / 4
        return obs.reshape((self.map_size*self.map_size, ))


