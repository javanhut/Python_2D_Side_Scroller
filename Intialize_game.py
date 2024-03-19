import pygame
from SpriteSheet import SpriteSheet

class Knight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing_right = True
        self.y_vel = 0
        self.on_ground = True

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
crouch_walk = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_CrouchWalk.png')
jump = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Jump.png')

knight = Knight(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 85)  # Adjusted for ground level
SPEED = 300
GRAVITY = 980
JUMP_VELOCITY = -500
frame_index = 0
animation_timer = 0
action = "idle"

running_animation = []
idle_animation = []
roll_animation = []
slide_animation = []
attack_animation = []
crouch_animation = []
crouch_walk_animation = []
jump_animation = []
animation_list = {
    "running": running_animation,
    "idle": idle_animation,
    "roll": roll_animation,
    "slide": slide_animation,
    "attack": attack_animation,
    "crouch": crouch_animation,
    "crouch_walk": crouch_walk_animation,
    "jump": jump_animation
}

animation_steps = {
    "idle": 10,
    "running": 10,
    "slide": 4,
    "roll": 12,
    "attack": 4,
    "crouch": 3,
    "crouch_walk": 8,
    "jump": 3,
}

animation_speed = {
    "idle": 0.2,
    "running": 0.1,
    "slide": 0.4,
    "roll": 0.1,
    "attack": 0.2,
    "crouch": 0.30,
    "crouch_walk": 0.30,
    "jump": 0.2
}

BLACK = (0, 0, 0)

running_sheet = SpriteSheet(run)
idle_sheet = SpriteSheet(idle)
roll_sheet = SpriteSheet(roll)
slide_sheet = SpriteSheet(slide)
attack_sheet = SpriteSheet(attack)
crouch_sheet = SpriteSheet(crouch)
crouch_walk_sheet = SpriteSheet(crouch_walk)
jump_sheet = SpriteSheet(jump)

for key, animation in animation_list.items():
    sheet = eval(f"{key}_sheet")
    for step in range(animation_steps[key]):
        animation.append(sheet.get_image(step, 120, 85, 2, BLACK))

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and action != "attack":
                action = "attack"
                frame_index = 0
            if event.key == pygame.K_UP and knight.on_ground:
                knight.y_vel = JUMP_VELOCITY
                knight.on_ground = False
                action = "jump"

    key = pygame.key.get_pressed()
    if action != "attack":
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
        elif key[pygame.K_DOWN] and key[pygame.K_c]:
            action = "crouch_walk"
            knight.x += SPEED * dt
        elif not any(key):
            action = "idle"

    if not knight.on_ground:
        knight.y_vel += GRAVITY * dt
        knight.y += knight.y_vel * dt
        if knight.y >= SCREEN_HEIGHT - 85:  # Ground level adjustment
            knight.y = SCREEN_HEIGHT - 85
            knight.on_ground = True
            knight.y_vel = 0

    animation_timer += dt
    if animation_timer >= animation_speed[action]:
        frame_index += 1
        animation_timer = 0
        if action == "attack" and frame_index >= animation_steps[action]:
            action = "idle"
            frame_index = 0

    frame_index %= animation_steps[action]

    screen.fill((50, 50, 50))
    current_frame = animation_list[action][frame_index]
    if not knight.facing_right:
        current_frame = pygame.transform.flip(current_frame, True, False)
    current_frame.set_colorkey(BLACK)
    screen.blit(current_frame, (knight.x, knight.y))

    pygame.display.update()

pygame.quit()
