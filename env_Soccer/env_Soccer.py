import numpy as np
from PIL import Image,ImageFont,ImageDraw
import math
import random

class Ball(object):
    def __init__(self, friction):
        self.pos = [277., 244.]
        self.last_pos = self.pos
        self.vel = [0., 0.]
        self.friction = friction
        self.radius = 20.

    def reset(self):
        self.pos = [277., 244.]
        self.last_pos = self.pos
        self.vel = [0., 0.]

    def step(self, add_vel, player_list):
        self.last_pos = self.pos
        self.pos = self.list_add(self.pos, self.vel)
        self.vel[0] = self.vel[0] * self.friction
        self.vel[1] = self.vel[1] * self.friction
        self.vel = self.list_add(self.vel, add_vel)
        self.bound_ball_pos()

        for i in range(len(player_list)):
            if self.is_ball_bump_player(player_list[i]):
                if random.random() < 0.6:
                    self.vel = self.cal_vel_after_bump(player_list[i])
                    self.pos = self.cal_pos_after_bump()

    def list_add(self, a, b):
        c = []
        for i in range(len(a)):
            c.append(a[i] + b[i])
        return c

    def vec_minus(self, vec):
        new_vec = [0., 0.]
        new_vec[0] = -vec[0]
        new_vec[1] = -vec[1]
        return new_vec

    def bound_angle(self, theta):
        new_theta = theta
        if new_theta > 180:
            new_theta = new_theta - 360
        if new_theta < -180:
            new_theta = new_theta + 360
        return new_theta

    def vec_mul_const(self, vec, con):
        new_vec = [0., 0.]
        new_vec[0] = vec[0] * con
        new_vec[1] = vec[1] * con
        return new_vec

    def vec_angle(self, start, target):
        base = [1, 0]
        theta_1 = math.acos((self.vec_mul(target, base)) / (self.vec_mode(target) * self.vec_mode(base)))
        if target[1] < 0:
            theta_1 = -theta_1
        theta_2 = math.acos((self.vec_mul(start, base)) / (self.vec_mode(start) * self.vec_mode(base)))
        if start[1] < 0:
            theta_2 = -theta_2
        theta = self.rad_to_angle(theta_1 - theta_2)
        theta = self.bound_angle(theta)
        return theta

    def angle_to_rad(self, angle):
        rad = angle / 180
        rad = rad * math.pi
        return rad

    def rad_to_angle(self, rad):
        angle = rad / math.pi
        angle = angle * 180
        return angle

    def vec_mul(self, vec_1, vec_2):
        mul = vec_1[0]*vec_2[0]+vec_1[1]*vec_2[1]
        return mul

    def vec_rotate(self, vec, theta):
        new_vec = [0., 0.]
        new_vec[0] = vec[0]*math.cos(self.angle_to_rad(theta)) - vec[1]*math.sin(self.angle_to_rad(theta))
        new_vec[1] = vec[0] * math.sin(self.angle_to_rad(theta)) + vec[1] * math.cos(self.angle_to_rad(theta))
        return new_vec

    def is_ball_bump_player(self, player):
        is_bump = False
        temp = self.vec_sub(self.pos, player.pos)
        dist = self.vec_mode(temp)
        last_temp = self.vec_sub(self.last_pos, player.pos)
        last_dist = self.vec_mode(last_temp)
        if dist < player.radius and last_dist>=player.radius:
            is_bump = True
        return is_bump

    def cal_pos_after_bump(self):
        new_pos = self.last_pos
        return new_pos

    def cal_vel_after_bump(self, player):
        temp_1 = self.vec_sub(self.last_pos, self.pos)
        temp_2 = self.vec_sub(self.last_pos, player.pos)
        theta = self.vec_angle(temp_1, temp_2)
        new_vel = self.vec_minus(self.vel)
        new_vel = self.vec_mul_const(new_vel, 0.8)
        new_vel = self.vec_rotate(new_vel, theta)
        return new_vel

    def vec_mode(self, vec):
        mode = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
        return mode

    def vec_sub(self, start, target):
        vec = [0., 0.]
        vec[0] = target[0] - start[0]
        vec[1] = target[1] - start[1]
        return vec

    def bound_ball_pos(self):
        if self.pos[0] <= 0 and self.last_pos[0] > 0 :
            self.pos[0] = 0
            self.vel[0] = -self.vel[0]
            self.vel[0] = self.vel[0] * 0.8
        if self.pos[0] >= 550 and self.last_pos[0] < 550:
            self.pos[0] = 550
            self.vel[0] = -self.vel[0]
            self.vel[0] = self.vel[0] * 0.8
        if self.pos[1] <= 0 and self.last_pos[1] > 0:
            self.pos[1] = 0
            self.vel[1] = -self.vel[1]
            self.vel[1] = self.vel[1] * 0.8
        if self.pos[1] >= 500 and self.last_pos[1] < 500:
            self.pos[1] = 500
            self.vel[1] = -self.vel[1]
            self.vel[1] = self.vel[1] * 0.8

