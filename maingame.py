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
    if keys[pygame.K_w]:
        pointer1[1] -= speed
    if keys[pygame.K_s]:
        pointer1[1] += speed
    if keys[pygame.K_a]:
        pointer1[0] -= speed
    if keys[pygame.K_d]:
        pointer1[0] += speed
    
    # Pointer 2 movement (Arrow Keys)
    if keys[pygame.K_UP]:
        pointer2[1] -= speed
    if keys[pygame.K_DOWN]:
        pointer2[1] += speed
    if keys[pygame.K_LEFT]:
        pointer2[0] -= speed
    if keys[pygame.K_RIGHT]:
        pointer2[0] += speed
    
    # Draw traces
    for x, y, color in traces:
        pygame.draw.circle(screen, color, (x, y), 3)
    
    # Update display
    pygame.display.flip()
    
    # Limit frame rate
    pygame.time.delay(30)

pygame.quit()
