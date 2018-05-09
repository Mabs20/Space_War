# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1200
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Fonts
FONT_GAME = pygame.font.Font('assets/fonts/Game_text.ttf', 96)
FONT_SCORE = pygame.font.Font('assets/fonts/Computerfont.ttf', 24)

# Images
ship_img = pygame.image.load('assets/images/spaceShips_007.png')
ship_img2 = pygame.image.load('assets/images/spaceShips_Damage1.png')
ship_img3 = pygame.image.load('assets/images/spaceShips_Damage2.png')
ship_img4 = pygame.image.load('assets/images/spaceShips_Damage3.png')
ship_img5 = pygame.image.load('assets/images/spaceShips_Damage4.png')
lasers_img = pygame.image.load('assets/images/laserGreen11.png')
bluemob_img = pygame.image.load('assets/images/enemyBlack5.png')
mob_img = pygame.image.load('assets/images/enemyBlack5.png')
bomb_img = pygame.image.load('assets/images/laserBlue01.png')
background_img = pygame.image.load('assets/images/back_ground/darkPurple.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
PLAYER_LASER = pygame.mixer.Sound('assets/sounds/sfx_laser1.ogg')
ENEMY_LASER = pygame.mixer.Sound('assets/sounds/sfx_laser2.ogg')
SHIELD_DOWN = pygame.mixer.Sound('assets/sounds/sfx_shieldDown.ogg')
GAME_MUSIC = pygame.mixer.Sound('assets/sounds/game_music.ogg')

# Stages
START = 0
PLAYING = 1
END = 2
PAUSE = 3

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 3
        self.shield = 5

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(lasers_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        PLAYER_LASER.play()
        
    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            self.shield -= 1
            SHIELD_DOWN.play()

        if self.shield == 0:
            EXPLOSION.play()
            self.kill()

        hit_list = pygame.sprite.spritecollide(self, bombs, False)
        
        if len(hit_list)> 0:
            self.shield = 0

        if self.shield == 4:
            self.image = ship_img2

        if self.shield == 3:
            self.image = ship_img3

        if self.shield == 2:
            self.image = ship_img4

        if self.shield == 1:
            self.image = ship_img5

        if self.shield == 0:
            self.kill()





        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()
    
        self.image = image
        self.rect = self.image.get_rect()

        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill

    
class Mob(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            
            EXPLOSION.play()
            self.kill()


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

        ENEMY_LASER.play()

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        

        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
        
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()
    
# Make game objects
ship = Ship(550, 536, ship_img)
mob1 = Mob(128, 64, mob_img)
mob2 = Mob(256, 64, mob_img)
mob3 = Mob(384, 64, mob_img)
mob4 = Mob(512, 64, mob_img)
mob5 = Mob(640, 64, mob_img)
bluemob6 = Mob(128, -25, mob_img)
bluemob7 = Mob(256, -25, mob_img)
bluemob8 = Mob(384, -25, mob_img)
bluemob9 = Mob(512, -25, mob_img)
bluemob10 = Mob(640, -25, mob_img)

# Make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)
player.score = 0

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5)

bluemobs = pygame.sprite.Group()
bluemobs.add(bluemob6, bluemob7, bluemob8, bluemob9, bluemob10)

bombs = pygame.sprite.Group()


fleet = Fleet(mobs)

# Set stage
stage = START

# Game helper functions
    
def show_title_screen():
    title_text = FONT_GAME.render("SPACE WAR!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_stats(player):
    score_text = FONT_SCORE.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])
    
# Game loop
done = False
GAME_MUSIC.play()

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()
                
    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers)
        bombs.update()
        fleet.update()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
