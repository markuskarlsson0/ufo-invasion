import pygame, random
from pygame.locals import *

from classes.Asteroid import *

# Asteroid management class
class AsteroidManager:
  def __init__(self, screen):
    self.screen = screen
    self.screen_width = screen.get_width()
    self.screen_height = screen.get_height()
    self.resolution = f'{self.screen_width}x{self.screen_height}'
    self.resolution_multiplier = self.screen_width / 1280

    # Loads images and creates list with their sizes
    self.images = []
    for i in range(3):
      self.images.append(pygame.image.load(f'images/{self.resolution}/asteroid_{i + 1}.png').convert_alpha())

    self.images_width = []
    self.images_height = []
    for image in self.images:
      self.images_width.append(image.get_width())
      self.images_height.append(image.get_height())

    self.show_hitbox = False
    self.hitbox_width = int(2 * self.resolution_multiplier)

    self.asteroids = []

  # Creates asteroid
  def create(self):
    velocity_1 = 50 * self.resolution_multiplier
    velocity_2 = 100 * self.resolution_multiplier

    # Randomizes asteroid size
    asteroid_size = random.randint(0, 32)

    if asteroid_size >= 0 and asteroid_size <= 4:
      asteroid_size = 0
    elif asteroid_size >= 5 and asteroid_size <= 24:
      asteroid_size = 1
    else:
      asteroid_size = 2

    # Randomizes spawn side
    side = random.choice(['top', 'bottom', 'left', 'right'])

    # Randomizes asteroid position and velocity
    if side == 'top':
      position_x = random.uniform(0, self.screen_width)
      position_y = -self.images_height[asteroid_size] // 2
      velocity_x = random.uniform(velocity_1, velocity_2)

      if random.randint(0, 1):
        velocity_y = random.uniform(velocity_1, velocity_2)
      else:
        velocity_y = random.uniform(-velocity_2, -velocity_1)

    elif side == 'bottom':
      position_x = random.uniform(0, self.screen_width)
      position_y = self.screen_height + self.images_width[asteroid_size] // 2
      velocity_x = random.uniform(-velocity_2, -velocity_1)

      if random.randint(0, 1):
        velocity_y = random.uniform(velocity_2, velocity_1)
      else:
        velocity_y = random.uniform(-velocity_2, -velocity_1)

    elif side == 'left':
      position_x = -self.images_width[asteroid_size] // 2
      position_y = random.uniform(0, self.screen_height)
      velocity_x = random.uniform(velocity_1, velocity_2)

      if random.randint(0, 1):
        velocity_y = random.uniform(velocity_1, velocity_2)
      else:
        velocity_y = random.uniform(-velocity_2, -velocity_1)

    elif side == 'right':
      position_x = self.screen_width + self.images_width[asteroid_size] // 2
      position_y = random.uniform(0, self.screen_height)
      velocity_x = random.uniform(-velocity_2, -velocity_1)

      if random.randint(0, 1):
        velocity_y = random.uniform(velocity_1, velocity_2)
      else:
        velocity_y = random.uniform(-velocity_2, -velocity_1)

    # Creates asteroid
    if asteroid_size == 0:
      self.asteroids.append(SmallAsteroid(self.images[asteroid_size], position_x, position_y, velocity_x, velocity_y))
    elif asteroid_size == 1:
      self.asteroids.append(MediumAsteroid(self.images[asteroid_size], position_x, position_y, velocity_x, velocity_y))
    elif asteroid_size == 2:
      self.asteroids.append(LargeAsteroid(self.images[asteroid_size], position_x, position_y, velocity_x, velocity_y))

  # Moves asteroids
  def move(self, deltaTime):
    for asteroid in self.asteroids:
      # If asteroid is on screen corner
      if asteroid.position_x > self.screen_width + asteroid.width:
        self.remove(asteroid)

      elif asteroid.position_x < -asteroid.width:
        self.remove(asteroid)

      if asteroid.position_y > self.screen_height + asteroid.height:
        self.remove(asteroid)

      elif asteroid.position_y < -asteroid.width:
        self.remove(asteroid)

      asteroid.position_x += asteroid.velocity_x * deltaTime
      asteroid.position_y += asteroid.velocity_y * deltaTime
      asteroid.angle += asteroid.rotation * deltaTime

  # Renders asteroids
  def render(self):
    for asteroid in self.asteroids:
      asteroidImageCopy = pygame.transform.rotate(asteroid.image, asteroid.angle)
      self.screen.blit(asteroidImageCopy, (asteroid.position_x - int(asteroidImageCopy.get_width() / 2), asteroid.position_y - int(asteroidImageCopy.get_height() / 2)))

      # Renders hitbox
      if self.show_hitbox:
        pygame.draw.circle(self.screen, (255, 255, 255), (asteroid.position_x, asteroid.position_y), asteroid.radius, self.hitbox_width)

  # Removes asteroid
  def remove(self, asteroid):
    # There is a risk that while moving the window,
    # multiple asteroids are queued up to be deleted.
    # This causes the game to crash once window movement stops.
    # This fixes that problem.
    try:
      self.asteroids.remove(asteroid)
    except:
      pass