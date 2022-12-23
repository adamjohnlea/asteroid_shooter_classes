import pygame
import sys


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        # we have to init the parent class
        super().__init__()
        # we need a surface (image)
        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        # we need a rect
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))


class Laser(pygame.sprite.Sprite):
    def __init__(self, spawn_pos):
        super().__init__()
        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=spawn_pos)


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("-= ASTEROID SHOOTER w/CLASSES =-")
clock = pygame.time.Clock()

# Background
bg_surf = pygame.image.load('./graphics/background.png').convert()

# Sprite groups
ship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

# Sprite creation
# Ship
ship = Ship()
ship_group.add(ship)

# Laser
laser = Laser(ship.rect.midtop)
laser_group.add(laser)

# Game Loop
while True:  # run forever -> keeps our game going
    # Events (mouse click, button press, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Delta time
    dt = clock.tick() / 100

    # Background
    display_surface.blit(bg_surf, (0, 0))

    # Graphics
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)

    # Draw the frame
    pygame.display.update()