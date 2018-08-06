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
    self.colors     = ['r', 'g', 'b', 'c', 'm']
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
    return vis.update(frame)

  def clear(self):
    self.ax.clear()
    self.ax.axis('equal')

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
    return plt.scatter(x, y, c=c, s=s)