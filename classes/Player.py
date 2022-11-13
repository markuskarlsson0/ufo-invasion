import pygame
from pygame.locals import *

# Player class
class Player:
  def __init__(self, screen):
    self.screen = screen
    self.screen_width = screen.get_width()
    self.screen_height = screen.get_height()
    self.resolution = f'{self.screen_width}x{self.screen_height}'
    self.resolution_multiplier = self.screen_width / 1280

    # Loads image
    self.image = pygame.image.load(f'images/{self.resolution}/player.png').convert_alpha()
    self.width = self.image.get_width()
    self.height = self.image.get_height()

    self.position_x = (self.screen_width // 2) - (self.width // 2)
    self.position_y = (self.screen_height // 2) - (self.height // 2)
    self.velocity_x = 200 * self.resolution_multiplier
    self.velocity_y = 200 * self.resolution_multiplier

    # Calculates radiuses of hitbox circles
    self.radius_1 = int(self.width / 3)
    self.radius_2 = int(self.height / 5)

    # Calculates hitbox values
    self.hitbox_1 = int(self.width / 2)
    self.hitbox_2 = int(self.height / 2)
    self.hitbox_3 = int(self.height / 4)
    self.hitbox_4 = int(self.height / 1.5)
    self.hitbox_5 = int(self.width / 1.2)
    self.hitbox_6 = int(self.height / 1.5)
    self.hitbox_7 = 0
    self.hitbox_8 = 0
    self.hitbox_9 = 0
    self.hitbox_10 = 0
    self.hitbox_11 = 0
    self.hitbox_12 = 0
    self.hitbox_width = int(2 * self.resolution_multiplier)
    self.show_hitbox = False

    self.points = 0
    self.health = 100
    self.energy = 100

  # Moves player
  def move(self):
    # If player is on screen corner
    if self.position_x > self.screen_width - self.width:
      self.position_x = self.screen_width - self.width

    if self.position_x < 0:
      self.position_x = 0

    if self.position_y > self.screen_height - self.height:
        self.position_y = self.screen_height - self.height

    if self.position_y < 0:
        self.position_y = 0

  # Renders player
  def render(self):
    self.screen.blit(self.image, (self.position_x, self.position_y))

    # Renders hitbox
    if self.show_hitbox:
      pygame.draw.circle(self.screen, (255, 255, 255), (self.hitbox_7, self.hitbox_8), self.radius_1, self.hitbox_width)
      pygame.draw.circle(self.screen, (255, 255, 255), (self.hitbox_9, self.hitbox_10), self.radius_2, self.hitbox_width)
      pygame.draw.circle(self.screen, (255, 255, 255), (self.hitbox_11, self.hitbox_12), self.radius_2, self.hitbox_width)