import pygame
from sys import exit

from utilities.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PURPLE, PINK, FONT_PATH, SKY_PATH, GROUND_PATH, PLAYER_PATH, SNAIL_PATH


pygame.init()
pygame.display.set_caption('Blob Climbers')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(FONT_PATH, 100)

sky_surf = pygame.image.load(SKY_PATH).convert()
ground_surf = pygame.image.load(GROUND_PATH).convert()
score_surf = font.render('Jump!', False, PURPLE)
player_surf = pygame.image.load(PLAYER_PATH).convert_alpha()
snail_surf = pygame.image.load(SNAIL_PATH).convert_alpha()

score_rect = score_surf.get_rect(center = (400, 50))
player_rect = player_surf.get_rect(midbottom = (80, 300))
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom >= 300:
            player_gravity = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                player_gravity = -20

    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    pygame.draw.rect(screen, PINK, score_rect)
    pygame.draw.rect(screen, PINK, score_rect, 10)
    screen.blit(score_surf, score_rect)

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

    pygame.display.update()
    clock.tick(FPS)
