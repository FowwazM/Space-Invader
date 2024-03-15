import pygame, sys
from random import choice, randint
from player import Player
import obstacle
from alien import Alien, Extra
from laser import Laser

class Game:
    # Initialize
    def __init__(self):
        # Player set-up
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and score set-up
        self.lives = 3
        self.live_surf = pygame.image.load('../Graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('../Graphics/pixeled.ttf',20)

        # Obstacle set-up
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.create_block(40, 480)
        self.create_block(190, 480)
        self.create_block(340, 480)
        self.create_block(490, 480)

        # Alient set-up
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(6, 8, 60, 48, 70, 100)
        self.alien_direction = 1

        # Extra alien set-up
        self.extra_alien = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)

        # Audio set-up
        music = pygame.mixer.Sound('../Audio/music.wav')
        music.set_volume(0.2)
        music.play(loops = -1)
        self.laser_sound = pygame.mixer.Sound('../Audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../Audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

    # Create blocks
    def create_block(self, init_x, init_y):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = init_x + col_index * self.block_size
                    y = init_y + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)
    
    # Create aliens
    def alien_setup(self, rows, cols, x_dist, y_dist, x_offset, y_offset):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_offset
                y = row_index * y_dist + y_offset

                # Choose alien type
                if row_index == 0: color = 'yellow'
                elif 1 <= row_index <= 2: color = 'green'
                else: color = 'red'

                # Create alien
                alien_sprite = Alien(color, x, y)
                self.aliens.add(alien_sprite)
    
    # Reverse alien movement
    def reverse_aliens(self, drop_dist):
        drop = False
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                drop = True
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                drop = True
        for alien in all_aliens:
            if drop == True:
                alien.rect.y += drop_dist
    
    # Select a random alien and make it shoot a laser
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    # Timer to create the extra alien
    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra_alien.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    # Check for collisions
    def collision_check(self):

        # Check players lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True): laser.kill()

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()
                
                if pygame.sprite.spritecollide(laser, self.extra_alien, True):
                    self.score += 500
                    laser.kill()
        
        # Check alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, True): laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()
        
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    # Display player's lives
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    # Display player's score
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)

    # Display victory message
    def display_victory(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('You won',False,'white')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf,victory_rect)

    # Update and draw all sprites
    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra_alien.update()
        self.aliens.update(self.alien_direction)

        self.reverse_aliens(3)
        self.extra_alien_timer()
        self.collision_check()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra_alien.draw(screen)
        self.display_lives()
        self.display_score()
        self.display_victory()

# If statement to handle use of multiple files
if __name__ == '__main__':
    # Initializing Pygame
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    alien_laser_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(alien_laser_timer, 750)

    while True:
        # Check for escape button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alien_laser_timer:
                game.alien_shoot()
        
        # Draw a background color
        screen.fill((30,30,30))

        # Update the display to draw anything from the game
        game.run()
        pygame.display.flip()
        clock.tick(60)