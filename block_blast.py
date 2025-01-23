import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
CELL_SIZE = 30
COLUMNS = SCREEN_WIDTH // CELL_SIZE
ROWS = SCREEN_HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Shapes and their rotations
SHAPES = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]],  # Z shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]]   # J shape
]

SHAPE_COLORS = [RED, GREEN, BLUE, PURPLE, YELLOW, CYAN, WHITE]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Game variables
grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
current_shape = None
current_color = None
current_position = [0, COLUMNS // 2 - 2]
next_shape = None
next_color = None
score = 0
speed = 500
last_move_down = pygame.time.get_ticks()
game_over = False

# Functions
def create_shape():
    """Create a new random shape."""
    global current_shape, current_color, current_position, next_shape, next_color
    if next_shape is None:
        current_shape = random.choice(SHAPES)
        current_color = random.choice(SHAPE_COLORS)
    else:
        current_shape = next_shape
        current_color = next_color

    next_shape = random.choice(SHAPES)
    next_color = random.choice(SHAPE_COLORS)

    current_position = [0, COLUMNS // 2 - len(current_shape[0]) // 2]

    if not is_valid_position(current_position):
        return False  # Game over condition
    return True

def draw_grid():
    """Draw the grid and placed blocks."""
    for row in range(ROWS):
        for col in range(COLUMNS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if grid[row][col]:
                pygame.draw.rect(screen, grid[row][col], rect)

def draw_shape():
    """Draw the current falling shape."""
    for row, line in enumerate(current_shape):
        for col, cell in enumerate(line):
            if cell:
                x = (current_position[1] + col) * CELL_SIZE
                y = (current_position[0] + row) * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, current_color, rect)

def draw_next_shape():
    """Draw the next shape preview."""
    start_x = SCREEN_WIDTH - 5 * CELL_SIZE
    start_y = 2 * CELL_SIZE
    text = font.render("Next:", True, WHITE)
    screen.blit(text, (start_x, start_y - CELL_SIZE))
    for row, line in enumerate(next_shape):
        for col, cell in enumerate(line):
            if cell:
                x = start_x + col * CELL_SIZE
                y = start_y + row * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, next_color, rect)

def rotate_shape():
    """Rotate the current shape clockwise."""
    global current_shape
    current_shape = [list(row) for row in zip(*current_shape[::-1])]

def is_valid_position(new_position):
    """Check if the shape can be placed at the new position."""
    for row, line in enumerate(current_shape):
        for col, cell in enumerate(line):
            if cell:
                new_row = new_position[0] + row
                new_col = new_position[1] + col
                if (
                    new_row < 0 or new_row >= ROWS or
                    new_col < 0 or new_col >= COLUMNS or
                    grid[new_row][new_col]
                ):
                    return False
    return True

def place_shape():
    """Place the current shape on the grid."""
    global grid
    for row, line in enumerate(current_shape):
        for col, cell in enumerate(line):
            if cell:
                grid[current_position[0] + row][current_position[1] + col] = current_color

def clear_lines():
    """Clear full lines and update the grid and score."""
    global grid, score
    lines_to_clear = [row for row in range(ROWS) if all(grid[row])]
    for row in lines_to_clear:
        del grid[row]
        grid.insert(0, [0 for _ in range(COLUMNS)])
    score += len(lines_to_clear) * 100

def move_shape(direction):
    """Move the shape left, right, or down."""
    global current_position, game_over
    if direction == "left":
        new_position = [current_position[0], current_position[1] - 1]
    elif direction == "right":
        new_position = [current_position[0], current_position[1] + 1]
    elif direction == "down":
        new_position = [current_position[0] + 1, current_position[1]]

    if is_valid_position(new_position):
        current_position = new_position
    elif direction == "down":
        place_shape()
        clear_lines()
        if not create_shape():
            game_over = True

# Start the game
def reset_game():
    global grid, score, game_over, current_shape, next_shape, current_color, next_color
    grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    score = 0
    game_over = False
    current_shape = None
    next_shape = None
    current_color = None
    next_color = None
    create_shape()

create_shape()
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    move_shape("left")
                elif event.key == pygame.K_RIGHT:
                    move_shape("right")
                elif event.key == pygame.K_DOWN:
                    move_shape("down")
                elif event.key == pygame.K_UP:
                    rotate_shape()
            elif event.key == pygame.K_r:
                reset_game()

    # Automatic downward movement
    if not game_over and pygame.time.get_ticks() - last_move_down > speed:
        move_shape("down")
        last_move_down = pygame.time.get_ticks()

    draw_grid()
    if not game_over:
        draw_shape()
        draw_next_shape()

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display game over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
