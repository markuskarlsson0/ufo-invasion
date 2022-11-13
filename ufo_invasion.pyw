import pygame, json, datetime, time, sys, os, subprocess, math
from pygame.locals import *

from classes.AsteroidManager import AsteroidManager
from classes.BulletManager import BulletManager
from classes.ExplosionManager import ExplosionManager
from classes.Player import Player

pygame.init()

# Restarts game
def restart_game():
  pygame.quit()
  subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

# Exits game
def exit_game():
  pygame.quit()
  sys.exit()

# Loads settings
def load_settings():
  with open('player_data/settings.json', 'r') as file:
    settings = json.load(file)

  global resolution, max_fps, last_state
  resolution = settings.get('resolution')
  max_fps = settings.get('max_fps')
  last_state = settings.get('last_state')

# Saves settings
def save_settings():
  settings = {}
  settings['resolution'] = resolution
  settings['max_fps'] = max_fps
  settings['last_state'] = last_state

  with open('player_data/settings.json', 'w') as file:
    json.dump(settings, file)

load_settings()

# Initializes scoreboard (in case 'player_data/scoreboard.json' does not exist)
global scoreboard, scoreboard_players, scoreboard_points
scoreboard = []

# Loads 'player_data/scoreboard.json' and creates two lists containing players and points
def load_scoreboard():
  global scoreboard, scoreboard_players, scoreboard_points
  scoreboard_players = []
  scoreboard_points = []

  with open('player_data/scoreboard.json', 'r') as file:
    scoreboard = json.load(file)

  # Sorts scoreboard with most points at the top
  sorted_scoreboard = sorted(scoreboard, key=lambda value: value['points'], reverse=True)

  for scoreboard_player in sorted_scoreboard:
    scoreboard_players.append(scoreboard_player.get('name'))
    scoreboard_points.append(scoreboard_player.get('points'))

# Saves score to 'player_data/scoreboard.json'
def save_scoreboard(name, points):
  with open('player_data/scoreboard.json', 'w') as file:
    scoreboard.append({'name': f'{name}', 'points': points})
    json.dump(scoreboard, file)

# Goes to settings if game is restarted due to resolution change
if last_state == 'settings':
  last_state = ''
  state = 'settings'
  save_settings()
else:
  state = 'title_screen'

# Sets resolution

# Create custom resolution:
# 1. Create a folder with the name of your resolution in the folder 'images'.
# 2. Put all your images in the folder.
# 3. Set the resolution in player_data/settings.json to your resolution.
screen_width, screen_height = resolution.split('x')
screen_width = int(screen_width)
screen_height = int(screen_height)
resolution_multiplier = screen_width / 1280

# Starts pygame window and clock
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Loads images
icon_image = pygame.image.load(f'images/icon.png').convert_alpha()
background_image = pygame.image.load(f'images/{resolution}/background.png').convert_alpha()
pygame.display.set_caption('UFO Invasion')
pygame.display.set_icon(icon_image)

background = pygame.Surface((screen_width, screen_height))
pygame.display.update()

# Sets timers
asteroid_timer = datetime.datetime.now()
bullet_timer = datetime.datetime.now()
hitbox_timer = datetime.datetime.now()
fps_timer = datetime.datetime.now()
player_death_timer = datetime.datetime.now()

# Text class
class Text:
  def __init__(self, position_x, position_y, font, text):
    self.position_x = position_x
    self.position_y = position_y
    self.font = font
    self.text = text

  # Renders text
  def render(self):
    text = self.font.render(self.text, True, (255, 255, 255))
    text_position = text.get_rect(center = (self.position_x, self.position_y))

    screen.blit(text, text_position)
    pygame.display.update()

# Button class
class Button:
  def __init__(self, position_x, position_y, text, action):
    self.position_x = position_x
    self.position_y = position_y
    self.text = text
    self.action = action

  # Renders button
  def render(self, state):
    if state == 'normal':
      background_color = (255, 255, 255)
      text_color = (0, 0, 0)

    elif state == 'clicked':
      background_color = (0, 0, 0)
      text_color = (255, 255, 255)

    text = medium_font.render(self.text, True, text_color)
    button = text.get_rect(center = (self.position_x, self.position_y))
    self.button = pygame.draw.rect(screen, background_color, (button.x - button_offset_1, button.y, button.width + button_offset_2, button.height), border_radius = button_radius)

    screen.blit(text, (button.x, button.y))
    pygame.display.update(self.button)

