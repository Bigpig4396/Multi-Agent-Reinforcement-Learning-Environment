# Multi-Agent-Learning-Environments
Hello, I pushed some python environments for Multi Agent Reinforcement Learning. Some are single agent version that can be used for algorithm testing. I provide documents for each environment, you can check the corresponding pdf files in each directory. Some environments are like:


## Multi Agent Soccer Game
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/Soccer.gif)


## Multi Agent Rescue
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/Rescue.gif)

## Multi Agent Cleaner
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/Cleaner.gif)

## Multi Agent Move Box
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/MoveBox.gif)


## Multi Agent Catching Pig
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/CatchPigs.gif)


## Multi Drones Monitoring
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/Drones.gif)


## Multi Agent Maze Running
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/FindGoal.gif)


## Multi Agent Find Treasure
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/FindTreasure.gif)


## Firefighters
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/FireFighter.png)


## Go Together
![image](https://github.com/Bigpig4396/Multi-Agent-Reinforcement-Learning-Environment/blob/master/README/GoTogether.gif)



## Dependency
OpenCV, swig


## Multi-Agent Environment Standard

**Assumption:**

Each agent works synchronously.


**Member Functions**

reset()

reward_list, done = step(action_list)

obs_list = get_obs()



reward_list records the single step reward for each agent, it should be a list like [reward1, 	reward2,......]. The length should be the same as the number of agents. Each element in the 	list should be a integer.

done True/False, mark when an episode finishes.

<font color=Blue>action_list</font> records the single step action instruction for each agent, it should be a list like [action1, 	action2,...]. The length should be the same as the number of agents. Each element in the 	list should be a non-negative integer.

<font color=Blue>obs_list</font> records the single step observation for each agent, it should be a list like [obs1, obs2,...]. The length should be the same as the number of agents. Each element in the 	list can be any form of data, but should be in same dimension, usually a list of variables or 	an image.


**Typical Monte Carlo Procedures**

reset environment by calling reset()
get initial observation get_obs()
for i in range(max_MC_iter):
  get action_list from controller
  apply action by step()
  record returned reward list
  record new observation by get_obs()
