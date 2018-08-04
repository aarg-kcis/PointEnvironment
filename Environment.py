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

  def reset(self, poses={}):
    assert type(poses) == dict, ERR.TYPE_MISMATCH(poses, dict)
    for i in self.agents:
      try:
        i.reset(poses[i.id])
      except KeyError:
        print ERR.RESET_POSE_MISSING(i.id)
        i.reset()

  def step(self, actions):
    assert type(actions) == dict
    actions = {k: np.matrix(v) for k,v in actions.items()}
    for i in xrange(self.iterations):
      for agent in self.agents:
        try:
          # print "Action for Agent {}: {}".format(i.id, actions[i.id])
          agent.step(actions[agent.id], self.dt)
        except KeyError:
          pass
      if ((i+1) % 50) == 0 and self._collisionOccured():
        break
    for i in self.agents:
      i.updateTrajectory()

  def _collisionOccured(self):
    print 'checking for collision'
    for i in self.agents:
      for j in self.agents:
        if i >= j:
          continue
        print i.id, j.id, np.linalg.norm((i.pose-j.pose))
        if np.linalg.norm((i.pose-j.pose)[0,:2]) <= 1.05*(i.collsionRadius+j.collsionRadius):
          print ERR.COLLISION(i.id, j.id)
          return True
    return False

  # def _reward(self):
  #   if self.COLLISION:
  #     cost = {}
  #     for i,j in self.pairs:
  #       cost[i.ID, j.ID] = -250
  #   else:
  #     cost = self.shape - self.SHAPE
  #   return cost


if __name__ == '__main__':
  env = PointEnvironment(num_iterations=100)
  ad = [Agent(0, Pose(1,1,1), Pose(6,6,6)), Agent(3, Pose(1,1,1), Pose(6,6,6)), Agent(11, Pose(1,1,0))]
  env.addAgents(ad)
  print [i.pose for i in env.agents]
  env.reset({1: Pose(9,9,0), 0: Pose(0,0,np.pi/4)})
  print [(i.pose, i.id) for i in env.agents]
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  env.step({0:[1,0]})
  # env.step({0:[1,0]})
  print [i.pose for i in env.agents]
  print [i.trajectory for i in env.agents]
