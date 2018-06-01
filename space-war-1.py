# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1200
HEIGHT = 672
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
ship_img = pygame.image.load('assets/images/playerShip1_red.png')
ship_img2 = pygame.image.load('assets/images/playerShip1_Damage1.png')
ship_img3 = pygame.image.load('assets/images/playerShip1_Damage2.png')
ship_img4 = pygame.image.load('assets/images/playerShip1_Damage3.png')
ship_img5 = pygame.image.load('assets/images/playerShip1_Damage4.png')
ship_img6 = pygame.image.load('assets/images/playerShip1_Damage5.png')

lasers_img = pygame.image.load('assets/images/laserGreen11.png')

mob_img = pygame.image.load('assets/images/enemyBlack5.png')
mob_img2 = pygame.image.load('assets/images/enemyBlack5_Damage1.png')
mob_img3 = pygame.image.load('assets/images/enemyBlack5_Damage2.png')
mob_img4 = pygame.image.load('assets/images/enemyBlack5_Damage3.png')
mob_img5 = pygame.image.load('assets/images/enemyBlack5_Damage4.png')


bluemob_img = pygame.image.load('assets/images/enemyBlue1.png')
bluemob_img1 = pygame.image.load('assets/images/enemyBlue1_Damage3.png')
bluemob_img2 = pygame.image.load('assets/images/enemyBlue1_Damage5.png')

bomb_img = pygame.image.load('assets/images/laserBlue01.png')

background_img = pygame.image.load('assets/images/back_ground/darkPurple.png')

death_screen = pygame.image.load('assets/images/death_screen.png')


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
    
    def __init__(self, x, y, image, shield):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.shield = shield

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers):
         hit_list = pygame.sprite.spritecollide(self, lasers, True)

         for hit in hit_list:
             self.shield -= 1
             SHIELD_DOWN.play()

         if self.shield <= 0:
             player.score += 20
             EXPLOSION.play()
             self.kill()

         hit_list = pygame.sprite.spritecollide(self, lasers, False)
        
         if len(hit_list)> 0:
             self.shield = 0

         if self.shield == 5:
             self.image = mob_img

         if self.shield == 4:
             self.image = mob_img2

         if self.shield == 3:
             self.image = mob_img3

         if self.shield == 2:
             self.image = mob_img4

         if self.shield == 1:
             self.image = mob_img5

         if self.shield == 0:
             self.kill()



class Bluemob(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.shield = 3

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers):
         hit_list = pygame.sprite.spritecollide(self, lasers, True)

         for hit in hit_list:
             self.shield -= 1
             SHIELD_DOWN.play()

         if self.shield <= 0:
             player.score += 10
             EXPLOSION.play()
             self.kill()

         hit_list = pygame.sprite.spritecollide(self, lasers, False)
        
         if len(hit_list)> 0:
             self.shield = 0

         if self.shield == 3:
             self.image = bluemob_img

         if self.shield == 2:
             self.image = bluemob_img1
             
         if self.shield == 1:
             self.image = bluemob_img2

         if self.shield == 0:
             self.kill()




         if self.rect.left < 0:
             self.rect.left = 0

         if self.rect.right > WIDTH:
             self.rect.right = WIDTH


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

    def __init__(self, mobs, bluemobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 5
        self.bomb_rate = 60

    def move(self):
        reverse = False
        all_mobs = mobs.sprites() + bluemobs.sprites()
        for a in all_mobs:
            if self.moving_right:
                a.rect.x += self.speed
                if a.rect.right >= WIDTH:
                    reverse = True
            else:
                a.rect.x -= self.speed
                if a.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for a in all_mobs:
                a.rect.y += 32

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
    

def setup():
    global ship, mobs, stage, player, bombs, lasers, fleet, bluemobs
    
# Make game objects
ship = Ship(550, 536, ship_img)
mob1 = Mob(128, 64, mob_img)
mob2 = Mob(256, 64, mob_img)
mob3 = Mob(384, 64, mob_img)
mob4 = Mob(512, 64, mob_img)
mob5 = Mob(640, 64, mob_img)
mob6 = Mob(768, 64, mob_img)
mob7 = Mob(896, 64, mob_img)

bluemob6 = Bluemob(128, 150, bluemob_img)
bluemob7 = Bluemob(256, 150, bluemob_img)
bluemob8 = Bluemob(384, 150, bluemob_img)
bluemob9 = Bluemob(512, 150, bluemob_img)
bluemob10 = Bluemob(640, 150, bluemob_img)

# Make sprite groups
player = pygame.sprite.GroupSingle()    
player.add(ship)
player.score = 0


lasers = pygame.sprite.Group()


mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7)

