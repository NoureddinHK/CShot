import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two Pointers Movement and Shooting")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Play area boundaries
PLAY_AREA = pygame.Rect(100, 100, 1000, 500)

# Initialize font
font = pygame.font.Font(None, 36)

# Load target image
target_image = pygame.image.load("target.png")
target_image = pygame.transform.scale(target_image, (40, 40))


class Player:
    def __init__(self, color, controls, name):
        self.position = [
            random.randint(PLAY_AREA.left + 20, PLAY_AREA.right - 20),
            random.randint(PLAY_AREA.top + 20, PLAY_AREA.bottom - 20),
        ]
        self.color = color
        self.controls = controls
        self.bullets = 30
        self.score = 0
        self.can_shoot = True
        self.last_hit_position = None
        self.name = name  # Placeholder for future SQL integration

    def move(self, keys):
        if keys[self.controls["up"]] and self.position[1] - 7 > PLAY_AREA.top:
            self.position[1] -= 7
        if keys[self.controls["down"]] and self.position[1] + 7 < PLAY_AREA.bottom:
            self.position[1] += 7
        if keys[self.controls["left"]] and self.position[0] - 7 > PLAY_AREA.left:
            self.position[0] -= 7
        if keys[self.controls["right"]] and self.position[0] + 7 < PLAY_AREA.right:
            self.position[0] += 7

    def shoot(self, traces):
        if self.can_shoot and self.bullets > 0:
            traces.append((self.position[0], self.position[1], self.color))
            self.can_shoot = False
            self.bullets -= 1


class Target:
    def __init__(self):
        self.position = [
            random.randint(PLAY_AREA.left + 20, PLAY_AREA.right - 40),
            random.randint(PLAY_AREA.top + 20, PLAY_AREA.bottom - 40),
        ]
        self.image = target_image
        self.width, self.height = self.image.get_size()

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))

    def is_hit(self, trace):
        x, y = trace[0], trace[1]
        return (
            self.position[0] <= x <= self.position[0] + self.width
            and self.position[1] <= y <= self.position[1] + self.height
        )

    def respawn(self):
        self.position = [
            random.randint(PLAY_AREA.left + 20, PLAY_AREA.right - 40),
            random.randint(PLAY_AREA.top + 20, PLAY_AREA.bottom - 40),
        ]


players = [
    Player(
        RED,
        {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "shoot": pygame.K_f,
        },
        "Player 1",
    ),
    Player(
        BLUE,
        {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "shoot": pygame.K_RETURN,
        },
        "Player 2",
    ),
]

traces = []
targets = [Target() for _ in range(8)]  # number of targets spawning

running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, PLAY_AREA, 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            for player in players:
                if event.key == player.controls["shoot"]:
                    player.can_shoot = True
        elif event.type == pygame.KEYDOWN:
            for player in players:
                if event.key == player.controls["shoot"]:
                    player.shoot(traces)

    keys = pygame.key.get_pressed()
    for player in players:
        player.move(keys)

    for x, y, color in traces:
        pygame.draw.circle(screen, color, (x, y), 5)  # color and radius for pointers

    for target in targets:
        target.draw(screen)

    new_traces = []
    for trace in traces:
        hit_target = None
        for target in targets:
            if target.is_hit(trace):
                hit_target = target
                break

        if hit_target:
            hit_target.respawn()

            for player in players:
                if trace[2] == player.color:
                    if player.last_hit_position is None:
                        player.score += 50  # First hit gives 50 points
                    else:
                        distance = math.sqrt(
                            (player.last_hit_position[0] - hit_target.position[0]) ** 2
                            + (player.last_hit_position[1] - hit_target.position[1]) ** 2
                        )
                        player.score += max(1, int(distance // 10))
                    player.last_hit_position = hit_target.position
        else:
            new_traces.append(trace)
    traces = new_traces

    name_text1 = font.render(f"{players[0].name}", True, RED)
    name_text2 = font.render(f"{players[1].name}", True, BLUE)
    bullet_text1 = font.render(
        f"Bullets: {players[0].bullets} | Score: {players[0].score}", True, RED
    )
    bullet_text2 = font.render(
        f"Bullets: {players[1].bullets} | Score: {players[1].score}", True, BLUE
    )

    screen.blit(name_text1, (20, 20))
    screen.blit(bullet_text1, (20, 50))
    screen.blit(name_text2, (WIDTH - 250, 20))
    screen.blit(bullet_text2, (WIDTH - 250, 50))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
