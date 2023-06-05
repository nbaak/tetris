import pygame
import random
import config
import uuid 
import os

# Initialize the game
pygame.init()

# Set up the game window
block_size = config.block_size
grid_width = config.game_width
grid_height = config.game_height
next_shape_x = grid_width + 2
next_shape_y = 2

window_width = (grid_width + config.info_width) * block_size
window_height = grid_height * block_size
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

# Define the colors of the tetrominoes
COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

# Initialize the game grid
grid = [[BLACK] * grid_width for _ in range(grid_height)]


# Class representing a tetromino shape
class Shape:
    def __init__(self, grid, color, name='Shape'):
        self.grid = grid
        self.color = color
        self.name = name

    def rotate(self):
        self.grid = list(zip(*reversed(self.grid)))

    def get_height(self):
        return len(self.grid)

    def get_width(self):
        return len(self.grid[0])

    def draw(self, x, y):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 1:
                    pygame.draw.rect(
                        window,
                        self.color,
                        (
                            (x + col) * block_size,
                            (y + row) * block_size,
                            block_size,
                            block_size,
                        ),
                    )

    def __repr__(self):
        return f"{self.name} ({self.color})"


# Define the shapes of the tetrominoes
SHAPES = [
    Shape([[1, 1, 1, 1]], CYAN, 'I'),
    Shape([[1, 1], [1, 1]], YELLOW, 'O'),
    Shape([[1, 1, 0], [0, 1, 1]], PURPLE, 'S'),
    Shape([[0, 1, 1], [1, 1, 0]], GREEN, 'Z'),
    Shape([[1, 1, 1], [0, 1, 0]], RED, 'T'),
    Shape([[1, 1, 1], [1, 0, 0]], BLUE, 'L'),
    Shape([[1, 1, 1], [0, 0, 1]], ORANGE, 'J'),
]


# Function to draw the game grid
def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            pygame.draw.rect(
                window,
                grid[y][x],
                (x * block_size, y * block_size, block_size, block_size),
            )

    # Draw background for the right side
    pygame.draw.rect(
        window,
        GRAY,
        (grid_width * block_size, 0, window_width - grid_width * block_size, window_height),
    )

    # Draw the score on the right side
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.center = (
        (grid_width + config.info_width // 2) * block_size,
        window_height // 2,
    )
    window.blit(score_text, score_rect)


# Function to check if the current tetromino collides with the game grid or other tetrominoes
def is_collision(shape, x, y):
    for row in range(shape.get_height()):
        for col in range(shape.get_width()):
            if (
                shape.grid[row][col] == 1
                and (
                    x + col < 0
                    or x + col >= grid_width
                    or y + row >= grid_height
                    or grid[y + row][x + col] != BLACK
                )
            ):
                return True
    return False


# Function to place the current tetromino in the game grid
def place_tetromino(shape, x, y):
    for row in range(shape.get_height()):
        for col in range(shape.get_width()):
            if shape.grid[row][col] == 1:
                grid[y + row][x + col] = shape.color


# Define the score variables
score = 0
score_increment = config.score_increment

# Function to remove completed rows from the game grid and update the score
def remove_rows():
    global score
    full_rows = []
    for y in range(grid_height):
        if all(color != BLACK for color in grid[y]):
            full_rows.append(y)

    num_rows = len(full_rows)
    score_increase = num_rows * score_increment
    score += score_increase

    for y in full_rows:
        del grid[y]
        grid.insert(0, [BLACK] * grid_width)

    print("Score:", score)


# Function to draw the ghost figure
def draw_ghost(shape, x, y):
    ghost_y = y
    while not is_collision(shape, x, ghost_y):
        ghost_y += 1
    ghost_y -= 1

    for row in range(shape.get_height()):
        for col in range(shape.get_width()):
            if shape.grid[row][col] == 1:
                pygame.draw.rect(
                    window,
                    shape.color + (100,),  # Set the transparency to make it a ghost figure
                    (
                        (x + col) * block_size,
                        (ghost_y + row) * block_size,
                        block_size,
                        block_size,
                    ),
                    1,
                )


# Function to draw the next shape preview
def draw_preview(shape, x, y):
    for row in range(shape.get_height()):
        for col in range(shape.get_width()):
            if shape.grid[row][col] == 1:
                pygame.draw.rect(
                    window,
                    shape.color,
                    (
                        (x + col) * block_size,
                        (y + row) * block_size,
                        block_size,
                        block_size,
                    ),
                )


def main():
    
    # Create the screenshots folder if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Create a random tetromino shape for the current and next shapes
    current_shape = random.choice(SHAPES)
    next_shape = random.choice(SHAPES)
    current_x = grid_width // 2 - current_shape.get_width() // 2
    current_y = 0

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not is_collision(current_shape, current_x - 1, current_y):
                        current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not is_collision(current_shape, current_x + 1, current_y):
                        current_x += 1
                elif event.key == pygame.K_DOWN:
                    if not is_collision(current_shape, current_x, current_y + 1):
                        current_y += 1
                elif event.key == pygame.K_SPACE:
                    rotated_shape = Shape(
                        current_shape.grid[:], current_shape.color, current_shape.name
                    )
                    rotated_shape.rotate()
                    if not is_collision(rotated_shape, current_x, current_y):
                        current_shape = rotated_shape
                elif event.key == pygame.K_q:
                    game_over = True
                elif event.key == pygame.K_d:
                    while not is_collision(current_shape, current_x, current_y + 1):
                        current_y += 1
                elif event.key == pygame.K_s:
                    # Generate a unique filename using UUID
                    screenshot_name = str(uuid.uuid4()) + ".png"
                    # Save the screenshot in the "screenshots" folder
                    pygame.image.save(window, os.path.join("screenshots", screenshot_name))


        # Move the current shape down
        if not is_collision(current_shape, current_x, current_y + 1):
            current_y += 1
        else:
            place_tetromino(current_shape, current_x, current_y)
            remove_rows()
            current_shape = next_shape
            next_shape = random.choice(SHAPES)
            current_x = grid_width // 2 - current_shape.get_width() // 2
            current_y = 0

            if is_collision(current_shape, current_x, current_y):
                game_over = True

        # Clear the window
        window.fill(BLACK)

        # Draw the game grid
        draw_grid()

        # Draw the current shape
        current_shape.draw(current_x, current_y)

        # Draw the ghost figure
        if config.ghost:
            draw_ghost(current_shape, current_x, current_y)

        # Draw the next shape preview
        draw_preview(next_shape, next_shape_x, next_shape_y)

        # Update the display
        pygame.display.update()

        # Tick the clock
        clock.tick(5)


# Run the game
if __name__ == "__main__":
    main()

