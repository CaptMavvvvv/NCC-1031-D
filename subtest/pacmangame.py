import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Maze layout (1 = wall, 0 = path, 2 = food, 3 = power pellet)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 2, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

TILE_SIZE = 40

# Pac-Man setup
pacman_x, pacman_y = 1, 1
pacman_speed = 5
direction = "NONE"

# Ghost setup
ghosts = [
    {"x": 11, "y": 1, "color": RED, "speed": 2, "direction": "LEFT"},
    {"x": 11, "y": 7, "color": BLUE, "speed": 2, "direction": "UP"},
]

# Score and lives
score = 0
lives = 3

# Helper functions
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            if maze[row][col] == 1:  # Wall
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
            elif maze[row][col] == 2:  # Food
                pygame.draw.circle(screen, WHITE, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 5)
            elif maze[row][col] == 3:  # Power pellet
                pygame.draw.circle(screen, YELLOW, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 10)

def move_pacman():
    global pacman_x, pacman_y, score, maze, lives
    new_x, new_y = pacman_x, pacman_y
    if direction == "UP":
        new_y -= 1
    elif direction == "DOWN":
        new_y += 1
    elif direction == "LEFT":
        new_x -= 1
    elif direction == "RIGHT":
        new_x += 1

    if maze[new_y][new_x] != 1:  # Check for walls
        pacman_x, pacman_y = new_x, new_y

    # Eat food
    if maze[pacman_y][pacman_x] == 2:
        maze[pacman_y][pacman_x] = 0
        score += 10
    elif maze[pacman_y][pacman_x] == 3:  # Power pellet
        maze[pacman_y][pacman_x] = 0
        score += 50

def move_ghosts():
    for ghost in ghosts:
        if "direction" not in ghost or random.random() < 0.2:  # Change direction occasionally
            ghost["direction"] = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        new_x, new_y = ghost["x"], ghost["y"]
        if ghost["direction"] == "UP":
            new_y -= 1
        elif ghost["direction"] == "DOWN":
            new_y += 1
        elif ghost["direction"] == "LEFT":
            new_x -= 1
        elif ghost["direction"] == "RIGHT":
            new_x += 1

        if maze[new_y][new_x] != 1:  # Check for walls
            ghost["x"], ghost["y"] = new_x, new_y

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        direction = "UP"
    if keys[pygame.K_DOWN]:
        direction = "DOWN"
    if keys[pygame.K_LEFT]:
        direction = "LEFT"
    if keys[pygame.K_RIGHT]:
        direction = "RIGHT"

    move_pacman()
    move_ghosts()

    # Check for collisions with ghosts
    for ghost in ghosts:
        if pacman_x == ghost["x"] and pacman_y == ghost["y"]:
            lives -= 1
            if lives <= 0:
                print("Game Over!")
                running = False
            else:
                pacman_x, pacman_y = 1, 1  # Reset Pac-Man position

    # Draw maze, Pac-Man, and ghosts
    draw_maze()
    pygame.draw.circle(screen, YELLOW, (pacman_x * TILE_SIZE + TILE_SIZE // 2, pacman_y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)
    for ghost in ghosts:
        pygame.draw.rect(screen, ghost["color"], (ghost["x"] * TILE_SIZE, ghost["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
sys.exit()
