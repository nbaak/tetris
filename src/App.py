import pygame
import random
import config
import uuid
import os
import colors
from shape import Shape

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

# Define the colors of the tetrominoes
COLORS = [colors.CYAN, colors.YELLOW, colors.PURPLE, colors.GREEN, colors.RED, colors.BLUE, colors.ORANGE]

# Initialize the game grid
grid = [[colors.BLACK] * grid_width for _ in range(grid_height)]




# Define the shapes of the tetrominoes
SHAPES = [
    Shape([[1, 1, 1, 1]], colors.CYAN, 'I'),
    Shape([[1, 1], [1, 1]], colors.YELLOW, 'O'),
    Shape([[1, 1, 0], [0, 1, 1]], colors.PURPLE, 'S'),
    Shape([[0, 1, 1], [1, 1, 0]], colors.GREEN, 'Z'),
    Shape([[1, 1, 1], [0, 1, 0]], colors.RED, 'T'),
    Shape([[1, 1, 1], [1, 0, 0]], colors.BLUE, 'L'),
    Shape([[1, 1, 1], [0, 0, 1]], colors.ORANGE, 'J'),
]


# Function to draw the game grid
def draw_grid(score):
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
        colors.GRAY,
        (grid_width * block_size, 0, window_width - grid_width * block_size, window_height),
    )

    # Draw the score on the right side
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, colors.WHITE)
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
                    or grid[y + row][x + col] != colors.BLACK
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


# Function to remove completed rows from the game grid and update the score
def remove_rows(score=0) -> int:
    full_rows = []
    for y in range(grid_height):
        if all(color != colors.BLACK for color in grid[y]):
            full_rows.append(y)

    num_rows = len(full_rows)
    score_increase = num_rows * config.score_increment
    score += score_increase

    for y in full_rows:
        del grid[y]
        grid.insert(0, [colors.BLACK] * grid_width)

    print("Score:", score)
    return score


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

    score = 0

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
            score = remove_rows(score)
            current_shape = next_shape
            next_shape = random.choice(SHAPES)
            current_x = grid_width // 2 - current_shape.get_width() // 2
            current_y = 0

            if is_collision(current_shape, current_x, current_y):
                game_over = True

        # Clear the window
        window.fill(colors.BLACK)

        # Draw the game grid
        draw_grid(score)

        # Draw the current shape
        current_shape.draw(window, current_x, current_y, block_size)

        # Draw the ghost figure
        if config.ghost:
            draw_ghost(current_shape, current_x, current_y)

        # Draw the next shape preview
        draw_preview(next_shape, next_shape_x, next_shape_y)

        # Update the display
        pygame.display.update()

        # Tick the clock
        clock.tick(config.game_speed)


# Run the game
if __name__ == "__main__":
    main()

