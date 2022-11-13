import random

# Asteroid class
class Asteroid:
  def __init__(self, image, position_x, position_y, velocity_x, velocity_y):
    self.image = image
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.radius = self.width // 2
    self.position_x = position_x
    self.position_y = position_y
    self.velocity_x = velocity_x
    self.velocity_y = velocity_y
    self.angle = 1

    # Sets asteroid rotation
    if random.randint(0, 1) == 0:
      self.rotation = random.uniform(50, 200)
    else:
      self.rotation = random.uniform(-50, -200)

    self.__hitbox = self.image.get_rect()

  # Gets hitbox used by bullet collision
  def hitbox(self):
    self.__hitbox.x = self.position_x - self.width // 2
    self.__hitbox.y = self.position_y - self.height // 2
    return self.__hitbox

# Small asteroid class
class SmallAsteroid(Asteroid):
  def __init__(self, image, position_x, position_y, velocity_x, velocity_y):
    super().__init__(image, position_x, position_y, velocity_x, velocity_y)
    self.points = 1
    self.health = 5
    self.energy = 10
    self.damage = 10

# Medium asteroid class
class MediumAsteroid(Asteroid):
  def __init__(self, image, position_x, position_y, velocity_x, velocity_y):
    super().__init__(image, position_x, position_y, velocity_x, velocity_y)
    self.points = 1
    self.damage = 25

# Large asteroid class
class LargeAsteroid(Asteroid):
  def __init__(self, image, position_x, position_y, velocity_x, velocity_y):
    super().__init__(image, position_x, position_y, velocity_x, velocity_y)
    self.health = -100
    self.damage = 100