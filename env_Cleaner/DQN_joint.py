from collections import deque
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from env_Cleaner import EnvCleaner
import numpy as np
import matplotlib.pyplot as plt
import math

class ReplayMemory(object):
    def __init__(self, capacity=200000):
        self.capacity = capacity
        self.memory = deque(maxlen=self.capacity)
        self.is_av = False
        self.batch_size = 64

    def remember(self, state, action, reward, next_state):
        self.memory.append([state, action, reward, next_state])

    def sample(self):
        return random.sample(self.memory, self.batch_size)

    def is_available(self):
        if len(self.memory) > self.batch_size:
            self.is_av = True
        return self.is_av

class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1)

class DQN(nn.Module):
    def __init__(self, n_action):
        super(DQN, self).__init__()

        self.n_action = n_action
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=2)
        self.flat1 = Flatten()
        self.fc1 = nn.Linear(512)
        self.fc2 = nn.Linear(512, self.n_action*self.n_action)

        self.optimizer = torch.optim.Adam(self.parameters(), lr=1e-4)

    def forward(self, x):
        # print('x', x.size())
        h = F.relu(self.conv1(x))
        h = self.flat1(h)
        # print(h.size())
        h = F.relu(self.fc1(h))
        h = self.fc2(h)
        return h

class Agent(object):
    def __init__(self, n_action):
        self.n_action = n_action
        self.dqn = DQN(self.n_action)
        self.gamma = 0.98
        self.loss_fn = torch.nn.MSELoss()

    def get_action_list(self, obs, epsilon):
        if random.random() > epsilon:
            q = self.dqn.forward(self.img_to_tensor(obs).unsqueeze(0))
            # print('q', q1.size())   # size(1, 16)
            action = q.max(1)[1].data[0].item()
            action1 = int(action/self.n_action)
            action2 = action%self.n_action
        else:
            action1 = random.randint(0, self.n_action - 1)
            action2 = random.randint(0, self.n_action - 1)
        return action1, action2

    def img_to_tensor(self, img):
        img_tensor = torch.FloatTensor(img)     # 17*17*3
        img_tensor = img_tensor.permute(2, 0, 1)    # 3*17*17
        return img_tensor

    def list_to_batch(self, x):
        # transform a list of image to a batch of tensor [batch size, input channel, width, height]
        temp_batch = self.img_to_tensor(x[0])
        temp_batch = temp_batch.unsqueeze(0)
        for i in range(1, len(x)):
            img = self.img_to_tensor(x[i])
            img = img.unsqueeze(0)
            temp_batch = torch.cat([temp_batch, img], dim=0)
        return temp_batch

    def train(self, x):
        obs_list = []
        action_list = []
        reward_list = []
        next_obs_list = []
        for i in range(len(x)):
            obs_list.append(x[i][0])
            action_list.append(x[i][1])
            reward_list.append(x[i][2])
            next_obs_list.append(x[i][3])
        obs_list = self.list_to_batch(obs_list)
        next_obs_list = self.list_to_batch(next_obs_list)
        q_list = self.dqn.forward(obs_list)
        next_q_list = self.dqn.forward(next_obs_list)
        next_q_list_max_v, next_q_list_max_i = next_q_list.max(1)
        expected_q_value = q_list.clone()
        for i in range(len(x)):
            temp_index = next_q_list_max_i[i].item()
            expected_q_value[i][action_list[i]] = reward_list[i] + self.gamma * next_q_list[i][temp_index]
        loss1 = self.loss_fn(q_list, expected_q_value.detach())
        self.dqn.optimizer.zero_grad()
        loss1.backward()
        self.dqn.optimizer.step()

    def save_model(self):
        torch.save(self.dqn.state_dict(), 'DQN_joint.pkl')

    def load_model(self):
        self.dqn.load_state_dict(torch.load('DQN_joint.pkl'))

def get_decay(epi_iter):
    decay = math.pow(0.99, epi_iter)
    if decay < 0.05:
        decay = 0.05
    return decay

if __name__ == '__main__':
    env = EnvCleaner(2, 13, 0)
    max_epi_iter = 2000
    max_MC_iter = 2000
    agent = Agent(4)
    memory = ReplayMemory()
    train_curve = []
    for epi_iter in range(max_epi_iter):
        env.reset()
        reward_count = 0
        for MC_iter in range(max_MC_iter):
            env.render()
            obs = env.get_global_obs()
            action1, action2 = agent.get_action_list(obs, get_decay(epi_iter))
            reward = env.step([action1, action2])
            reward_count = reward_count + reward
            next_obs = env.get_global_obs()
            memory.remember(obs, 4*action1+action2, reward, next_obs)
            if memory.is_available():
                agent.train(memory.sample())
            if MC_iter == max_MC_iter - 1:
                print('Episode', epi_iter, 'finished, reward', reward_count)
                train_curve.append(reward_count)
        agent.save_model()
    np.save("DQN_joint_train0.npy", np.array(train_curve))