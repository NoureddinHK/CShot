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
GREEN = (0, 255, 0)

# Play area boundaries
PLAY_AREA = pygame.Rect(100, 100, 1000, 500)

# Initialize font
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self, x, y, color, controls):
        self.position = [x, y]
        self.color = color
        self.controls = controls
        self.bullets = 30
        self.score = 0
        self.can_shoot = True
        self.last_hit_position = None
    
    def move(self, keys):
        if keys[self.controls['up']] and self.position[1] - 7 > PLAY_AREA.top:
            self.position[1] -= 7
        if keys[self.controls['down']] and self.position[1] + 7 < PLAY_AREA.bottom:
            self.position[1] += 7
        if keys[self.controls['left']] and self.position[0] - 7 > PLAY_AREA.left:
            self.position[0] -= 7
        if keys[self.controls['right']] and self.position[0] + 7 < PLAY_AREA.right:
            self.position[0] += 7
    
    def shoot(self, traces):
        if self.can_shoot and self.bullets > 0:
            traces.append((self.position[0], self.position[1], self.color))
            self.can_shoot = False
            self.bullets -= 1

players = [
    Player(200, 300, RED, {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_f}),
    Player(600, 300, BLUE, {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_RETURN})
]

traces = []
objects = [(random.randint(120, 1080), random.randint(120, 580)) for _ in range(8)]

running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, PLAY_AREA, 3)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            for player in players:
                if event.key == player.controls['shoot']:
                    player.can_shoot = True
        elif event.type == pygame.KEYDOWN:
            for player in players:
                if event.key == player.controls['shoot']:
                    player.shoot(traces)
    
    keys = pygame.key.get_pressed()
    for player in players:
        player.move(keys)
    
    for x, y, color in traces:
        pygame.draw.circle(screen, color, (x, y), 3)
    
    for obj in objects:
        pygame.draw.rect(screen, GREEN, (obj[0], obj[1], 20, 20))
    
    new_traces = []
    for trace in traces:
        hit = None
        for obj in objects:
            if obj[0] <= trace[0] <= obj[0] + 20 and obj[1] <= trace[1] <= obj[1] + 20:
                hit = obj
                break
        if hit:
            objects.remove(hit)
            objects.append((random.randint(120, 1080), random.randint(120, 580)))
            
            for player in players:
                if trace[2] == player.color:
                    if player.last_hit_position is None:
                        player.score += 50  # First hit gives 50 points
                    else:
                        distance = math.sqrt((player.last_hit_position[0] - hit[0])**2 + (player.last_hit_position[1] - hit[1])**2)
                        player.score += max(1, int(distance // 10))
                    player.last_hit_position = hit
        else:
            new_traces.append(trace)
    traces = new_traces
    
    bullet_text1 = font.render(f"Bullets: {players[0].bullets} | Score: {players[0].score}", True, RED)
    bullet_text2 = font.render(f"Bullets: {players[1].bullets} | Score: {players[1].score}", True, BLUE)
    screen.blit(bullet_text1, (20, 20))
    screen.blit(bullet_text2, (WIDTH - 250, 20))
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
