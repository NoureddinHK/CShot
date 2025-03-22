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
large_font = pygame.font.Font(None, 72)  # Bigger font for Game Over screen

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
        self.name = name

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


def game_over_screen():
    screen.fill(WHITE)

    # Determine the winner
    if players[0].score > players[1].score:
        winner_text = f"{players[0].name} Wins!"
        winner_color = RED
    elif players[1].score > players[0].score:
        winner_text = f"{players[1].name} Wins!"
        winner_color = BLUE
    else:
        winner_text = "It's a Tie!"
        winner_color = BLACK

    # Render game over text
    text = large_font.render("Game Over", True, BLACK)
    winner_display = large_font.render(winner_text, True, winner_color)
    score_text1 = font.render(f"{players[0].name}: {players[0].score} points", True, RED)
    score_text2 = font.render(f"{players[1].name}: {players[1].score} points", True, BLUE)
    restart_text = font.render("Press 'R' to Restart or 'ESC' to Exit", True, BLACK)

    # Positioning the texts
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))
    screen.blit(winner_display, (WIDTH // 2 - winner_display.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text1, (WIDTH // 2 - score_text1.get_width() // 2, HEIGHT // 2))
    screen.blit(score_text2, (WIDTH // 2 - score_text2.get_width() // 2, HEIGHT // 1.8))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Restart game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


while True:  # Restart game loop
    players = [
        Player(RED, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_f}, "Player 1"),
        Player(BLUE, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_RETURN}, "Player 2"),
    ]

    traces = []
    targets = [Target() for _ in range(8)] # number of targets spawning

    running = True
    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, PLAY_AREA, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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
            pygame.draw.circle(screen, color, (x, y), 5)  # color and radius of pointers

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
                            player.score += 50
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
        bullet_text1 = font.render(f"Bullets: {players[0].bullets} | Score: {players[0].score}", True, RED)
        bullet_text2 = font.render(f"Bullets: {players[1].bullets} | Score: {players[1].score}", True, BLUE)

        screen.blit(name_text1, (20, 20))
        screen.blit(bullet_text1, (20, 50))
        screen.blit(name_text2, (WIDTH - 250, 20))
        screen.blit(bullet_text2, (WIDTH - 250, 50))

        pygame.display.flip()
        pygame.time.delay(30)

        # Check if both players are out of bullets
        if players[0].bullets == 0 and players[1].bullets == 0:
            running = False

    game_over_screen()
