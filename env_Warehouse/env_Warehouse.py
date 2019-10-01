import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2

class Box(object):
    def __init__(self, pos, size, id):
        self.id = id
        self.pos = pos
        self.size = size    # 0, large, 1, small

class Agent(object):
    def __init__(self, pos, id):
        self.id = id
        self.pos = pos
        self.catch_box = -1

class EnvWarehouse(object):
    def __init__(self, agt_num):
        random.seed()
        self.raw_occupancy = np.zeros((13, 17))
        for i in range(13):
            self.raw_occupancy[i, 0] = 1
            self.raw_occupancy[i, 16] = 1
        for i in range(17):
            self.raw_occupancy[0, i] = 1
            self.raw_occupancy[12, i] = 1
        self.raw_occupancy[1, 1] = 1
        self.raw_occupancy[1, 2] = 1
        self.raw_occupancy[1, 3] = 1
        self.raw_occupancy[1, 7] = 1
        self.raw_occupancy[1, 8] = 1
        self.raw_occupancy[1, 9] = 1
        self.raw_occupancy[1, 13] = 1
        self.raw_occupancy[1, 14] = 1
        self.raw_occupancy[1, 15] = 1

        self.occupancy = self.raw_occupancy.copy()

        self.agt_num = agt_num
        if self.agt_num > 6:
            self.agt_num = 6
        if self.agt_num < 2:
            self.agt_num = 2

        self.agt_list = []
        for i in range(self.agt_num):
            temp_agt = Agent([4+i, 1], i)
            self.occupancy[temp_agt.pos[0], temp_agt.pos[1]] = 1
            self.agt_list.append(temp_agt)
        
        self.spawn_pos1 = [11, 3]
        self.spawn_pos2 = [11, 8]
        self.spawn_pos3 = [11, 13]
        
        self.box_list = []
        temp_box = Box(self.spawn_pos1, random.randint(0, 1), 0)
        self.box_list.append(temp_box)
        self.occupancy[self.box_list[0].pos[0], self.box_list[0].pos[1]] = 1
        temp_box = Box(self.spawn_pos2, random.randint(0, 1), 1)
        self.box_list.append(temp_box)
        self.occupancy[self.box_list[1].pos[0], self.box_list[1].pos[1]] = 1
        temp_box = Box(self.spawn_pos3, random.randint(0, 1), 2)
        self.box_list.append(temp_box)
        self.occupancy[self.box_list[2].pos[0], self.box_list[2].pos[1]] = 1
        
    def reset(self, agt_num):
        self.occupancy = self.raw_occupancy.copy()

        self.agt_num = agt_num
        if self.agt_num > 5:
            self.agt_num = 5
        if self.agt_num < 2:
            self.agt_num = 2

        self.agt_list = []
        for i in range(self.agt_num):
            temp_agt = Agent([4 + i, 1], i)
            self.occupancy[temp_agt.pos[0], temp_agt.pos[1]] = 1
            self.agt_list.append(temp_agt)

        self.spawn_pos1 = [11, 3]
        self.spawn_pos2 = [11, 8]
        self.spawn_pos3 = [11, 13]

        self.box_list = []
        temp_box = Box(self.spawn_pos1, random.randint(0, 1), 0)
        self.box_list.append(temp_box)
        self.occupancy[self.box_list[0].pos[0], self.box_list[0].pos[1]] = 1
        temp_box = Box(self.spawn_pos2, random.randint(0, 1), 1)
        self.box_list.append(temp_box)
        self.occupancy[self.box_list[1].pos[0], self.box_list[1].pos[1]] = 1
        temp_box = Box(self.spawn_pos3, random.randint(0, 1), 2)
        self.box_list.append(temp_box)
        self.occupancy[self.box_list[2].pos[0], self.box_list[2].pos[1]] = 1

    def step(self, action_list):
        for i in range(self.agt_num):
            if self.agt_list[i].catch_box == -1:    # agent is not carrying any box
                if action_list[i] == 0:     # up
                    if self.occupancy[self.agt_list[i].pos[0] - 1][self.agt_list[i].pos[1]] != 1:  # if can move
                        self.agt_list[i].pos[0] = self.agt_list[i].pos[0] - 1
                        self.occupancy[self.agt_list[i].pos[0] + 1][self.agt_list[i].pos[1]] = 0
                        self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1]] = 1
                if action_list[i] == 1:   # down
                    if self.occupancy[self.agt_list[i].pos[0] + 1][self.agt_list[i].pos[1]] != 1:  # if can move
                        self.agt_list[i].pos[0] = self.agt_list[i].pos[0] + 1
                        self.occupancy[self.agt_list[i].pos[0] - 1][self.agt_list[i].pos[1]] = 0
                        self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1]] = 1
                if action_list[i] == 2:   # left
                    if self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1] - 1] != 1:  # if can move
                        self.agt_list[i].pos[1] = self.agt_list[i].pos[1] - 1
                        self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1] + 1] = 0
                        self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1]] = 1
                if action_list[i] == 3:  # right
                    if self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1] + 1] != 1:  # if can move
                        self.agt_list[i].pos[1] = self.agt_list[i].pos[1] + 1
                        self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1] - 1] = 0
                        self.occupancy[self.agt_list[i].pos[0]][self.agt_list[i].pos[1]] = 1

        # joint move
        for i in range(len(self.box_list)):     # for each box
            agt_index_list = self.get_caught_agt_index_list(self.box_list[i].id)  # get all agents carrying it

            if len(agt_index_list) == 1:    # only one agent is catching it
                if self.box_list[i].size == 1:
                    common_action = action_list[agt_index_list[0]]
                    if common_action == 0:  # up
                        if self.occupancy[self.box_list[i].pos[0] - 1, self.box_list[i].pos[1]] == 0 and self.occupancy[self.agt_list[agt_index_list[0]].pos[0] - 1, self.agt_list[agt_index_list[0]].pos[1]] == 0:
                            self.box_list[i].pos[0] = self.box_list[i].pos[0] - 1
                            self.occupancy[self.box_list[i].pos[0] + 1, self.box_list[i].pos[1]] = 0
                            self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1]] = 1
                            self.agt_list[agt_index_list[0]].pos[0] = self.agt_list[agt_index_list[0]].pos[0] - 1
                            self.occupancy[self.agt_list[agt_index_list[0]].pos[0] + 1, self.agt_list[agt_index_list[0]].pos[1]] = 0
                            self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1]] = 1
                    if common_action == 1:  # down
                        if self.occupancy[self.box_list[i].pos[0] + 1, self.box_list[i].pos[1]] == 0 and self.occupancy[self.agt_list[agt_index_list[0]].pos[0] + 1, self.agt_list[agt_index_list[0]].pos[1]] == 0:
                            self.box_list[i].pos[0] = self.box_list[i].pos[0] + 1
                            self.occupancy[self.box_list[i].pos[0] - 1, self.box_list[i].pos[1]] = 0
                            self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1]] = 1
                            self.agt_list[agt_index_list[0]].pos[0] = self.agt_list[agt_index_list[0]].pos[0] + 1
                            self.occupancy[self.agt_list[agt_index_list[0]].pos[0] - 1, self.agt_list[agt_index_list[0]].pos[1]] = 0
                            self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1]] = 1
                    if common_action == 2:  # left
                        if self.agt_list[agt_index_list[0]].pos[1] > self.box_list[i].pos[1]: # agent is at right side of box
                            if self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] - 1] == 0:
                                # print('box', i, 'joint move left')
                                self.box_list[i].pos[1] = self.box_list[i].pos[1] - 1
                                self.agt_list[agt_index_list[0]].pos[1] = self.agt_list[agt_index_list[0]].pos[1] - 1
                                self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1]] = 1
                                self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] + 2] = 0
                        if self.agt_list[agt_index_list[0]].pos[1] < self.box_list[i].pos[1]: # agent is at left side of box
                            if self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1] - 1] == 0:
                                # print('box', i, 'joint move left')
                                self.box_list[i].pos[1] = self.box_list[i].pos[1] - 1
                                self.agt_list[agt_index_list[0]].pos[1] = self.agt_list[agt_index_list[0]].pos[1] - 1
                                self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1]] = 1
                                self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1] + 2] = 0
                    if common_action == 3:  # right
                        if self.agt_list[agt_index_list[0]].pos[1] > self.box_list[i].pos[1]: # agent is at right side of box
                            if self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1] + 1] == 0:
                                # print('box', i, 'joint move right')
                                self.box_list[i].pos[1] = self.box_list[i].pos[1] + 1
                                self.agt_list[agt_index_list[0]].pos[1] = self.agt_list[agt_index_list[0]].pos[1] + 1
                                self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1]] = 1
                                self.occupancy[self.agt_list[agt_index_list[0]].pos[0], self.agt_list[agt_index_list[0]].pos[1] - 2] = 0
                        if self.agt_list[agt_index_list[0]].pos[1] < self.box_list[i].pos[1]: # agent is at left side of box
                            if self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] + 1] == 0:
                                # print('box', i, 'joint move right')
                                self.box_list[i].pos[1] = self.box_list[i].pos[1] + 1
                                self.agt_list[agt_index_list[0]].pos[1] = self.agt_list[agt_index_list[0]].pos[1] + 1
                                self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1]] = 1
                                self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] - 2] = 0

            if len(agt_index_list) == 2:
                common_action = self.get_common_action(action_list, agt_index_list, self.box_list[i].size)
                if common_action == 0:  # up
                    if self.occupancy[self.box_list[i].pos[0] - 1, self.box_list[i].pos[1]] == 0 and self.occupancy[self.box_list[i].pos[0] - 1, self.box_list[i].pos[1] - 1] == 0 and self.occupancy[self.box_list[i].pos[0] - 1, self.box_list[i].pos[1] + 1] == 0:
                        # print('box', i, 'joint move up')
                        self.box_list[i].pos[0] = self.box_list[i].pos[0] - 1
                        self.occupancy[self.box_list[i].pos[0] + 1, self.box_list[i].pos[1]] = 0
                        self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1]] = 1
                        for k in range(len(agt_index_list)):
                            self.agt_list[agt_index_list[k]].pos[0] = self.agt_list[agt_index_list[k]].pos[0] - 1
                            self.occupancy[self.agt_list[agt_index_list[k]].pos[0] + 1, self.agt_list[agt_index_list[k]].pos[1]] = 0
                            self.occupancy[self.agt_list[agt_index_list[k]].pos[0], self.agt_list[agt_index_list[k]].pos[1]] = 1

                if common_action == 1:  # down
                    if self.occupancy[self.box_list[i].pos[0] + 1, self.box_list[i].pos[1]] == 0 and self.occupancy[self.box_list[i].pos[0] + 1, self.box_list[i].pos[1] - 1] == 0 and self.occupancy[self.box_list[i].pos[0] + 1, self.box_list[i].pos[1] + 1] == 0:
                        # print('box', i, 'joint move down')
                        self.box_list[i].pos[0] = self.box_list[i].pos[0] + 1
                        self.occupancy[self.box_list[i].pos[0] - 1, self.box_list[i].pos[1]] = 0
                        self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1]] = 1
                        for k in range(len(agt_index_list)):
                            self.agt_list[agt_index_list[k]].pos[0] = self.agt_list[agt_index_list[k]].pos[0] + 1
                            self.occupancy[self.agt_list[agt_index_list[k]].pos[0] - 1, self.agt_list[agt_index_list[k]].pos[1]] = 0
                            self.occupancy[self.agt_list[agt_index_list[k]].pos[0], self.agt_list[agt_index_list[k]].pos[1]] = 1

                if common_action == 2:  # left
                    if self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] - 2] == 0:
                        # print('box', i, 'joint move left')
                        self.box_list[i].pos[1] = self.box_list[i].pos[1] - 1
                        self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] - 1] = 1
                        self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] + 2] = 0
                        # print('agt_list', agt_index_list)
                        for k in range(len(agt_index_list)):
                            self.agt_list[agt_index_list[k]].pos[1] = self.agt_list[agt_index_list[k]].pos[1] - 1

                if common_action == 3:  # right
                    if self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] + 2] == 0:
                        # print('box', i, 'joint move right')
                        self.box_list[i].pos[1] = self.box_list[i].pos[1] + 1
                        self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] + 1] = 1
                        self.occupancy[self.box_list[i].pos[0], self.box_list[i].pos[1] - 2] = 0
                        for k in range(len(agt_index_list)):
                            self.agt_list[agt_index_list[k]].pos[1] = self.agt_list[agt_index_list[k]].pos[1] + 1

        # catch box
        for i in range(self.agt_num):
            if self.agt_list[i].catch_box == -1:    # agent is not carrying any box
                for k in range(len(self.box_list)):
                    if self.agt_list[i].pos[0] == self.box_list[k].pos[0] and abs(self.agt_list[i].pos[1] - self.box_list[k].pos[1]) == 1:
                        self.agt_list[i].catch_box = self.box_list[k].id

        # generate new box
        self.gene_new_box()

        # check if box is correctly delivered
        reward = 0
        # print('len(self.box_list)', len(self.box_list))
        delete_id_list = []
        for k in range(len(self.box_list)):
            # print('k', k)
            if self.box_list[k].size == 0:  # large box
                if self.box_list[k].pos == [1, 4] or self.box_list[k].pos == [1, 5] or self.box_list[k].pos == [1, 6]:
                    reward = reward + 15
                    delete_id_list.append(self.box_list[k].id)
                if self.box_list[k].pos == [1, 10] or self.box_list[k].pos == [1, 11] or self.box_list[k].pos == [1, 12]:
                    reward = reward - 15
                    delete_id_list.append(self.box_list[k].id)
            else:   # small box
                if self.box_list[k].pos == [1, 4] or self.box_list[k].pos == [1, 5] or self.box_list[k].pos == [1, 6]:
                    reward = reward - 5
                    delete_id_list.append(self.box_list[k].id)
                if self.box_list[k].pos == [1, 10] or self.box_list[k].pos == [1, 11] or self.box_list[k].pos == [1, 12]:
                    reward = reward + 5
                    delete_id_list.append(self.box_list[k].id)
        for k in range(len(delete_id_list)):
            self.delete_box(delete_id_list[k])
            print('delete box', delete_id_list[k])
        return reward

    def is_box_in_list(self, id):
        for i in range(len(self.box_list)):
            if id == self.box_list[i].id:
                return True
        return False

    def get_new_box_id(self):
        new_id = 0
        while self.is_box_in_list(new_id):
            new_id = new_id + 1
        return new_id

    def gene_new_box(self):
        if self.occupancy[11, 3] == 0:
            # print('position 1', [11, 3], 'add box')
            new_id = self.get_new_box_id()
            temp_box = Box([11, 3], random.randint(0, 1), new_id)
            self.box_list.append(temp_box)
            self.occupancy[11, 3] = 1

        if self.occupancy[11, 8] == 0:
            # print('position 2', [11, 8], 'add box')
            new_id = self.get_new_box_id()
            temp_box = Box([11, 8], random.randint(0, 1), new_id)
            self.box_list.append(temp_box)
            self.occupancy[11, 8] = 1

        if self.occupancy[11, 13] == 0:
            # print('position 3', [11, 13], 'add box')
            new_id = self.get_new_box_id()
            temp_box = Box([11, 13], random.randint(0, 1), new_id)
            self.box_list.append(temp_box)
            self.occupancy[11, 13] = 1

    def get_agt_states(self):
        state_list = []
        for i in range(len(self.agt_list)):
            temp_state = np.zeros((1, 6))
            temp_state[0, 0] = self.agt_list[i].pos[0] / 13
            temp_state[0, 1] = self.agt_list[i].pos[1] / 17
            temp_state[0, 2] = -1
            temp_state[0, 3] = -1
            if self.agt_list[i].catch_box != -1:    # is carring box
                temp_state[0, 2] = self.box_list[self.get_box_index(self.agt_list[i].catch_box)].pos[0]
                temp_state[0, 3] = self.box_list[self.get_box_index(self.agt_list[i].catch_box)].pos[1]
            temp_state[0, 4] = 0
            temp_state[0, 5] = 0
            state_list.append(temp_state)
        return state_list

    def get_box_states(self):
        state_list = []
        for i in range(len(self.box_list)):
            temp_state = np.zeros((1, 6))
            temp_state[0, 0] = self.box_list[i].pos[0] / 13
            temp_state[0, 1] = self.box_list[i].pos[1] / 17
            temp_state[0, 2] = -1
            temp_state[0, 3] = -1
            if self.box_list[i].size == 0:
                temp_state[0, 4] = 1
                temp_state[0, 5] = 0
            else:
                temp_state[0, 4] = 0
                temp_state[0, 5] = 1
            state_list.append(temp_state)
        return state_list

    def get_box_index(self, box_id):
        index = -1
        for i in range(len(self.box_list)):
            if box_id == self.box_list[i].id:
                index = i
        return index

    def get_caught_agt_index_list(self, box_id):
        new_agt_index_list = []
        for i in range(self.agt_num):
            if self.agt_list[i].catch_box == box_id:
                new_agt_index_list.append(i)
        return new_agt_index_list

    def delete_box(self, box_id):
        # print('delete box', box_id)
        self.occupancy[self.box_list[self.get_box_index(box_id)].pos[0], self.box_list[self.get_box_index(box_id)].pos[1]] = 0

        temp_list = []
        agt_index_list = self.get_caught_agt_index_list(box_id)
        for i in range(len(agt_index_list)):
            self.agt_list[agt_index_list[i]].catch_box = -1
            # print('set agent', agt_index_list[i], 'free')

        for i in range(len(self.box_list)):
            if box_id != self.box_list[i].id:
                temp_list.append(self.box_list[i])
        self.box_list = temp_list

        # print('new box list')
        '''for k in range(len(self.box_list)):
            print('box', self.box_list[k].id, 'is at', self.box_list[k].pos, ', caught by',
                  self.get_caught_agt_index_list(self.box_list[k].id))'''

    def get_common_action(self, action_list, agt_index_list, size):
        if len(agt_index_list) == 0:
            return -1

        if len(agt_index_list) == 1:
            if size == 0:   # large box
                common_action = -1
            if size == 1:   # small box
                common_action = action_list[agt_index_list[0]]

        if len(agt_index_list) >= 2:
            common_action = action_list[agt_index_list[0]]
            for i in range(1, len(agt_index_list)):
                if action_list[agt_index_list[i]] != common_action:
                    common_action = -1
        return common_action

    def get_global_obs(self):
        obs = np.ones((13, 17, 3))
        for i in range(13):
            for j in range(17):
                if self.raw_occupancy[i, j] == 1:
                    obs[i, j, 0] = 0.0
                    obs[i, j, 1] = 0.0
                    obs[i, j, 2] = 0.0

        for i in range(self.agt_num):
            obs[self.agt_list[i].pos[0], self.agt_list[i].pos[1], 0] = i/self.agt_num
            obs[self.agt_list[i].pos[0], self.agt_list[i].pos[1], 1] = 1-i/self.agt_num
            obs[self.agt_list[i].pos[0], self.agt_list[i].pos[1], 2] = i/self.agt_num

        for i in range(len(self.box_list)):
            if self.box_list[i].size == 0:  # large
                obs[self.box_list[i].pos[0], self.box_list[i].pos[1], 0] = 0
                obs[self.box_list[i].pos[0], self.box_list[i].pos[1], 1] = 0
                obs[self.box_list[i].pos[0], self.box_list[i].pos[1], 2] = 1
            if self.box_list[i].size == 1:
                obs[self.box_list[i].pos[0], self.box_list[i].pos[1], 0] = 1
                obs[self.box_list[i].pos[0], self.box_list[i].pos[1], 1] = 0
                obs[self.box_list[i].pos[0], self.box_list[i].pos[1], 2] = 0
        return obs

    def plot_scene(self):
        fig = plt.figure(figsize=(5, 5))
        gs = GridSpec(2, 1, figure=fig)
        ax1 = fig.add_subplot(gs[0, 0])
        plt.xticks([])
        plt.yticks([])
        ax2 = fig.add_subplot(gs[1, 0])
        plt.xticks([])
        plt.yticks([])
        ax1.imshow(self.get_global_obs())
        ax2.imshow(self.occupancy)
        plt.show()

    def render(self):
        obs = np.ones((13 * 20, 17 * 20, 3))
        for i in range(13):
            for j in range(17):
                if self.raw_occupancy[i, j] == 1:
                    cv2.rectangle(obs, (j*20, i*20), (j*20+20, i*20+20), (0, 0, 0), -1)

        for i in range(self.agt_num):
            cv2.rectangle(obs, (self.agt_list[i].pos[1] * 20, self.agt_list[i].pos[0] * 20), (self.agt_list[i].pos[1] * 20 + 20, self.agt_list[i].pos[0] * 20 + 20), (0, 255, 0), -1)

        for i in range(len(self.box_list)):
            if self.box_list[i].size == 0:  # large
                cv2.rectangle(obs, (self.box_list[i].pos[1] * 20, self.box_list[i].pos[0] * 20), (self.box_list[i].pos[1] * 20 + 20, self.box_list[i].pos[0] * 20 + 20), (255, 0, 0), -1)
            else:   # small
                cv2.rectangle(obs, (self.box_list[i].pos[1] * 20, self.box_list[i].pos[0] * 20),
                              (self.box_list[i].pos[1] * 20 + 20, self.box_list[i].pos[0] * 20 + 20), (0, 0, 255), -1)
        cv2.imshow('image', obs)
        cv2.waitKey(50)








    
        
