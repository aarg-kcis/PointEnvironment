import matplotlib.pyplot as plt
from threading import Thread
from Environment import PointEnvironment
from Agent import Agent
from Pose import Pose
import numpy as np
import matplotlib.animation as animation

class Visualizer:
  def __init__(self, env, tailLength=5, speedup=1):
    self.tailLength = tailLength
    self.speedup    = speedup
    self.agents     = env.agents
    self.num_agents = env.num_agents
    # self.x          = np.zeros((env.num_agents, tailLength))
    # self.y          = np.zeros((env.num_agents, tailLength))
    # self.sizes      = np.array([range(1,tailLength+1)]*env.num_agents)
    # self.colors     = ['r', 'g', 'b', 'c', 'm']
    # self.c = np.array([[self.colors[i] for j in xrange(tailLength)]\
    #                    for i in xrange(self.num_agents)])
    self.thread     = Thread(target=self._initPlot)
    dtype           = [('position', 'f', 2),('color', 'str', 1),('size', 'i', 1)] 
    self.data       = np.zeros(env.num_agents*tailLength, dtype=dtype)

  def _initPlot(self):
    self.fig = plt.figure(figsize=(8, 8))
    self.ax = plt.subplot(111, frameon=False)
    self.clear()
    anim = animation.FuncAnimation(self.fig, Visualizer.updater, interval=env.iterations*env.dt*1000/self.speedup, fargs=(self,))
    plt.show()

  @staticmethod
  def updater(frame, vis):
    # if np.array([len(i.trajectory) < vis.tailLength for i in vis.agents.values()]).any():
    #   return
    return vis.update(frame)

  def clear(self):
    self.ax.clear()
    self.ax.axis('equal')
    # self.ax.set_xticks([])
    # self.ax.set_yticks([])
    # self.ax.set_xlim(-10, 10)
    # self.ax.set_ylim(-10, 10)

  def update(self, frame):
    self.clear()
    self.ax.set_title("Iter: {}".format(frame))
    # r = range(min(max(frame-self.tailLength+1, 0), 1499), min(frame+1, 1500)) 
    # x = np.array([[i.trajectory[n][0] for n in r] for i in env.agents.values()]).flatten()
    # y = np.array([[i.trajectory[n][1] for n in r] for i in env.agents.values()]).flatten()
    x = np.array([i.trajectory[0][-self.tailLength:] for i in self.env.agents.values()]).flatten()
    y = np.array([i.trajectory[0][-self.tailLength:] for i in self.env.agents.values()]).flatten()
    scatter = plt.scatter(x, y, c=self.c[:,0:len(r)].flatten(), s=self.sizes[:,(self.tailLength-len(r)):].flatten())
    return scatter

env = PointEnvironment()
env.addAgent(Agent(0, Pose(0,0), lenTrajectory=100))
env.addAgent(Agent(1, Pose(-5,1), lenTrajectory=100))
env.addAgent(Agent(2, Pose(-2,7), lenTrajectory=100))
# env.reset()
# print np.array(env.agents[0].trajectory)
v = Visualizer(env, speedup = 20, tailLength=5)
v.thread.start()
# a = []
# for i in env.agents.values():
#   print len(i.trajectory)
#   print range(0,0)
#   x = range(-np.min(5, len(i.trajectory)),0)
#   print x
  # for j in x
# print np.array([[i.trajectory[n][0] for n in range(-min(5, len(i.trajectory)),0)] for i in env.agents.values()]).flatten()
for i in range(1500):
  env.step({k:[.2, 0] for k in [0,1]})
# print env.agents[0].trajectory, len(env.agents[0].trajectory)

  # print [i.pose for i in env.agents.values()]


# print v.x
# print v.y
# print v.sizes
# print v.colors
# print v.c
# v.update()
# print len(env.agents[0].trajectory)
# print env.agents[0].trajectory[-1], range(-5,0)
# print [[env.agents[i].trajectory[n][0] for n in range(-5,0)] for i in env.agents.keys()]
