from Pose import Pose
import numpy as np

class Agent:
  def __init__(self, id, startingPose=False, collisionRadius=0.15):
    assert startingPose == False or isinstance(startingPose, Pose)
    self.type           = "AGENT"
    self.id             = id
    self.pose           = Pose()
    self.startingPose   = startingPose if startingPose else Pose()
    self.collsionRadius = collisionRadius

  def reset(self, pose=False):
    self.prevActions    = []
    self.trajectory     = []
    assert pose == False or isinstance(pose, Pose), ERR.BAD_RESET_POSE(pose)
    self.pose = pose if pose else self.startingPose
    
  def step(self, action, dt=0.01):
    self.trajectory.append(self.pose)
    self.pose.updateHolonomic(action, dt)

  def isUnique(self, agents):
    for i in agents:
      if i.id == self.id:
        return False
    return True

  def __str__(self):
    info = "{} {}:\n-Pose: {}\n-Starting Pose: {}\n-Collision Radius: {}\n-Edge Networks: {}".\
            format(self.type, self.id, self.pose, self.startingPose, self.collsionRadius, self.edgeNetworks)
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