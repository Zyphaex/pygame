import pygame
from sys import exit
from random import randint

from utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PURPLE, GROUND_HEIGHT, FONT_PATH, SKY_PATH, GROUND_PATH, PLAYER_WALK_1_PATH, PLAYER_WALK_2_PATH, PLAYER_JUMP_PATH, SNAIL_FRAME_1_PATH, SNAIL_FRAME_2_PATH, FLY_FRAME_1_PATH, FLY_FRAME_2_PATH, PLAYER_STAND_PATH

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(PLAYER_WALK_1_PATH).convert_alpha()
        player_walk_2 = pygame.image.load(PLAYER_WALK_2_PATH).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load(PLAYER_JUMP_PATH).convert_alpha()
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, GROUND_HEIGHT))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= GROUND_HEIGHT:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT

    def animation_state(self):
        if self.rect.bottom < GROUND_HEIGHT:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    
pygame.init()
pygame.display.set_caption('Jumping Game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_PATH, 100)
game_active = False
start_time = 0
hiscore = 0
player_gravity = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

# World
sky_surf = pygame.image.load(SKY_PATH).convert()
sky_surf = pygame.transform.scale(sky_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_surf = pygame.image.load(GROUND_PATH).convert()
ground_surf = pygame.transform.scale(ground_surf, (SCREEN_WIDTH, SCREEN_HEIGHT - 300))

# Player
player_index = 0
player_walk_1 = pygame.image.load(PLAYER_WALK_1_PATH).convert_alpha()
player_walk_2 = pygame.image.load(PLAYER_WALK_2_PATH).convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_jump = pygame.image.load(PLAYER_JUMP_PATH).convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(100, GROUND_HEIGHT))

# Player Animation
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < GROUND_HEIGHT:
        # Jumping
        player_surf = player_jump
    else:
        # Walking
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

# Obstacles
snail_index = 0
snail_frame_1 = pygame.image.load(SNAIL_FRAME_1_PATH).convert_alpha()
snail_frame_2 = pygame.image.load(SNAIL_FRAME_2_PATH).convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_surf = snail_frames[snail_index]

fly_index = 0
fly_frame_1 = pygame.image.load(FLY_FRAME_1_PATH).convert_alpha()
fly_frame_2 = pygame.image.load(FLY_FRAME_2_PATH).convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

def obstacle_move(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == GROUND_HEIGHT:
                screen.blit(snail_frames[snail_index], obstacle_rect)
            else:
                screen.blit(fly_frames[fly_index], obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    
    else:
        return []

# Collisions
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
            
    return True

# Score
def display_score():
    score = int(pygame.time.get_ticks() / 10) - start_time
    score_surf = font.render(f'{score}', False, PURPLE)
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 60))
    screen.blit(score_surf, score_rect)

    return score

# Main Menu
game_name = font.render('Blob Climbers', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (640, 200))
player_stand = pygame.image.load(PLAYER_STAND_PATH).convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (640, 360))
game_message = font.render('Press space to play', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= GROUND_HEIGHT:
                player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= GROUND_HEIGHT:
                    player_gravity = -20
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 10)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), GROUND_HEIGHT)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), GROUND_HEIGHT - 90)))
            
            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index == 0
                snail_surf = snail_frames[snail_index]
            
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, GROUND_HEIGHT))

        # Hiscore
        if display_score() >= hiscore:
            hiscore = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        player_animation()
        player.draw(screen)
        player.update()
        if player_rect.bottom >= GROUND_HEIGHT:
            player_rect.bottom = GROUND_HEIGHT
            player_gravity = 0
        
        # Obstacle Movement
        obstacle_rect_list = obstacle_move(obstacle_rect_list)
        
        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)
        score_message = font.render(f'Hiscore: {hiscore}', False, PURPLE)
        score_message_rect = score_message.get_rect(center = (SCREEN_WIDTH // 2, 540))
        obstacle_rect_list.clear()
        player_rect.midbottom = (100, GROUND_HEIGHT)
        player_gravity = 0
        if hiscore == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(FPS)
