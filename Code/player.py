import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    # Initialize sprite
    def __init__(self, pos, width, speed):
        super().__init__()
        # Player set-up
        self.image = pygame.image.load('../Graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.max_x = width
        self.speed = speed
        self.ready = True

        # Player laser set-up
        self.laser_time = 0
        self.laser_cooldown = 750
        self.lasers = pygame.sprite.Group()

        # Player laser audio
        self.laser_sound = pygame.mixer.Sound('../Audio/laser.wav')
        self.laser_sound.set_volume(0.5)
    
    def get_input(self):
        keys = pygame.key.get_pressed()

        # Move player right or left
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        # Constraint player movement to the window
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x:
            self.rect.right = self.max_x

        # Call shoot_laser when space key is pressed and cooldown has passed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
    
    # Cooldown function for laser
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
    
    # Function to shoot laser
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
    
    def update(self):
        self.get_input()
        self.recharge()
        self.lasers.update()