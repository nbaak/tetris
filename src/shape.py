
import pygame

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

    def draw(self, window, x, y, block_size):
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
                            block_size
                        )
                    )

    def __repr__(self):
        return f"{self.name} ({self.color})"
