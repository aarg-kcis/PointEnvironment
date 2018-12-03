import numpy as np
import PointEnvironment.Errors as ERR
from PointEnvironment.Utils import wrap_angle

class Pose(object):

  M = staticmethod(lambda x: np.matrix([[np.cos(x), np.sin(x), 0],[0, 0, 1]]))

  def __init__(self, x=0, y=0, t=0):
    self.reset(x, y, t)

  def reset(self, x, y, t):
    self.x      = x
    self.y      = y
    self.theta  = wrap_angle(t)

  def updateHolonomic(self, action, dt):
    self += (action * dt * Pose.M(self.theta))

  def todict(self):
    return {'x':self.x, 'y':self.y, 'theta':self.theta}

  def tolist(self):
    return [self.x, self.y, self.theta]

  def __add__(self, other):
    if isinstance(other, Pose):
      x = self.x + other.x
      y = self.y + other.y
      theta = wrap_angle(self.theta + other.theta)
    elif other.shape == (1,3):
      x = self.x + other[0][0]
      y = self.y + other[0][1]
      theta = wrap_angle(self.theta + other[0][2])
    else:
      raise NotImplementedError(ERR.CANT_ADD_POSE(a))
    return Pose(x, y, theta)

  def __sub__(self, other):
    dx = self.x - other.x
    dy = self.y - other.y
    dtheta = wrap_angle(self.theta - other.theta)
    return np.array([dx, dy, dtheta])

  def __iter__(self):
    return iter([self.x, self.y, self.theta])

  def __iadd__(self, other):
    if isinstance(other, Pose):
      self.x += other.x
      self.y += other.y
      self.theta += other.theta
    elif isinstance(other, np.ndarray) and other.shape == (1,3):
      self.x += other[0, 0]
      self.y += other[0, 1]
      self.theta += other[0, 2]
    else:
      raise NotImplementedError(ERR.CANT_ADD_POSE(other))
    self.theta = wrap_angle(self.theta)
    return self

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "[X: {}  Y: {}  TH: {}]".format(self.x, self.y, self.theta)

  def __nonzero__(self):
    return True

  def transform_pose(self, pose):
    # Return the pose with respect to this pose's reference frame.
    # Assumes the pose is in world frame
    if type(pose) == list:
      pose = Pose(*pose)
    assert type(pose) == Pose
    Rt = np.matrix([[np.cos(self.theta), -np.sin(self.theta), 0],
                    [np.sin(self.theta), np.cos(self.theta), 0], [0, 0, 1]])
    