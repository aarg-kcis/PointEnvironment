import copy
from Pose import Pose
import Errors as ERR
import numpy as np

class Agent(object):
  def __init__(self, id, pose=None, defaultPose=False, collisionRadius=0.15):
    assert defaultPose == False or isinstance(defaultPose, Pose), ERR.TYPE_MISMATCH(defaultPose, Pose)
    self.type           = "AGENT"
    self.id             = id
    self.defaultPose    = defaultPose if defaultPose else copy.deepcopy(pose)
    self.collisionRadius= collisionRadius
    if pose == None:
      pose = Pose()
    self.reset(pose)

  def reset(self, pose=False):
    self.prevActions    = []
    assert pose == False or isinstance(pose, Pose), ERR.BAD_RESET_POSE(pose)
    self.pose = pose if pose else copy.deepcopy(self.defaultPose)
    self.trajectory     = Trajectory(initdata=[self.pose.tolist()])

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
            format(self.type, self.id, self.pose, self.defaultPose, self.collisionRadius)
    return info+"\n"+"-"*10

  def __repr__(self):
    return self.type + " {}".format(self.id)

class Trajectory:
  def __init__(self, initdata=None):
    self.data = []
    if initdata != None:
      self.data = initdata[:]

  def append(self, item):
    self.data.append(item)

  def getEarliest(self):
    if len(self) == 1:
      return self.data[0]
    return self.data.pop(0)

  def __getitem__(self, index):
    return self.data[index]

  def __str__(self):
    return str(self.data)

  def __repr__(self):
    return str(self.data)

  def __len__(self):
    return len(self.data)
