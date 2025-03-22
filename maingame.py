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


# Timer settings (seconds)
TIMER_DURATION = 60  # Each player gets 60 seconds


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
        target_image = pygame.image.load("target.png")
        target_image = pygame.transform.scale(target_image, (40, 40))
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

class BonusTarget(Target):
    def __init__(self):
        super().__init__()
        ammo_image = pygame.image.load("ammo.png")
        self.image = pygame.transform.scale(ammo_image, (50, 50))  # Larger size for distinction

    def special_effect(self, player):
        """Define a special effect when hit, e.g., extra points or bullets."""
        player.score += 100  # Example: Award extra points for hitting a bonus target

class AmmoTarget(Target):
    def __init__(self):
        super().__init__()
        ammo_image = pygame.image.load("ammo.png")
        self.image = pygame.transform.scale(ammo_image, (55, 45))  # Slightly different size for differentiation

    def grant_ammo(self, player):
        """Grants extra bullets when hit."""
        player.bullets += 5  # Example: Reward 5 extra bullets


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
    targets = [Target() for _ in range(5)] + [BonusTarget() for _ in range(2)] + [AmmoTarget() for _ in range(1)]  # Mix of normal and bonus targets # number of targets spawning

    # Timers for each player
    player_timers = [TIMER_DURATION, TIMER_DURATION]
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, PLAY_AREA, 3)

        dt = clock.tick(30) / 1000  # Delta time in seconds
        for i in range(2):
            if player_timers[i] > 0:
                player_timers[i] -= dt
            else:
                player_timers[i] = 0  # Prevent negative timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYUP:
                for player in players:
                    if event.key == player.controls["shoot"]:
                        player.can_shoot = True
            elif event.type == pygame.KEYDOWN:
                for i, player in enumerate(players):
                    if event.key == player.controls["shoot"] and player_timers[i] > 0:
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
                for player in players:
                    if trace[2] == player.color:
                        if isinstance(hit_target, BonusTarget):
                            player.score += 100  # Bonus target gives extra points
                        elif isinstance(hit_target, AmmoTarget):
                            hit_target.grant_ammo(player)  # Ammo target gives extra bullets
                        else:
                            player.score += 50  # Normal target scoring

                hit_target.respawn()  # Respawn the target after being hit
            else:
                new_traces.append(trace)

        traces = new_traces

        name_text1 = font.render(f"{players[0].name} | Time: {int(player_timers[0])}s", True, RED)
        name_text2 = font.render(f"{players[1].name} | Time: {int(player_timers[1])}s", True, BLUE)
        bullet_text1 = font.render(f"Bullets: {players[0].bullets} | Score: {players[0].score}", True, RED)
        bullet_text2 = font.render(f"Bullets: {players[1].bullets} | Score: {players[1].score}", True, BLUE)

        screen.blit(name_text1, (20, 20))
        screen.blit(bullet_text1, (20, 50))
        screen.blit(name_text2, (WIDTH - 300, 20))
        screen.blit(bullet_text2, (WIDTH - 300, 50))

        pygame.display.flip()

        if (players[0].bullets == 0 and players[1].bullets == 0) or (player_timers[0] == 0 and player_timers[1] == 0):
            running = False

    game_over_screen()