class Player(object):
    def __init__(self, team, role):   # team = 0, 1   role = 1, 2, 3
        self.vel = [0., 0.]
        self.omega = 0.
        self.radius = 25.
        self.kick_radius = 50.
        self.view_angle = 50.
        self.max_speed = 30
        self.team = team
        self.role = role
        self.map_img = Image.open("map.png")
        if self.team == 0:  # red team
            if self.role == 1:
                self.pos = [103., 241.]
                self.theta = 0
            elif self.role == 2:
                self.pos = [115., 390.]
                self.theta = 0
            else:
                self.pos = [120., 93.]
                self.theta = 0
        else:               # blue team
            if self.role == 1:
                self.pos = [477., 241.]
                self.theta = 180
            elif self.role == 2:
                self.pos = [401., 411.]
                self.theta = 180
            else:
                self.pos = [402., 115.]
                self.theta = 180

    def reset(self):
        if self.team == 0:  # red team
            if self.role == 1:
                self.pos = [103., 241.]
                self.theta = 0
            elif self.role == 2:
                self.pos = [115., 390.]
                self.theta = 0
            else:
                self.pos = [120., 93.]
                self.theta = 0
        else:               # blue team
            if self.role == 1:
                self.pos = [477., 241.]
                self.theta = 180
            elif self.role == 2:
                self.pos = [401., 411.]
                self.theta = 180
            else:
                self.pos = [402., 115.]
                self.theta = 180
        self.vel = [0., 0.]
        self.omega = 0.

    def step(self, action_index, action_vector, action_const, player_list, ball):
        temp_pos = self.list_add(self.pos, self.vel)
        if self.is_bump_other_player(temp_pos, player_list) == False:
            self.pos = temp_pos
        self.theta = self.theta + self.omega
        self.theta = self.bound_angle(self.theta)
        self.bound_player_pos()
        if action_index == 0:   # kick [,], const
            self.vel = self.vec_mul_const(self.vel, 0.8)
            self.regulate_speed()
            ori_vec = self.vec_rotate([1, 0], self.theta)
            kick_angle = self.vec_angle(ori_vec, action_vector)
            kick_angle = self.bound_angle(kick_angle)
            kick_angle = abs(kick_angle)
            k = - 0.7 / 180
            attenuation = k * kick_angle + 1
            temp_force = self.vec_mul_const(action_vector, attenuation)
            ball.vel = self.vec_add(ball.vel, temp_force)
        if action_index == 1:   # stop ball
            self.vel = [0, 0]
            if self.vec_distance(ball.pos, self.pos) < self.kick_radius:
                ball.vel = [0, 0]
        if action_index == 2:   # run [,], const
            temp_vel = self.vec_normalize(action_vector)
            temp_vel = self.vec_mul_const(temp_vel, action_const)
            ori_vec = self.vec_rotate([1, 0], self.theta)
            kick_angle = self.vec_angle(ori_vec, action_vector)
            kick_angle = self.bound_angle(kick_angle)
            kick_angle = abs(kick_angle)
            k = - 0.7 / 180
            attenuation = k * kick_angle + 1
            temp_vel = self.vec_mul_const(temp_vel, attenuation)
            self.vel = temp_vel
            self.regulate_speed()
        if action_index == 3:   # turn const
            temp_omega = action_const
            temp_omega = self.bound_const(temp_omega, -20, 20)
            self.omega = temp_omega
            self.vel = self.vec_mul_const(self.vel, 0.8)
        if action_index == 4:   # run with ball [,], const
            temp_vel = self.vec_normalize(action_vector)
            temp_vel = self.vec_mul_const(temp_vel, action_const)
            ori_vec = self.vec_rotate([1, 0], self.theta)
            kick_angle = self.vec_angle(ori_vec, action_vector)
            kick_angle = self.bound_angle(kick_angle)
            kick_angle = abs(kick_angle)
            k = - 0.7 / 180
            attenuation = k * kick_angle + 1
            temp_vel = self.vec_mul_const(temp_vel, attenuation)
            self.vel = temp_vel
            self.regulate_speed()
            if self.vec_distance(self.pos, ball.pos) < self.kick_radius:
                ball.vel = temp_vel

        if self.vec_distance(self.pos, ball.pos) < self.radius:
            temp_force = self.vec_sub(self.pos, ball.pos)
            ball.vel = self.vec_add(ball.vel, temp_force)
        return

    def list_add(self, a, b):
        c = []
        for i in range(len(a)):
            c.append(a[i] + b[i])
        return c

    def angle_to_rad(self, angle):
        rad = angle / 180
        rad = rad * math.pi
        return rad

    def vec_rotate(self, vec, theta):
        new_vec = [0., 0.]
        new_vec[0] = vec[0]*math.cos(self.angle_to_rad(theta)) - vec[1]*math.sin(self.angle_to_rad(theta))
        new_vec[1] = vec[0] * math.sin(self.angle_to_rad(theta)) + vec[1] * math.cos(self.angle_to_rad(theta))
        return new_vec

    def vec_sub(self, start, target):
        vec = [0., 0.]
        vec[0] = target[0] - start[0]
        vec[1] = target[1] - start[1]
        return vec

    def vec_distance(self, vec_1, vec_2):
        dist = (vec_1[0]-vec_2[0])*(vec_1[0]-vec_2[0])+(vec_1[1]-vec_2[1])*(vec_1[1]-vec_2[1])
        dist = math.sqrt(dist)
        return dist

    def bound_const(self, const, lowerbound, upperbound):
        new_const = const
        if new_const < lowerbound:
            new_const = lowerbound
        if new_const > upperbound:
            new_const =  upperbound
        return new_const

    def bound_angle(self, theta):
        new_theta = theta
        if new_theta > 180:
            new_theta = new_theta - 360
        if new_theta < -180:
            new_theta = new_theta + 360
        return new_theta

    def vec_mode(self, vec):
        mode = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
        return mode

    def rad_to_angle(self, rad):
        angle = rad / math.pi
        angle = angle * 180
        return angle

    def vec_angle(self, start, target):
        base = [1, 0]
        theta_1 = math.acos((self.vec_mul(target, base)) / (self.vec_mode(target) * self.vec_mode(base)))
        if target[1] < 0:
            theta_1 = -theta_1
        theta_2 = math.acos((self.vec_mul(start, base)) / (self.vec_mode(start) * self.vec_mode(base)))
        if start[1]<0:
            theta_2 = -theta_2
        theta = self.rad_to_angle(theta_1 - theta_2)
        theta = self.bound_angle(theta)
        return theta

    def vec_mul(self, vec_1, vec_2):
        mul = vec_1[0]*vec_2[0]+vec_1[1]*vec_2[1]
        return mul

    def vec_add(self, start, target):
        vec = [0., 0.]
        vec[0] = target[0] + start[0]
        vec[1] = target[1] + start[1]
        return vec

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

    def bound_player_pos(self):
        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > 550:
            self.pos[0] = 550
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > 500:
            self.pos[1] = 500

    def is_bump_other_player(self, temp_pos, player_list):
        other_player_list = []
        is_bump = False
        for i in range(len(player_list)):
            if player_list[i].team != self.team or player_list[i].role != self.role:
                other_player_list.append(player_list[i])
        for i in range(len(other_player_list)):
            if self.vec_distance(temp_pos, other_player_list[i].pos) < self.radius + other_player_list[i].radius:
                is_bump = True
        return is_bump

    def regulate_speed(self):
        speed = self.vec_mode(self.vel)
        if speed > self.max_speed:
            self.vel = self.vec_normalize(self.vel)
            self.vel = self.vec_mul_const(self.vel, self.max_speed)

