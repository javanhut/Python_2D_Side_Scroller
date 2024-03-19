import pygame
def Main_background(image, screen):
    size = pygame.transform.scale(image, (1280,720))
    screen.blit(size, (0,0))