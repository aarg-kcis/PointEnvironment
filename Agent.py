import copy
from Pose import Pose
import Errors as ERR
import numpy as np
from collections import deque

class Agent(object):
  def __init__(self, id, pose=Pose(), defaultPose=False, collisionRadius=0.15, lenTrajectory=100):
    assert defaultPose == False or isinstance(defaultPose, Pose), ERR.TYPE_MISMATCH(defaultPose, Pose)
    self.type           = "AGENT"
    self.id             = id
    self.defaultPose    = defaultPose if defaultPose else copy.deepcopy(pose)
    self.collisionRadius= collisionRadius
    self.lenTrajectory  = lenTrajectory
    self.reset(pose)

  def reset(self, pose=False):
    self.prevActions    = []
    assert pose == False or isinstance(pose, Pose), ERR.BAD_RESET_POSE(pose)
    self.pose = pose if pose else copy.deepcopy(self.defaultPose)
    self.trajectory     = Trajectory(maxlen=self.lenTrajectory, data=[self.pose.tolist()])

  def step(self, action, dt=0.01):
    action = np.matrix(action)
    if action.any():
      self.pose.updateHolonomic(action, dt)

  def updateTrajectory(self):
    self.trajectory.append(self.pose.tolist())

  def isUnique(self, agents):
    for i in agents:
      if i.id == self.id:
        return False
    return True

  def distanceFrom(self, x):
    assert isinstance(x, Pose) or isinstance(x, Agent)
    x = x.pose if isinstance(x, Agent) else x
    return np.linalg.norm((self.pose - x)[:-1])

  def __str__(self):
    info = "{} {}:\n-Pose: {}\n-Default Pose: {}\n-Collision Radius: {}\n".\
            format(self.type, self.id, self.pose, self.defaultPose, self.collsionRadius)
    return info+"\n"+"-"*10

  def __repr__(self):
    return self.type + " {}".format(self.id)

class Trajectory:
  def __init__(self, maxlen=None, data=[]):
    self.maxlen = maxlen
    self.data = data[:]

  def append(self, item):
    self.data.append(item)
    if self.maxlen and len(self.data) > self.maxlen:
      self.data.pop(0)

  def __getitem__(self, index):
    return self.data[index]

  def __str__(self):
    return str(self.data)

  def __repr__(self):
    return str(self.data)

  def __len__(self):
    return len(self.data)


"""Should go in RLAgent Class"""
  # def __init__(self):
  #   self.edgeNetworks   = {}
  #   self.controller     = None

  # def addController(self, network):
  #   self.controller = network

  # def addEdgeNetwork(self, id, network):
  #   self.edgeNetworks[id] = network

  # def act(self, observations):
  #   self.prevAction = np.matrix([0, 0])
  #   if controller is not None:
  #     self.prevAction = self.controller.act(observations)
  #   elif self.edgeNetworks:
  #     for idx, obs in observations:
  #       self.prevAction += self.edgeNetworks.act(observations[idx])
  #   else:
  #     raise NotImplementedError, 'Agents must have edge network(s)'
  #   return self.prevAction
