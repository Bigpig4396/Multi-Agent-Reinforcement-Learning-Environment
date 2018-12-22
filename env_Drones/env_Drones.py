import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import random

class Drones(object):
    def __init__(self, pos, view_range):
        self.pos = pos
        self.view_range = view_range

class Human(object):
    def __init__(self, pos):
        self.pos = pos

class EnvDrones(object):
    def __init__(self, map_size, drone_num, view_range, tree_num, human_num):
        self.map_size = map_size
        self.drone_num = drone_num
        self.tree_num = tree_num
        self.human_num = human_num

        # initialize blocks and trees
        self.land_mark_map = np.zeros((self.map_size, self.map_size))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if random.random() < 0.01:
                    self.land_mark_map[i, j] = 1    # wall

        # intialize tree
        for i in range(self.tree_num):
            temp_pos = [random.randint(0, self.map_size-1), random.randint(0, self.map_size-1)]
            while self.land_mark_map[temp_pos[0], temp_pos[1]] != 0:
                temp_pos = [random.randint(0, self.map_size-1), random.randint(0, self.map_size-1)]
            self.land_mark_map[temp_pos[0], temp_pos[1]] = 2


        # initialize humans
        self.human_list = []
        for i in range(self.human_num):
            temp_pos = [random.randint(0, self.map_size-1), random.randint(0, self.map_size-1)]
            while self.land_mark_map[temp_pos[0], temp_pos[1]] != 0:
                temp_pos = [random.randint(0, self.map_size-1), random.randint(0, self.map_size-1)]
            temp_human = Human(temp_pos)
            self.human_list.append(temp_human)


        # initialize drones
        self.start_pos = [self.map_size-1, self.map_size-1]
        self.drone_list = []
        for i in range(drone_num):
            temp_drone = Drones(self.start_pos, view_range)
            self.drone_list.append(temp_drone)

    def get_full_obs(self):
        obs = np.ones((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                if self.land_mark_map[i, j] == 1:
                    obs[i, j, 0] = 0
                    obs[i, j, 1] = 0
                    obs[i, j, 2] = 0
                if self.land_mark_map[i, j] == 2:
                    obs[i, j, 0] = 0
                    obs[i, j, 1] = 1
                    obs[i, j, 2] = 0

        for i in range(self.human_num):
            obs[self.human_list[i].pos[0], self.human_list[i].pos[1], 0] = 1
            obs[self.human_list[i].pos[0], self.human_list[i].pos[1], 1] = 0
            obs[self.human_list[i].pos[0], self.human_list[i].pos[1], 2] = 0
        return obs

    def get_drone_obs(self, drone):
        obs_size = 2 * drone.view_range - 1
        obs = np.ones((obs_size, obs_size, 3))
        for i in range(obs_size):
            for j in range(obs_size):
                x = i + drone.pos[0] - drone.view_range + 1
                y = j + drone.pos[1] - drone.view_range + 1

                for k in range(self.human_num):
                    if self.human_list[k].pos[0] == x and self.human_list[k].pos[1] == y:
                        obs[i, j, 0] = 1
                        obs[i, j, 1] = 0
                        obs[i, j, 2] = 0

                if x>=0 and x<=self.map_size-1 and y>=0 and y<=self.map_size-1:
                    if self.land_mark_map[x, y] == 1:
                        obs[i, j, 0] = 0
                        obs[i, j, 1] = 0
                        obs[i, j, 2] = 0
                    if self.land_mark_map[x, y] == 2:
                        obs[i, j, 0] = 0
                        obs[i, j, 1] = 1
                        obs[i, j, 2] = 0
                else:
                    obs[i, j, 0] = 0.5
                    obs[i, j, 1] = 0.5
                    obs[i, j, 2] = 0.5

                if (drone.view_range - 1 - i)*(drone.view_range - 1 - i)+(drone.view_range - 1 - j)*(drone.view_range - 1 - j) > drone.view_range*drone.view_range:
                    obs[i, j, 0] = 0.5
                    obs[i, j, 1] = 0.5
                    obs[i, j, 2] = 0.5

        return obs

    def get_joint_obs(self):
        obs = np.ones((self.map_size, self.map_size, 3))
        for i in range(self.map_size):
            for j in range(self.map_size):
                obs[i, j, 0] = 0.5
                obs[i, j, 1] = 0.5
                obs[i, j, 2] = 0.5
        for k in range(self.drone_num):
            temp = self.get_drone_obs(self.drone_list[k])
            size = temp.shape[0]
            for i in range(size):
                for j in range(size):
                    x = i + self.drone_list[k].pos[0] - self.drone_list[k].view_range + 1
                    y = j + self.drone_list[k].pos[1] - self.drone_list[k].view_range + 1
                    if_obs = True
                    if temp[i, j, 0] == 0.5 and temp[i, j, 1] == 0.5 and temp[i, j, 2] == 0.5:
                        if_obs = False
                    if if_obs == True:
                        obs[x, y, 0] = temp[i, j, 0]
                        obs[x, y, 1] = temp[i, j, 1]
                        obs[x, y, 2] = temp[i, j, 2]
        return obs

    def rand_reset_drone_pos(self):
        for k in range(self.drone_num):
            self.drone_list[k].pos = [random.randint(0, self.map_size-1), random.randint(0, self.map_size-1)]

    def drone_step(self, drone_act_list):
        if len(drone_act_list) != self.drone_num:
            return
        for k in range(self.drone_num):
            if drone_act_list[k] == 0:
                if self.drone_list[k].pos[0] > 0:
                    self.drone_list[k].pos[0] = self.drone_list[k].pos[0] - 1
            elif drone_act_list[k] == 1:
                if self.drone_list[k].pos[0] < self.map_size - 1:
                    self.drone_list[k].pos[0] = self.drone_list[k].pos[0] + 1
            elif drone_act_list[k] == 2:
                if self.drone_list[k].pos[1] > 0:
                    self.drone_list[k].pos[1] = self.drone_list[k].pos[1] - 1
            elif drone_act_list[k] == 3:
                if self.drone_list[k].pos[1] < self.map_size - 1:
                    self.drone_list[k].pos[1] = self.drone_list[k].pos[1] + 1

    def human_step(self, human_act_list):
        if len(human_act_list) != self.human_num:
            return
        for k in range(self.human_num):
            if human_act_list[k] == 0:
                if self.human_list[k].pos[0] > 0:
                    free_space = self.land_mark_map[self.human_list[k].pos[0] - 1, self.human_list[k].pos[1]]
                    if free_space == 0:
                        self.human_list[k].pos[0] = self.human_list[k].pos[0] - 1
            elif human_act_list[k] == 1:
                if self.human_list[k].pos[0] < self.map_size - 1:
                    free_space = self.land_mark_map[self.human_list[k].pos[0] + 1, self.human_list[k].pos[1]]
                    if free_space == 0:
                        self.human_list[k].pos[0] = self.human_list[k].pos[0] + 1
            elif human_act_list[k] == 2:
                if self.human_list[k].pos[1] > 0:
                    free_space = self.land_mark_map[self.human_list[k].pos[0], self.human_list[k].pos[1] - 1]
                    if free_space == 0:
                        self.human_list[k].pos[1] = self.human_list[k].pos[1] - 1
            elif human_act_list[k] == 3:
                if self.human_list[k].pos[1] < self.map_size - 1:
                    free_space = self.land_mark_map[self.human_list[k].pos[0], self.human_list[k].pos[1] + 1]
                    if free_space == 0:
                        self.human_list[k].pos[1] = self.human_list[k].pos[1] + 1

    def step(self, human_act_list, drone_act_list):
        self.drone_step(drone_act_list)
        self.human_step(human_act_list)