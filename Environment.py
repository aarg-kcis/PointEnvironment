import numpy as np
import Errors as ERR
from Pose import Pose
from Agent import Agent
from Visualize import Visualizer

class PointEnvironment(object):
  def __init__(self, mode, num_iterations=100, dt=0.01, agents=None, \
               visualize=False, visualOptions={}):
    self.iterations = num_iterations
    self.dt         = dt
    self.agents     = {}
    self.num_agents = 0
    self.updatetype = mode
    self.visualize  = visualize
    self.v_options  = visualOptions
    self.initVisualizer()
    self.addAgents(agents)
    self.reset()

  def addAgent(self, agent):
    assert isinstance(agent, Agent), ERR.TYPE_MISMATCH(agent, Agent)
    assert agent.isUnique(self.agents.values()), ERR.AGENT_NOT_UNIQUE(agent)
    self.agents[agent.id] = agent
    self.num_agents += 1
    if self.visualize:
      self.visual.flush()

  def addAgents(self, agents):
    if agents is None: return
    for i in agents:
      self.addAgent(i)

  def initVisualizer(self):
    assert type(self.visualize) == bool
    if self.visualize:
      self.visual = Visualizer(self, **self.v_options)

  def startVisualiser(self):
    assert self.visualize
    self.visual.thread.start()

  def reset(self, poses={}):
    self.collisionOccured = False
    if self.visualize:
      self.visual.flush()
    assert type(poses) == dict, ERR.TYPE_MISMATCH(poses, dict)
    for i in self.agents.values():
      try:
        i.reset(poses[i.id])
      except KeyError:
        print ERR.RESET_POSE_MISSING(i.id)
        i.reset()

  def step(self, args):
    if self.visualize:
      while not self.visual.isdone:
        pass
    if self.updatetype == 'action':
      self._stepUsingActions(args)
    elif self.updatetype == 'pose':
      self._stepUsingPoseUpdate(args)
    if self.visualize:
      self.visual.isdone = False

  def _stepUsingActions(self, actions):
    assert type(actions) == dict
    actions = {k: np.matrix(v) for k,v in actions.items()}
    for i in xrange(self.iterations):
      for agent in self.agents.values():
        try:
          agent.step(actions[agent.id], self.dt)
        except KeyError:
          pass
      if ((i) % 50) == 0 and self.num_agents > 1 and self._collisionOccured():
        self.collisionOccured = True
        break
    for i in self.agents.values():
      i.updateTrajectory()

  def _stepUsingPoseUpdate(self, poses):
    assert type(poses) == dict
    for agent in self.agents.values():
      try:
        agent.poseUpdate(poses[agent.id])
        agent.updateTrajectory()
      except:
        pass

  def _collisionOccured(self):
    for i in self.agents.values():
      for j in self.agents.values():
        if i.id >= j.id:
          continue
        if i.distanceFrom(j) <= 1.05*(i.collisionRadius+j.collisionRadius):
          print ERR.COLLISION(i.id, j.id)
          return True
    return False
