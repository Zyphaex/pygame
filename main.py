import pygame
from sys import exit

from utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PURPLE, PINK, FONT_PATH, SKY_PATH, GROUND_PATH, PLAYER_PATH, SNAIL_PATH

def display_score():
    score = int(pygame.time.get_ticks() / 10) - start_time
    score_surf = font.render(f'{score}', False, PURPLE)
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return score

pygame.init()
pygame.display.set_caption('Blob Climbers')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_PATH, 100)
game_active = False
start_time = 0
hiscore = 0

sky_surf = pygame.image.load(SKY_PATH).convert()
ground_surf = pygame.image.load(GROUND_PATH).convert()
player_surf = pygame.image.load(PLAYER_PATH).convert_alpha()
snail_surf = pygame.image.load(SNAIL_PATH).convert_alpha()

player_rect = player_surf.get_rect(midbottom = (80, 300))
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_gravity = 0

# Main Menu
game_name = font.render('Blob Climbers', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (640, 200))

player_stand = pygame.image.load('assets/graphics/player/player_stand.png').convert_alpha()
player_stand_rect = player_stand.get_rect(center = (640, 360))
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (640, 360))

game_message = font.render('Press space to play', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (640, 540))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
                player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 600
                start_time = int(pygame.time.get_ticks() / 10)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        # pygame.draw.rect(screen, PINK, score_rect)
        # pygame.draw.rect(screen, PINK, score_rect, 10)
        # screen.blit(score_surf, score_rect)
        
        # Hiscore
        if display_score() >= hiscore:
            hiscore = display_score()

        # Snail
        screen.blit(snail_surf, snail_rect)
        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 600

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        screen.blit(player_surf, player_rect)
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
            player_gravity = 0

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)
        score_message = font.render(f'{hiscore}', False, PURPLE)
        score_message_rect = score_message.get_rect(center = (640, 540))
        
        if hiscore == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(FPS)
