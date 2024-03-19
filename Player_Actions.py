import pygame
from SpriteSheet import SpriteSheet
class Knight:
    BLACK = (0, 0, 0)
    running_animation = []
    idle_animation = []
    roll_animation = []
    slide_animation = []
    attack_animation = []
    crouch_animation = []
    crouch_walk_animation = []
    jump_animation = []
    run = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Run.png')
    idle = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Idle.png')
    roll = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Roll.png')
    slide = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_SlideFull.png')
    attack = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_AttackNoMovement.png')
    crouch = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Crouch.png')
    crouch_walk = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_CrouchWalk.png')
    jump = pygame.image.load('./Resources/FreeKnight_v1/Colour1/Outline/120x80_PNGSheets/_Jump.png')
    running_sheet = SpriteSheet(run)
    idle_sheet = SpriteSheet(idle)
    roll_sheet = SpriteSheet(roll)
    slide_sheet = SpriteSheet(slide)
    attack_sheet = SpriteSheet(attack)
    crouch_sheet = SpriteSheet(crouch)
    crouch_walk_sheet = SpriteSheet(crouch_walk)
    jump_sheet = SpriteSheet(jump)
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
        "crouch": 0.10,
        "crouch_walk": 0.30,
        "jump": 0.2
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.facing_right = True
        self.y_vel = 0
        self.on_ground = True

    def add_to_animation_list(self, animation_list: dict, animation_steps: dict):
        for key, animation in animation_list.items():
            sheet = eval(f"self.{key}_sheet")
            for step in range(animation_steps[key]):
                animation.append(sheet.get_image(step, 120, 85, 2, self.BLACK))

    def get_animation_list(self):
        self.add_to_animation_list(self.animation_list, self.animation_steps)
        return self.animation_list

    def get_animation_speed(self):
        return self.animation_speed

    def get_animation_steps(self):
        return self.animation_steps



class PlayerActions(Knight):
    def __init__(self, x, y, speed, jump_velocity, gravity, screen_height, screen_width):
        super().__init__(x, y)
        self.speed = speed
        self.jump_velocity = jump_velocity
        self.gravity = gravity
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.key = None
        self.action = "idle"
        self.previous_action = None

    def update_key(self, key):
        self.key = key

    def player_movement(self, frame_index, dt, animation_timer):
        if self.key[pygame.K_RIGHT]:
            self.action = "running"
            self.x += self.speed * dt
            self.facing_right = True
        elif self.key[pygame.K_LEFT]:
            self.action = "running"
            self.x -= self.speed * dt
            self.facing_right = False
        elif self.key[pygame.K_DOWN]:
            if self.key[pygame.K_c]:
                self.action = "crouch_walk"
                self.x += self.speed * dt if self.facing_right else -self.speed * dt
            else:
                self.action = "crouch"
        elif self.action not in ["jump", "attack"]:
            self.action = "idle"

        if not self.on_ground:
            self.y_vel += self.gravity * dt
            self.y += self.y_vel * dt
            if self.y >= self.screen_height - 250:
                self.y = self.screen_height - 250
                self.on_ground = True
                self.y_vel = 0
                if self.action == "jump":
                    self.action = "idle"

        if self.action != self.previous_action:
            frame_index = 0
            animation_timer = 0
            self.previous_action = self.action

        return frame_index, self.action, animation_timer

    def start_attack(self):
        if self.action != "attack":
            self.action = "attack"
            return 0, 0
        return None, None

    def jump(self):
        if self.on_ground:
            self.y_vel = self.jump_velocity
            self.on_ground = False
            self.action = "jump"
            return 0, 0
        return None, None


