import numpy as np
import Errors as ERR
from Pose import Pose
from Agent import Agent
from Visualize import Visualizer

class PointEnvironment(object):
  def __init__(self, num_iterations=100, dt=0.01, agents=[], visualise=False, visualiseOptions={}):
    self.iterations = num_iterations
    self.dt         = dt
    self.agents     = {}
    self.num_agents = 0
    self.visualise  = visualise
    self.v_options  = visualiseOptions
    self.initVisualiser()
    self.addAgents(agents)
    self.reset()

  def addAgent(self, agent):
    assert isinstance(agent, Agent), ERR.TYPE_MISMATCH(agent, Agent)
    assert agent.isUnique(self.agents.values()), ERR.AGENT_NOT_UNIQUE(agent)
    self.agents[agent.id] = agent
    self.num_agents += 1
    if self.visualise:
      self.visual.flush()

  def addAgents(self, agents):
    for i in agents:
      self.addAgent(i)

  def initVisualiser(self):
    assert type(self.visualise) == bool
    if self.visualise:
      self.visual = Visualizer(self, **self.v_options)

  def reset(self, poses={}):
    self.collisionOccured = False
    if self.visualise:
      self.visual.flush()
    assert type(poses) == dict, ERR.TYPE_MISMATCH(poses, dict)
    for i in self.agents.values():
      try:
        i.reset(poses[i.id])
      except KeyError:
        print ERR.RESET_POSE_MISSING(i.id)
        i.reset()

  def step(self, actions):
    if self.visualise:
      while not self.visual.isdone:
        pass
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
    if self.visualise:
      self.visual.isdone = False

  def _collisionOccured(self):
    for i in self.agents.values():
      for j in self.agents.values():
        if i.id >= j.id:
          continue
        if i.distanceFrom(j) <= 1.05*(i.collisionRadius+j.collisionRadius):
          print ERR.COLLISION(i.id, j.id)
          return True
    return False


env = PointEnvironment(num_iterations=100, visualise=True, visualiseOptions={"speedup":10, "tailLength":5, 'bounds':[-6,6,-6,6]})
env.addAgent(Agent(5, Pose(0,5, 0)))
env.addAgent(Agent(1, Pose(0,1, 0)))
env.addAgent(Agent(0, Pose(0,0, 0)))
env.addAgent(Agent(2, Pose(0,2, 0)))
env.addAgent(Agent(3, Pose(0,3, 0)))
env.addAgent(Agent(4, Pose(0,4, 0)))
print env.agents
env.visual.thread.start()
for i in range(10):
  env.step({k:[k/10., -1/10.] for k in [5,1,2,3,4,0]})
env.reset({0:Pose(0,-1), 1:Pose(), 2:Pose(0,1), 3:Pose(1,0), 4:Pose(-1,0), 5:Pose(-2,0)})

# for i in range(100):
#   env.step({k:np.random.random(2)*np.array([.4, .5])-np.array([0, .25]) for k in [5,1,2,3,4,0]})
