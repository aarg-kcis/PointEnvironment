import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import PatchCollection

from Pose import Pose
from Agent import Agent, Trajectory
from Environment import PointEnvironment

class Visualizer:
  def __init__(self, env, tailLength=5, speedup=1):
    self.env        = env
    self.tailLength = tailLength
    self.speedup    = speedup
    self.agents     = env.agents
    self.num_agents = env.num_agents
    self.colors     = ['r', 'g', 'b', 'c', 'm', 'r']
    self.thread     = Thread(target=self._initPlot)
    dtype           = [('position', 'f', 2),('color', 'str', 1),('size', 'i', 1)]
    self.data       = np.zeros(env.num_agents*tailLength, dtype=dtype)
    self.min_limits = np.array([-1, -1], 'f')
    self.max_limits = np.array([6, 6], 'f')
    self.padding    = 0
    self.isdone     = True
    self.trajectories = {}
    for _id in self.env.agents.keys():
      self.trajectories[_id] = Trajectory(maxlen=self.tailLength)

  def _initPlot(self):
    self.fig = plt.figure()
    self.ax = plt.subplot(111, frameon=True)
    self.clear()
    anim = animation.FuncAnimation(self.fig, Visualizer.updater, \
      interval=self.speedup, fargs=(self,))
    self.frame_idx = 0
    plt.show()

  @staticmethod
  def updater(frame, vis):
    return vis.update(frame)

  def clear(self):
    self.ax.clear()
    # self.ax.axis('equal', auto_scale=True)
    # self.ax.axis([-6,6,-6,6])
    self.ax.set_aspect(1)
    # self.ax.set_xticks([])
    # self.ax.set_yticks([])
    self.ax.grid()
    # sx = self.ax.set_xlim(self.min_limits[0]-self.padding, self.max_limits[0]+self.padding, auto=False)
    # sy = self.ax.set_ylim(self.min_limits[1]-self.padding, self.max_limits[1]+self.padding, auto=False)

  def update(self, frame):
    self.isdone = False
    self.clear()
    # self.ax.grid()
    # circles = []
    # for _id, agent in self.agents.items():
    #   self.trajectories[_id].append(agent.pose.tolist()[:-1])
    # for _id, a_t in self.trajectories.items():
    #   agentrad = self.agents[_id].collisionRadius/self.tailLength
    #   for i, x in enumerate(a_t):
    #     c = self.colors[_id]
    #     self.ax.add_artist(plt.Circle(x, radius=agentrad*(i+1), color=c))
    #   # circles += [plt.Circle(x, radius=.3, color='r') for i, x in enumerate(a_t)]
    # # self.ax.add_collection(PatchCollection(circles))
    # return
    x, y, c, s = [], [], [], []
    for agent in self.agents.values():
      self.trajectories[agent.id].append(agent.pose.tolist())
    for _id, a_t in self.trajectories.items():
      x += [i[0] for i in a_t]
      y += [i[1] for i in a_t]
      c += [self.colors[_id]]*len(a_t)
      s += [self.agents[_id].collisionRadius*1000/(2**i) for i in xrange(len(a_t))][::-1]
    self.ax.set_title("Iter: {}".format(self.frame_idx))
    self.isdone = True
    self.frame_idx += 1
    return plt.scatter(x, y, c=c, s=s)

  def updateLimits(self, min_x, max_x, min_y, max_y):
    self.min_limits = np.array([min_x, min_y])
    self.max_limits = np.array([max_x, max_y])

  def resetEnv(self, poses={}):
    self.frame_idx = 0
    self.env.reset(poses)

  # def stepEnv(self, actions={}):
  #   assert type(actions) == dict
  #   env.step(actions)
  #   while self.plotting

env = PointEnvironment()
env.addAgent(Agent(5, Pose(0,5, 0), lenTrajectory=5000))
env.addAgent(Agent(1, Pose(0,1, 0), lenTrajectory=5000))
env.addAgent(Agent(2, Pose(0,2, 0), lenTrajectory=5000))
env.addAgent(Agent(3, Pose(0,3, 0), lenTrajectory=5000))
env.addAgent(Agent(4, Pose(0,4, 0), lenTrajectory=5000))
# print env

v = Visualizer(env, speedup=10, tailLength=5)
v.thread.start()
# print v.env
for i in range(400):
  env.step({k:[k/10., -1/10.] for k in [5,1,2,3,4]})
  while v.isdone:
    pass
for i in env.agents.values():
  print i.pose
print "assss"
# v.resetEnv()
# for i in env.agents.values():
#   print i.pose
# for i in range(150):
#   env.step({k:[0.2*np.random.random(), np.random.random()*0.2-0.1] for k in [0,1,2,3,4]})
#   while v.isdone:
#     pass
# print "assss"
# for i in env.agents.values():
#   print i.pose
