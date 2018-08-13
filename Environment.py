import numpy as np
import Errors as ERR
from Agent import Agent
from Pose import Pose

class PointEnvironment(object):
  def __init__(self, num_iterations=100, dt=0.01, agents={}):
    self.iterations = num_iterations
    self.dt         = dt
    self.agents     = agents
    self.num_agents = 0
    self.addAgents(agents)
    self.reset()

  def addAgent(self, agent):
    assert isinstance(agent, Agent), ERR.TYPE_MISMATCH(agent, Agent)
    assert agent.isUnique(self.agents.values()), ERR.AGENT_NOT_UNIQUE(agent)
    self.agents[agent.id] = agent
    self.num_agents += 1

  def addAgents(self, agents):
    for i in agents:
      self.addAgent(i)

  def reset(self, poses={}):
    self.collisionOccured = False
    assert type(poses) == dict, ERR.TYPE_MISMATCH(poses, dict)
    for i in self.agents.values():
      try:
        i.reset(poses[i.id])
      except KeyError:
        print ERR.RESET_POSE_MISSING(i.id)
        i.reset()

  def step(self, actions):
    assert type(actions) == dict
    actions = {k: np.matrix(v) for k,v in actions.items()}
    for i in xrange(self.iterations):
      for agent in self.agents.values():
        try:
          agent.step(actions[agent.id], self.dt)
        except KeyError:
          pass
      if ((i+1) % 50) == 0 and self.num_agents > 1 and self._collisionOccured():
        self.collisionOccured = True
        break
    for i in self.agents.values():
      i.updateTrajectory()

  def _collisionOccured(self):
    for i in self.agents.values():
      for j in self.agents.values():
        if i.id >= j.id:
          continue
        if i.distanceFrom(j) <= 1.05*(i.collsionRadius+j.collsionRadius):
          print ERR.COLLISION(i.id, j.id)
          return True
    return False

  def pauseForVisualizer(self):
    if self.attachedToVisualizer:
      while self.waitingforVisualizer:
        print "waitingforVisualizer", self.waitingforVisualizer
        pass

