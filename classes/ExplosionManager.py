import pygame, datetime
from pygame.locals import *

from classes.Explosion import Explosion

pygame.init()

# Explosion management class
class ExplosionManager:
  def __init__(self, screen):
    self.screen = screen
    self.screen_width = screen.get_width()
    self.screen_height = screen.get_height()
    self.resolution = f'{self.screen_width}x{self.screen_height}'

    # Loads images
    self.images = []
    for i in range(12):
      self.images.append(pygame.image.load(f'images/{self.resolution}/explosion_{i + 1}.png').convert_alpha())

    self.image_width = self.images[0].get_width()
    self.image_height = self.images[0].get_height()

    # Loads sound
    self.sound = pygame.mixer.Sound('sounds/explosion.mp3')

    self.explosions = []

  # Creates explosion
  def create(self, position_x, position_y):
    self.sound.play()
    self.explosions.append(Explosion(position_x, position_y))

  # Updates explosion states
  def update(self):
    # Deletes explosion if state is too high
    for explosion in self.explosions:
      if explosion.state == 11:
        self.remove(explosion)
      else:
        # Sets timer
        if datetime.datetime.now() >= explosion.timer:
          explosion.state += 1
          explosion.timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.1)

  # Renders explosions
  def render(self):
    for explosion in self.explosions:
      self.screen.blit(self.images[explosion.state], (explosion.position_x, explosion.position_y))

  # Removes explosion
  def remove(self, explosion):
    self.explosions.remove(explosion)