class EnvSoccer(object):
    def __init__(self):
        self.map_size = [500, 700]
        self.ball = Ball(0.99)
        self.red_score = 0
        self.blue_score = 0
        self.player_list = []

        self.add_player(0)
        self.add_player(0)
        self.add_player(0)
        self.add_player(1)
        self.add_player(1)
        self.add_player(1)

        self.map_img = Image.open("map.png")
        self.map_img = self.map_img.convert('RGBA')
        self.soccer_img = Image.open("soccer.png")
        self.soccer_img = self.soccer_img.convert('RGBA')
        self.redbot_img = Image.open("redbot.png")
        self.redbot_img = self.redbot_img.convert('RGBA')
        self.bluebot_img = Image.open("bluebot.png")
        self.bluebot_img = self.bluebot_img.convert('RGBA')

    def get_global_obs(self):
        # load Image
        obs = self.map_img.crop((0, 0, 700, 500))

        r, g, b, alpha = self.soccer_img.split()
        obs.paste(self.soccer_img, (round(self.ball.pos[0] - 25), round(self.ball.pos[1] - 25)), mask=alpha)

        for i in range(len(self.player_list)):
            if self.player_list[i].team == 0:
                temp_redbot_img = self.redbot_img.rotate(self.player_list[i].theta)
                draw = ImageDraw.Draw(temp_redbot_img)
                ttfront = ImageFont.truetype('simhei.ttf', 30)  # 字体大小
                draw.text((30, 22), str(self.player_list[i].role), (255, 255, 0), font=ttfront)
                r, g, b, alpha = temp_redbot_img.split()
                obs.paste(temp_redbot_img, (round(self.player_list[i].pos[0] - 40), round(self.player_list[i].pos[1] - 40)), mask=alpha)
            if self.player_list[i].team == 1:
                temp_bluebot_img = self.bluebot_img.rotate(self.player_list[i].theta)
                draw = ImageDraw.Draw(temp_bluebot_img)
                ttfront = ImageFont.truetype('simhei.ttf', 30)  # 字体大小
                draw.text((30, 22), str(self.player_list[i].role), (255, 255, 0), font=ttfront)
                r, g, b, alpha = temp_bluebot_img.split()
                obs.paste(temp_bluebot_img, (round(self.player_list[i].pos[0] - 40), round(self.player_list[i].pos[1] - 40)), mask=alpha)
        obs = obs.convert('RGB')
        obs = np.array(obs)
        return obs

    def get_agt_obs(self, index):
        if index < 0 or index >= len(self.player_list):
            return []
        else:
            obs = self.get_global_obs()
            ori_vec = self.vec_rotate([1, 0], self.player_list[index].theta)
            img = Image.fromarray(obs).convert('RGB')
            draw = ImageDraw.Draw(img)
            x = self.player_list[index].pos[0]
            y = self.player_list[index].pos[1]
            theta = self.player_list[index].theta
            draw.pieslice((x - 800, y - 800, x + 800, y + 800),  -theta + self.player_list[index].view_angle, -theta - self.player_list[index].view_angle, fill=(149, 149, 149))
            obs = np.array(img)
            return obs

    def step(self, action_index_list, action_vector_list, action_const_list):
        self.ball.step([0., 0.], self.player_list)

        # check ball in gate
        if self.is_ball_in_gate():
            self.red_score = self.red_score + 10
            self.blue_score = self.blue_score - 10
            self.relocate()
            return

        # check bump to player


        # player move
        action_index_list = self.reform_action_list(action_index_list)
        action_vector_list = self.reform_action_list(action_vector_list)
        action_const_list = self.reform_action_list(action_const_list)
        for i in range(len(self.player_list)):
            self.player_list[i].step(action_index_list[i], action_vector_list[i], action_const_list[i], self.player_list, self.ball)

        # player bump to ball

    def reset_game(self):
        self.relocate()

        self.red_score = 0
        self.blue_score = 0

    def relocate(self):
        # reset ball
        self.ball.reset()

        # reset players
        for i in range(len(self.player_list)):
            self.player_list[i].reset()

    def is_ball_in_gate(self):
        is_in = False
        if self.ball.pos[0] > 550 and self.ball.pos[0] <700 and self.ball.pos[1] > 150 and self.ball.pos[1] <350:
            is_in = True
        return is_in

    def count_red_player_num(self):
        red_num = 0
        for i in range(len(self.player_list)):
            if self.player_list[i].team == 0:
                red_num = red_num + 1
        return red_num

    def count_blue_player_num(self):
        blue_num = 0
        for i in range(len(self.player_list)):
            if self.player_list[i].team == 1:
                blue_num = blue_num + 1
        return blue_num

    def add_player(self, team):
        if team == 0:   # add red team
            if self.count_red_player_num() < 3:
                temp_player = Player(team, self.count_red_player_num() + 1)
                self.player_list.append(temp_player)
        else:           # add blue team
            if self.count_blue_player_num() < 3:
                temp_player = Player(team, self.count_blue_player_num() + 1)
                self.player_list.append(temp_player)

    def reform_action_list(self, action_list):
        new_list = []
        if len(action_list) > len(self.player_list):
            for i in range(len(self.player_list)):
                new_list.append(action_list[i])
        elif len(action_list) < len(self.player_list):
            for i in range(len(action_list)):
                new_list.append(action_list[i])
            for i in range(len(self.player_list) - len(action_list)):
                new_list.append(action_list[0])
        else:
            new_list = action_list
        return new_list

    def vec_sub(self, start, target):
        vec = [0., 0.]
        vec[0] = target[0] - start[0]
        vec[1] = target[1] - start[1]
        return vec

    def vec_add(self, start, target):
        vec = [0., 0.]
        vec[0] = target[0] + start[0]
        vec[1] = target[1] + start[1]
        return vec

    def cal_pos_after_bump(self, ball):
        new_pos = ball.last_pos
        return new_pos

    def cal_vel_after_bump(self, ball, player):
        temp_1 = self.vec_sub(ball.last_pos, ball.pos)
        temp_2 = self.vec_sub(ball.last_pos, player.pos)
        theta = self.vec_angle(temp_1, temp_2)
        new_vel = self.vec_minus(ball.vel)
        new_vel = self.vec_mul_const(new_vel, 0.8)
        new_vel = self.vec_rotate(new_vel, theta)
        return new_vel

    def vec_mode(self, vec):
        mode = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
        return mode

    def vec_minus(self, vec):
        new_vec = [0., 0.]
        new_vec[0] = -vec[0]
        new_vec[1] = -vec[1]
        return new_vec

    def vec_mul(self, vec_1, vec_2):
        mul = vec_1[0]*vec_2[0]+vec_1[1]*vec_2[1]
        return mul

    def vec_angle(self, start, target):
        base = [1, 0]
        theta_1 = math.acos((self.vec_mul(target, base)) / (self.vec_mode(target) * self.vec_mode(base)))
        if target[1] < 0:
            theta_1 = -theta_1
        theta_2 = math.acos((self.vec_mul(start, base)) / (self.vec_mode(start) * self.vec_mode(base)))
        if start[1]<0:
            theta_2 = -theta_2
        theta = self.rad_to_angle(theta_1 - theta_2)
        theta = self.bound_angle(theta)
        return theta

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

    def rad_to_angle(self, rad):
        angle = rad / math.pi
        angle = angle * 180
        return angle

    def angle_to_rad(self, angle):
        rad = angle / 180
        rad = rad * math.pi
        return rad

    def vec_rotate(self, vec, theta):
        new_vec = [0., 0.]
        new_vec[0] = vec[0]*math.cos(self.angle_to_rad(theta)) - vec[1]*math.sin(self.angle_to_rad(theta))
        new_vec[1] = vec[0] * math.sin(self.angle_to_rad(theta)) + vec[1] * math.cos(self.angle_to_rad(theta))
        return new_vec

    def is_ball_bump_player(self, ball, player):
        is_bump = False
        temp = self.vec_sub(ball.pos, player.pos)
        dist = self.vec_mode(temp)
        last_temp = self.vec_sub(ball.last_pos, player.pos)
        last_dist = self.vec_mode(last_temp)
        if dist < player.radius and last_dist>=player.radius:
            is_bump = True
        return is_bump

    def vec_distance(self, vec_1, vec_2):
        dist = (vec_1[0]-vec_2[0])*(vec_1[0]-vec_2[0])-(vec_1[1]-vec_2[1])*(vec_1[1]-vec_2[1])
        dist = math.sqrt(dist)
        return dist

    def bound_angle(self, theta):
        new_theta = theta
        if new_theta > 180:
            new_theta = new_theta - 360
        if new_theta < -180:
            new_theta = new_theta + 360
        return new_theta
