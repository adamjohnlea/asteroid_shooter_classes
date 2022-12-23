import pygame
import sys
from random import randint
from random import uniform


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

    def asteroid_collisions(self):
        if pygame.sprite.spritecollide(self, asteroid_group, True):
            pygame.quit()
            sys.exit()

    def update(self):
        self.time_laser()
        self.input_position()
        self.shoot_laser()
        self.asteroid_collisions()


class Laser(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=spawn_pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def asteroid_collision(self):
        if pygame.sprite.spritecollide(self, asteroid_group, True):
            self.kill()

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom < 0:
            self.kill()
        self.asteroid_collision()


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        asteroid_surf = pygame.image.load('./graphics/meteor.png').convert_alpha()
        asteroid_size = pygame.math.Vector2(asteroid_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(asteroid_surf, asteroid_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

        self.rotation = 0
        self.rotation_speed = randint(20, 50)

    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotate(self.scaled_surf, self.rotation)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


class Text:
    def __init__(self):
        self.font = pygame.font.Font('./graphics/subatomic.ttf', 30)

    def score(self):
        score_text = f'Score: {pygame.time.get_ticks() // 1000}'
        text_surf = self.font.render(score_text, True, 'white')
        text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 80))
        display_surface.blit(text_surf, text_rect)

    def title(self):
        score_text = "-= ASTEROID SHOOTER=-"
        text_surf = self.font.render(score_text, True, 'white')
        text_rect = text_surf.get_rect(midtop=(WINDOW_WIDTH/2, text_surf.get_height()))
        display_surface.blit(text_surf, text_rect)


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

# Asteroid timer
asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 400)


# Game Loop
while True:  # run forever -> keeps our game going
    # Events (mouse click, button press, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == asteroid_timer:
            asteroid_y_pos = randint(-150, -50)
            asteroid_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Asteroid((asteroid_x_pos, asteroid_y_pos), groups=asteroid_group)

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
    asteroid_group.update()

    # Background
    display_surface.blit(bg_surf, (0, 0))

    Text().score()
    Text().title()

    # Graphics
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)
    asteroid_group.draw(display_surface)

    # Draw the frame
    pygame.display.update()
