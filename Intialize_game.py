import pygame
from SpriteSheet import SpriteSheet

class Knight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing_right = True

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
running = True

run = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Run.png')
idle = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Idle.png')
roll = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Roll.png')
slide = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_SlideFull.png')
attack = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_AttackNoMovement.png')
crouch = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Crouch.png')

player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
run_sheet = SpriteSheet(run)
idle_sheet = SpriteSheet(idle)
rolling_sheet = SpriteSheet(roll)
slide_sheet = SpriteSheet(slide)
attack_sheet = SpriteSheet(attack)
crouch_sheet = SpriteSheet(crouch)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

running_animation = []
idle_animation = []
roll_animation = []
slide_animation = []
attack_animation = []
crouch_animation = []
animation_list = {
    "running": running_animation,
    "idle": idle_animation,
    "roll": roll_animation,
    "slide": slide_animation,
    "attack": attack_animation,
    "crouch": crouch_animation
}

action = "idle"
animation_steps = {
    "idle": 10,
    "running": 10,
    "slide": 4,
    "roll": 12,
    "attack": 4,
    "crouch": 3
}

animation_speed = {
    "idle": 0.2,
    "running": 0.2,
    "slide": 0.4,
    "roll": 0.1,
    "attack": 0.3,
    "crouch": 0.10

}

for step in range(animation_steps["running"]):
    running_animation.append(run_sheet.get_image(step, 120, 85, 2, BLACK))
for step in range(animation_steps["idle"]):
    idle_animation.append(idle_sheet.get_image(step, 120, 85, 2, BLACK))
for step in range(animation_steps["roll"]):
    roll_animation.append(rolling_sheet.get_image(step, 120, 85, 2, BLACK))
for step in range(animation_steps["slide"]):
    slide_animation.append(slide_sheet.get_image(step, 120, 85, 2, BLACK))
for step in range(animation_steps["attack"]):
    attack_animation.append(attack_sheet.get_image(step, 120, 85, 2, BLACK))
for step in range(animation_steps["crouch"]):
    crouch_animation.append(crouch_sheet.get_image(step, 120, 85, 2, BLACK))

knight = Knight(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SPEED = 300
frame_index = 0
animation_timer = 0
action = "idle"

while running:
    dt = clock.tick(60) / 1000
    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and action != "attack":
                action = "attack"
                frame_index = 0  # Reset frame index for attack animation

    key = pygame.key.get_pressed()
    if action != "attack":  # Prevent movement keys from overriding attack animation
        if key[pygame.K_RIGHT]:
            action = "running"
            knight.x += SPEED * dt
            knight.facing_right = True
        elif key[pygame.K_LEFT]:
            action = "running"
            knight.x -= SPEED * dt
            knight.facing_right = False
        elif key[pygame.K_DOWN]:
            action = "crouch"
        elif not any(key):  # If no relevant keys are pressed, revert to idle
            action = "idle"

    animation_timer += dt
    if animation_timer >= animation_speed[action]:
        frame_index += 1
        animation_timer = 0
        if action == "attack" and frame_index >= animation_steps[action]:
            action = "idle"  # Return to idle after completing attack animation
            frame_index = 0  # Reset frame index for next action

    frame_index %= animation_steps[action]  # Ensure frame index loops correctly

    current_frame = animation_list[action][frame_index]
    if not knight.facing_right:
        current_frame = pygame.transform.flip(current_frame, True, False)
    current_frame.set_colorkey(BLACK)
    screen.blit(current_frame, (knight.x, knight.y))

    pygame.display.update()

pygame.quit()