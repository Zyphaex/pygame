from sys import exit

import pygame


pygame.init()
pygame.display.set_caption('Blob Climbers')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font('assets/font/Pixeltype.ttf', 100)

sky_surf = pygame.image.load('assets/graphics/sky.png').convert()
ground_surf = pygame.image.load('assets/graphics/ground.png').convert()
text_surf = font.render('Hello World!', False, 'Purple')

snail_surf = pygame.image.load('assets/graphics/snail/snail_1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_surf = pygame.image.load('assets/graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 300))
    screen.blit(text_surf, (250, 50))

    screen.blit(snail_surf, snail_rect)
    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 600

    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)
