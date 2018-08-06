from Environment import PointEnvironment

class FormationEnvironment(PointEnvironment):
  def __init__(self, num_iterations=100, dt=0.01, agents={}):
    self.actions = {}
    super(FormationEnvironment, self).__init__(num_iterations, dt, agents)

  def stepAgent(self, action, agent_id):
    action = np.matrix(action)
    self.actions[agent_id] = action

  def step(self):
    super(FormationEnvironment, self).step(self.actions)

  # def reset(self):
  #   pass

class AgentObservedEnvironment:
  def __init__(self, world, agent):
    self.id     = agent.id
    self.agent  = agent
    self.world  = world

  def step(self, action):
    world.stepAgent(action, self.id)

    