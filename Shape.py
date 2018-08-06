from Edge import Edge, AgentEdge
from Utils import rreplace, wrap_angle, R
from Agent import Agent
import numpy as np

class Shape(object):
  def __init__(self, edges):
    self.edges = edges
    self.TYPE  = "SHAPE OBJECT"

  def __str__(self):
    info = self.TYPE
    for i, j in self.edges.items():
        info += "\n{}: {}".format(i, j)
    return info

  def __getitem__(self, index):
    return self.edges[index]

  def __sub__(self, other):
    cost = {}
    for i,j in self.edges.keys():
      cost[i,j] = (self.edges[i,j]-other.edges[i,j]) 
    return cost

class ShapeByAgents(Shape):
  def __init__(self, agent_pairs):
    self.agent_pairs = agent_pairs
    self.TYPE = "SHAPE OBJECT BY AGENTS"
    edges = {}
    for i, j in self.agent_pairs:
      edges[i.id, j.id] = AgentEdge((i,j))
    super(ShapeByAgents, self).__init__(edges)
    self.update()

  def update(self):
    for i,j in self.agent_pairs:
      self.edges[i.id, j.id].update()

class ShapeByGeometry(Shape):
  def __init__(self, geometry):
    self.type = "SHAPE OBJECT BY GEOMETRY"
    c = geometry['coordinates']
    r = geometry['orientations']
    edges = {}
    for i in xrange(len(c)):
      for j in xrange(len(c)):
        if i == j:
          continue
        d     = np.linalg.norm(c[j] - c[i])
        t_ij  = np.matrix((c[j]-c[i]))
        theta = np.arctan2(*t_ij.tolist()[0][::-1])
        edges[i, j] = Edge(d, theta, r[i])
    super(ShapeByGeometry, self).__init__(edges)


if __name__ == '__main__':
  from Pose import Pose
  poses = [Pose(4,0,np.radians(-150)), Pose(0,0,np.radians(-150)),  Pose(2,4*np.sin(np.radians(60)),np.radians(-150)) ]
  agents = [Agent(i) for i in range(3)]
  ap = [(i, j) for i in agents for j in agents if i.id != j.id]
  for i in agents:
    i.reset(poses[i.id])
  s = ShapeByAgents(ap)

  pp = {'coordinates': [np.matrix([1,1]), np.matrix([3,1+1+4*np.sin(np.radians(60))]), np.matrix([5,1])],
  'orientations': [np.pi/2, np.pi/2, np.pi/2]}
  ss = ShapeByGeometry(pp)
  
  print ss-s
  agents[1].step([2, 0])
  s.update()
  
  print ss-s
  
  for i in agents:
    print i.pose