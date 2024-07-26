import pygame
import random
from atom import Atom

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Circles")

# Set up the colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up the circles
circles = []
for _ in range(2):
    radius = 5
    x = random.randint(radius, screen_width - radius)
    y = random.randint(radius, screen_height - radius)
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    atom = Atom(x, y, radius, dx, dy, 25)
    circles.append(atom)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update circles position
    for i, atom in enumerate(circles):
        atom.x += atom.dx
        atom.y += atom.dy

        # Check for collision with screen edges
        if atom.x - atom.radius < 0 or atom.x + atom.radius > screen_width:
            atom.dx = -atom.dx
        if atom.y - atom.radius < 0 or atom.y + atom.radius > screen_height:
            atom.dy = -atom.dy

        # circles[i] = (x, y, radius, dx, dy)

    # Clear the screen
    screen.fill(BLACK)

    # Draw circles
    for atom in circles:
        pygame.draw.circle(screen, WHITE, (atom.x, atom.y), atom.radius)
        pygame.draw.circle(screen, RED, (atom.x, atom.y), atom.outer_radius)

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()