bluemobs = pygame.sprite.Group()
bluemobs.add(bluemob6, bluemob7, bluemob8, bluemob9, bluemob10)


bombs = pygame.sprite.Group()


fleet = Fleet(mobs, bluemobs)


# Set stage
stage = START

# Game helper functions
    
def show_title_screen():
    title_text = FONT_GAME.render("SPACE WAR!", 1, WHITE)
    screen.blit(title_text, [128, 204])

def show_death_screen():
    screen.blit(death_screen, [0, 0])

def show_win_screen():
    won_text = FONT_GAME.render("WINNER!", 1, RED)
    screen.blit(won_text, [178, 275])
    
def show_stats(player):
    score_text = FONT_SCORE.render("Score: " + str(player.score), 1, WHITE)
    shield_text = FONT_SCORE.render("Shield: ", 1, WHITE)

    if ship.shield == 5:
        shield_display = FONT_SCORE.render("5", 1, WHITE)
    elif ship.shield == 4:
        shield_display = FONT_SCORE.render("4", 1, WHITE)
    elif ship.shield == 3:
       shield_display = FONT_SCORE.render("3", 1, WHITE)
    elif ship.shield == 2:
        shield_display = FONT_SCORE.render("2", 1, WHITE)
    elif ship.shield == 1:
        shield_display = FONT_SCORE.render("1", 1, WHITE)
    else:
        shield_display = FONT_SCORE.render("X", 1, WHITE)


    if ship.shield == 5:
        pygame.draw.rect(screen, WHITE, [25, 95, 100, 18])
        pygame.draw.rect(screen, GREEN, [25, 95, 100, 18])
    elif ship.shield == 4:
        pygame.draw.rect(screen, WHITE, [25, 95, 100, 18])
        pygame.draw.rect(screen, GREEN, [25, 95, 80, 18])
    elif ship.shield == 3:
        pygame.draw.rect(screen, WHITE, [25, 95, 100, 18])
        pygame.draw.rect(screen, GREEN, [25, 95, 60, 18])
    elif ship.shield == 2:
        pygame.draw.rect(screen, WHITE, [25, 95, 100, 18])
        pygame.draw.rect(screen, GREEN, [25, 95, 40, 18])
    elif ship.shield == 1:
        pygame.draw.rect(screen, WHITE, [25, 95, 100, 18])
        pygame.draw.rect(screen, GREEN, [25, 95, 20, 18])
    else:
        pygame.draw.rect(screen, RED, [25, 95, 0, 18])

    screen.blit(score_text, [32, 32])
    screen.blit(shield_text, [32, 64])
    screen.blit(shield_display, [118, 64])

    
# Game loop
setup()
done = False
GAME_MUSIC.play()

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

                    
            elif stage == END:
                if event.key == pygame.K_r:
                    setup()
                

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
        bluemobs.update(lasers)
        bombs.update()
        fleet.update()

    if stage == PLAYING:
        if len(player) == 0:
            stage = END
        elif len(mobs) == 0:
            stage = END
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    bluemobs.draw(screen)
    mobs.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()
        
    if stage == END:
        if len(player) == 0:
            show_death_screen()
        else:
            show_win_screen()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
