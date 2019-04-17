import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


class EnvSingleMaze(object):

    def __init__(self):
        self.start1 = [3, 9]
        self.dest1 = [9, 9]
        self.agt1_pos = [3, 9]
        self.occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
                          [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                          [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                          [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
                          [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def list_add(self, a, b):
        c = [a[i] + b[i] for i in range(min(len(a), len(b)))]
        return c

    def get_obs(self):
        vec = np.zeros((5, 5, 3))
        for i in range(5):
            for j in range(5):
                vec[i, j, 0] = 1.0
                vec[i, j, 1] = 1.0
                vec[i, j, 2] = 1.0

        # detect block
        for k in range(5):
            if self.occupancy[self.agt1_pos[0] - 2][self.agt1_pos[1] + k -2] == 1:
                vec[4-k, 0, 0] = 0.0
                vec[4-k, 0, 1] = 0.0
                vec[4-k, 0, 2] = 0.0
            if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1] + k -2] == 1:
                vec[4-k, 1, 0] = 0.0
                vec[4-k, 1, 1] = 0.0
                vec[4-k, 1, 2] = 0.0
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + k -2] == 1:
                vec[4-k, 2, 0] = 0.0
                vec[4-k, 2, 1] = 0.0
                vec[4-k, 2, 2] = 0.0
            if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1] + k -2] == 1:
                vec[4-k, 3, 0] = 0.0
                vec[4-k, 3, 1] = 0.0
                vec[4-k, 3, 2] = 0.0
            if self.occupancy[self.agt1_pos[0] + 2][self.agt1_pos[1] + k -2] == 1:
                vec[4-k, 4, 0] = 0.0
                vec[4-k, 4, 1] = 0.0
                vec[4-k, 4, 2] = 0.0

        vec[2, 2, 0] = 1.0
        vec[2, 2, 1] = 0.0
        vec[2, 2, 2] = 0.0


        for i in range(5):
            if self.dest1 == self.list_add(self.agt1_pos, [-2, i-2]):
                vec[4-i, 0, 0] = 1.0
                vec[4-i, 0, 1] = 1.0
                vec[4-i, 0, 2] = 0.0
            if self.dest1 == self.list_add(self.agt1_pos, [-1, i-2]):
                vec[4-i, 1, 0] = 1.0
                vec[4-i, 1, 1] = 1.0
                vec[4-i, 1, 2] = 0.0
            if self.dest1 == self.list_add(self.agt1_pos, [0, i-2]):
                vec[4-i, 2, 0] = 1.0
                vec[4-i, 2, 1] = 1.0
                vec[4-i, 2, 2] = 0.0
            if self.dest1 == self.list_add(self.agt1_pos, [1, i-2]):
                vec[4-i, 3, 0] = 1.0
                vec[4-i, 3, 1] = 1.0
                vec[4-i, 3, 2] = 0.0
            if self.dest1 == self.list_add(self.agt1_pos, [2, i-2]):
                vec[4-i, 4, 0] = 1.0
                vec[4-i, 4, 1] = 1.0
                vec[4-i, 4, 2] = 0.0

        return vec

    def get_global_obs(self):
        vec = np.zeros((13, 13, 3))
        for i in range(13):
            for j in range(13):
                vec[i, j, 0] = 1.0
                vec[i, j, 1] = 1.0
                vec[i, j, 2] = 1.0
        for i in range(13):
            for j in range(13):
                if self.occupancy[j][12-i] == 1:
                    vec[i, j, 0] = 0.0
                    vec[i, j, 1] = 0.0
                    vec[i, j, 2] = 0.0

        vec[12-self.agt1_pos[1], self.agt1_pos[0], 0] = 1.0
        vec[12-self.agt1_pos[1], self.agt1_pos[0], 1] = 0.0
        vec[12-self.agt1_pos[1], self.agt1_pos[0], 2] = 0.0

        vec[12-self.dest1[1], self.dest1[0], 0] = 1.0
        vec[12-self.dest1[1], self.dest1[0], 1] = 1.0
        vec[12-self.dest1[1], self.dest1[0], 2] = 0.0

        return vec

    def step(self, action1):
        reward_1 = 0
        self.start1 = [3, 9]
        self.dest1 = [9, 9]
        # agent1 move
        if action1 == 0:    # move up
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] != 1:     # if can move
                self.agt1_pos[1] = self.agt1_pos[1] + 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 5
        elif action1 == 1:  # move down
            if self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] - 1] != 1:  # if can move
                self.agt1_pos[1] = self.agt1_pos[1] - 1
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1] + 1] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 5
        elif action1 == 2:  # move left
            if self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] - 1
                self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 5
        elif action1 == 3:  # move right
            if self.occupancy[self.agt1_pos[0] + 1][self.agt1_pos[1]] != 1:  # if can move
                self.agt1_pos[0] = self.agt1_pos[0] + 1
                self.occupancy[self.agt1_pos[0] - 1][self.agt1_pos[1]] = 0
                self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            else:
                reward_1 = reward_1 - 5

        if self.agt1_pos == self.dest1:
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 0
            self.agt1_pos = self.start1
            self.occupancy[self.agt1_pos[0]][self.agt1_pos[1]] = 1
            reward_1 = reward_1 + 50

        done = False
        if reward_1 > 0:
            done = True
            self.reset()
        return reward_1, done

    def reset(self):
        self.start1 = [3, 9]
        self.dest1 = [9, 9]
        self.agt1_pos = [3, 9]

        self.occupancy = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
                          [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                          [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                          [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
                          [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
                          [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def plot_scene(self):
        fig = plt.figure(figsize=(8, 8))
        gs = GridSpec(3, 2, figure=fig)
        ax1 = fig.add_subplot(gs[0:2, 0:2])
        ax2 = fig.add_subplot(gs[2, 0:1])

        ax1.imshow(self.get_global_obs())
        ax2.imshow(self.get_agt1_obs())
        plt.show()
