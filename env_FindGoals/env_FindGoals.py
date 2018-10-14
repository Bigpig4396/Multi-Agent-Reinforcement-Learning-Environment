import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation  # 动图的核心函数


class EnvFindGoals(object):
    """docstring for Hotel"""
    def __init__(self):
        self.start1 = [3, 1]
        self.start2 = [6, 1]
        self.dest1 = [8, 2]
        self.dest2 = [1, 2]
        self.agent1_pos = [3, 1]
        self.agent2_pos = [6, 1]
        self.occupancy = [[1, 1, 1, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 1, 1]]
        self.fig = plt.figure(figsize=(10, 4))
        self.ax1 = self.fig.add_subplot(1, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 4)
        self.action1_list = []
        self.action2_list = []
        self.agt1_pos_list = []
        self.agt2_pos_list = []

    def list_add(self, a, b):
        c = [a[i] + b[i] for i in range(min(len(a), len(b)))]
        return c

    def get_agt1_obs(self):
        vec = np.zeros((1, 8))

        # detect block
        if self.occupancy[self.agent1_pos[0] - 1][self.agent1_pos[1] + 1] == 1:
            vec[0, 0] = 1
        if self.occupancy[self.agent1_pos[0]][self.agent1_pos[1] + 1] == 1:
            vec[0, 1] = 1
        if self.occupancy[self.agent1_pos[0] + 1][self.agent1_pos[1] + 1] == 1:
            vec[0, 2] = 1
        if self.occupancy[self.agent1_pos[0] - 1][self.agent1_pos[1]] == 1:
            vec[0, 3] = 1
        if self.occupancy[self.agent1_pos[0] + 1][self.agent1_pos[1]] == 1:
            vec[0, 4] = 1
        if self.occupancy[self.agent1_pos[0] - 1][self.agent1_pos[1] - 1] == 1:
            vec[0, 5] = 1
        if self.occupancy[self.agent1_pos[0]][self.agent1_pos[1] - 1] == 1:
            vec[0, 6] = 1
        if self.occupancy[self.agent1_pos[0] + 1][self.agent1_pos[1] - 1] == 1:
            vec[0, 7] = 1

        # detect agent2
        if self.agent2_pos == self.list_add(self.agent1_pos, [-1, 1]):
            vec[0, 0] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [0, 1]):
            vec[0, 1] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [1, 1]):
            vec[0, 2] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [-1, 0]):
            vec[0, 3] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [1, 0]):
            vec[0, 4] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [-1, -1]):
            vec[0, 5] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [0, -1]):
            vec[0, 6] = 2
        if self.agent2_pos == self.list_add(self.agent1_pos, [1, -1]):
            vec[0, 7] = 2
        return vec

    def get_agt2_obs(self):
        vec = np.zeros((1, 8))

        # detect block
        if self.occupancy[self.agent2_pos[0] - 1][self.agent2_pos[1] + 1] == 1:
            vec[0, 0] = 1
        if self.occupancy[self.agent2_pos[0]][self.agent2_pos[1] + 1] == 1:
            vec[0, 1] = 1
        if self.occupancy[self.agent2_pos[0] + 1][self.agent2_pos[1] + 1] == 1:
            vec[0, 2] = 1
        if self.occupancy[self.agent2_pos[0] - 1][self.agent2_pos[1]] == 1:
            vec[0, 3] = 1
        if self.occupancy[self.agent2_pos[0] + 1][self.agent2_pos[1]] == 1:
            vec[0, 4] = 1
        if self.occupancy[self.agent2_pos[0] - 1][self.agent2_pos[1] - 1] == 1:
            vec[0, 5] = 1
        if self.occupancy[self.agent2_pos[0]][self.agent2_pos[1] - 1] == 1:
            vec[0, 6] = 1
        if self.occupancy[self.agent2_pos[0] + 1][self.agent2_pos[1] - 1] == 1:
            vec[0, 7] = 1

        # detect agent1
        if self.agent1_pos == self.list_add(self.agent2_pos, [-1, 1]):
            vec[0, 0] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [0, 1]):
            vec[0, 1] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [1, 1]):
            vec[0, 2] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [-1, 0]):
            vec[0, 3] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [1, 0]):
            vec[0, 4] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [-1, -1]):
            vec[0, 5] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [0, -1]):
            vec[0, 6] = 2
        if self.agent1_pos == self.list_add(self.agent2_pos, [1, -1]):
            vec[0, 7] = 2
        return vec

    def step(self, action1, action2):
        reward = 0
        # agent1 move
        if action1 == 0:    # move up
            reward = reward - 1
            if self.occupancy[self.agent1_pos[0]][self.agent1_pos[1] + 1] != 1:     # if can move
                self.agent1_pos[1] = self.agent1_pos[1] + 1
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1] - 1] = 0
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
            if self.agent1_pos == self.dest1:
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 0
                self.agent1_pos = self.start1
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
                reward = reward + 100
        elif action1 == 1:  # move down
            reward = reward - 1
            if self.occupancy[self.agent1_pos[0]][self.agent1_pos[1] - 1] != 1:  # if can move
                self.agent1_pos[1] = self.agent1_pos[1] - 1
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1] + 1] = 0
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
            if self.agent1_pos == self.dest1:
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 0
                self.agent1_pos = self.start1
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
                reward = reward + 100
        elif action1 == 2:  # move left
            reward = reward - 1
            if self.occupancy[self.agent1_pos[0] - 1][self.agent1_pos[1]] != 1:  # if can move
                self.agent1_pos[0] = self.agent1_pos[0] - 1
                self.occupancy[self.agent1_pos[0] + 1][self.agent1_pos[1]] = 0
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
            if self.agent1_pos == self.dest1:
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 0
                self.agent1_pos = self.start1
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
                reward = reward + 100
        elif action1 == 3:  # move right
            reward = reward - 1
            if self.occupancy[self.agent1_pos[0] + 1][self.agent1_pos[1]] != 1:  # if can move
                self.agent1_pos[0] = self.agent1_pos[0] + 1
                self.occupancy[self.agent1_pos[0] - 1][self.agent1_pos[1]] = 0
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
            if self.agent1_pos == self.dest1:
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 0
                self.agent1_pos = self.start1
                self.occupancy[self.agent1_pos[0]][self.agent1_pos[1]] = 1
                reward = reward + 100

        # agent2 move
        if action2 == 0:    # move up
            reward = reward - 1
            if self.occupancy[self.agent2_pos[0]][self.agent2_pos[1] + 1] != 1:     # if can move
                self.agent2_pos[1] = self.agent2_pos[1] + 1
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1] - 1] = 0
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
            if self.agent2_pos == self.dest2:
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 0
                self.agent2_pos = self.start2
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
                reward = reward + 100
        elif action2 == 1:  # move down
            reward = reward - 1
            if self.occupancy[self.agent2_pos[0]][self.agent2_pos[1] - 1] != 1:  # if can move
                self.agent2_pos[1] = self.agent2_pos[1] - 1
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1] + 1] = 0
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
            if self.agent2_pos == self.dest2:
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 0
                self.agent2_pos = self.start2
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
                reward = reward + 100
        elif action2 == 2:  # move left
            reward = reward - 1
            if self.occupancy[self.agent2_pos[0] - 1][self.agent2_pos[1]] != 1:  # if can move
                self.agent2_pos[0] = self.agent2_pos[0] - 1
                self.occupancy[self.agent2_pos[0] + 1][self.agent2_pos[1]] = 0
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
            if self.agent2_pos == self.dest2:
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 0
                self.agent2_pos = self.start2
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
                reward = reward + 100
        elif action2 == 3:  # move right
            reward = reward - 1
            if self.occupancy[self.agent2_pos[0] + 1][self.agent2_pos[1]] != 1:  # if can move
                self.agent2_pos[0] = self.agent2_pos[0] + 1
                self.occupancy[self.agent2_pos[0] - 1][self.agent2_pos[1]] = 0
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
            if self.agent2_pos == self.dest2:
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 0
                self.agent2_pos = self.start2
                self.occupancy[self.agent2_pos[0]][self.agent2_pos[1]] = 1
                reward = reward + 100

        obs_1 = self.get_agt1_obs()
        obs_2 = self.get_agt2_obs()
        return reward, obs_1, obs_2

    def reset(self):
        self.agent1_pos = [3, 1]
        self.agent2_pos = [6, 1]
        self.occupancy = [[1, 1, 1, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 0, 1],
                          [1, 1, 1, 1]]

    def output_info(self):
        print("agent 1 position is at ", self.agent1_pos)
        print("agent 2 position is at ", self.agent2_pos)

    def test(self, action1_list, action2_list, max_iter, interval, if_plot):
        self.reset()
        if if_plot:
            self.action1_list = action1_list
            self.action2_list = action2_list
            self.agt1_pos_list = self.start1
            self.agt2_pos_list = self.start2
            for i in range(max_iter):
                self.step(action1_list[0][i], action2_list[0][i])
                self.agt1_pos_list = np.vstack((self.agt1_pos_list, self.agent1_pos))
                self.agt2_pos_list = np.vstack((self.agt2_pos_list, self.agent2_pos))

            # plot
            anim1 = FuncAnimation(self.fig, self.update_1, frames=np.arange(0, max_iter+1), interval=interval)
            anim2 = FuncAnimation(self.fig, self.update_2, frames=np.arange(0, max_iter+1), interval=interval)
            anim3 = FuncAnimation(self.fig, self.update_3, frames=np.arange(0, max_iter+1), interval=interval)
            plt.show()

        else:
            reward = np.zeros((1, max_iter))
            for iter in range(max_iter):
                step_reward, obs_1, obs_2 = self.step(action1_list[iter], action2_list[iter])
                reward[0, iter] = step_reward

                print("iter= ", iter)
                print("action 1= ", action1_list[iter])
                print("action 2= ", action2_list[iter])
                print("reward= ", step_reward)
                print("accumulated reward= ", np.sum(reward))
                print("action 1 observartion= ", obs_1)
                print("action 2 observartion= ", obs_2)
                print("agent 1 position= ", self.agent1_pos)
                print("agent 2 position= ", self.agent2_pos)
                print("")

    def update_1(self, i):
        self.ax1.cla()
        label = 'timestep {0}'.format(i)
        self.ax1.set_xlabel(label)  # 这里是重点，更新x轴的标签

        # plot grid
        for k in range(10):
            for j in range(4):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax1.add_patch(rect)

        # plot block
        temp_occupancy = [[1, 1, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 1]]
        for k in range(10):
            for j in range(4):
                if temp_occupancy[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax1.add_patch(rect)

        # plot agent

        rect = plt.Rectangle((self.agt1_pos_list[i][0], self.agt1_pos_list[i][1]), 1, 1, color='r')
        self.ax1.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos_list[i][0], self.agt2_pos_list[i][1]), 1, 1, color='b')
        self.ax1.add_patch(rect)

        self.ax1.set_xlim([-1, 12])
        self.ax1.set_ylim([-1, 5])
        return self.ax1

    def update_2(self, i):
        self.ax2.cla()
        label = 'timestep {0}'.format(i)
        self.ax2.set_xlabel(label)  # 这里是重点，更新x轴的标签
        for k in range(10):
            for j in range(4):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax2.add_patch(rect)

        # plot block
        temp_occupancy = [[1, 1, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 1]]
        for k in range(10):
            for j in range(4):
                if temp_occupancy[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax2.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos_list[i][0], self.agt1_pos_list[i][1]), 1, 1, color='r')
        self.ax2.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos_list[i][0], self.agt2_pos_list[i][1]), 1, 1, color='b')
        self.ax2.add_patch(rect)

        # plot fog
        x = self.agt1_pos_list[i][0]
        y = self.agt1_pos_list[i][1]
        for k in range(10):
            for j in range(4):
                if np.abs(k-x) > 1 or np.abs(j-y) > 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    self.ax2.add_patch(rect)

        self.ax2.set_xlim([-1, 12])
        self.ax2.set_ylim([-1, 5])
        return self.ax2

    def update_3(self, i):

        self.ax3.cla()
        label = 'timestep {0}'.format(i)
        self.ax3.set_xlabel(label)  # 这里是重点，更新x轴的标签

        for k in range(10):
            for j in range(4):
                rect = plt.Rectangle((k, j), 1, 1, color='k', fill=False)
                self.ax3.add_patch(rect)

        # plot block
        temp_occupancy = [[1, 1, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 1]]
        for k in range(10):
            for j in range(4):
                if temp_occupancy[k][j] == 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='k')
                    self.ax3.add_patch(rect)

        # plot agent
        rect = plt.Rectangle((self.agt1_pos_list[i][0], self.agt1_pos_list[i][1]), 1, 1, color='r')
        self.ax3.add_patch(rect)
        rect = plt.Rectangle((self.agt2_pos_list[i][0], self.agt2_pos_list[i][1]), 1, 1, color='b')
        self.ax3.add_patch(rect)

        # plot fog
        x = self.agt2_pos_list[i][0]
        y = self.agt2_pos_list[i][1]
        for k in range(10):
            for j in range(4):
                if np.abs(k - x) > 1 or np.abs(j - y) > 1:
                    rect = plt.Rectangle((k, j), 1, 1, color='lightgray')
                    self.ax3.add_patch(rect)
        self.ax3.set_xlim([-1, 12])
        self.ax3.set_ylim([-1, 5])
        return self.ax3

