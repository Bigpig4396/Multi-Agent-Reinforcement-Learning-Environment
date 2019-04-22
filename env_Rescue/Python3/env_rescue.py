from CEnvRescue import CEnvRescue
import numpy as np
import maze
import matplotlib.pyplot as plt
import random

class EnvRescue(object):
    def __init__(self, map_size, N_agent, N_human, seed):
        self.map_size = map_size
        self.generate_maze(seed)
        self.N_agent = N_agent
        self.N_human = N_human
        self.cenv = CEnvRescue(random.randint(0, 10000), self.N_agent, self.N_human)
        self.edge_blk_num = self.cenv.edge_blk_num

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
        maze_obj = maze.Maze(int((self.map_size-1)/2), int((self.map_size-1)/2), seed, symbols, 1)
        grid_map = maze_obj.to_np()
        print('generate map with size', grid_map.shape[0], grid_map.shape[1])
        np.savetxt("map.csv", grid_map, fmt = "%d", delimiter=",")

    def step(self, action_list):
        for i in range(self.N_agent):
            if action_list[i][0]>0.5:
                action_list[i][0]=0.5
            if action_list[i][0]<-0.5:
                action_list[i][0]=-0.5
            self.cenv.d_x = action_list[i][0]

            if action_list[i][1]>0.5:
                action_list[i][1]=0.5
            if action_list[i][1]<-0.5:
                action_list[i][1]=-0.5
            self.cenv.d_y = action_list[i][1]


            if action_list[i][2]>10:
                action_list[i][2]=10
            if action_list[i][2]<-10:
                action_list[i][2]=-10
            self.cenv.omega = action_list[i][2]

            self.cenv.if_pick = action_list[i][3]


            self.cenv.step(i)

    def get_obs(self):
        obs_list = []
        for i in range(self.N_agent):
            obs_list.append(self.get_agt_obs(i))
        return obs_list

    def get_agt_obs(self, agt_id):
        self.cenv.init_obs(agt_id)
        obs = np.zeros((1,self.cenv.obs_size*self.cenv.obs_size*3))
        for i in range(self.cenv.obs_size*self.cenv.obs_size*3):
            self.cenv.get_obs(agt_id, i)
            obs[0, i] = self.cenv.obs
        obs = obs.reshape((self.cenv.obs_size, self.cenv.obs_size, 3))
        return obs

    def get_global_obs(self):
        self.cenv.init_global_obs()
        obs = np.zeros((1,self.cenv.edge_blk_num*self.cenv.edge_blk_num*3))
        for i in range(self.cenv.edge_blk_num*self.cenv.edge_blk_num*3):
            self.cenv.get_global_obs(i)
            obs[0, i] = self.cenv.global_obs
        obs = obs.reshape((self.cenv.edge_blk_num, self.cenv.edge_blk_num, 3))
        for i in range(self.N_agent):
            agt_pos = self.get_agent_pos(i)
            agt_pos = self.real_pos_to_img_pos(agt_pos)
            if i % 2 == 0:
                obs[int(agt_pos[0]), int(agt_pos[1]), 0] = 1
                obs[int(agt_pos[0]), int(agt_pos[1]), 1] = 0
                obs[int(agt_pos[0]), int(agt_pos[1]), 2] = 0
            else:
                obs[int(agt_pos[0]), int(agt_pos[1]), 0] = 0
                obs[int(agt_pos[0]), int(agt_pos[1]), 1] = 0
                obs[int(agt_pos[0]), int(agt_pos[1]), 2] = 1
        return obs

    def get_real_obs(self):
        self.cenv.init_global_obs()
        obs = np.zeros((1, self.cenv.edge_blk_num*self.cenv.edge_blk_num*3))
        for i in range(self.cenv.edge_blk_num*self.cenv.edge_blk_num*3):
            self.cenv.get_global_obs(i)
            obs[0, i] = self.cenv.global_obs
        obs = obs.reshape((self.cenv.edge_blk_num, self.cenv.edge_blk_num, 3))
        real_obs = np.zeros((7*self.cenv.edge_blk_num, 7*self.cenv.edge_blk_num, 3))
        for i in range(self.N_agent):
            agt_pos = self.get_agent_pos(i)
            agt_pos = self.real_pos_to_img_pos(agt_pos)
            if i % 2 == 0:
                obs[agt_pos[0], agt_pos[1], 0] = 1
                obs[agt_pos[0], agt_pos[1], 1] = 0
                obs[agt_pos[0], agt_pos[1], 2] = 0
            else:
                obs[agt_pos[0], agt_pos[1], 0] = 0
                obs[agt_pos[0], agt_pos[1], 1] = 0
                obs[agt_pos[0], agt_pos[1], 2] = 1
        for i in range(self.cenv.edge_blk_num):
            for j in range(self.cenv.edge_blk_num):
                for k in range(7):
                    for l in range(7):
                        real_obs[7*i+k, 7*j+l, 0] = obs[i, j, 0]
                        real_obs[7 * i + k, 7 * j + l, 1] = obs[i, j, 1]
                        real_obs[7 * i + k, 7 * j + l, 2] = obs[i, j, 2]
        return real_obs

    def real_pos_to_img_pos(self, pos):
        half_view_range = 2
        k = round(pos[0] * 5)
        l = round(pos[1] * 5)
        index_x = k + half_view_range
        index_y = l + half_view_range
        return [index_x, index_y]

    def reset(self):
        self.cenv.reset()

    def get_agent_pos(self, agt_id):
        self.cenv.get_agt_x(agt_id)
        self.cenv.get_agt_y(agt_id)
        return [self.cenv.x, self.cenv.y]

    def get_agent_last_pos(self, agt_id):
        self.cenv.get_agt_last_x(agt_id)
        self.cenv.get_agt_last_y(agt_id)
        return [self.cenv.last_x, self.cenv.last_y]

    def get_agent_ori(self, agt_id):
        self.cenv.get_agt_ori(agt_id)
        return self.cenv.ori

    def get_human_pos(self, human_id):
        self.cenv.get_human_x(human_id)
        self.cenv.get_human_y(human_id)
        return [self.cenv.x, self.cenv.y]

    def get_carry_human_id(self, agt_id):
        self.cenv.get_carry_human_id(agt_id)
        return self.cenv.carry_human_id
	
    def get_picked_by(self, human_id):
        self.cenv.get_human_picked_by(human_id)
        return self.cenv.picked_by

    def is_pos_free(self, pos):
        self.cenv.is_pos_free(pos[0], pos[1])
        haha = self.cenv.is_free
        if haha == 0:
            return False
        else:
            return True

    def vec_sqdist(self, pos1, pos2):
        # return squared distance between two vectors
        return (pos1[0] - pos2[0]) * (pos1[0] - pos2[0]) + (pos1[1] - pos2[1]) * (pos1[1] - pos2[1])

    def is_human_safe(self, human_id):
        pos = self.get_human_pos(human_id)
        safe_pos1 = [1, 1]
        safe_pos2 = [self.map_size-2, 1]
        if self.vec_sqdist(pos, safe_pos1) < 1 or self.vec_sqdist(pos, safe_pos2)<1:
            return True
        else:
            return False

    def get_rescued_human_num(self):
        num = 0
        for i in range(self.N_human):
            if self.is_human_safe(i):
                num = num + 1
        return num

    def is_episode_finish(self):
        is_finish = True
        for i in range(self.N_agent):
            pos1 = self.get_agent_pos(i)
            if i % 2 == 0:
                pos2 = [1, 1]
            else:
                pos2 = [self.map_size-2, 1]
            if self.vec_sqdist(pos1, pos2) > 1:
                is_finish = False
        if self.get_rescued_human_num() != self.N_human:
            is_finish = False
        for i in range(self.N_agent):
            if self.get_carry_human_id(i) != -1:
                 is_finish = False
        return is_finish
            


