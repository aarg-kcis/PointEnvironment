import numpy as np
import Errors as ERR
from Agent import Agent
from Pose import Pose

class PointEnvironment:
  def __init__(self, num_iterations=100, dt=0.01, agents=[]):
    self.iterations = num_iterations
    self.dt         = dt
    self.agents     = []
    self.num_agents = 0
    self.addAgents(agents)

  def addAgent(self, agent):
    assert isinstance(agent, Agent), ERR.TYPE_MISMATCH(agent, Agent)
    assert agent.isUnique(self.agents), ERR.AGENT_NOT_UNIQUE(agent)
    self.agents.append(agent)
    self.num_agents += 1

  def addAgents(self, agents):
    for i in agents:
      self.addAgent(i)

  def reset(self, poses):
    assert type(poses) = dict, ERR.TYPE_MISMATCH(poses, dict)
    for i in self.agents:
      try:
        i.reset(poses[i.id]):
      except KeyError:
        print ERR.RESET_POSE_MISSING(i.id)


  def step(self, actions):
    assert len(actions) == self.N_AGENTS
    for i in xrange(self.IPS*self.STEPS):
      for i in self.agents:
        i.step(actions[i.ID], self.DT)
      self.trajectory.append([i.pose.tolist()[0] for i in self.agents])
      if self._collisionOccured():
        self.COLLISION = True
        break
    self.shape.updateShapeFromAgents()
    return self._reward()

  def _collisionOccured(self):
    for i, j in self.pairs:
      if np.linalg.norm((i.pose-j.pose)[0,:2]) <= 2*self.BOT_RADIUS:
        print "collision b/w {} and {} with poses {} and {}"\
        .format(i.ID, j.ID, i.pose, j.pose)
        return True
      return False

  def _reward(self):
    if self.COLLISION:
      cost = {}
      for i,j in self.pairs:
        cost[i.ID, j.ID] = -250
    else:
      cost = self.shape - self.SHAPE
    return cost


if __name__ == '__main__':
  env = PointEnvironment()
  env.addAgent(Agent(0))
  env.addAgent(Agent(1))