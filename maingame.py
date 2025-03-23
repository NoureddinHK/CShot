import pygame
import random

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
        self.double_points_active = False  # To check if double points are active
        self.double_points_timer = 0  # Timer for the double points effect

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

    def update(self):
        """Updates the player's double points timer."""
        if self.double_points_active:
            if self.double_points_timer > 0:
                self.double_points_timer -= 1
            else:
                self.double_points_active = False  # Deactivate double points after timer runs out
                self.double_points_timer = 0


class Target:
    def __init__(self):
        self.position = [
            random.randint(PLAY_AREA.left + 20, PLAY_AREA.right - 40),
            random.randint(PLAY_AREA.top + 20, PLAY_AREA.bottom - 40),
        ]
        target_image = pygame.image.load("target.png")
        target_image = pygame.transform.scale(target_image, (45, 45))
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

class TimerTarget(Target):
    def __init__(self):
        super().__init__()
        timer_image = pygame.image.load("timer.png")
        self.image = pygame.transform.scale(timer_image, (50, 50))  # Larger size for distinction

    def grant_time(self, player_index):
        """Adds extra time to the respective player's timer."""
        player_timers[player_index] += 20  # Example: Grants 20 extra seconds


class AmmoTarget(Target):
    def __init__(self):
        super().__init__()
        ammo_image = pygame.image.load("ammo.png")
        self.image = pygame.transform.scale(ammo_image, (50, 50))  # Slightly different size for differentiation

    def grant_ammo(self, player):
        """Grants extra bullets when hit."""
        player.bullets += 8  # Example: Reward 8 extra bullets

class DoublePointsTarget(Target):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("double_points.png")  # Use a special image for this target
        self.image = pygame.transform.scale(self.image, (50, 50))  # Set a different size for visibility

    def grant_double_points(self, player):
        """Grants double points effect for the player."""
        player.double_points_active = True
        player.double_points_timer = 300  # Set the duration for double points (in frames)

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
    targets = [Target() for _ in range(5)]

    # Timers for each player
    player_timers = [TIMER_DURATION, TIMER_DURATION]
    clock = pygame.time.Clock()

    last_special_spawn = pygame.time.get_ticks()  # Track last spawn time


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
                        if isinstance(hit_target, TimerTarget):
                            hit_target.grant_time(players.index(player))  # Grants extra time to the hitting player
                        elif isinstance(hit_target, AmmoTarget):
                            hit_target.grant_ammo(player)  # Ammo target gives extra bullets
                        elif isinstance(hit_target, DoublePointsTarget):
                            hit_target.grant_double_points(player)  # Double points effect
                        else:
                            points = 50  # Normal target scoring
                            if player.double_points_active:
                                points *= 2  # Double the points if active
                            player.score += points  # Add points

                    if isinstance(hit_target, (TimerTarget, AmmoTarget, DoublePointsTarget)):
                        if hit_target in targets:
                            targets.remove(hit_target)  # Remove special item when hit
                    else:
                        hit_target.respawn()  # Normal target respawns
            else:
                new_traces.append(trace)

        traces = new_traces

        # Update players' double points timers
        for player in players:
            player.update()

        name_text1 = font.render(f"{players[0].name} | Time: {int(player_timers[0])}s", True, RED)
        name_text2 = font.render(f"{players[1].name} | Time: {int(player_timers[1])}s", True, BLUE)
        bullet_text1 = font.render(f"Bullets: {players[0].bullets} | Score: {players[0].score}", True, RED)
        bullet_text2 = font.render(f"Bullets: {players[1].bullets} | Score: {players[1].score}", True, BLUE)

        screen.blit(name_text1, (20, 20))
        screen.blit(bullet_text1, (20, 50))
        screen.blit(name_text2, (WIDTH - 300, 20))
        screen.blit(bullet_text2, (WIDTH - 300, 50))

        # Spawn a special item every 15 seconds if none exists
        if pygame.time.get_ticks() - last_special_spawn >= 15000:
            special_item = random.choice([TimerTarget(), AmmoTarget(), DoublePointsTarget()])
            targets.append(special_item)
            last_special_spawn = pygame.time.get_ticks()  # Reset spawn timer

        pygame.display.flip()

        if (players[0].bullets == 0 and players[1].bullets == 0) or (player_timers[0] == 0 and player_timers[1] == 0) or (players[0].bullets == 0 and player_timers[1] == 0) or (players[1].bullets == 0 and player_timers[0] == 0):
            running = False


    game_over_screen()
