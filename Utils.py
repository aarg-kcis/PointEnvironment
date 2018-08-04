import numpy as np

def wrap_angle(angle):
  angle = angle % (2*np.pi)
  return angle - 2*np.pi if angle > np.pi else angle

def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)

R = lambda x: np.matrix([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])