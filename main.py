from sys import exit

import pygame


pygame.init()
pygame.display.set_caption('Blob Climbers')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.Font('assets/font/Pixeltype.ttf', 100)

sky_surface = pygame.image.load('assets/graphics/sky.png').convert()
ground_surface = pygame.image.load('assets/graphics/ground.png').convert()
text_surface = font.render('Hello World!', False, 'Purple')

snail_surface = pygame.image.load('assets/graphics/snail/snail_1.png').convert_alpha()
snail_x_pos = 600

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (250, 50))
    snail_x_pos -= 3
    if snail_x_pos < -100:
        snail_x_pos = 600
    screen.blit(snail_surface, (snail_x_pos, 268))

    pygame.display.update()
    clock.tick(60)
