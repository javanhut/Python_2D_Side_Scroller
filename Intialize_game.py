import pygame
# Assuming necessary imports like SpriteSheet, Main_background, Knight, PlayerActions
from SpriteSheet import SpriteSheet
from Asset_management import Main_background
from Player_Actions import Knight, PlayerActions

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True

main_background = pygame.image.load('./Resources/DarkForest1.2/main_background.png')
knight = PlayerActions(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 250, 300, -500, 980, SCREEN_HEIGHT, SCREEN_WIDTH)

frame_index = 0
animation_timer = 0

while running:
    dt = clock.tick(60) / 1000
    screen.fill((50, 50, 50))
    Main_background(main_background, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                temp_frame_index, temp_animation_timer = knight.start_attack()
                if temp_frame_index is not None:
                    frame_index, animation_timer = temp_frame_index, temp_animation_timer
            elif event.key == pygame.K_UP:
                temp_frame_index, temp_animation_timer = knight.jump()
                if temp_frame_index is not None:
                    frame_index, animation_timer = temp_frame_index, temp_animation_timer

    key = pygame.key.get_pressed()
    knight.update_key(key)
    frame_index, action, animation_timer = knight.player_movement(frame_index, dt, animation_timer)

    animation_list = knight.get_animation_list()
    animation_speed = knight.get_animation_speed()
    animation_steps = knight.get_animation_steps()

    if animation_timer >= animation_speed[action]:
        frame_index += 1
        if frame_index >= animation_steps[action]:
            frame_index = 0
            if action in ["attack", "jump"]:
                knight.action = "idle"
        animation_timer = 0

    current_frame = animation_list[action][frame_index]
    if not knight.facing_right:
        current_frame = pygame.transform.flip(current_frame, True, False)
    current_frame.set_colorkey(Knight.BLACK)
    screen.blit(current_frame, (knight.x, knight.y))

    pygame.display.update()

pygame.quit()
