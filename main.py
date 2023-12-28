import pygame
from sys import exit
from random import randint, choice

GROUND = 582
WINDOW_HEIGHT = 683
WINDOW_WIDTH = 1024

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/chel.png').convert_alpha()
        player_walk_1 = pygame.transform.rotozoom(player_walk_1,0,0.15).convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/chel.png').convert_alpha()
        player_walk_2 = pygame.transform.rotozoom(player_walk_2,0,0.15).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.player_jump = pygame.transform.rotozoom(player_jump,0,0.15).convert_alpha()
        player_sit = pygame.image.load('graphics/player/sit.png').convert_alpha()
        self.player_sit = pygame.transform.rotozoom(player_sit,0,0.15).convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,GROUND))
        self.gravity = 0
        self.sit = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.bottom >= GROUND:
            self.gravity = -20
            self.jump_sound.play()
        elif keys[pygame.K_s] and self.rect.bottom <= GROUND:
            self.gravity = 2
            self.sit = 1
        elif self.rect.bottom == GROUND:
            self.sit = 0

    def apply_gravity(self):
        if self.sit == 1:
            self.gravity -= 0.1
            self.rect.y += self.gravity
            if self.rect.bottom <= GROUND: 
                self.rect.bottom = GROUND
        else:
            self.gravity += 1
            self.rect.y += self.gravity
            if self.rect.bottom >= GROUND: 
                self.rect.bottom = GROUND
        
    def animation_state(self):
        if self.rect.bottom < GROUND:
            self.image = self.player_jump
        elif self.sit == 1:
            self.image = self.player_sit
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            self.type = 'fly'
            self.dir = 1
            self.height = 1
            self.amplitude = 15
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.y_pos = randint(250,GROUND-158)

        elif type == 'snail':
            self.type = 'snail'
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.y_pos = GROUND

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (
            randint(WINDOW_WIDTH+100,WINDOW_WIDTH+300),
            self.y_pos))
            
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.right == 0:
            self.kill

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        if self.type == 'fly':
            if self.height == 15 or self.height == 0:
                self.dir *= -1
                self.height += self.dir
            elif self.dir == 1:
                self.height += 1
            elif self.dir == -1:
                self.height -=1
            self.rect.y = self.y_pos + self.height
        self.destroy()

def display_score():
    current_time = (pygame.time.get_ticks() - start_time)//1000
    score_surf = test_font.render(str(current_time),False,'#5B7269')
    score_rect = score_surf.get_rect(center = (512, 140))
    screen.blit(score_surf,score_rect)
    return current_time

def display_lives():
    lives_surf = test_font.render(lives * 'x',False,'#5B7269')
    lives_rect = lives_surf.get_rect(center = (950,50))
    screen.blit(lives_surf,lives_rect)
                
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,True):
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Strogino Runner')
icon = pygame.image.load('graphics/icon.png') 
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/PixemontrialRegular-x3KqK.otf',60)
game_active = False
start_time = 0
lives = 3
score = 0
bg_music = pygame.mixer.Sound('audio/bg_music.mp3')
bg_music.set_volume(0.3)
bg_music .play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

bg_surface = pygame.image.load('graphics/background.png').convert()

title_surf = test_font.render('STROGINO RUNNER', False, '#7E7087')
title_rect = title_surf.get_rect(center = (512, 90))

# Intro screen
player_stand = pygame.image.load('graphics/player/start.png')
player_stand = pygame.transform.rotozoom(player_stand,0,0.6).convert_alpha()
player_stand_rect = player_stand.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

game_message = test_font.render('Press SPACE to run',False,'White')
game_message_rect = game_message.get_rect(center = (512, 600))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','fly'])))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            start_time = pygame.time.get_ticks()
            
    if game_active:
        screen.blit(bg_surface,(0,0))
        score = display_score()
        display_lives()
        
        #Player
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #Collsions
        collis = collision_sprite()
        if not collis:
            if lives == 1:
                game_active = False
                lives = 3
            else:
                lives -= 1
    else:
        bg_stand = pygame.image.load('graphics/strogino.png')
        bg_stand = pygame.transform.rotozoom(bg_stand,0,1.3).convert_alpha()
        bg_stand_rect = bg_stand.get_rect(center = (WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        screen.blit(bg_stand,bg_stand_rect)
        screen.blit(player_stand,player_stand_rect)
        score_message = test_font.render(f'Your score: {score}',False,'White')
        score_message_rect = score_message.get_rect(center = (512, 600))
        
        screen.blit(title_surf,title_rect)

        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)
