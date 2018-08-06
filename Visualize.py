import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from Pose import Pose
from Agent import Agent
from Environment import PointEnvironment

class Visualizer:
  def __init__(self, env, tailLength=5, speedup=1):
    self.tailLength = tailLength
    self.speedup    = speedup
    self.agents     = env.agents
    self.num_agents = env.num_agents
    self.colors     = ['r', 'g', 'b', 'c', 'm']
    self.thread     = Thread(target=self._initPlot)
    dtype           = [('position', 'f', 2),('color', 'str', 1),('size', 'i', 1)] 
    self.data       = np.zeros(env.num_agents*tailLength, dtype=dtype)
    self.min_limits = np.array([-1, 1], 'f')
    self.max_limits = np.array([-1, 1], 'f')
    self.padding    = 0.25  

  def _initPlot(self):  
    self.fig = plt.figure()
    self.ax = plt.subplot(111, frameon=False)
    self.clear()
    anim = animation.FuncAnimation(self.fig, Visualizer.updater, \
      interval=env.iterations*env.dt*1000/self.speedup, fargs=(self,))
    plt.show()

  @staticmethod
  def updater(frame, vis):
    return vis.update(frame)

  def clear(self):
    self.ax.clear()
    self.ax.axis('equal')
    sx = self.ax.set_xlim(self.min_limits[0]-self.padding, self.max_limits[0]+self.padding, auto=False)
    sy = self.ax.set_ylim(self.min_limits[1]-self.padding, self.max_limits[1]+self.padding, auto=False)
    print "ss ", sx, sy

  def update(self, frame):
    self.clear()
    self.ax.set_title("Iter: {}".format(frame))
    x, y, c, s = [], [], [], []
    for agent in self.agents.values():
      frame = frame if frame < len(agent.trajectory) else len(agent.trajectory)-1
      tr = agent.trajectory[frame:frame+self.tailLength]
      x += [i[0] for i in tr][::-1]
      y += [i[1] for i in tr][::-1]
      c += [self.colors[agent.id] for i in tr]
      s += range(self.tailLength, 0, -1)[:len(tr)]
      self.updateLimits(min(x), max(x), min(y), max(y))
    return plt.scatter(x, y, c=c, s=s)

  def updateLimits(self, min_x, max_x, min_y, max_y):
    min_c = np.array([min_x, min_y])
    self.min_limits[self.min_limits>min_c] = min_c[self.min_limits>min_c]
    max_c = np.array([max_x, max_y])
    self.max_limits[self.max_limits<max_c] = max_c[self.max_limits<max_c]
