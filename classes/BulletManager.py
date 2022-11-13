import pygame, random
from pygame.locals import *

from classes.Bullet import Bullet

pygame.init()

# Bullet management class
class BulletManager:
  def __init__(self, screen):
    self.screen = screen
    self.screen_width = screen.get_width()
    self.screen_height = screen.get_height()
    self.resolution = f'{self.screen_width}x{self.screen_height}'
    self.resolution_multiplier = self.screen_width / 1280

    # Loads images
    self.images = []
    for i in range(3):
      self.images.append(pygame.image.load(f'images/{self.resolution}/bullet_{i + 1}.png').convert_alpha())

    self.image_width = self.images[0].get_width()
    self.image_height = self.images[0].get_height()

    # Loads sound
    self.sound = pygame.mixer.Sound('sounds/bullet.mp3')

    self.show_hitbox = False
    self.hitbox_width = int(2 * self.resolution_multiplier)

    self.bullets = []

  # Creates bullet
  def create(self, position_x, position_y, direction):
    self.sound.play()

    # Sets position and velocity
    if direction == 'left':
      velocity_x = -1500 * self.resolution_multiplier
    elif direction == 'right':
      position_x -= self.image_width
      velocity_x = 1500 * self.resolution_multiplier

    position_y += int(40 * self.resolution_multiplier)

    # Creates bullet
    self.bullets.append(Bullet(self.images[random.randint(0, 2)], position_x, position_y, velocity_x))

  # Moves bullets
  def move(self, delta_time):
    for bullet in self.bullets:
      bullet.position_x += bullet.velocity_x * delta_time

      # Deletes bullet if it is not on screen
      if bullet.position_x > self.screen_width:
        self.remove(bullet)
      elif bullet.position_x < -bullet.width:
        self.remove(bullet)

  # Renders bullets
  def render(self):
    for bullet in self.bullets:
      self.screen.blit(bullet.image, (bullet.position_x, bullet.position_y))

      # Renders hitbox
      if self.show_hitbox:
        bullet_hitbox = bullet.hitbox()
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(bullet_hitbox.x, bullet_hitbox.y, bullet_hitbox.width, bullet_hitbox.height), self.hitbox_width)

  # Removes bullet
  def remove(self, bullet):
    self.bullets.remove(bullet)