# Sets fonts
small_font = pygame.font.SysFont('Arial', int(20 * resolution_multiplier))
medium_font = pygame.font.SysFont('Arial', int(40 * resolution_multiplier))
large_font = pygame.font.SysFont('Arial', int(80 * resolution_multiplier))

# Sets constant button variables
button_offset_1 = int(20 * resolution_multiplier)
button_offset_2 = int(40 * resolution_multiplier)
button_radius = int(40 * resolution_multiplier)

# Creates lists with menu text and buttons
screen_width_divide = screen_width // 2
screen_height_divide = screen_height // 12

title_screen_text = [Text(screen_width_divide, screen_height_divide * 3, large_font, 'UFO Invasion')]
title_screen_buttons = [Button(screen_width_divide, screen_height_divide * 6, 'Start game', 'game'), Button(screen_width_divide, screen_height_divide * 7, 'Scoreboard', 'scoreboard'), Button(screen_width_divide, screen_height_divide * 8, 'Settings', 'settings'), Button(screen_width_divide, screen_height_divide * 9, 'Exit', 'exit')]
scoreboard_text = [Text(screen_width_divide, screen_height_divide, large_font, 'Scoreboard')]
scoreboard_buttons = [Button(screen_width_divide, screen_height_divide * 11.5, 'Back', 'title_screen')]
settings_text = [Text(screen_width_divide, screen_height_divide, large_font, 'Settings'), Text(screen_width_divide, screen_height_divide * 2.5, medium_font, 'Resolution'), Text(screen_width_divide, screen_height_divide * 6, medium_font, 'Frames per second')]
settings_buttons = [Button(screen_width_divide, screen_height_divide * 3.5, '1280 x 720', '1280x720'), Button(screen_width_divide, screen_height_divide * 4.5, '1920 x 1080', '1920x1080'), Button(screen_width_divide, screen_height_divide * 7, '30', 30), Button(screen_width_divide, screen_height_divide * 8, '60', 60), Button(screen_width_divide, screen_height_divide * 9, '120', 120), Button(screen_width_divide, screen_height_divide * 10, 'Unlimited', 1000), Button(screen_width_divide, screen_height_divide * 11.5, 'Back', 'title_screen')]
pause_text = [Text(screen_width_divide, screen_height_divide * 3, large_font, 'UFO Invasion'), Text(screen_width_divide, screen_height_divide * 4.25, medium_font, 'Paused')]
pause_buttons = [Button(screen_width_divide, screen_height_divide * 6, 'Resume game', 'game'), Button(screen_width_divide, screen_height_divide * 7, 'Quit game', 'title_screen'), Button(screen_width_divide, screen_height_divide * 8, 'Exit', 'exit')]
end_text = [Text(screen_width_divide, screen_height_divide * 3, large_font, 'UFO Invasion'), Text(screen_width_divide, screen_height_divide * 4.25, medium_font, 'Game over')]
end_buttons = [Button(screen_width_divide, screen_height_divide * 6, 'New game', 'game'), Button(screen_width_divide, screen_height_divide * 7, 'Save score', 'save_score'), Button(screen_width_divide, screen_height_divide * 8, 'Title screen', 'title_screen'), Button(screen_width_divide, screen_height_divide * 9, 'Exit', 'exit')]
save_score_text = [Text(screen_width_divide, screen_height_divide * 3, large_font, 'UFO Invasion'), Text(screen_width_divide, screen_height_divide * 4.25, medium_font, 'Save score'), Text(screen_width_divide, screen_height_divide * 6, medium_font, 'Type your name...')]
save_score_buttons = [Button(screen_width_divide, screen_height_divide * 11.5, 'Save', 'title_screen')]

# Renders status
def render_status():
  pygame.draw.rect(status_background, (255, 255, 255, 100), status_background.get_rect(), border_radius = status_offset_2)
  screen.blit(status_background, status_position_size)

