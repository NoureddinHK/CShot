import pygame

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
PLAY_AREA = pygame.Rect(100, 100, 1000, 500)  # x, y, width, height

# Initialize font
font = pygame.font.Font(None, 36)

# Initial positions for pointers
pointer1 = [200, 300]  # Controlled by WASD
pointer2 = [600, 300]  # Controlled by Arrow Keys

# Traces list
traces = []

# Movement speed
speed = 7

# Shooting control
can_shoot1 = True
can_shoot2 = True

# Bullet limits
bullets1 = 30
bullets2 = 30

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Clear screen
    pygame.draw.rect(screen, BLACK, PLAY_AREA, 3)  # Draw play area border
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                can_shoot1 = True
            if event.key == pygame.K_RETURN:
                can_shoot2 = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and can_shoot1 and bullets1 > 0:  # Pointer 1 shoots with 'F'
                traces.append((pointer1[0], pointer1[1], RED))
                can_shoot1 = False
                bullets1 -= 1
            if event.key == pygame.K_RETURN and can_shoot2 and bullets2 > 0:  # Pointer 2 shoots with 'Enter'
                traces.append((pointer2[0], pointer2[1], BLUE))
                can_shoot2 = False
                bullets2 -= 1
    
    # Get keys pressed
    keys = pygame.key.get_pressed()
    
    # Pointer 1 movement (WASD)
    if keys[pygame.K_w] and pointer1[1] - speed > PLAY_AREA.top:
        pointer1[1] -= speed
    if keys[pygame.K_s] and pointer1[1] + speed < PLAY_AREA.bottom:
        pointer1[1] += speed
    if keys[pygame.K_a] and pointer1[0] - speed > PLAY_AREA.left:
        pointer1[0] -= speed
    if keys[pygame.K_d] and pointer1[0] + speed < PLAY_AREA.right:
        pointer1[0] += speed
    
    # Pointer 2 movement (Arrow Keys)
    if keys[pygame.K_UP] and pointer2[1] - speed > PLAY_AREA.top:
        pointer2[1] -= speed
    if keys[pygame.K_DOWN] and pointer2[1] + speed < PLAY_AREA.bottom:
        pointer2[1] += speed
    if keys[pygame.K_LEFT] and pointer2[0] - speed > PLAY_AREA.left:
        pointer2[0] -= speed
    if keys[pygame.K_RIGHT] and pointer2[0] + speed < PLAY_AREA.right:
        pointer2[0] += speed
    
    # Draw traces
    for x, y, color in traces:
        pygame.draw.circle(screen, color, (x, y), 3)
    
    # Display bullet count
    bullet_text1 = font.render(f"Bullets: {bullets1}", True, RED)
    bullet_text2 = font.render(f"Bullets: {bullets2}", True, BLUE)
    screen.blit(bullet_text1, (20, 20))  # Top left corner
    screen.blit(bullet_text2, (WIDTH - 150, 20))  # Top right corner
    
    # Update display
    pygame.display.flip()
    
    # Limit frame rate
    pygame.time.delay(30)

pygame.quit()
