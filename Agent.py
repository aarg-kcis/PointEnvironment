from Pose import Pose
import Errors as ERR
import numpy as np

class Agent:
  def __init__(self, id, pose=Pose(), defaultPose=False, collisionRadius=0.15):
    assert defaultPose == False or isinstance(defaultPose, Pose), ERR.TYPE_MISMATCH(defaultPose, Pose)
    self.type           = "AGENT"
    self.id             = id
    self.pose           = pose
    self.defaultPose    = defaultPose if defaultPose else Pose()
    self.collsionRadius = collisionRadius

  def reset(self, pose=False):
    self.prevActions    = []
    self.trajectory     = []
    assert pose == False or isinstance(pose, Pose), ERR.BAD_RESET_POSE(pose)
    self.pose = pose if pose else self.defaultPose
    
  def step(self, action=[0,0], dt=0.01):
    if action == [0,0]:
      return
    self.pose.updateHolonomic(action, dt)

  def updateTrajectory(self):
    self.trajectory.append(self.pose)
    
  def isUnique(self, agents):
    for i in agents:
      if i.id == self.id:
        return False
    return True

  def __str__(self):
    info = "{} {}:\n-Pose: {}\n-Default Pose: {}\n-Collision Radius: {}\n".\
            format(self.type, self.id, self.pose, self.defaultPose, self.collsionRadius)
    return info+"\n"+"-"*10

  def __repr__(self):
    return self.type + " {}".format(self.id)

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