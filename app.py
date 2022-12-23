import pygame
import sys


class Ship(pygame.sprite.Sprite):

    def __init__(self, groups):
        # we have to init the parent class
        super().__init__(groups)
        # we need a surface (image)
        self.image = pygame.image.load('./graphics/ship.png').convert_alpha()
        # we need a rect
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Timer
        self.can_shoot = True
        self.shoot_time = None

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def time_laser(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def shoot_laser(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.rect.midtop, laser_group)
        pygame.event.pump()

    def update(self):
        self.time_laser()
        self.input_position()
        self.shoot_laser()


class Laser(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=spawn_pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))


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
ship = Ship(ship_group)


# Game Loop
while True:  # run forever -> keeps our game going
    # Events (mouse click, button press, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Delta time
    dt = clock.tick() / 1000

    # Updates
    ship_group.update()
    laser_group.update()

    # Background
    display_surface.blit(bg_surf, (0, 0))

    # Graphics
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)

    # Draw the frame
    pygame.display.update()
