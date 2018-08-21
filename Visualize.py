import numpy as np
from threading import Thread
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import PatchCollection

from Pose import Pose
from Agent import Agent, Trajectory

class Visualizer:
  def __init__(self, env, tailLength=5, speedup=1, bounds=None):
    self.env        = env
    self.tailLength = tailLength
    self.speedup    = speedup
    self.agents     = env.agents
    self.num_agents = env.num_agents
    self.colors     = ['r', 'g', 'b', 'c', 'm', 'r']
    self.thread     = Thread(target=self._initPlot)
    self.isdone     = True
    self.bounds     = bounds
    self.envStepTime = self.env.dt*self.env.iterations*1e3
    self.flush()

  def _initPlot(self):
    self.fig = plt.figure()
    self.fig.subplots_adjust(bottom=0, top=1)
    self.ax = plt.subplot(111, frameon=True)
    self.clear()
    anim = animation.FuncAnimation(self.fig, Visualizer.updater, \
      interval=self.envStepTime/self.speedup, fargs=(self,))
    plt.show()

  @staticmethod
  def updater(frame, vis):
    return vis.update(frame)

  def flush(self):
    self.trajectories = {}
    print self.env.agents
    for _id in self.env.agents.keys():
      self.trajectories[_id] = deque(maxlen=self.tailLength)

  def clear(self):
    self.ax.clear()
    self.ax.set_aspect(1)
    # self.ax.axis('equal')
    if self.bounds != None:
      assert type(self.bounds) == list and len(self.bounds) == 4
      self.ax.axis(self.bounds)
    else:
      pass
    self.ax.grid()

  def update(self, frame):
    self.clear()
    circles = []
    for _id, agent in self.agents.items():
      self.trajectories[_id].append(agent.trajectory.getEarliest()[:-1])

    for _id, a_t in self.trajectories.items():
      agentrad = self.agents[_id].collisionRadius/len(a_t)
      for i, x in enumerate(a_t):
        c = self.colors[_id]
        self.ax.add_artist(plt.Circle(x, radius=agentrad*(i+1), color=c))
    self.ax.set_title("Iter: {}".format(frame))
    self.isdone = True
    # print self.ax.__dict__
    # print "*"*80
    return self.ax.artists
