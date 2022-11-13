# Bullet class
class Bullet:
  def __init__(self, image, position_x, position_y, velocity_x):
    self.image = image
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.position_x = position_x
    self.position_y = position_y
    self.velocity_x = velocity_x

    self.__hitbox = self.image.get_rect()
    self.__hitbox.width = self.__hitbox.width - (self.__hitbox.width // 3) * 2

  # Gets hitbox
  def hitbox(self):
    self.__hitbox.x = self.position_x + self.__hitbox.width
    self.__hitbox.y = self.position_y
    return self.__hitbox