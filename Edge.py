import numpy as np
from Utils import rreplace, wrap_angle, R

class Edge(object):
  def __init__(self, d, theta, r):
    self.d      = d
    self.t_ij   = np.matrix([np.cos(theta), np.sin(theta)])*R(r)
    self.theta  = np.arctan2(*self.t_ij.tolist()[0][::-1])
    self.TYPE   = "EDGE"

  def __repr__(self):
    info = self.TYPE + "\tr: {}, theta: {}, t: {}".format(self.d, self.theta, self.t_ij)
    return info

  def __sub__(self, other):
    return self.d*self.t_ij - other.d*other.t_ij


class AgentEdge(Edge):
  def __init__(self, agent_pair):
    self.i, self.j = agent_pair
    super(AgentEdge, self).__init__(0, 0, 0)

  def update(self):
    dx, dy, self.r_ij = self.j.pose - self.i.pose
    self.d      = np.linalg.norm([dx, dy])
    self.t_ij   = np.matrix([dx, dy])*R(self.i.pose.theta)/self.d
    self.theta  = np.arctan2(*self.t_ij.tolist()[0][::-1])

  def __repr__(self):
    info = super(AgentEdge, self).__repr__()
    return info +", r_ij: {}".format(self.r_ij)