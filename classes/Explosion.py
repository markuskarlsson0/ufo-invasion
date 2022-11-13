import datetime

# Explosion class
class Explosion:
  def __init__(self, position_x, position_y):
    self.position_x = position_x
    self.position_y = position_y
    self.state = 0
    self.timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.1)