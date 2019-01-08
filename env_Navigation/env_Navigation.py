import numpy as np
from PIL import Image,ImageDraw
import math
import random

class Runner(object):
    def __init__(self):
        self.pos = [103., 241.]
        self.vel = [0., 0.]
        self.target_pos = [random.randint(1, 550), random.randint(1, 500)]
        self.check_radius = 25
        self.max_speed = 30
        self.theta = 0.
        self.omega = 0.

class EnvNavigation(object):
    def __init__(self):
        self.map_img = Image.open("map.png")
        self.map_img = self.map_img.convert('RGBA')
        self.redbot_img = Image.open("redbot.png")
        self.redbot_img = self.redbot_img.convert('RGBA')
        self.target_img = Image.open("target.png")
        self.target_img = self.target_img.convert('RGBA')
        self.runner = Runner()

    def get_global_obs(self):
        # load Image
        obs = self.map_img.crop((0, 0, 550, 500))
        temp_redbot_img = self.redbot_img.rotate(-self.runner.theta)
        draw = ImageDraw.Draw(temp_redbot_img)
        r, g, b, alpha = temp_redbot_img.split()
        obs.paste(temp_redbot_img, (round(self.runner.pos[0] - 40), round(self.runner.pos[1] - 40)), mask=alpha)
        r, g, b, alpha = self.target_img.split()
        obs.paste(self.target_img, (round(self.runner.target_pos[0] - 40), round(self.runner.target_pos[1] - 40)), mask=alpha)
        obs = obs.convert('RGB')
        obs = np.array(obs)
        return obs

    def step(self, action):
        self.runner.pos = self.list_add(self.runner.pos, self.runner.vel)
        self.bound_player_pos()
        self.runner.theta = self.runner.theta + self.runner.omega
        self.runner.theta = self.bound_angle(self.runner.theta)
        self.runner.vel = [self.bound_const(action[0], -20, 20), self.bound_const(action[1], -20, 20)]
        self.regulate_speed()
        self.runner.omega = self.bound_const(action[2], -20, 20)
        if self.vec_distance(self.runner.pos, self.runner.target_pos) < self.runner.check_radius:
            self.runner.target_pos = [random.randint(1, 550), random.randint(1, 500)]
        return -self.vec_distance(self.runner.pos, self.runner.target_pos) / 500

    def vec_distance(self, vec_1, vec_2):
        dist = (vec_1[0]-vec_2[0])*(vec_1[0]-vec_2[0])-(vec_1[1]-vec_2[1])*(vec_1[1]-vec_2[1])
        dist = math.sqrt(abs(dist))
        return dist

    def list_add(self, a, b):
        c = []
        for i in range(len(a)):
            c.append(a[i] + b[i])
        return c

    def vec_sub(self, start, target):
        vec = [0., 0.]
        vec[0] = target[0] - start[0]
        vec[1] = target[1] - start[1]
        return vec

    def bound_angle(self, theta):
        new_theta = theta
        if new_theta > 180:
            new_theta = new_theta - 360
        if new_theta < -180:
            new_theta = new_theta + 360
        return new_theta

    def bound_const(self, const, lowerbound, upperbound):
        new_const = const
        if new_const < lowerbound:
            new_const = lowerbound
        if new_const > upperbound:
            new_const =  upperbound
        return new_const

    def vec_rotate(self, vec, theta):
        new_vec = [0., 0.]
        new_vec[0] = vec[0]*math.cos(self.angle_to_rad(theta)) - vec[1]*math.sin(self.angle_to_rad(theta))
        new_vec[1] = vec[0] * math.sin(self.angle_to_rad(theta)) + vec[1] * math.cos(self.angle_to_rad(theta))
        return new_vec

    def angle_to_rad(self, angle):
        rad = angle / 180
        rad = rad * math.pi
        return rad

    def bound_player_pos(self):
        if self.runner.pos[0] < 0:
            self.runner.pos[0] = 0
        if self.runner.pos[0] > 550:
            self.runner.pos[0] = 550
        if self.runner.pos[1] < 0:
            self.runner.pos[1] = 0
        if self.runner.pos[1] > 500:
            self.runner.pos[1] = 500

    def vec_mode(self, vec):
        mode = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
        return mode

    def vec_normalize(self, vec):
        new_vec = [0., 0.]
        new_vec[0] = vec[0] / self.vec_mode(vec)
        new_vec[1] = vec[1] / self.vec_mode(vec)
        return new_vec

    def vec_mul_const(self, vec, con):
        new_vec = [0., 0.]
        new_vec[0] = vec[0] * con
        new_vec[1] = vec[1] * con
        return new_vec

    def regulate_speed(self):
        speed = self.vec_mode(self.runner.vel)
        if speed > self.runner.max_speed:
            self.runner.vel = self.vec_normalize(self.runner.vel)
            self.runner.vel = self.vec_mul_const(self.runner.vel, self.runner.max_speed)