# Sets constant status variables
status_offset_1 = int(8 * resolution_multiplier)
status_offset_2 = int(16 * resolution_multiplier)

# Sets constant variables for status background
status_position_size = (screen_width // 4, (screen_height // 7) * 6, screen_width // 2, screen_height)
status_background = pygame.Surface(pygame.Rect(status_position_size).size, pygame.SRCALPHA)

# Renders points status
def render_points_status():
  points_text = medium_font.render(f'{player.points}', True, (0, 0, 0))
  points_text_position_x = (screen_width // 2) - (points_text.get_width() / 2)
  points_text_position_y = ((screen_height // 16) * 14.25) - (points_text.get_height() / 2)

  screen.blit(points_text, (points_text_position_x, points_text_position_y))

# Renders health status
def render_health_status():
  screen.blit(health_bar, (health_bar_position_x, health_bar_position_y, health_bar_width, health_bar_height))

  # Health determine bar color
  if player.health < 25:
    health_bar_color = (255, 0, 0, 125)
  elif player.health < 50:
    health_bar_color = (255, 255, 0, 125)
  else:
    health_bar_color = (0, 255, 0, 125)

  health_bar_2 = pygame.Surface(pygame.Rect((health_bar_position_x, health_bar_position_y, ((health_bar_width / 100) * player.health), health_bar_height)).size, pygame.SRCALPHA)
  pygame.draw.rect(health_bar_2, health_bar_color, health_bar.get_rect(), border_radius = status_offset_2)
  screen.blit(health_bar_2, (health_bar_position_x, health_bar_position_y, health_bar_width, health_bar_height))

  screen.blit(health_text, (health_text_position_x, health_text_position_y))

# Sets constant variables for health status
health_bar_width = (screen_width // 4) - status_offset_1 - (status_offset_1 // 2)
health_bar_height = screen_height // 16
health_bar_position_x = (screen_width // 4) + status_offset_1
health_bar_position_y = screen_height - health_bar_height - status_offset_1

# Sets constant background for health status
health_bar = pygame.Surface(pygame.Rect((health_bar_position_x, health_bar_position_y, health_bar_width, health_bar_height)).size, pygame.SRCALPHA)
pygame.draw.rect(health_bar, (255, 255, 255, 100), health_bar.get_rect(), border_radius = status_offset_2)

# Sets constant text for health status
health_text = small_font.render('Health', True, (0, 0, 0))
health_text_position_x = health_bar_position_x + health_bar_width // 2 - health_text.get_width() // 2
health_text_position_y = health_bar_position_y + health_text.get_height() // 2

# Renders energy status
def render_energy_status():
  screen.blit(energy_bar, (energy_bar_position_x, energy_bar_position_y, energy_bar_width, energy_bar_height))

  # Points determine bar color
  if player.energy < 25:
    energy_bar_color = (255, 0, 0, 125)
  elif player.energy < 50:
    energy_bar_color = (255, 255, 0, 125)
  else:
    energy_bar_color = (0, 255, 0, 125)

  energy_bar_2 = pygame.Surface(pygame.Rect((energy_bar_position_x, energy_bar_position_y, ((energy_bar_width / 100) * player.energy), energy_bar_height)).size, pygame.SRCALPHA)
  pygame.draw.rect(energy_bar_2, energy_bar_color, energy_bar.get_rect(), border_radius = status_offset_2)
  screen.blit(energy_bar_2, (energy_bar_position_x, energy_bar_position_y, energy_bar_width, energy_bar_height))

  screen.blit(energy_text, (energy_text_position_x, energy_text_position_y))

# Sets constant variables for energy status
energy_bar_width = (screen_width // 4) - (status_offset_1 * 2)
energy_bar_height = screen_height // 16
energy_bar_position_x = ((screen_width // 4) * 2) + status_offset_1
energy_bar_position_y = screen_height - energy_bar_height - status_offset_1

# Sets constant background for energy status
energy_bar = pygame.Surface(pygame.Rect((energy_bar_position_x, energy_bar_position_y, energy_bar_width, energy_bar_height)).size, pygame.SRCALPHA)
pygame.draw.rect(energy_bar, (255, 255, 255, 100), energy_bar.get_rect(), border_radius = status_offset_2)

# Sets constant text for energy status
energy_text = small_font.render('Energy', True, (0, 0, 0))
energy_text_position_x = energy_bar_position_x + energy_bar_width // 2 - energy_text.get_width() // 2
energy_text_position_y = energy_bar_position_y + energy_text.get_height() // 2

# Renders pause button
def render_pause_button():
  pygame.draw.rect(screen, pause_button_color, (screen_width - int(50 * resolution_multiplier), int(20 * resolution_multiplier), int(10 * resolution_multiplier), int(40 * resolution_multiplier)), border_radius = int(4 * resolution_multiplier))
  pygame.draw.rect(screen, pause_button_color, (screen_width - int(30 * resolution_multiplier), int(20 * resolution_multiplier), int(10 * resolution_multiplier), int(40 * resolution_multiplier)), border_radius = int(4 * resolution_multiplier))

# Sets constant pause button icon
global pause_button, pause_button_color
pause_button = pygame.Rect((screen_width - int(50 * resolution_multiplier), int(20 * resolution_multiplier), int(30 * resolution_multiplier), int(40 * resolution_multiplier)))
pause_button_color = (255, 255, 255)

# Renders FPS text
def render_fps(clock):
  fps_text = medium_font.render(str(round(clock.get_fps())), True, (255, 255, 255))
  screen.blit(fps_text, (fps_text_position_x, fps_text_position_y))

# Sets constant FPS variables
fps_text_position_x = int(10 * resolution_multiplier)
fps_text_position_y = int(10 * resolution_multiplier)

render = 'all'

# Entire program loop
while True:
  # Title screen menu
  while state == 'title_screen':
    # Renders screen
    if render == 'all':
      screen.blit(background_image, (0, 0))

      for text in title_screen_text:
        text.render()

      for button in title_screen_buttons:
        button.render('normal')

      render = 'null'

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in title_screen_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            button.render('clicked')

      # Goes to clicked buttons menu
      if event.type == pygame.MOUSEBUTTONUP:
        for button in title_screen_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            button.render('clicked')
            state = button.action
            render = 'all'

    clock.tick(max_fps)

  # Scoreboard menu
  while state == 'scoreboard':
    # Renders screen
    if render == 'all':
      screen.blit(background_image, (0, 0))

      for text in scoreboard_text:
        text.render()

      for button in scoreboard_buttons:
        button.render('normal')

      # Loads scoreboard if 'player_data/scoreboard.json' exists
      if os.path.exists('player_data/scoreboard.json'):
        load_scoreboard()

        # Renders scoreboard
        for index, scoreboard_player in enumerate(scoreboard_players):
          if index != 9:
            player_text = Text((screen_width // 3), screen_height_divide * (index + 2.5), medium_font, scoreboard_player)
            player_text.render()

        for index, scoreboard_point in enumerate(scoreboard_points):
          if index != 9:
            points_text = Text((screen_width // 3) * 2, screen_height_divide * (index + 2.5), medium_font, str(scoreboard_point))
            points_text.render()

      render = 'null'

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in scoreboard_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            button.render('clicked')

      # Goes to clicked buttons menu
      if event.type == pygame.MOUSEBUTTONUP:
        for button in scoreboard_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            state = button.action
            render = 'all'
            continue

    clock.tick(max_fps)

  # Settings menu
  while state == 'settings':
    # Renders screen
    if render == 'all':
      screen.blit(background_image, (0, 0))

      for text in settings_text:
        text.render()

      change_settings = False
      exit_state = False

      render = 'buttons'

    # Renders buttons
    if render == 'buttons':
      for button in settings_buttons:
        if button.action == resolution:
          button.render('clicked')

        elif button.action == max_fps:
          button.render('clicked')

        else:
          button.render('normal')

      render = 'null'

    # Saves settings if they are changed
    if change_settings:
      if change_settings_restart:
        last_state = 'settings'
      else:
        last_state = ''

      save_settings()

      # Restarts game if setting requires it
      if change_settings_restart:
        change_settings_restart = False
        change_settings = False
        restart_game()
      change_settings = False
      change_settings_restart = False

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click and sets setting if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in settings_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            if button.action == 'title_screen':
              button.render('clicked')

            # 1280x720 button
            elif button.action == '1280x720':
              if resolution == '1920x1080':
                button.render('clicked')
                resolution = button.action
                change_settings = True
                change_settings_restart = True
                render = 'buttons'

            # 1920x1080 button
            elif button.action == '1920x1080':
              if resolution == '1280x720':
                button.render('clicked')
                resolution = button.action
                change_settings = True
                change_settings_restart = True
                render = 'buttons'

            # FPS buttons
            elif not button.action == max_fps:
              button.render('clicked')
              max_fps = button.action
              change_settings = True
              change_settings_restart = False
              render = 'buttons'

      # Goes to clicked buttons menu
      if event.type == pygame.MOUSEBUTTONUP:
        for button in settings_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            if button.action == 'title_screen':
              state = 'title_screen'
              render = 'all'
              continue

    clock.tick(max_fps)

  # Game loop
  while state == 'game':
    # Renders screen and sets first run variables
    if render == 'all':
      # Resets game classes
      asteroid_manager = AsteroidManager(screen)
      bullet_manager = BulletManager(screen)
      explosion_manager = ExplosionManager(screen)
      player = Player(screen)

      # Resets key presses
      w_key = False
      a_key = False
      s_key = False
      d_key = False
      eKey = False
      qKey = False

      pause_button_color = (255, 255, 255)
      show_fps = False

      last_time = time.time()
      delta_time = 0

      render = 'null'

    # Calculates frame times
    clock.tick(max_fps)
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        if pause_button.collidepoint(pygame.mouse.get_pos()):
          pause_button_color = (0, 0, 0)

      # Goes to clicked buttons menu
      if event.type == pygame.MOUSEBUTTONUP:
        if pause_button.collidepoint(pygame.mouse.get_pos()):
          state = 'pause'
          render = 'all'
          continue

      # Gets key presses
      pressed_keys = pygame.key.get_pressed()

      # ESC key
      if pressed_keys[K_ESCAPE]:
        state = 'pause'
        render = 'all'
        continue

      # W key
      if pressed_keys[K_w]:
        w_key = True
      else:
        w_key = False

      # A key
      if pressed_keys[K_a]:
        a_key = True
      else:
        a_key = False

      # S key
      if pressed_keys[K_s]:
        s_key = True
      else:
        s_key = False

      # D key
      if pressed_keys[K_d]:
        d_key = True
      else:
        d_key = False

      # H key, toggles hitboxes
      if pressed_keys[K_h]:
        # Toggles hitboxes if timer is over
        if datetime.datetime.now() >= hitbox_timer:
          if player.show_hitbox:
            asteroid_manager.show_hitbox = False
            bullet_manager.show_hitbox = False
            player.show_hitbox = False
          else:
            asteroid_manager.show_hitbox = True
            bullet_manager.show_hitbox = True
            player.show_hitbox = True

          # Sets timer
          hitbox_timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.1)

      # J key, toggles FPS text
      if pressed_keys[K_j]:
        # Toggles FPS text if timer is over
        if datetime.datetime.now() >= fps_timer:
          if show_fps:
            show_fps = False
          else:
            show_fps = True

          # Sets timer
          fps_timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.1)

      # Q key, shoots bullet left
      if pressed_keys[K_q]:
        if player.energy >= 5 and player.health > 0:
          # If timer is over
          if datetime.datetime.now() >= bullet_timer:
            player.energy -= 5

            # Creates timer if player dies
            if player.energy <= 0:
              player.energy = 0
              player_death_timer = datetime.datetime.now() + datetime.timedelta(seconds = 1)

            # Creates bullet and timer
            bullet_manager.create(player.position_x, player.position_y, 'left')
            bullet_timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.5)

      # E key, shoots bullet right
      if pressed_keys[K_e]:
        if player.energy >= 5 and player.health > 0:
          # If timer is over
          if datetime.datetime.now() >= bullet_timer:
            player.energy -= 5

            # Creates timer if player dies
            if player.energy <= 0:
              player.energy = 0
              player_death_timer = datetime.datetime.now() + datetime.timedelta(seconds = 1)

            # Creates bullet and timer
            bullet_manager.create(player.position_x + player.width, player.position_y, 'right')
            bullet_timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.5)

    # Limits player max health
    if player.health > 100:
      player.health = 100

    # Limits player max energy
    if player.energy > 100:
      player.energy = 100

    # If player dies
    if player.health <= 0 or player.energy <= 0:
      # Goes to end menu if timer is over
      if datetime.datetime.now() >= player_death_timer:
        render = 'all'
        state = 'end'
        continue
      else:
        # Prevents player from moving
        w_key = False
        a_key = False
        s_key = False
        d_key = False

    # Moves player
    if w_key:
      player.position_y -= player.velocity_y * delta_time

    if a_key:
      player.position_x -= player.velocity_x * delta_time

    if s_key:
      player.position_y += player.velocity_y * delta_time

    if d_key:
      player.position_x += player.velocity_x * delta_time

    # Checks if asteroids collides with player or bullets
    for asteroid in asteroid_manager.asteroids:
      # Calculates distance between player hitbox 1 and asteroid
      player.hitbox_7 = player.position_x + player.hitbox_1
      player.hitbox_8 = player.position_y + player.hitbox_2
      distance_1 = math.hypot(asteroid.position_x - player.hitbox_7, asteroid.position_y - player.hitbox_8)

      # Calculates distance between player hitbox 2 and asteroid
      player.hitbox_9 = player.position_x + player.hitbox_3
      player.hitbox_10 = player.position_y + player.hitbox_4
      distance_2 = math.hypot(asteroid.position_x - player.hitbox_9, asteroid.position_y - player.hitbox_10)

      # Calculates distance between player hitbox 3 and asteroid
      player.hitbox_11 = player.position_x + player.hitbox_5
      player.hitbox_12 = player.position_y + player.hitbox_6
      distance_3 = math.hypot(asteroid.position_x - player.hitbox_11, asteroid.position_y - player.hitbox_12)

      # If asteroid collides with player
      if distance_1 <= asteroid.radius + player.radius_1 or distance_2 <= asteroid.radius + player.radius_2 or distance_3 <= asteroid.radius + player.radius_2:
        player.health -= asteroid.damage

        # Creates timer if player dies
        if player.health <= 0:
          player.health = 0
          player_death_timer = datetime.datetime.now() + datetime.timedelta(seconds = 1)

        # Creates explosion and removes asteroid
        explosion_manager.create(asteroid.position_x - (explosion_manager.image_width // 2), asteroid.position_y - (explosion_manager.image_height // 2))
        asteroid_manager.remove(asteroid)

      # Checks if asteroids collides with bullets
      for bullet in bullet_manager.bullets:
        # Gets rectangular hitbox
        bullet_hitbox = bullet.hitbox()
        asteroid_hitbox = asteroid.hitbox()

        # If collision between asteroid and bullet
        if bullet_hitbox.colliderect(asteroid_hitbox):
          # Checks what properties the asteroid has
          if hasattr(asteroid, 'health'):
            player.health += asteroid.health

            # Creates timer if player dies
            if player.health <= 0:
              player.health = 0
              player_death_timer = datetime.datetime.now() + datetime.timedelta(seconds = 1)

          if hasattr(asteroid, 'energy'):
            player.energy += asteroid.energy

          if hasattr(asteroid, 'points'):
            player.points += asteroid.points

          # Removes asteroid and bullet and creates explosion
          asteroid_manager.asteroids.remove(asteroid)
          bullet_manager.bullets.remove(bullet)
          explosion_manager.create(asteroid.position_x - (explosion_manager.image_width // 2), asteroid.position_y - (explosion_manager.image_height // 2))

    # Create asteroid if timer is over and there are less than 20 asteroids
    if datetime.datetime.now() >= asteroid_timer:
      if len(asteroid_manager.asteroids) < 20:
        asteroid_manager.create()

      asteroid_timer = datetime.datetime.now() + datetime.timedelta(seconds = 0.01)

    # Renders screen
    screen.blit(background_image, (0, 0))
    asteroid_manager.move(delta_time)
    asteroid_manager.render()
    bullet_manager.move(delta_time)
    bullet_manager.render()
    player.move()
    player.render()
    explosion_manager.update()
    explosion_manager.render()

    render_status()
    render_points_status()
    render_health_status()
    render_energy_status()
    render_pause_button()

    if show_fps:
      render_fps(clock)

    pygame.display.update()

  # Pause menu
  while state == 'pause':
    # Renders screen
    if render == 'all':
      screen.blit(background_image, (0, 0))

      for text in pause_text:
        text.render()

      for button in pause_buttons:
        button.render('normal')

      render = 'null'

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in pause_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            button.render('clicked')

      # Goes to clicked buttons menu
      if event.type == pygame.MOUSEBUTTONUP:
        for button in pause_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            state = button.action
            if button.action == 'game':
              w_key = False
              a_key = False
              s_key = False
              d_key = False

              pause_button_color = (255, 255, 255)
              last_time = time.time()
              delta_time = 0
            else:
              render = 'all'
            continue

      # Resume game if ESC key is pressed
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          state = 'game'

          w_key = False
          a_key = False
          s_key = False
          d_key = False

          pause_button_color = (255, 255, 255)
          last_time = time.time()
          delta_time = 0
          continue

    clock.tick(max_fps)

  # End menu
  while state == 'end':
    # Renders screen
    if render == 'all':
      screen.blit(background_image, (0, 0))

      for text in end_text:
        text.render()

      for button in end_buttons:
        button.render('normal')

      render = 'null'

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in end_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            button.render('clicked')

      # Goes to clicked buttons menu
      if event.type == pygame.MOUSEBUTTONUP:
        for button in end_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            state = button.action
            render = 'all'
            continue

    clock.tick(max_fps)

  # Save score menu
  while state == 'save_score':
    # Renders screen
    if render == 'all':
      screen.blit(background_image, (0, 0))

      for text in save_score_text:
        text.render()

      for button in save_score_buttons:
        button.render('normal')

      capslock = False
      name = ''

      render = 'null'

    # Gets events
    for event in pygame.event.get():
      if event.type == QUIT:
        state = 'exit'
        continue

      # Renders button click if mouse clicks on it
      if event.type == pygame.MOUSEBUTTONDOWN:
        for button in save_score_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            button.render('clicked')

      # If save button is clicked
      if event.type == pygame.MOUSEBUTTONUP:
        for button in save_score_buttons:
          if button.button.collidepoint(pygame.mouse.get_pos()):
            # Saves score if name is entered
            if name != '':
              # Creates 'player_data/scoreboard.json' if it does not exist
              if not os.path.exists('player_data/scoreboard.json'):
                with open('player_data/scoreboard.json', 'w') as file:
                  file.write('')
                  save_scoreboard(f'{name}', player.points)
              else:
                load_scoreboard()
                save_scoreboard(f'{name}', player.points)

            state = button.action
            render = 'all'
            continue

      # If key is pressed
      if event.type == KEYUP:
        # Tab
        if event.key == 9:
          continue

        # Caps lock
        elif event.key == 1073741881:
          if capslock:
            capslock = False
          else:
            capslock = True

        # Backspace
        elif event.key == 8:
          name = name[:-1]

        # Enter
        elif event.key == 13:
          # Saves score if name is entered
          if name != '':
            # Creates 'player_data/scoreboard.json' if it does not exist
            if not os.path.exists('player_data/scoreboard.json'):
              with open('player_data/scoreboard.json', 'w') as file:
                file.write('')
                save_scoreboard(f'{name}', player.points)
            else:
              load_scoreboard()
              save_scoreboard(f'{name}', player.points)

          state = button.action
          render = 'all'
          continue

        # Other keys
        else:
          if capslock:
            # Tries to convert key number to uppercase letter
            try:
              name += chr(event.key).upper()
            except:
              pass
          else:
            # Tries to convert key number to lowercase letter
            try:
              name += chr(event.key)
            except:
              pass

        # Renders screen
        screen.blit(background_image, (0, 0))

        for text in save_score_text[:-1]:
          text.render()

        for button in save_score_buttons:
          button.render('normal')

        Text(screen_width // 2, screen_height_divide * 6, medium_font, f'{name}').render()

    clock.tick(max_fps)

  # Exits game
  while state == 'exit':
    exit_game()